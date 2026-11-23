# Python Video Downloader (Tkinter)

A small desktop Python project with a **Tkinter GUI** and a reusable video-download module. It demonstrates desktop event handling, basic URL validation, background work and progress/error messages.

The original experimental scripts `d.py` and `downalod.py` remain in the repository as historical references. The new supported entry point is **`app.py`**.

## Features

- Paste a YouTube video URL and choose a local save directory
- Select a maximum preferred video height (480p, 720p or 1080p)
- Use `yt-dlp` for current extractor support rather than the old `pytube` implementation
- Keep the desktop UI responsive while downloading in a worker thread
- Report download progress, errors and completion through Tkinter's main thread

## Install & run

Requires Python 3.10+, Tkinter (typically bundled with Python on Windows), and `ffmpeg` available on PATH for merging separate audio/video tracks.

```bash
python -m pip install -r requirements.txt
python app.py
python -m unittest discover -s tests -v
```

Check `ffmpeg -version` in your terminal if a high-resolution download fails at the merge step. The best available format depends on the source.

## Project scope and responsibility

**Only download media you own, have permission to save, or are otherwise authorized to download.** Respect copyright and the website's terms of service. This project does not bypass DRM or access restrictions, and it is not a general-purpose downloader for arbitrary hosts.

No playlist automation or cloud service is provided. YouTube and downloader dependencies change over time, so an extractor that works today is not guaranteed to continue working.
