import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube

def browse_output_path():
    output_path = filedialog.askdirectory()
    entry_output_path.delete(0, tk.END)  # Clear the current output path
    entry_output_path.insert(0, output_path)  # Insert the selected output path

def download_video():
    video_url = entry_url.get()
    output_path = entry_output_path.get()
    resolution = resolution_var.get()
    file_format = file_format_var.get()

    try:
        yt = YouTube(video_url)
        stream = yt.streams.filter(res=resolution, file_extension=file_format).first()
        stream.download(output_path)
        messagebox.showinfo("Success", "Video downloaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create the main window
root = tk.Tk()
root.title("YouTube Video Downloader")

# Create and place widgets
label_url = tk.Label(root, text="YouTube Video URL:")
label_url.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_url = tk.Entry(root, width=50)
entry_url.grid(row=0, column=1, padx=5, pady=5)

label_output_path = tk.Label(root, text="Output Path:")
label_output_path.grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_output_path = tk.Entry(root, width=40)
entry_output_path.grid(row=1, column=1, padx=5, pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_output_path)
browse_button.grid(row=1, column=2, padx=5, pady=5)

label_resolution = tk.Label(root, text="Video Resolution:")
label_resolution.grid(row=2, column=0, padx=5, pady=5, sticky="w")
resolution_var = tk.StringVar(root)
resolution_var.set("1080p")  # Default resolution
resolution_options = ["1080p", "720p", "480p"]
resolution_menu = tk.OptionMenu(root, resolution_var, *resolution_options)
resolution_menu.grid(row=2, column=1, padx=5, pady=5)

label_format = tk.Label(root, text="Video Format:")
label_format.grid(row=3, column=0, padx=5, pady=5, sticky="w")
file_format_var = tk.StringVar(root)
file_format_var.set("mp4")  # Default format
file_format_options = ["mp4", "webm", "3gp"]
file_format_menu = tk.OptionMenu(root, file_format_var, *file_format_options)
file_format_menu.grid(row=3, column=1, padx=5, pady=5)

download_button = tk.Button(root, text="Download", command=download_video)
download_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Run the application
root.mainloop()
