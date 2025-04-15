import tkinter
import customtkinter
import re
import os
# Switch from pytubefix to pytube with additional handling
from pytube import YouTube
import subprocess
import sys

# Available video qualities
VIDEO_QUALITIES = ["1080p", "720p", "480p", "360p"]

# Check if yt-dlp is installed, and install if not
def ensure_yt_dlp():
    try:
        subprocess.run(["yt-dlp", "--version"], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        print("yt-dlp not found, installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)
            return True
        except Exception as e:
            print(f"Failed to install yt-dlp: {e}")
            return False

# Get available qualities using yt-dlp
def get_available_formats(url):
    try:
        # Get video info using yt-dlp
        cmd = ["yt-dlp", "-F", url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error getting formats: {result.stderr}")
            return {}
        
        formats = {}
        best_audio_id = None
        best_audio_size = 0
        # First find best audio stream
        for line in result.stdout.split('\n'):
            if "audio only" in line.lower():
                parts = line.split()
                if len(parts) >= 2:
                    format_id = parts[0]
                    # Try to get audio size
                    size_match = re.search(r'(\d+)k', line.lower())
                    if size_match:
                        size = int(size_match.group(1))
                        if size > best_audio_size:
                            best_audio_size = size
                            best_audio_id = format_id
        
        # Store best audio id
        if best_audio_id:
            formats["audio_only"] = best_audio_id
        
        # Now find video formats
        for line in result.stdout.split('\n'):
            if re.search(r'^\d+\s', line):  # Lines starting with a number
                parts = line.split()
                if len(parts) >= 3:
                    format_id = parts[0]
                    # Extract resolution if available
                    resolution_match = re.search(r'(\d+)x(\d+)', line)
                    if resolution_match:
                        height = int(resolution_match.group(2))
                        # Only store video formats that have video
                        if "video only" in line.lower():
                            if height == 1080:
                                formats["1080p_video"] = format_id
                            elif height == 720:
                                formats["720p_video"] = format_id
                            elif height == 480:
                                formats["480p_video"] = format_id
                            elif height == 360:
                                formats["360p_video"] = format_id
                        # Store combined formats
                        elif "video" in line.lower():
                            if height == 1080:
                                formats["1080p"] = format_id
                            elif height == 720:
                                formats["720p"] = format_id
                            elif height == 480:
                                formats["480p"] = format_id
                            elif height == 360:
                                formats["360p"] = format_id
        
        return formats
    except Exception as e:
        print(f"Error in get_available_formats: {e}")
        return {}

# download setting
def startDownload():
    try:
        # First ensure yt-dlp is installed
        if not ensure_yt_dlp():
            finishLabel.configure(text="Failed to setup yt-dlp. Please install it manually.", text_color="red")
            return
            
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
            
            # First try to get video title using pytube
            try:
                yt = YouTube(ytLink)
                title.configure(text=yt.title, text_color="white")
            except Exception as e:
                print(f"Error getting video info with pytube: {e}")
                # Fallback to getting title with yt-dlp
                try:
                    cmd = ["yt-dlp", "--get-title", ytLink]
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        title.configure(text=result.stdout.strip(), text_color="white")
                except Exception as e:
                    print(f"Error getting title with yt-dlp: {e}")
                    title.configure(text="Unknown Title", text_color="white")
            
            # Get available formats using yt-dlp
            available_formats = get_available_formats(ytLink)
            print(f"Available formats: {available_formats}")
            
            if not available_formats:
                finishLabel.configure(text="No available formats found for this video.", text_color="red")
                return
                
            # Get available qualities for dropdown (without the _video suffix)
            display_qualities = []
            for quality in ["1080p", "720p", "480p", "360p"]:
                if quality in available_formats or f"{quality}_video" in available_formats:
                    display_qualities.append(quality)
            
            # Add audio only option if available
            if "audio_only" in available_formats:
                display_qualities.append("Audio Only")
                
            # Update dropdown with available qualities
            quality_dropdown.configure(values=display_qualities)
            
            # Get selected quality
            selected_quality = quality_var.get()
            
            # If the selected quality is not available, default to the highest
            if selected_quality not in display_qualities:
                if display_qualities:
                    selected_quality = display_qualities[0]
                    quality_var.set(selected_quality)
            
            # Create downloads directory
            download_path = os.path.join(os.getcwd(), "downloads")
            os.makedirs(download_path, exist_ok=True)
            
            # Generate a safe filename from the video ID
            output_file = os.path.join(download_path, f"{video_id}")
            
            # Command to run
            cmd = []
            
            # Determine format ID based on selected quality
            if selected_quality == "Audio Only":
                format_id = available_formats.get("audio_only")
                output_file += ".mp3"
                # Audio download command
                cmd = ["yt-dlp", "-f", format_id, "-o", output_file, "--extract-audio", "--audio-format", "mp3", ytLink]
            else:
                # For video, check if we need to use bestvideo+bestaudio or a specific format
                output_file += ".mp4"
                
                if selected_quality in available_formats:
                    # We have a combined format with both audio and video
                    format_id = available_formats.get(selected_quality)
                    cmd = ["yt-dlp", "-f", format_id, "-o", output_file, ytLink]
                elif f"{selected_quality}_video" in available_formats:
                    # We need to use the video format + best audio
                    video_format = available_formats.get(f"{selected_quality}_video")
                    cmd = ["yt-dlp", "-f", f"{video_format}+bestaudio", "-o", output_file, "--merge-output-format", "mp4", ytLink]
                else:
                    # Let yt-dlp choose the best format matching the selected resolution
                    height = selected_quality.replace("p", "")
                    cmd = ["yt-dlp", "-f", f"bestvideo[height<={height}]+bestaudio/best[height<={height}]", 
                           "-o", output_file, "--merge-output-format", "mp4", ytLink]
            
            if not cmd:
                finishLabel.configure(text=f"Could not determine suitable format. Try another quality.", text_color="orange")
                return
                
            # Add additional parameters for more reliable downloads
            if selected_quality != "Audio Only":
                if "--merge-output-format" not in " ".join(cmd):
                    cmd.append("--merge-output-format")
                    cmd.append("mp4")
                    
            # Force overwrite if file exists to avoid errors
            if "--force-overwrites" not in " ".join(cmd):
                cmd.append("--force-overwrites")
            
            # Show progress
            progressPercentage.configure(text="Starting download...")
            progressBar.set(0.1)  # Show some initial progress
            finishLabel.configure(text="")
            
            print(f"Running command: {' '.join(cmd)}")
            
            # Run the download in a subprocess
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            app.update_idletasks()
            
            # Process the output to track progress
            for line in process.stdout:
                if "%" in line:
                    # Try to extract percentage
                    percent_match = re.search(r'(\d+\.\d+)%', line)
                    if percent_match:
                        percent = float(percent_match.group(1))
                        progressPercentage.configure(text=f"{percent:.1f}%")
                        progressBar.set(percent / 100)
                        app.update_idletasks()
                print(line, end='')  # Print output for debugging
                
            # Wait for process to complete
            exit_code = process.wait()
            
            if exit_code == 0:
                progressBar.set(1.0)
                progressPercentage.configure(text="100%")
                finishLabel.configure(
                    text=f"Downloaded in {selected_quality}!", 
                    text_color="green"
                )
                locationLabel.configure(
                    text=f"Saved to: {output_file}",
                    text_color="white"
                )
            else:
                finishLabel.configure(text=f"Download failed with code {exit_code}", text_color="red")
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

# Quality selection dropdown
quality_frame = customtkinter.CTkFrame(app)
quality_frame.pack(padx=10, pady=10)

quality_label = customtkinter.CTkLabel(quality_frame, text="Select Quality:")
quality_label.pack(side="left", padx=5)

quality_var = customtkinter.StringVar(value=VIDEO_QUALITIES[0])  # Default to highest quality
quality_dropdown = customtkinter.CTkOptionMenu(
    quality_frame,
    values=VIDEO_QUALITIES,
    variable=quality_var
)
quality_dropdown.pack(side="left", padx=5)

# Finished Downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# File location
locationLabel = customtkinter.CTkLabel(app, text="")
locationLabel.pack()

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
