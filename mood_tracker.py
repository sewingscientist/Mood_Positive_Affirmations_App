import tkinter as tk
from tkinter import messagebox
from datetime import datetime


def record_mood(mood):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mood_entry = f"{current_time} - {mood}\n"

    with open("Archived/mood_records.txt", "a", encoding="utf-8") as file:
        file.write(mood_entry)

    messagebox.showinfo("Mood Tracker", f"You feel: {mood}")


def create_gui():
    root = tk.Tk()
    root.title("Mood Tracker")
    label = tk.Label(root, text="Please select how you feel:")
    label.pack(pady=10)


    emojis = ["😃", "😐", "😢", "😡"]

    for emoji in emojis:
        mood_button = tk.Button(root, text=emoji, font=("Arial", 20), command=lambda e=emoji: record_mood(e))
        mood_button.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    create_gui()