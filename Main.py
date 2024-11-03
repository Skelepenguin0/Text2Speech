#pip install gTTS
import tkinter as tk
from tkinter import filedialog, messagebox
from gtts import gTTS
import os
import platform
import subprocess

def select_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        file_path_entry.delete(0, tk.END)
        file_path_entry.insert(0, filepath)

def select_save_directory():
    directory = filedialog.askdirectory()
    if directory:
        save_path_entry.delete(0, tk.END)
        save_path_entry.insert(0, directory)

def convert_to_speech():
    file_path = file_path_entry.get()
    save_directory = save_path_entry.get()

    if not os.path.isfile(file_path):
        messagebox.showerror("Error", "Please select a valid .txt file.")
        return

    if not os.path.isdir(save_directory):
        messagebox.showerror("Error", "Please select a valid directory to save the file.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        speed = float(speed_entry.get())

        # Set up text-to-speech
        tts = gTTS(text=text, lang='en', slow=(speed < 1.0))
        audio_filename = os.path.join(save_directory, "output_audio.mp3")
        tts.save(audio_filename)

        # Play the audio file
        if platform.system() == "Windows":
            os.startfile(audio_filename)
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", audio_filename])
        else:  # Linux
            subprocess.call(["xdg-open", audio_filename])

        messagebox.showinfo("Success", f"Text-to-speech conversion complete. Saved as {audio_filename} and playing the audio.")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main application window
root = tk.Tk()
root.title("Text-to-Speech Converter")

# File selection section
tk.Label(root, text="Select .txt file:").pack(pady=5)
file_path_entry = tk.Entry(root, width=50)
file_path_entry.pack(pady=5)
tk.Button(root, text="Browse", command=select_file).pack(pady=5)

# Save directory selection
tk.Label(root, text="Select directory to save .mp3 file:").pack(pady=5)
save_path_entry = tk.Entry(root, width=50)
save_path_entry.pack(pady=5)
tk.Button(root, text="Select Directory", command=select_save_directory).pack(pady=5)

# Voice settings
tk.Label(root, text="Speed (0.5 for slow, 1.0 for normal, >1.0 for fast):").pack(pady=5)
speed_entry = tk.Entry(root)
speed_entry.insert(0, "1.0")
speed_entry.pack(pady=5)

# Convert button
tk.Button(root, text="Convert to Speech", command=convert_to_speech).pack(pady=10)

# Run the application
root.mainloop()
