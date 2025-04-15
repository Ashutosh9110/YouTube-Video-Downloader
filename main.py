import tkinter
import customtkinter
import re
# from pytube import YouTube
from pytubefix import YouTube

# download setting

def startDownload():
    try:
        ytLink = link.get()
        # Remove any trailing whitespace and validate URL format
        ytLink = ytLink.strip()
        
        # Remove @ symbol if it's at the beginning of the URL
        if ytLink.startswith('@'):
            ytLink = ytLink[1:]
            
        # Extract video ID from various YouTube URL formats
        video_id = None
        
        # Pattern for youtube.com/watch?v=VIDEO_ID
        watch_pattern = r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]+)'
        match = re.search(watch_pattern, ytLink)
        
        if match:
            video_id = match.group(1)
            # Reconstruct a clean YouTube URL
            ytLink = f"https://www.youtube.com/watch?v={video_id}"
            
            # Create the YouTube object with progress callback
            ytObject = YouTube(ytLink, on_progress_callback=on_progress)
            video = ytObject.streams.get_highest_resolution()

            title.configure(text=ytObject.title, text_color="white")
            finishLabel.configure(text="")
            video.download()
            finishLabel.configure(text="Downloaded!", text_color="green")
        else:
            finishLabel.configure(text="Please enter a valid YouTube video URL", text_color="red")
    except Exception as e:
        print(f"Error: {str(e)}")
        finishLabel.configure(text=f"Download failed: {str(e)}", text_color="red")
    
def on_progress(stream, chunk, bytes_remaining):
    try:
        total_size = stream.filesize
        if total_size > 0:  # Ensure we don't divide by zero
            bytes_downloaded = total_size - bytes_remaining
            percentage_of_completion = bytes_downloaded / total_size * 100
            per = str(int(percentage_of_completion))
            progressPercentage.configure(text = per + "%")
            progressPercentage.update()
            # update progress bar
            progressBar.set(float(percentage_of_completion) / 100)
    except Exception as e:
        print(f"Progress callback error: {str(e)}")
        # Don't update UI on error to avoid crashes
        pass

# system settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

def button_callback():
    print("button pressed")
# Our app frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("Youtube Downloader")
# app.grid_columnconfigure(0, weight=1)
# app.grid_rowconfigure(0, weight=1   )

# Adding UI elements
title = customtkinter.CTkLabel(app, text="Insert a youtube link")
# title.grid(row = 0, column = 0, padx = 20, pady = 20, stick="ew")
title.pack(padx=10, pady=10)

# Link input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# Finished Downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# Progress percentage
progressPercentage = customtkinter.CTkLabel(app, text="0%")
progressPercentage.pack()

progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)


# Download button
download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=10, pady=10)
# Run app
app.mainloop()
