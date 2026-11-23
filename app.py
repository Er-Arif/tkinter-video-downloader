"""Tkinter frontend for downloading authorized YouTube videos."""
from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from download import download_video, validate_youtube_url


class VideoDownloader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Video Downloader")
        self.geometry("580x265")
        self.resizable(True, False)
        self.events = queue.Queue()
        self.url = tk.StringVar()
        self.output_path = tk.StringVar()
        self.height_choice = tk.StringVar(value="720")
        self.status = tk.StringVar(value="Ready")
        self._build()
        self.after(150, self._handle_events)

    def _build(self):
        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)
        ttk.Label(frame, text="YouTube URL").grid(row=0, column=0, sticky="w", pady=7)
        ttk.Entry(frame, textvariable=self.url).grid(
            row=0, column=1, columnspan=2, sticky="ew", pady=7
        )
        ttk.Label(frame, text="Save to").grid(row=1, column=0, sticky="w", pady=7)
        ttk.Entry(frame, textvariable=self.output_path).grid(
            row=1, column=1, sticky="ew", pady=7
        )
        ttk.Button(frame, text="Browse", command=self._select_folder).grid(
            row=1, column=2, padx=(8, 0)
        )
        ttk.Label(frame, text="Maximum height").grid(row=2, column=0, sticky="w", pady=7)
        ttk.Combobox(
            frame, textvariable=self.height_choice, values=["480", "720", "1080"],
            state="readonly", width=12
        ).grid(row=2, column=1, sticky="w", pady=7)
        self.download_button = ttk.Button(
            frame, text="Download", command=self._start_download
        )
        self.download_button.grid(row=3, column=1, sticky="w", pady=12)
        ttk.Label(frame, textvariable=self.status, wraplength=500).grid(
            row=4, column=0, columnspan=3, sticky="w", pady=5
        )

    def _select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_path.set(folder)

    def _start_download(self):
        try:
            url = validate_youtube_url(self.url.get())
            folder = self.output_path.get()
            height = int(self.height_choice.get())
            if not folder:
                raise ValueError("Choose a download folder")
        except ValueError as error:
            messagebox.showerror("Check input", str(error))
            return
        self.download_button.configure(state="disabled")
        self.status.set("Starting...")
        threading.Thread(
            target=self._download_worker, args=(url, folder, height), daemon=True
        ).start()

    def _download_worker(self, url, folder, height):
        def on_progress(info):
            if info.get("status") == "downloading":
                downloaded = info.get("downloaded_bytes", 0)
                total = info.get("total_bytes") or info.get("total_bytes_estimate") or 0
                if total:
                    self.events.put(("progress", f"Downloading: {downloaded / total:.0%}"))
                else:
                    self.events.put(("progress", "Downloading..."))
            elif info.get("status") == "finished":
                self.events.put(("progress", "Download finished; processing media..."))
        try:
            download_video(url, folder, height, progress_callback=on_progress)
            self.events.put(("done", "Saved to selected folder"))
        except Exception as error:
            self.events.put(("error", str(error)))

    def _handle_events(self):
        try:
            while True:
                kind, value = self.events.get_nowait()
                if kind == "progress":
                    self.status.set(value)
                else:
                    self.download_button.configure(state="normal")
                    self.status.set(value)
                    if kind == "error":
                        messagebox.showerror("Download failed", value)
                    elif kind == "done":
                        messagebox.showinfo("Complete", value)
        except queue.Empty:
            pass
        self.after(150, self._handle_events)


if __name__ == "__main__":
    VideoDownloader().mainloop()
