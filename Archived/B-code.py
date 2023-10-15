import tkinter as tk
from mood_tracker import record_mood
from PIL import Image
from PIL import ImageTk
##from get_api_affirmations import get_positive_affirmation

root = tk.Tk()

root.geometry("600x900")
root.title('Positive Affirmations For You')
root.config(background="#009973")

def welcome_page():
    def page_two():
        label.destroy()
        button.destroy()

        second_page = tk.Frame(root, bg="#009973")
        second_page.pack(pady=15, fill="both", expand=True)

        second_page_label = tk.Label(second_page,
                                     text="Please select how you feel:",
                                     bg="#009973",
                                     font=("Segoe Print", 14))
        second_page_label.pack(pady=15, side="top") #adding using .pack on second_page_label lets you put it somewhere, "top" for this one but can be anywhere

        emojis = ["😃", "😐", "😢", "😡"]
        for emoji in emojis:
            mood_button = tk.Button(second_page,
                                    text=emoji,
                                    font=("Arial", 20),
                                    bg='white',
                                    command=lambda e=emoji: record_mood(e))
            mood_button.pack(pady=5)
        #Additional Button to Show Mood Records in a pop out window
        button_show_records_image = Image.open("Mood_Record.jpg")
        button_show_records_image = ImageTk.PhotoImage(button_show_records_image)
        button_show_records = tk.Button(second_page, image=button_show_records_image, bg="#91D8E4", width=130, height=100,
                                        command=display_mood_records)
        button_show_records.image = button_show_records_image
        button_show_records.pack(padx=5, pady=20)

        button3_image = Image.open("Affirmation.jpg")
        button3_image = ImageTk.PhotoImage(button3_image)
        button3 = tk.Button(second_page, image=button3_image, bg="#91D8E4", width=130, height=100)
        button3.image = button3_image
        button3.pack(padx=5, pady=20)

        def back_to_welcome():
            second_page.destroy()
            second_page_button.destroy()
            welcome_page()

        second_page_button_image = Image.open("Flattened_Welcome.jpg")
        second_page_button_image = ImageTk.PhotoImage(second_page_button_image)
        second_page_button = tk.Button(second_page, image=second_page_button_image, bg="white", width=130, height=100,
                                       command=back_to_welcome)
        second_page_button.image = second_page_button_image
        second_page_button.pack(padx=5, pady=20)

    label = tk.Label(root,
                     text='Welcome\n\nto a world\n\nof positive\n\nwonder',
                     font=('Segoe Script', 22),
                     background="#009973")
    label.pack(padx=40, pady=30)

    button_image = Image.open("Enter.jpg")
    button_image = ImageTk.PhotoImage(button_image)
    button = tk.Button(root, image=button_image, bg="white", width=130, height=100, command=page_two)
    button.image = button_image
    button.pack(padx=5, pady=30)

    def display_mood_records(): #Opens another window when the show mood records button is pressed that reads the text file
        try:
            with open("mood_records.txt", "r", encoding="utf-8") as file:
                records = file.read()

            records_window = tk.Toplevel(root)
            records_window.title("Mood Records")
            records_window.geometry("400x300")
            records_window.config(background="#009973")

            records_label = tk.Label(records_window, text="Mood Records", font=("Segoe Print", 25), background="#009973",
                                     foreground="black")
            records_label.pack(pady=10)

            records_text = tk.Text(records_window, wrap="word", font=("Segoe Print", 15), background="#009973",
                                   foreground="black")
            records_text.insert("1.0", records)
            records_text.pack(padx=10, pady=10, fill="both", expand=True)

        except FileNotFoundError:
            print("mood_records.txt not found")


welcome_page()
root.mainloop()