import tkinter as tk
from tkinter import filedialog
import moviepy.editor as mp
import speech_recognition as sr
import pyttsx3

class VideoSearchApp:
    def __init__(self, master):
        self.master = master
        master.title("Video Speech Search")

        self.label = tk.Label(master, text="Enter Target Word:")
        self.label.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.browse_button = tk.Button(master, text="Browse Video", command=self.browse_video)
        self.browse_button.pack()

        self.search_button = tk.Button(master, text="Search", command=self.search_video)
        self.search_button.pack()

        self.speak_button = tk.Button(master, text="Speak Text", command=self.speak_text)
        self.speak_button.pack()

    def browse_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
        self.video_path = file_path
        self.browse_button.config(text=f"Video Selected: {file_path}")

    def search_video(self):
        target_word = self.entry.get()
        if not target_word:
            self.label.config(text="Please enter a target word.")
            return

        if not hasattr(self, 'video_path'):
            self.label.config(text="Please select a video file.")
            return

        self.label.config(text="Searching...")

        try:
            video = mp.VideoFileClip(self.video_path)
            audio_path = "temp_audio.wav"
            video.audio.write_audiofile(audio_path)

            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_path) as source:
                audio = recognizer.record(source)

            transcribed_text = recognizer.recognize_google(audio)

            start_time = transcribed_text.find(target_word)
            end_time = start_time + len(target_word)

            start_seconds = video.duration if start_time == -1 else video.duration * (start_time / len(transcribed_text))
            end_seconds = video.duration if end_time == -1 else video.duration * (end_time / len(transcribed_text))

            self.label.config(text=f"Target word '{target_word}' found from {start_seconds:.2f} seconds to {end_seconds:.2f} seconds.")
        except Exception as e:
            self.label.config(text=f"Error: {str(e)}")

    def speak_text(self):
        text_to_speak = self.label.cget("text")
        engine = pyttsx3.init()
        engine.say(text_to_speak)
        engine.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoSearchApp(root)
    root.mainloop()