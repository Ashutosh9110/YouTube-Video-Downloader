import tkinter
import customtkinter
# from pytube import YouTube
from pytubefix import YouTube

# download setting

def startDownload():
    try:
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()

        title.configure(text=ytObject.title, text_color="white")
        finishLabel.configure(text="")
        video.download()
        finishLabel.configure(text="Downloaded!")
    except:
        finishLabel.configure(text="Youtube link is invalid", text_color="red")
    
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    progressPercentage.configure(text = per + "%")
    progressPercentage.update()

# update progress bar

    progressBar.set(float(percentage_of_completion) / 100 )

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
