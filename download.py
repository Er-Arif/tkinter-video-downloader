"""Backend helpers for permission-based YouTube downloads."""
from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse


_ALLOWED_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}


def validate_youtube_url(url: str) -> str:
    if not url or not url.strip():
        raise ValueError("Enter a YouTube video URL")
    value = url.strip()
    parsed = urlparse(value)
    if parsed.scheme != "https" or (parsed.hostname or "").lower() not in _ALLOWED_HOSTS:
        raise ValueError("Only HTTPS YouTube watch, Shorts or youtu.be links are supported")
    if not parsed.path or parsed.path == "/":
        raise ValueError("Link does not point to a video")
    return value


def format_for_height(height: int) -> str:
    if height not in (480, 720, 1080):
        raise ValueError("Supported heights: 480, 720, 1080")
    return (
        f"bestvideo[height<={height}]+bestaudio/"
        f"best[height<={height}]/best"
    )


def download_video(url: str, folder: str | Path, height: int = 720,
                   progress_callback=None) -> None:
    """Download an authorized video; merging may require ffmpeg on PATH."""
    from yt_dlp import YoutubeDL

    safe_url = validate_youtube_url(url)
    directory = Path(folder).expanduser()
    if not directory.is_dir():
        raise ValueError("Choose an existing output folder")
    options = {
        "format": format_for_height(height),
        "paths": {"home": str(directory)},
        "outtmpl": "%(title).180B [%(id)s].%(ext)s",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }
    if progress_callback:
        options["progress_hooks"] = [progress_callback]
    with YoutubeDL(options) as ydl:
        ydl.download([safe_url])
