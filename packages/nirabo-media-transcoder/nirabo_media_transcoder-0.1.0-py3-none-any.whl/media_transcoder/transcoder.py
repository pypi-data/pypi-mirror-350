#!/usr/bin/env -S uv run --script

# /// script
# dependencies = [
#   "rich>=13.7.0"
# ]
# ///

import argparse
import concurrent.futures
import datetime
import json
import os
import re
import shutil
import sqlite3
import subprocess
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from rich.console import Console
from rich.progress import (BarColumn, Progress, TextColumn, TimeElapsedColumn,
                           TimeRemainingColumn)
from rich.table import Table

# Global constants
CPU_CODEC = "libx264"
NVIDIA_CODEC = "h264_nvenc"
SUPPORTED_EXTENSIONS = [
    ".mp4",
    ".mkv",
    ".avi",
    ".mov",
    ".wmv",
    ".flv",
    ".webm",
    ".m4v",
    ".mpg",
    ".mpeg",
    ".ts",
    ".mts",
]
DEFAULT_DB_PATH = os.path.expanduser("~/.jellyfin_transcoder/transcoder.db")
BATCH_SIZE = 5  # Number of files to process in each batch

# Global variables
software_only = False


class FilenameUtils:
    """Utility class for handling filenames, including web-safe name generation."""

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Convert a filename to a web-safe version by replacing invalid characters.

        Args:
            filename: The original filename

        Returns:
            A web-safe version of the filename
        """
        # Replace characters that are problematic in URLs and filesystems
        invalid_chars = r'[\\/:*?"<>|&\s]'
        sanitized = re.sub(invalid_chars, "-", filename)

        # Replace multiple dashes with a single dash
        sanitized = re.sub(r"-+", "-", sanitized)

        # Remove leading/trailing dashes
        sanitized = sanitized.strip("-")

        # Ensure the filename is not empty
        if not sanitized:
            sanitized = "unnamed-file"

        return sanitized

    @staticmethod
    def get_jellyfin_safe_name(file_path: Path) -> Path:
        """Generate a web-safe filename optimized for Jellyfin.

        Args:
            file_path: Path to the original file

        Returns:
            Path object with the web-safe filename
        """
        stem = FilenameUtils.sanitize_filename(file_path.stem)
        # Always use .mp4 extension for Jellyfin compatibility
        return file_path.with_name(f"{stem}_jellyfin.mp4")

    @staticmethod
    def get_unique_filename(file_path: Path) -> Path:
        """Generate a unique filename if the target file already exists.

        Args:
            file_path: Path to the target file

        Returns:
            Path object with a unique filename
        """
        if not file_path.exists():
            return file_path

        counter = 1
        while True:
            new_path = file_path.with_name(
                f"{file_path.stem}_{counter}{file_path.suffix}"
            )
            if not new_path.exists():
                return new_path
            counter += 1


class TranscoderDB:
    """Database manager for tracking transcoding jobs and media library."""

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        """Initialize the database connection and create tables if needed.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = os.path.expanduser(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        self.conn = sqlite3.connect(self.db_path)
        self._create_tables()

    def _create_tables(self) -> None:
        """Create the necessary database tables if they don't exist."""
        cursor = self.conn.cursor()

        # Table for transcoding jobs
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS transcoding_jobs (
            id TEXT PRIMARY KEY,
            input_file TEXT NOT NULL,
            output_file TEXT NOT NULL,
            codec TEXT NOT NULL,
            hardware_accel INTEGER NOT NULL,
            duration REAL NOT NULL,
            status TEXT NOT NULL,
            error_message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        )

        # Table for media library
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS media_library (
            file_path TEXT PRIMARY KEY,
            file_size INTEGER NOT NULL,
            format TEXT NOT NULL,
            duration REAL,
            bitrate INTEGER,
            video_codec TEXT,
            audio_codec TEXT,
            resolution TEXT,
            status TEXT NOT NULL,
            notes TEXT,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
        )

        self.conn.commit()

    def record_job(
        self,
        input_file: Path,
        output_file: Path,
        codec: str,
        hardware_accel: bool,
        duration: float,
        status: str,
        error_message: str = None,
    ) -> str:
        """Record a transcoding job in the database.

        Args:
            input_file: Path to the input file
            output_file: Path to the output file
            codec: Codec used for transcoding
            hardware_accel: Whether hardware acceleration was used
            duration: Duration of the transcoding process in seconds
            status: Status of the job (success, failed, skipped)
            error_message: Error message if the job failed

        Returns:
            The ID of the recorded job
        """
        cursor = self.conn.cursor()
        job_id = str(uuid.uuid4())

        cursor.execute(
            """
        INSERT INTO transcoding_jobs 
        (id, input_file, output_file, codec, hardware_accel, duration, status, error_message) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                job_id,
                str(input_file),
                str(output_file),
                codec,
                1 if hardware_accel else 0,
                duration,
                status,
                error_message,
            ),
        )

        self.conn.commit()
        return job_id

    def get_recent_jobs(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent transcoding jobs from the database.

        Args:
            limit: Maximum number of jobs to return

        Returns:
            List of job dictionaries
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """
        SELECT id, input_file, output_file, codec, hardware_accel, 
               duration, status, error_message, timestamp 
        FROM transcoding_jobs 
        ORDER BY timestamp DESC 
        LIMIT ?
        """,
            (limit,),
        )

        jobs = []
        for row in cursor.fetchall():
            jobs.append(
                {
                    "id": row[0],
                    "input_file": row[1],
                    "output_file": row[2],
                    "codec": row[3],
                    "hardware_accel": bool(row[4]),
                    "duration": row[5],
                    "status": row[6],
                    "error_message": row[7],
                    "timestamp": row[8],
                }
            )

        return jobs

    def update_media_library(self, file_path: Path, file_info: Dict[str, Any]) -> None:
        """Update or insert a media file in the library.

        Args:
            file_path: Path to the media file
            file_info: Dictionary with file information
        """
        cursor = self.conn.cursor()

        # Check if the file already exists in the database
        cursor.execute(
            "SELECT file_path FROM media_library WHERE file_path = ?", (str(file_path),)
        )
        exists = cursor.fetchone() is not None

        if exists:
            # Update existing record
            fields = []
            values = []

            for key, value in file_info.items():
                if key != "file_path":
                    fields.append(f"{key} = ?")
                    values.append(value)

            # Add last_updated timestamp and file_path
            fields.append("last_updated = CURRENT_TIMESTAMP")
            values.append(str(file_path))

            query = f"UPDATE media_library SET {', '.join(fields)} WHERE file_path = ?"
            cursor.execute(query, values)
        else:
            # Insert new record
            fields = ["file_path"] + list(file_info.keys())
            placeholders = ["?"] * len(fields)
            values = [str(file_path)] + list(file_info.values())

            query = f"INSERT INTO media_library ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
            cursor.execute(query, values)

        self.conn.commit()

    def get_media_files(
        self, limit: int = 50, status: str = None
    ) -> List[Dict[str, Any]]:
        """Get media files from the library.

        Args:
            limit: Maximum number of files to return
            status: Filter by status (valid, invalid, etc.)

        Returns:
            List of media file dictionaries
        """
        return self.get_media_info(limit=limit, status=status)

    def remove_media_file(self, file_path: Path) -> bool:
        """Remove a media file from the library.

        Args:
            file_path: Path to the media file

        Returns:
            True if the file was removed, False otherwise
        """
        cursor = self.conn.cursor()

        # Check if the file exists in the database
        cursor.execute(
            "SELECT COUNT(*) FROM media_library WHERE file_path = ?", (str(file_path),)
        )
        count = cursor.fetchone()[0]

        if count == 0:
            return False

        # Remove the file from the database
        cursor.execute(
            "DELETE FROM media_library WHERE file_path = ?", (str(file_path),)
        )
        self.conn.commit()

        return True

    def get_media_info(
        self, file_path: Optional[Path] = None, limit: int = 50, status: str = None
    ) -> List[Dict[str, Any]]:
        """Get media files from the library.

        Args:
            limit: Maximum number of files to return
            status: Filter by status (valid, invalid, etc.)

        Returns:
            List of media file dictionaries
        """
        cursor = self.conn.cursor()

        query = "SELECT * FROM media_library"
        params = []

        # Add conditions
        conditions = []

        if file_path:
            conditions.append("file_path = ?")
            params.append(str(file_path))

        if status:
            conditions.append("status = ?")
            params.append(status)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Add ordering and limit
        query += " ORDER BY last_checked DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)

        columns = [desc[0] for desc in cursor.description]
        media_files = []

        for row in cursor.fetchall():
            media_file = {columns[i]: row[i] for i in range(len(columns))}
            media_files.append(media_file)

    def get_media_files(
        self, limit: int = 50, status: str = None
    ) -> List[Dict[str, Any]]:
        """Get media files from the library.

        Args:
            limit: Maximum number of files to return
            status: Filter by status (valid, invalid, etc.)

        Returns:
            List of media file dictionaries
        """
        return self.get_media_info(limit=limit, status=status)

    def remove_media_file(self, file_path: Path) -> bool:
        """Remove a media file from the library.

        Args:
            file_path: Path to the media file

        Returns:
            True if the file was removed, False otherwise
        """
        cursor = self.conn.cursor()

        # Check if the file exists in the database
        cursor.execute(
            "SELECT COUNT(*) FROM media_library WHERE file_path = ?", (str(file_path),)
        )
        count = cursor.fetchone()[0]

        if count == 0:
            return False

        # Remove the file from the database
        cursor.execute(
            "DELETE FROM media_library WHERE file_path = ?", (str(file_path),)
        )
        self.conn.commit()

        return True

        return media_files

    def close(self):
        """Close the database connection."""
        self.conn.close()


MULTIPLE_DASHES = re.compile(r"--+")
MULTIPLE_DOTS = re.compile(r"\.\.")
WEB_SAFE_CHARS = re.compile(
    r"[^a-zA-Z0-9.-]"
)  # Characters to replace for web-safe filenames

# Database schema
DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS transcoding_jobs (
    id TEXT PRIMARY KEY,
    input_file TEXT NOT NULL,
    output_file TEXT NOT NULL,
    input_size INTEGER,
    output_size INTEGER,
    input_format TEXT,
    output_format TEXT,
    codec_used TEXT,
    hardware_accel INTEGER,
    duration_seconds REAL,
    status TEXT,
    error_message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    parameters TEXT
);

CREATE TABLE IF NOT EXISTS media_library (
    file_path TEXT PRIMARY KEY,
    file_size INTEGER,
    format TEXT,
    duration REAL,
    video_codec TEXT,
    audio_codec TEXT,
    resolution TEXT,
    bitrate INTEGER,
    last_checked DATETIME,
    status TEXT,
    notes TEXT,
    web_optimized INTEGER DEFAULT 0
);
"""


class FilenameUtils:
    """Utilities for handling filenames"""

    @staticmethod
    def make_web_safe(filename: str) -> str:
        """Convert a filename to be web-safe

        Args:
            filename: The original filename

        Returns:
            A web-safe version of the filename
        """
        # Get the base name without extension
        name_parts = filename.rsplit(".", 1)
        name = name_parts[0]
        extension = name_parts[1] if len(name_parts) > 1 else ""

        # Replace spaces and special chars with dashes
        safe_name = WEB_SAFE_CHARS.sub("-", name)

        # Replace multiple dashes with a single dash
        safe_name = MULTIPLE_DASHES.sub("-", safe_name)

        # Remove leading/trailing dashes
        safe_name = safe_name.strip("-")

        # Combine with extension if present
        if extension:
            return f"{safe_name}.{extension}"
        return safe_name

    @staticmethod
    def get_jellyfin_safe_name(original_path: Path, suffix: str = "_jellyfin") -> Path:
        """Create a Jellyfin-friendly filename from the original path

        Args:
            original_path: The original file path
            suffix: Suffix to add before the extension

        Returns:
            A new Path with a web-safe name
        """
        # Get the stem and extension
        stem = original_path.stem
        extension = original_path.suffix

        # Create a web-safe stem
        safe_stem = FilenameUtils.make_web_safe(stem)

        # Add the suffix and extension
        new_name = f"{safe_stem}{suffix}{extension}"

        return original_path.with_name(new_name)


class TranscoderDB:
    """Database manager for transcoding operations"""

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        """Initialize the database

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = os.path.expanduser(db_path)
        self._ensure_db_directory()
        self.conn = self._connect_db()
        self._init_schema()

    def _ensure_db_directory(self) -> None:
        """Ensure the database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        os.makedirs(db_dir, exist_ok=True)

    def _connect_db(self) -> sqlite3.Connection:
        """Connect to the SQLite database"""
        return sqlite3.connect(self.db_path)

    def _init_schema(self) -> None:
        """Initialize the database schema"""
        cursor = self.conn.cursor()
        cursor.executescript(DB_SCHEMA)
        self.conn.commit()

        # Check if web_optimized column exists and add it if it doesn't
        try:
            cursor.execute("SELECT web_optimized FROM media_library LIMIT 1")
        except sqlite3.OperationalError:
            # Column doesn't exist, add it
            cursor.execute(
                "ALTER TABLE media_library ADD COLUMN web_optimized INTEGER DEFAULT 0"
            )
            self.conn.commit()

    def record_job(
        self,
        input_file: Path,
        output_file: Path,
        codec: str,
        hardware_accel: bool,
        duration: float,
        status: str,
        error_message: str = None,
        parameters: Dict[str, Any] = None,
    ) -> str:
        """Record a transcoding job in the database

        Args:
            input_file: Path to the input file
            output_file: Path to the output file
            codec: Codec used for transcoding
            hardware_accel: Whether hardware acceleration was used
            duration: Duration of the transcoding process in seconds
            status: Status of the job (success, failed, etc.)
            error_message: Error message if the job failed
            parameters: Additional parameters used for transcoding

        Returns:
            The ID of the recorded job
        """
        job_id = str(uuid.uuid4())

        # Get file sizes if files exist
        input_size = input_file.stat().st_size if input_file.exists() else None
        output_size = output_file.stat().st_size if output_file.exists() else None

        # Get file formats (extensions)
        input_format = input_file.suffix.lstrip(".")
        output_format = output_file.suffix.lstrip(".")

        # Serialize parameters if provided
        params_json = json.dumps(parameters) if parameters else None

        cursor = self.conn.cursor()
        cursor.execute(
            """INSERT INTO transcoding_jobs 
               (id, input_file, output_file, input_size, output_size, 
                input_format, output_format, codec_used, hardware_accel, 
                duration_seconds, status, error_message, timestamp, parameters) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                job_id,
                str(input_file),
                str(output_file),
                input_size,
                output_size,
                input_format,
                output_format,
                codec,
                int(hardware_accel),
                duration,
                status,
                error_message,
                datetime.datetime.now().isoformat(),
                params_json,
            ),
        )
        self.conn.commit()
        return job_id

    def update_media_library(self, file_path: Path, file_info: Dict[str, Any]) -> None:
        """Update the media library with file information

        Args:
            file_path: Path to the media file
            file_info: Dictionary containing file information
        """
        cursor = self.conn.cursor()

        # Check if the file already exists in the database
        cursor.execute(
            "SELECT 1 FROM media_library WHERE file_path = ?", (str(file_path),)
        )
        exists = cursor.fetchone() is not None

        if exists:
            # Update existing record
            set_clauses = [f"{key} = ?" for key in file_info.keys()]
            set_clause = ", ".join(set_clauses)
            query = f"UPDATE media_library SET {set_clause}, last_checked = ? WHERE file_path = ?"
            params = list(file_info.values())
            params.append(datetime.datetime.now().isoformat())
            params.append(str(file_path))
            cursor.execute(query, params)
        else:
            # Insert new record
            keys = list(file_info.keys()) + ["file_path", "last_checked"]
            placeholders = ["?"] * len(keys)
            query = f"INSERT INTO media_library ({', '.join(keys)}) VALUES ({', '.join(placeholders)})"
            params = list(file_info.values())
            params.append(str(file_path))
            params.append(datetime.datetime.now().isoformat())
            cursor.execute(query, params)

        self.conn.commit()

    def get_job_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get the history of transcoding jobs

        Args:
            limit: Maximum number of jobs to return

        Returns:
            A list of dictionaries containing job information
        """
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT * FROM transcoding_jobs 
               ORDER BY timestamp DESC LIMIT ?""",
            (limit,),
        )

        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_media_info(self, file_path: Optional[Path] = None) -> List[Dict[str, Any]]:
        """Get information about media files

        Args:
            file_path: Optional path to a specific file

        Returns:
            A list of dictionaries containing file information
        """
        cursor = self.conn.cursor()

        if file_path:
            cursor.execute(
                "SELECT * FROM media_library WHERE file_path = ?", (str(file_path),)
            )
        else:
            cursor.execute("SELECT * FROM media_library ORDER BY last_checked DESC")

        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_media_files(
        self, limit: int = 50, status: str = None
    ) -> List[Dict[str, Any]]:
        """Get media files from the library.

        Args:
            limit: Maximum number of files to return
            status: Filter by status (valid, invalid, etc.)

        Returns:
            List of media file dictionaries
        """
        cursor = self.conn.cursor()

        if status:
            cursor.execute(
                "SELECT * FROM media_library WHERE status = ? ORDER BY last_checked DESC LIMIT ?",
                (status, limit),
            )
        else:
            cursor.execute(
                "SELECT * FROM media_library ORDER BY last_checked DESC LIMIT ?",
                (limit,),
            )

        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def remove_media_file(self, file_path: Path) -> bool:
        """Remove a media file from the library.

        Args:
            file_path: Path to the media file

        Returns:
            True if the file was removed, False otherwise
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM media_library WHERE file_path = ?", (str(file_path),)
        )
        self.conn.commit()

        # Return True if any rows were affected, False otherwise
        return cursor.rowcount > 0

    def reset_database(self) -> None:
        """Reset the database by deleting all records."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM media_library")
        cursor.execute("DELETE FROM transcoding_jobs")
        self.conn.commit()

    def close(self) -> None:
        """Close the database connection"""
        if self.conn:
            self.conn.close()


# Jellyfin-optimized encoding parameters
def get_encoding_params(codec, use_hardware=True):
    """Return appropriate encoding parameters based on codec type

    Args:
        codec: The codec to use (NVIDIA_CODEC or CPU_CODEC)
        use_hardware: Whether to use hardware acceleration flags
    """
    if codec == NVIDIA_CODEC and use_hardware:
        # NVENC hardware encoding parameters
        return [
            # Video parameters for hardware encoding
            "-c:v",
            codec,
            "-preset",
            "p4",  # NVENC preset (p1-p7, p4 is balanced)
            "-b:v",
            "5M",  # Video bitrate
            "-maxrate",
            "8M",  # Maximum bitrate
            "-bufsize",
            "10M",  # Buffer size
            "-profile:v",
            "main",  # Main profile for compatibility
            "-pix_fmt",
            "yuv420p",  # Pixel format for maximum compatibility
            "-movflags",
            "+faststart",  # Optimize for web streaming
            # Audio parameters
            "-c:a",
            "aac",  # AAC audio codec for best compatibility
            "-b:a",
            "192k",  # Audio bitrate
            "-ac",
            "2",  # 2 audio channels (stereo)
            "-ar",
            "48000",  # Audio sample rate
            # Subtitle handling
            "-c:s",
            "mov_text",  # Text-based subtitles compatible with MP4
        ]
    else:
        # CPU encoding parameters (fallback or default)
        return [
            # Video parameters for CPU encoding
            "-c:v",
            CPU_CODEC,  # Always use CPU codec for fallback
            "-preset",
            "medium",  # CPU preset (slower = better quality)
            "-crf",
            "22",  # Constant Rate Factor (balance of quality and size)
            "-profile:v",
            "main",  # Main profile for compatibility
            "-pix_fmt",
            "yuv420p",  # Pixel format for maximum compatibility
            "-movflags",
            "+faststart",  # Optimize for web streaming
            # Audio parameters
            "-c:a",
            "aac",  # AAC audio codec for best compatibility
            "-b:a",
            "192k",  # Audio bitrate
            "-ac",
            "2",  # 2 audio channels (stereo)
            "-ar",
            "48000",  # Audio sample rate
            # Subtitle handling
            "-c:s",
            "mov_text",  # Text-based subtitles compatible with MP4
        ]


console = Console()


class Transcoder:
    def __init__(self, args):
        self.args = args
        self.target_location = args.target
        self.dry_run = args.dry_run
        self.destination = args.destination
        self.test_mode = args.test
        self.total_real_time = 0
        self.total_files = 0
        self.extension_counts = {ext: 0 for ext in SUPPORTED_EXTENSIONS}
        self.codec = ""
        self.hwaccel_flags = []
        self.force = args.force if hasattr(args, "force") else False
        self.skip_validation = (
            args.skip_validation if hasattr(args, "skip_validation") else False
        )
        self.keep_originals = (
            args.keep_originals if hasattr(args, "keep_originals") else False
        )
        self.web_safe_names = (
            args.web_safe_names if hasattr(args, "web_safe_names") else False
        )
        self.analyze_only = args.analyze if hasattr(args, "analyze") else False
        self.clean_mode = args.clean if hasattr(args, "clean") else False

        # Initialize database if needed
        self.db = None
        if hasattr(args, "db_path") and args.db_path is not None:
            self.db = TranscoderDB(args.db_path)
        elif not self.dry_run and not self.test_mode:
            self.db = TranscoderDB(DEFAULT_DB_PATH)

        # Statistics for the current run
        self.stats = {
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "skipped": 0,
            "repaired": 0,
            "total_size_before": 0,
            "total_size_after": 0,
            "start_time": time.time(),
        }

    def validate_media_file(self, file_path: Path) -> Tuple[bool, str]:
        """Validate if a file is a proper media file that can be transcoded.

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not file_path.exists():
            return False, f"File does not exist: {file_path}"

        if self.skip_validation:
            return True, ""

        # Use ffprobe to check if the file is a valid media file
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(file_path),
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)

            # Check if ffprobe returned successfully
            if result.returncode != 0:
                return False, f"Invalid media file: {result.stderr.strip()}"

            # Try to parse the JSON output
            try:
                data = json.loads(result.stdout)
                if "format" in data and "duration" in data["format"]:
                    return True, ""
                else:
                    return False, "Could not determine media duration"
            except json.JSONDecodeError:
                return False, "Could not parse ffprobe output"

        except Exception as e:
            return False, f"Error validating file: {str(e)}"

        return True, ""

    def analyze_media_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze a media file and extract detailed information.

        Args:
            file_path: Path to the media file

        Returns:
            Dictionary with media information or None if analysis failed
        """
        try:
            # Get file size
            file_size = file_path.stat().st_size

            # Run ffprobe to get media information
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "quiet",
                    "-print_format",
                    "json",
                    "-show_format",
                    "-show_streams",
                    str(file_path),
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            # Parse the JSON output
            probe_data = json.loads(result.stdout)

            # Extract relevant information
            file_info = {
                "file_size": file_size,
                "format": file_path.suffix.lstrip("."),
                "status": "valid",
                "notes": "",
            }

            # Extract format information
            if "format" in probe_data:
                format_data = probe_data["format"]
                if "duration" in format_data:
                    file_info["duration"] = float(format_data["duration"])
                if "bit_rate" in format_data:
                    file_info["bitrate"] = int(format_data["bit_rate"])

                # Get format name from ffprobe
                if "format_name" in format_data:
                    format_name = format_data["format_name"].split(",")[0]
                    file_info["format"] = format_name
            else:
                file_info["notes"] = "Missing format information"

            # Extract video stream information
            video_stream = None
            audio_stream = None

            if "streams" in probe_data:
                for stream in probe_data["streams"]:
                    if stream.get("codec_type") == "video" and not video_stream:
                        video_stream = stream
                    elif stream.get("codec_type") == "audio" and not audio_stream:
                        audio_stream = stream
            else:
                file_info["notes"] += " Missing stream information."

            if video_stream:
                file_info["video_codec"] = video_stream.get("codec_name", "unknown")
                width = video_stream.get("width", 0)
                height = video_stream.get("height", 0)
                file_info["resolution"] = f"{width}x{height}"

                # Check if the file is web-optimized
                is_web_optimized = self._is_web_optimized(
                    probe_data, file_info["format"]
                )
                file_info["web_optimized"] = 1 if is_web_optimized else 0
            else:
                file_info["notes"] += " No video stream found."

            if audio_stream:
                file_info["audio_codec"] = audio_stream.get("codec_name", "unknown")
            else:
                file_info["notes"] += " No audio stream found."

            # Update the database with the file information
            if self.db:
                self.db.update_media_library(file_path, file_info)

            return file_info

        except subprocess.CalledProcessError as e:
            error_msg = f"FFprobe failed with error code {e.returncode}"
            console.print(
                f"[ERROR] Failed to analyze file: {file_path.name}", style="red"
            )
            if e.stderr:
                stderr_output = (
                    e.stderr.decode() if isinstance(e.stderr, bytes) else str(e.stderr)
                )
                error_msg += f": {stderr_output.strip()}"
                console.print(f"[ERROR] {error_msg}", style="red")

            # Update the database with the error information
            if self.db:
                self.db.update_media_library(
                    file_path,
                    {
                        "file_size": (
                            file_path.stat().st_size if file_path.exists() else 0
                        ),
                        "format": file_path.suffix.lstrip("."),
                        "status": "invalid",
                        "notes": error_msg,
                    },
                )
            return None

        except json.JSONDecodeError as e:
            error_msg = f"Failed to parse FFprobe output: {str(e)}"
            console.print(f"[ERROR] {error_msg} for: {file_path.name}", style="red")

            # Update the database with the error information
            if self.db:
                self.db.update_media_library(
                    file_path,
                    {
                        "file_size": (
                            file_path.stat().st_size if file_path.exists() else 0
                        ),
                        "format": file_path.suffix.lstrip("."),
                        "status": "invalid",
                        "notes": error_msg,
                    },
                )
            return None

        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            console.print(
                f"[ERROR] {error_msg} analyzing {file_path.name}", style="red"
            )

            # Update the database with the error information
            if self.db:
                self.db.update_media_library(
                    file_path,
                    {
                        "file_size": (
                            file_path.stat().st_size if file_path.exists() else 0
                        ),
                        "format": file_path.suffix.lstrip("."),
                        "status": "invalid",
                        "notes": error_msg,
                    },
                )
            return None

    def check_hardware_acceleration(self) -> None:
        """Check for NVIDIA hardware acceleration and set appropriate codec and flags."""
        # Check if software-only mode is enabled
        software_only = (
            hasattr(self, "args")
            and hasattr(self.args, "software_only")
            and self.args.software_only
        )

        if software_only:
            self.codec = CPU_CODEC
            self.hwaccel_flags = []
            console.print(
                "[INFO] Software-only mode enabled (hardware acceleration disabled)",
                style="yellow",
            )
            return

        try:
            # Check for NVIDIA GPU using nvidia-smi
            nvidia_check = subprocess.run(
                ["nvidia-smi"], capture_output=True, text=True
            )

            has_nvidia_gpu = nvidia_check.returncode == 0
            if has_nvidia_gpu:
                console.print(
                    f"[DEBUG] NVIDIA GPU info:\n{nvidia_check.stdout.strip()}",
                    style="dim",
                )

            # Check for CUDA compiler
            cuda_check = subprocess.run(
                ["nvcc", "--version"], capture_output=True, text=True
            )

            has_cuda = cuda_check.returncode == 0
            if has_cuda:
                console.print(
                    f"[DEBUG] CUDA version:\n{cuda_check.stdout.strip()}", style="dim"
                )

            # Check ffmpeg encoders
            encoders_check = subprocess.run(
                ["ffmpeg", "-encoders"], capture_output=True, text=True
            )

            # Extract NVENC encoders for debugging
            encoders_output = encoders_check.stdout
            nvenc_encoders = [
                line for line in encoders_output.split("\n") if "nvenc" in line.lower()
            ]
            console.print(
                f"[DEBUG] Available NVENC encoders:\n{chr(10).join(nvenc_encoders) if nvenc_encoders else 'None found'}",
                style="dim",
            )

            # Check available hardware acceleration methods
            hwaccels_check = subprocess.run(
                ["ffmpeg", "-hwaccels"], capture_output=True, text=True
            )

            console.print(
                f"[DEBUG] Available hwaccels:\n{hwaccels_check.stdout.strip()}",
                style="dim",
            )

            # Simplified approach: if we have NVIDIA GPU and CUDA, try to use NVENC directly
            if has_nvidia_gpu and has_cuda:
                # Check if h264_nvenc is available
                has_nvenc = any("h264_nvenc" in line for line in nvenc_encoders)

                if has_nvenc:
                    self.codec = NVIDIA_CODEC
                    # Use minimal hardware acceleration flags to avoid compatibility issues
                    self.hwaccel_flags = []

                    # Simple NVENC parameters that work on most systems
                    self.nvenc_params = [
                        "-b:v",
                        "5M",  # Target bitrate
                        "-maxrate",
                        "8M",  # Maximum bitrate
                    ]

                    console.print(
                        "[INFO] NVIDIA hardware acceleration enabled with h264_nvenc",
                        style="green",
                    )
                    return
                else:
                    console.print(
                        "[WARNING] NVIDIA GPU detected but h264_nvenc encoder not available in ffmpeg",
                        style="yellow",
                    )

            # Fall back to CPU encoding
            self.codec = CPU_CODEC
            self.hwaccel_flags = []
            console.print(
                "[INFO] Using CPU encoding (no compatible hardware acceleration detected)",
                style="yellow",
            )

        except Exception as e:
            console.print(
                f"[ERROR] Failed to check for hardware acceleration: {e}", style="red"
            )
            self.codec = CPU_CODEC
            self.hwaccel_flags = []

    def find_video_files(self) -> List[Path]:
        """Find all supported video files in the target location."""
        video_files = []
        target_path = Path(self.target_location)

        if not target_path.exists():
            console.print(
                f"[ERROR] Target location does not exist: {self.target_location}",
                style="red",
            )
            return []

        # Add debug output
        console.print(
            f"[DEBUG] Searching for video files in: {target_path}", style="dim"
        )
        console.print(
            f"[DEBUG] Supported extensions: {SUPPORTED_EXTENSIONS}", style="dim"
        )

        for ext in SUPPORTED_EXTENSIONS:
            pattern = f"**/*{ext}"
            console.print(f"[DEBUG] Looking for pattern: {pattern}", style="dim")
            files = list(target_path.glob(pattern))
            console.print(
                f"[DEBUG] Found {len(files)} files with extension {ext}", style="dim"
            )
            self.extension_counts[ext] = len(files)
            video_files.extend(files)

        # Check if any files were found
        if not video_files:
            console.print(f"[DEBUG] No video files found in {target_path}", style="dim")
        else:
            console.print(
                f"[DEBUG] Found {len(video_files)} total video files", style="dim"
            )
            for file in video_files[:5]:  # Show first 5 files
                console.print(f"[DEBUG] Found: {file}", style="dim")
            if len(video_files) > 5:
                console.print(
                    f"[DEBUG] ... and {len(video_files) - 5} more files", style="dim"
                )

        return video_files

    def transcode(self, video_file: Path) -> float:
        """Transcode a video file to MP4 format optimized for Jellyfin streaming."""
        # First validate the file
        is_valid, error_message = self.validate_media_file(video_file)
        if not is_valid and not self.force:
            console.print(
                f"[ERROR] Skipping invalid file: {video_file.name}", style="red"
            )
            console.print(f"[ERROR] Validation error: {error_message}", style="red")
            console.print(
                f"[TIP] Use --force to attempt transcoding anyway or --skip-validation to bypass checks",
                style="blue",
            )

            # Record in database if available
            if self.db:
                self.db.record_job(
                    input_file=video_file,
                    output_file=video_file.with_suffix(".mp4"),  # Placeholder
                    codec=self.codec,
                    hardware_accel=False,
                    duration=0.0,
                    status="skipped",
                    error_message=error_message,
                )

            return 0.0

        # Create output filename with appropriate processing
        if self.web_safe_names:
            # Create a web-safe filename with MP4 extension for web compatibility
            safe_name = FilenameUtils.make_web_safe(video_file.stem)
            output_file = video_file.with_name(f"{safe_name}_jellyfin.mp4")
        else:
            # Use the standard naming convention with MP4 extension
            output_name = f"{video_file.stem}_jellyfin.mp4"
            output_file = video_file.with_name(output_name)

        # Set the destination path if specified
        if self.destination:
            dest_path = Path(self.destination)
            dest_path.mkdir(exist_ok=True)
            output_file = dest_path / output_file.name

        # Check if output file already exists
        if output_file.exists():
            console.print(
                f"[WARNING] Output file already exists: {output_file.name}",
                style="yellow",
            )
            if not self.dry_run and not self.force:
                console.print(
                    f"[INFO] Skipping: {video_file.name} (use --force to overwrite)",
                    style="blue",
                )

                # Record in database if available
                if self.db:
                    self.db.record_job(
                        input_file=video_file,
                        output_file=output_file,
                        codec=self.codec,
                        hardware_accel=False,
                        duration=0.0,
                        status="skipped",
                        error_message="Output file already exists",
                    )

                return 0.0
            elif not self.dry_run and self.force:
                console.print(
                    f"[INFO] Force flag set - will overwrite: {output_file.name}",
                    style="yellow",
                )

        if self.dry_run:
            console.print(
                f"[DRY RUN] Would transcode: {video_file.name} to {output_file.name}",
                style="blue",
            )
            return 1.0  # Return non-zero to indicate "success" for dry run

        # If analyze-only mode is enabled, just analyze the file and return
        if self.analyze_only:
            file_info = self.analyze_media_file(video_file)
            if self.db and file_info:
                self.db.update_media_library(video_file, file_info)
            return 0.0

        # Update statistics
        if video_file.exists():
            self.stats["total_size_before"] += video_file.stat().st_size

        # Try hardware acceleration first if available
        if self.codec == NVIDIA_CODEC:
            try:
                elapsed_time = self._try_transcode(
                    video_file, output_file, use_hardware=True
                )

                # Update statistics
                if output_file.exists():
                    self.stats["total_size_after"] += output_file.stat().st_size

                # Record in database if available
                if self.db:
                    self.db.record_job(
                        input_file=video_file,
                        output_file=output_file,
                        codec=self.codec,
                        hardware_accel=True,
                        duration=elapsed_time,
                        status="success",
                    )

                return elapsed_time
            except subprocess.CalledProcessError as e:
                # If hardware acceleration fails, try software encoding
                error_msg = e.stderr.decode() if e.stderr else ""
                if (
                    "Function not implemented" in error_msg
                    or "Impossible to convert" in error_msg
                ):
                    console.print(
                        f"[WARNING] Hardware acceleration failed, falling back to software encoding",
                        style="yellow",
                    )
                    try:
                        elapsed_time = self._try_transcode(
                            video_file, output_file, use_hardware=False
                        )

                        # Update statistics
                        if output_file.exists():
                            self.stats["total_size_after"] += output_file.stat().st_size

                        # Record in database if available
                        if self.db:
                            self.db.record_job(
                                input_file=video_file,
                                output_file=output_file,
                                codec=CPU_CODEC,
                                hardware_accel=False,
                                duration=elapsed_time,
                                status="success",
                                error_message="Hardware acceleration failed, used software encoding",
                            )

                        return elapsed_time
                    except subprocess.CalledProcessError as sw_e:
                        # Record failure in database
                        if self.db:
                            self.db.record_job(
                                input_file=video_file,
                                output_file=output_file,
                                codec=CPU_CODEC,
                                hardware_accel=False,
                                duration=0.0,
                                status="failed",
                                error_message=(
                                    sw_e.stderr.decode()
                                    if sw_e.stderr
                                    else "Software encoding failed"
                                ),
                            )
                        raise
                else:
                    # Record failure in database
                    if self.db:
                        self.db.record_job(
                            input_file=video_file,
                            output_file=output_file,
                            codec=self.codec,
                            hardware_accel=True,
                            duration=0.0,
                            status="failed",
                            error_message=error_msg,
                        )
                    # Re-raise for other types of errors
                    raise
        else:
            # Use software encoding directly
            try:
                elapsed_time = self._try_transcode(
                    video_file, output_file, use_hardware=False
                )

                # Update statistics
                if output_file.exists():
                    self.stats["total_size_after"] += output_file.stat().st_size

                # Record in database if available
                if self.db:
                    self.db.record_job(
                        input_file=video_file,
                        output_file=output_file,
                        codec=CPU_CODEC,
                        hardware_accel=False,
                        duration=elapsed_time,
                        status="success",
                    )

                return elapsed_time
            except subprocess.CalledProcessError as e:
                # Record failure in database
                if self.db:
                    self.db.record_job(
                        input_file=video_file,
                        output_file=output_file,
                        codec=CPU_CODEC,
                        hardware_accel=False,
                        duration=0.0,
                        status="failed",
                        error_message=(
                            e.stderr.decode()
                            if e.stderr
                            else "Software encoding failed"
                        ),
                    )
                raise

    def _try_transcode(
        self, video_file: Path, output_file: Path, use_hardware: bool = True
    ) -> float:
        """Internal method to attempt transcoding with specific settings."""
        # Build the command with Jellyfin-optimized parameters
        cmd = ["ffmpeg", "-y"]

        # Add verbose output for debugging
        if (
            hasattr(self, "args")
            and hasattr(self.args, "verbose")
            and self.args.verbose
        ):
            cmd.append("-v")
            cmd.append("info")
        else:
            cmd.append("-v")
            cmd.append("warning")

        # Only add hardware acceleration flags if using hardware
        if use_hardware and hasattr(self, "hwaccel_flags") and self.hwaccel_flags:
            cmd.extend(self.hwaccel_flags)
            console.print(
                f"[DEBUG] Using hardware acceleration flags: {self.hwaccel_flags}",
                style="dim",
            )

        # Add input file
        cmd.extend(["-i", str(video_file)])

        # Add encoding parameters based on codec and hardware acceleration
        if (
            use_hardware
            and self.codec == NVIDIA_CODEC
            and hasattr(self, "nvenc_params")
        ):
            # Use our custom NVENC parameters for better quality
            cmd.extend(
                [
                    "-c:v",
                    self.codec,
                    *self.nvenc_params,
                    "-pix_fmt",
                    "yuv420p",  # Pixel format for maximum compatibility
                    "-movflags",
                    "+faststart",  # Optimize for web streaming
                    # Audio parameters
                    "-c:a",
                    "aac",  # AAC audio codec for best compatibility
                    "-b:a",
                    "192k",  # Audio bitrate
                    "-ac",
                    "2",  # 2 audio channels (stereo)
                    "-ar",
                    "48000",  # Audio sample rate
                ]
            )

            # Only add subtitle encoding if the input has subtitles
            try:
                probe_data = self._get_media_info(video_file)
                has_subtitles = any(
                    stream.get("codec_type") == "subtitle"
                    for stream in probe_data.get("streams", [])
                )
                if has_subtitles:
                    cmd.extend(
                        ["-c:s", "mov_text"]
                    )  # Text-based subtitles compatible with MP4
                else:
                    cmd.extend(["-sn"])  # No subtitles
            except Exception:
                # If we can't determine subtitle info, just copy them
                cmd.extend(["-c:s", "copy"])

            console.print(
                f"[DEBUG] Using NVENC parameters: {self.nvenc_params}", style="dim"
            )
        else:
            # Get standard encoding parameters
            encoding_params = get_encoding_params(
                CPU_CODEC if not use_hardware else self.codec, use_hardware
            )
            cmd.extend(encoding_params)
            console.print(
                f"[DEBUG] Using standard encoding parameters: {encoding_params}",
                style="dim",
            )

        # Add output file
        cmd.append(str(output_file))

        # Print the full command for debugging
        if (
            hasattr(self, "args")
            and hasattr(self.args, "verbose")
            and self.args.verbose
        ):
            console.print(f"[DEBUG] Full ffmpeg command:\n{' '.join(cmd)}", style="dim")

        console.print(
            f"[INFO] Transcoding: {video_file.name} ({'hardware' if use_hardware else 'software'})",
            style="blue",
        )

        start_time = time.time()
        try:
            result = subprocess.run(cmd, check=True, capture_output=True)
            elapsed_time = time.time() - start_time
            console.print(
                f"[SUCCESS] Transcoded: {video_file.name} to {output_file.name}",
                style="green",
            )
            return elapsed_time
        except subprocess.CalledProcessError as e:
            console.print(f"[ERROR] Failed to transcode {video_file.name}", style="red")
            if e.stderr:
                error_msg = e.stderr.decode()
                # Show just the first few lines of error to avoid overwhelming output
                error_lines = error_msg.split("\n")[:3]
                console.print(
                    f"[ERROR] FFmpeg error: {' '.join(error_lines)}", style="red"
                )

                # Provide helpful suggestions based on error message
                if "moov atom not found" in error_msg:
                    console.print(
                        f"[TIP] File appears to be corrupted. Try repairing it with: ffmpeg -i {video_file.name} -c copy repaired_{video_file.name}",
                        style="blue",
                    )
                elif "Invalid data found when processing input" in error_msg:
                    console.print(
                        f"[TIP] File format may be unsupported or corrupted",
                        style="blue",
                    )
            raise  # Re-raise the exception to be caught by the caller

    def rename_file(self, video_file: Path) -> None:
        """Rename original video file with .backup extension."""
        # Check if we should keep originals
        if self.dry_run:
            console.print(
                f"[DRY RUN] Would rename: {video_file.name} to {video_file.name}.backup",
                style="blue",
            )
            return

        if self.keep_originals:
            console.print(
                f"[INFO] Keeping original file: {video_file.name}", style="blue"
            )
            return

        try:
            backup_file = video_file.with_suffix(f"{video_file.suffix}.backup")
            video_file.rename(backup_file)
            console.print(
                f"[INFO] Renamed original file to: {backup_file.name}", style="blue"
            )
        except Exception as e:
            console.print(
                f"[ERROR] Failed to rename original file: {str(e)}", style="red"
            )

    def _is_web_optimized(self, probe_data: Dict[str, Any], format_name: str) -> bool:
        """Check if a media file is optimized for web streaming.

        Args:
            probe_data: FFprobe data for the media file
            format_name: Format name of the media file

        Returns:
            True if the file is optimized for web streaming, False otherwise
        """
        # MP4 files with faststart are web optimized
        if format_name == "mp4":
            format_tags = probe_data.get("format", {}).get("tags", {})
            # Check for faststart flag in tags
            if format_tags.get("major_brand") == "isom" and "mov_text" in str(
                probe_data
            ):
                return True

        # Check video codec
        web_friendly_codecs = ["h264", "avc", "hevc", "vp9", "av1"]
        video_streams = [
            s for s in probe_data.get("streams", []) if s.get("codec_type") == "video"
        ]

        if not video_streams:
            return False

        video_codec = video_streams[0].get("codec_name", "").lower()

        # Check audio codec
        web_friendly_audio = ["aac", "mp3", "opus", "vorbis"]
        audio_streams = [
            s for s in probe_data.get("streams", []) if s.get("codec_type") == "audio"
        ]

        if not audio_streams:
            # No audio stream, just check video
            return video_codec in web_friendly_codecs

        audio_codec = audio_streams[0].get("codec_name", "").lower()

        # For MKV, check if it has web-friendly codecs
        if format_name == "matroska":
            return (
                video_codec in web_friendly_codecs and audio_codec in web_friendly_audio
            )

        # For MP4, already checked faststart above
        return False

    def repair_file(self, video_file: Path) -> Optional[Path]:
        """Attempt to repair a corrupted video file.

        Args:
            video_file: Path to the corrupted video file

        Returns:
            Optional[Path]: Path to repaired file if successful, None otherwise
        """
        if not video_file.exists():
            console.print(
                f"[ERROR] File does not exist: {video_file.name}", style="red"
            )
            return None

        console.print(
            f"[INFO] Attempting to repair file: {video_file.name}", style="blue"
        )

        # Create a temporary directory for repair operations
        temp_dir = Path("/tmp/jellyfin_repair")
        temp_dir.mkdir(exist_ok=True)

        # Generate a unique filename for the repaired file
        repaired_file = temp_dir / f"repaired_{video_file.name}"

        # Try different repair strategies
        repair_methods = [
            self._repair_remux,
            self._repair_rebuild_index,
            self._repair_copy_streams,
        ]

        for repair_method in repair_methods:
            try:
                result = repair_method(video_file, repaired_file)
                if result:
                    # Validate the repaired file
                    is_valid, _ = self.validate_media_file(repaired_file)
                    if is_valid:
                        # Copy the repaired file back to the original location with a different name
                        final_file = video_file.with_name(
                            f"{video_file.stem}_repaired{video_file.suffix}"
                        )
                        shutil.copy2(repaired_file, final_file)
                        console.print(
                            f"[SUCCESS] File repaired successfully: {final_file.name}",
                            style="green",
                        )

                        # Update stats
                        self.stats["repaired"] += 1

                        # Clean up temporary file
                        repaired_file.unlink(missing_ok=True)

                        return final_file
                    else:
                        console.print(
                            f"[ERROR] Repair attempt succeeded but file is still invalid",
                            style="red",
                        )
                        repaired_file.unlink(missing_ok=True)
            except Exception as e:
                console.print(f"[ERROR] Repair method failed: {str(e)}", style="red")

        console.print(
            f"[ERROR] All repair attempts failed for: {video_file.name}", style="red"
        )
        return None

    def _repair_remux(self, video_file: Path, output_file: Path) -> bool:
        """Repair by remuxing the file (simplest repair method).

        Args:
            video_file: Path to the corrupted video file
            output_file: Path to save the repaired file

        Returns:
            bool: True if repair was successful, False otherwise
        """
        console.print(
            f"[INFO] Trying repair by remuxing: {video_file.name}", style="blue"
        )

        cmd = [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(video_file),
            "-c",
            "copy",
            "-f",
            output_file.suffix.lstrip("."),
            str(output_file),
        ]

        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_file.exists() and output_file.stat().st_size > 0
        except subprocess.CalledProcessError:
            return False

    def _repair_rebuild_index(self, video_file: Path, output_file: Path) -> bool:
        """Repair by rebuilding the index (moov atom).

        Args:
            video_file: Path to the corrupted video file
            output_file: Path to save the repaired file

        Returns:
            bool: True if repair was successful, False otherwise
        """
        console.print(
            f"[INFO] Trying repair by rebuilding index: {video_file.name}", style="blue"
        )

        cmd = [
            "ffmpeg",
            "-v",
            "error",
            "-err_detect",
            "ignore_err",
            "-i",
            str(video_file),
            "-c",
            "copy",
            "-movflags",
            "faststart",
            str(output_file),
        ]

        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_file.exists() and output_file.stat().st_size > 0
        except subprocess.CalledProcessError:
            return False

    def _repair_copy_streams(self, video_file: Path, output_file: Path) -> bool:
        """Repair by extracting and copying individual streams.

        Args:
            video_file: Path to the corrupted video file
            output_file: Path to save the repaired file

        Returns:
            bool: True if repair was successful, False otherwise
        """
        console.print(
            f"[INFO] Trying repair by copying streams: {video_file.name}", style="blue"
        )

        # First, try to get stream information
        cmd_probe = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "stream=index,codec_type",
            "-of",
            "json",
            str(video_file),
        ]

        try:
            result = subprocess.run(
                cmd_probe, capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)

            if "streams" not in data or not data["streams"]:
                return False

            # Build a command to extract each stream individually
            cmd = ["ffmpeg", "-v", "error"]

            # Add input file
            cmd.extend(["-i", str(video_file)])

            # Map all streams
            for stream in data["streams"]:
                cmd.extend(["-map", f"0:{stream['index']}"])

            # Copy all codecs
            cmd.extend(["-c", "copy"])

            # Add output file
            cmd.append(str(output_file))

            # Run the command
            subprocess.run(cmd, capture_output=True, check=True)
            return output_file.exists() and output_file.stat().st_size > 0
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            return False

        repaired_file = video_file.with_name(f"repaired_{video_file.name}")

        # Skip if repaired file already exists
        if repaired_file.exists():
            console.print(
                f"[INFO] Repaired file already exists: {repaired_file.name}",
                style="blue",
            )
            return repaired_file

        console.print(
            f"[INFO] Attempting to repair file: {video_file.name}", style="blue"
        )

        # Try to repair the file using ffmpeg's stream copy
        cmd = [
            "ffmpeg",
            "-v",
            "warning",
            "-y",
            "-i",
            str(video_file),
            "-c",
            "copy",
            str(repaired_file),
        ]

        try:
            result = subprocess.run(cmd, check=True, capture_output=True)
            console.print(
                f"[SUCCESS] Repaired file: {video_file.name} -> {repaired_file.name}",
                style="green",
            )
            return repaired_file
        except subprocess.CalledProcessError as e:
            console.print(
                f"[ERROR] Failed to repair file: {video_file.name}", style="red"
            )
            if e.stderr:
                error_msg = e.stderr.decode()
                error_lines = error_msg.split("\n")[:2]
                console.print(
                    f"[ERROR] FFmpeg repair error: {' '.join(error_lines)}", style="red"
                )
            return None

    def _process_batch_files(self, batch: List[Path], progress) -> None:
        """Process a batch of video files with a shared progress bar."""
        console.print(
            f"[INFO] Starting batch processing of {len(batch)} files", style="blue"
        )

        # Add a nested task for the files in this batch
        files_task = progress.add_task(f"[green]Transcoding files...", total=len(batch))

        # Track successful and failed files
        successful = 0
        failed = 0
        skipped = 0

        # Process each file in the batch
        for video_file in batch:
            # Skip files that are already transcoded (have _jellyfin.mp4 suffix)
            if "_jellyfin.mp4" in video_file.name:
                console.print(
                    f"[INFO] Skipping already transcoded file: {video_file.name}",
                    style="blue",
                )
                skipped += 1
                progress.update(files_task, advance=1)
                self.total_files += 1
                continue

            # First validate the file (quick check if it exists)
            if not video_file.exists():
                console.print(
                    f"[ERROR] File does not exist: {video_file.name}", style="red"
                )
                failed += 1
                progress.update(files_task, advance=1)
                self.total_files += 1
                continue

            try:
                # Try to transcode the file
                elapsed_time = self.transcode(video_file)
                self.total_real_time += elapsed_time

                # Only rename if transcoding was successful
                if elapsed_time > 0 or self.dry_run:
                    self.rename_file(video_file)
                    successful += 1
                else:
                    failed += 1

            except Exception as e:
                # Handle transcoding errors
                console.print(
                    f"[ERROR] Exception during transcoding: {str(e)}", style="red"
                )

                # Try to repair the file if enabled
                if self.args.repair:
                    repaired_file = self.repair_file(video_file)
                    if repaired_file:
                        console.print(
                            f"[INFO] Attempting to transcode repaired file",
                            style="blue",
                        )
                        try:
                            # Try to transcode the repaired file
                            elapsed_time = self.transcode(repaired_file)
                            self.total_real_time += elapsed_time

                            if elapsed_time > 0:
                                console.print(
                                    f"[SUCCESS] Transcoded repaired file successfully",
                                    style="green",
                                )
                                successful += 1
                            else:
                                failed += 1
                        except Exception as repair_e:
                            console.print(
                                f"[ERROR] Failed to transcode repaired file: {str(repair_e)}",
                                style="red",
                            )
                            failed += 1
                    else:
                        failed += 1
                else:
                    failed += 1

            self.total_files += 1
            progress.update(files_task, advance=1)

        # Report batch results
        console.print(
            f"[INFO] Batch results: {successful} successful, {failed} failed, {skipped} skipped",
            style="blue",
        )
        console.print(
            f"[INFO] Completed batch processing of {len(batch)} files", style="green"
        )

    def process_files_parallel(
        self, video_files: List[Path], max_workers: int = 2
    ) -> None:
        """Process video files in parallel batches."""
        # Split files into batches
        batches = [
            video_files[i : i + BATCH_SIZE]
            for i in range(0, len(video_files), BATCH_SIZE)
        ]

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            batch_task = progress.add_task(
                "[cyan]Processing batches...", total=len(batches)
            )

            for batch in batches:
                self._process_batch_files(batch, progress)
                progress.update(batch_task, advance=1)

    def generate_report(self) -> None:
        """Generate a report of transcoding statistics."""
        table = Table(title="Transcoding Report")

        table.add_column("Extension", style="cyan")
        table.add_column("Count", style="green", justify="right")

        for ext, count in self.extension_counts.items():
            table.add_row(ext, str(count))

        console.print(table)

        console.print(
            f"Total processing time: {self.total_real_time:.3f} seconds", style="blue"
        )

        if self.total_files > 0:
            avg_time = self.total_real_time / self.total_files
            console.print(
                f"Average time per file: {avg_time:.2f} seconds", style="blue"
            )

        # Display size reduction if applicable
        if self.stats["total_size_before"] > 0 and self.stats["total_size_after"] > 0:
            size_before_mb = self.stats["total_size_before"] / (1024 * 1024)
            size_after_mb = self.stats["total_size_after"] / (1024 * 1024)
            reduction = (
                (1 - (size_after_mb / size_before_mb)) * 100
                if size_before_mb > 0
                else 0
            )

            console.print(f"Total size before: {size_before_mb:.2f} MB", style="blue")
            console.print(f"Total size after: {size_after_mb:.2f} MB", style="blue")
            console.print(
                f"Size reduction: {reduction:.2f}%",
                style="green" if reduction > 0 else "red",
            )

        # Display processing statistics
        console.print(f"Files processed: {self.stats['processed']}", style="blue")
        console.print(
            f"Successfully transcoded: {self.stats['successful']}", style="green"
        )
        console.print(f"Failed: {self.stats['failed']}", style="red")
        console.print(f"Skipped: {self.stats['skipped']}", style="yellow")
        if self.stats["repaired"] > 0:
            console.print(f"Repaired: {self.stats['repaired']}", style="blue")

    def clean_media_library(self, directory: Path) -> None:
        """Clean the media library by removing corrupted files and updating the database.

        Args:
            directory: Directory to clean
        """
        if not directory.exists() or not directory.is_dir():
            console.print(f"[ERROR] Invalid directory: {directory}", style="red")
            return

        console.print(
            f"[INFO] Scanning directory for media files: {directory}", style="blue"
        )

        # Find all media files
        media_files = []
        for ext in SUPPORTED_EXTENSIONS:
            media_files.extend(list(directory.glob(f"**/*{ext}")))

        if not media_files:
            console.print("[INFO] No media files found", style="yellow")
            return

        console.print(
            f"[INFO] Found {len(media_files)} media files to analyze", style="blue"
        )

        # Track statistics
        stats = {
            "total": len(media_files),
            "valid": 0,
            "invalid": 0,
            "repaired": 0,
            "removed": 0,
        }

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Analyzing files...", total=len(media_files))

            for media_file in media_files:
                # Check if the file is valid
                is_valid, error_message = self.validate_media_file(media_file)

                if is_valid:
                    stats["valid"] += 1

                    # Update the database if available
                    if self.db:
                        file_info = self.analyze_media_file(media_file)
                        if file_info:
                            self.db.update_media_library(media_file, file_info)
                else:
                    stats["invalid"] += 1
                    console.print(
                        f"[WARNING] Invalid file: {media_file.name} - {error_message}",
                        style="yellow",
                    )

                    # Try to repair the file if repair flag is set
                    if self.args.repair:
                        console.print(
                            f"[INFO] Attempting to repair: {media_file.name}",
                            style="blue",
                        )
                        repaired_file = self.repair_file(media_file)

                        if repaired_file:
                            stats["repaired"] += 1
                            console.print(
                                f"[SUCCESS] Repaired file: {media_file.name}",
                                style="green",
                            )

                            # Update the database if available
                            if self.db:
                                file_info = self.analyze_media_file(repaired_file)
                                if file_info:
                                    file_info["status"] = "repaired"
                                    file_info["notes"] = (
                                        f"Repaired from {media_file.name}"
                                    )
                                    self.db.update_media_library(
                                        repaired_file, file_info
                                    )
                        else:
                            console.print(
                                f"[ERROR] Could not repair: {media_file.name}",
                                style="red",
                            )

                            # Remove the file if force flag is set or if we're in clean mode with --force
                            if self.force:
                                try:
                                    media_file.unlink()
                                    stats["removed"] += 1
                                    console.print(
                                        f"[INFO] Removed corrupted file: {media_file.name}",
                                        style="blue",
                                    )

                                    # Remove from database if available
                                    if self.db and hasattr(
                                        self.db, "remove_media_file"
                                    ):
                                        self.db.remove_media_file(media_file)
                                except Exception as e:
                                    console.print(
                                        f"[ERROR] Failed to remove file: {media_file.name} - {str(e)}",
                                        style="red",
                                    )
                    else:
                        # If repair is not enabled but force is, remove invalid files directly
                        if self.force:
                            try:
                                media_file.unlink()
                                stats["removed"] += 1
                                console.print(
                                    f"[INFO] Removed invalid file: {media_file.name}",
                                    style="blue",
                                )

                                # Remove from database if available
                                if self.db and hasattr(self.db, "remove_media_file"):
                                    self.db.remove_media_file(media_file)
                            except Exception as e:
                                console.print(
                                    f"[ERROR] Failed to remove file: {media_file.name} - {str(e)}",
                                    style="red",
                                )
                        else:
                            # If neither repair nor force is enabled, suggest using --force
                            console.print(
                                f"[TIP] Use --force to remove invalid files or --repair to attempt repair",
                                style="blue",
                            )

                progress.update(task, advance=1)

        # Print summary
        console.print("\n[bold]Media Library Cleaning Summary:[/bold]")
        console.print(f"Total files: {stats['total']}")
        console.print(f"Valid files: {stats['valid']}", style="green")
        console.print(f"Invalid files: {stats['invalid']}", style="yellow")
        console.print(f"Repaired files: {stats['repaired']}", style="blue")
        console.print(f"Removed files: {stats['removed']}", style="red")

    def analyze_media_library(self, directory: Path) -> None:
        """Analyze all media files in a directory and update the database.

        Args:
            directory: Directory to analyze
        """
        if not directory.exists() or not directory.is_dir():
            console.print(f"[ERROR] Invalid directory: {directory}", style="red")
            return

        console.print(
            f"[INFO] Scanning directory for media files: {directory}", style="blue"
        )

        # Find all media files
        media_files = []
        for ext in SUPPORTED_EXTENSIONS:
            media_files.extend(list(directory.glob(f"**/*{ext}")))

        if not media_files:
            console.print("[INFO] No media files found", style="yellow")
            return

        console.print(
            f"[INFO] Found {len(media_files)} media files to analyze", style="blue"
        )

        # Track statistics
        stats = {"total": len(media_files), "analyzed": 0, "failed": 0}

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Analyzing files...", total=len(media_files))

            for media_file in media_files:
                file_info = self.analyze_media_file(media_file)

                if file_info:
                    stats["analyzed"] += 1

                    # Update the database if available
                    if self.db:
                        self.db.update_media_library(media_file, file_info)

                    # Print file information if verbose
                    if self.args.verbose if hasattr(self.args, "verbose") else False:
                        console.print(
                            f"[INFO] Analyzed: {media_file.name}", style="blue"
                        )
                        for key, value in file_info.items():
                            console.print(f"  {key}: {value}")
                else:
                    stats["failed"] += 1
                    console.print(
                        f"[ERROR] Failed to analyze: {media_file.name}", style="red"
                    )

                progress.update(task, advance=1)

        # Print summary
        console.print("\n[bold]Media Library Analysis Summary:[/bold]")
        console.print(f"Total files: {stats['total']}")
        console.print(f"Successfully analyzed: {stats['analyzed']}", style="green")
        console.print(f"Failed to analyze: {stats['failed']}", style="red")

    def run_tests(self) -> bool:
        """Run unit tests for the transcoder."""
        console.print("[INFO] Running unit tests", style="blue")

        tests_passed = True

        # Test 1: Check if ffmpeg is available
        try:
            subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
            console.print("[TEST PASSED] FFmpeg is available", style="green")
        except (subprocess.CalledProcessError, FileNotFoundError):
            console.print("[TEST FAILED] FFmpeg is not available", style="red")
            tests_passed = False

        # Test 2: Check hardware acceleration detection
        self.check_hardware_acceleration()
        if self.codec in [NVIDIA_CODEC, CPU_CODEC]:
            console.print(
                "[TEST PASSED] Hardware acceleration check works", style="green"
            )
        else:
            console.print(
                "[TEST FAILED] Hardware acceleration check failed", style="red"
            )
            tests_passed = False

        # Test 3: Check if we can create temporary files
        try:
            temp_file = Path("/tmp/transcoder_test.txt")
            temp_file.write_text("test")
            temp_file.unlink()
            console.print("[TEST PASSED] File operations work", style="green")
        except Exception as e:
            console.print(f"[TEST FAILED] File operations failed: {e}", style="red")
            tests_passed = False

        # Test 4: Test NVENC parameters if available
        if self.codec == NVIDIA_CODEC:
            try:
                test_cmd = ["ffmpeg", "-hide_banner", "-h", "encoder=hevc_nvenc"]
                result = subprocess.run(
                    test_cmd, capture_output=True, text=True, check=True
                )
                if "b:v" in result.stdout and "preset" in result.stdout:
                    console.print(
                        "[TEST PASSED] FFmpeg supports NVENC parameters", style="green"
                    )
                else:
                    console.print(
                        "[TEST WARNING] FFmpeg may not support all NVENC parameters",
                        style="yellow",
                    )
            except Exception as e:
                console.print(
                    f"[TEST WARNING] Could not verify NVENC parameter support: {e}",
                    style="yellow",
                )

        # Test 5: Test CPU encoding parameters
        try:
            test_cmd = ["ffmpeg", "-hide_banner", "-h", "encoder=libx264"]
            result = subprocess.run(
                test_cmd, capture_output=True, text=True, check=True
            )
            if "crf" in result.stdout and "preset" in result.stdout:
                console.print(
                    "[TEST PASSED] FFmpeg supports x264 parameters", style="green"
                )
            else:
                console.print(
                    "[TEST WARNING] FFmpeg may not support all x264 parameters",
                    style="yellow",
                )
        except Exception as e:
            console.print(
                f"[TEST WARNING] Could not verify x264 parameter support: {e}",
                style="yellow",
            )

        return tests_passed

    def run(self) -> int:
        """Main function to run the transcoder."""
        if self.test_mode:
            if self.run_tests():
                console.print("[INFO] All tests passed", style="green")
                return 0
            else:
                console.print("[ERROR] Some tests failed", style="red")
                return 1

        if not self.target_location:
            console.print("[ERROR] Target location must be specified", style="red")
            return 1

        self.check_hardware_acceleration()

        # Handle clean mode
        if self.clean_mode:
            console.print(
                f"[INFO] Running in clean mode for {self.target_location}", style="blue"
            )
            self.clean_media_library(Path(self.target_location))
            return 0

        # Handle analyze-only mode
        if self.analyze_only:
            console.print(
                f"[INFO] Running in analyze-only mode for {self.target_location}",
                style="blue",
            )
            self.analyze_media_library(Path(self.target_location))
            return 0

        video_files = self.find_video_files()
        if not video_files:
            console.print("[INFO] No supported video files found", style="yellow")
            return 0

        console.print(
            f"[INFO] Found {len(video_files)} video files to process", style="blue"
        )

        if self.dry_run:
            console.print(
                "[INFO] Running in dry-run mode, no files will be modified",
                style="blue",
            )

        self.process_files_parallel(video_files, max_workers=self.args.parallel)
        self.generate_report()

        return 0


def main():
    parser = argparse.ArgumentParser(
        description="Transcode video files to MP4 format optimized for Jellyfin streaming"
    )

    # Basic options
    parser.add_argument(
        "-t", "--target", help="Target location to operate on", type=str
    )
    parser.add_argument(
        "-n", "--dry-run", help="Enable dry-run mode", action="store_true"
    )
    parser.add_argument(
        "-d", "--destination", help="Specify a destination for output files", type=str
    )
    parser.add_argument("-T", "--test", help="Enable test mode", action="store_true")
    parser.add_argument(
        "-p",
        "--parallel",
        help="Number of parallel workers (default: 2)",
        type=int,
        default=2,
    )
    parser.add_argument(
        "-v", "--verbose", help="Enable verbose output", action="store_true"
    )

    # Transcoding options
    parser.add_argument(
        "-f",
        "--force",
        help="Force transcoding even if file validation fails or output exists",
        action="store_true",
    )
    parser.add_argument(
        "--skip-validation",
        help="Skip media file validation (faster but less safe)",
        action="store_true",
    )
    parser.add_argument(
        "--keep-originals",
        help="Don't rename original files (keep both versions)",
        action="store_true",
    )
    parser.add_argument(
        "--software-only",
        help="Use software encoding only (disable hardware acceleration)",
        action="store_true",
    )
    parser.add_argument(
        "--repair",
        help="Attempt to repair corrupted files before transcoding",
        action="store_true",
    )

    # Filename options
    parser.add_argument(
        "--web-safe-names",
        help="Generate web-safe filenames for output files",
        action="store_true",
    )

    # Database options
    parser.add_argument(
        "--db-path",
        help=f"Path to the database file (default: {DEFAULT_DB_PATH})",
        type=str,
    )
    parser.add_argument(
        "--list-jobs",
        help="List recent transcoding jobs from the database",
        action="store_true",
    )
    parser.add_argument(
        "--job-limit",
        help="Maximum number of jobs to list (default: 20)",
        type=int,
        default=20,
    )

    # Media library management options
    parser.add_argument(
        "--analyze", help="Analyze media files without transcoding", action="store_true"
    )
    parser.add_argument(
        "--clean",
        help="Clean the media library by removing corrupted files",
        action="store_true",
    )
    parser.add_argument(
        "--list-media", help="List media files in the database", action="store_true"
    )
    parser.add_argument(
        "--media-limit",
        help="Maximum number of media files to list (default: 50)",
        type=int,
        default=50,
    )
    parser.add_argument(
        "--update-library",
        help="Update the media library with information from files",
        action="store_true",
    )
    parser.add_argument(
        "--reset-db",
        help="Reset the database by deleting all records",
        action="store_true",
    )

    args = parser.parse_args()

    # Display banner
    console.print("[bold blue]Jellyfin Transcoder[/bold blue]")
    console.print("Optimizing video files for Jellyfin streaming...\n")

    # Set global variables
    global software_only
    software_only = args.software_only if hasattr(args, "software_only") else False

    # Handle database operations first
    if args.list_jobs or args.list_media or args.reset_db:
        db_path = (
            args.db_path
            if hasattr(args, "db_path") and args.db_path
            else DEFAULT_DB_PATH
        )
        db = TranscoderDB(db_path)

        if args.reset_db:
            console.print(f"[INFO] Resetting database: {db_path}", style="yellow")
            db.reset_database()
            console.print(
                "[INFO] Database has been reset. All records have been deleted.",
                style="green",
            )
            db.close()
            return 0

        if args.list_jobs:
            console.print(
                f"[INFO] Listing recent transcoding jobs from database: {db_path}",
                style="blue",
            )
            jobs = db.get_recent_jobs(limit=args.job_limit)

            if not jobs:
                console.print(
                    "[INFO] No transcoding jobs found in the database", style="yellow"
                )
            else:
                table = Table(
                    title=f"Recent Transcoding Jobs (showing {len(jobs)} of {args.job_limit} requested)"
                )
                table.add_column("ID", style="cyan")
                table.add_column("Input File", style="green")
                table.add_column("Status", style="yellow")
                table.add_column("Codec", style="blue")
                table.add_column("HW Accel", style="magenta")
                table.add_column("Duration", style="cyan")
                table.add_column("Timestamp", style="blue")

                for job in jobs:
                    input_file = os.path.basename(job["input_file"])
                    table.add_row(
                        job["id"][:8],  # Show only first 8 chars of UUID
                        input_file,
                        job["status"],
                        job["codec"],
                        "Yes" if job["hardware_accel"] else "No",
                        f"{job['duration']:.2f}s",
                        job["timestamp"],
                    )

                console.print(table)

        if args.list_media:
            console.print(
                f"[INFO] Listing media files from database: {db_path}", style="blue"
            )
            media_files = db.get_media_files(limit=args.media_limit)

            if not media_files:
                console.print(
                    "[INFO] No media files found in the database", style="yellow"
                )
            else:
                table = Table(
                    title=f"Media Library (showing {len(media_files)} of {args.media_limit} requested)"
                )
                table.add_column("File", style="cyan")
                table.add_column("Format", style="green")
                table.add_column("Size", style="yellow")
                table.add_column("Duration", style="blue")
                table.add_column("Resolution", style="magenta")
                table.add_column("Video Codec", style="cyan")
                table.add_column("Web Optimized", style="green")
                table.add_column("Status", style="blue")

                for media in media_files:
                    file_name = os.path.basename(media["file_path"])
                    file_size = f"{media['file_size'] / (1024*1024):.2f} MB"
                    duration = (
                        f"{media.get('duration', 0):.2f}s"
                        if media.get("duration")
                        else "N/A"
                    )

                    # Determine web optimization status
                    web_optimized = "Yes" if media.get("web_optimized", False) else "No"
                    web_opt_style = "green" if web_optimized == "Yes" else "red"

                    table.add_row(
                        file_name,
                        media["format"],
                        file_size,
                        duration,
                        media.get("resolution", "N/A"),
                        media.get("video_codec", "N/A"),
                        web_optimized,
                        media["status"],
                    )

                console.print(table)

        db.close()
        return 0

    transcoder = Transcoder(args)
    return transcoder.run()


if __name__ == "__main__":
    exit(main())
