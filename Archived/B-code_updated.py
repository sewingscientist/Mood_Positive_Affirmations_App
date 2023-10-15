import tkinter as tk
from mood_tracker import record_mood
from PIL import Image
from PIL import ImageTk
import requests


def get_positive_affirmation():
    """ Allows us to access zenquotes API to retrieve a random quote."""
    url = 'https://zenquotes.io/api/random'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        affirmation = data[0]['q']
        quote.config(text=affirmation)
    else:
        pass
        quote.config(text='Failed to fetch affirmation')


def display_affirmation_with_timer():
    """Function to set a timer in millisecond. Affirmations/quotes will change depending on the time set"""
    get_positive_affirmation()
    delay = 1800000  # 30 minutes - (adjust this value as desired)
    root.after(delay, display_affirmation_with_timer)


# The code below starts up the app
root = tk.Tk()
root.geometry("600x900")
root.title('Positive Affirmations For You')
root.iconbitmap('download.icon.jpg')


root.config(background="#F0D5E7")
quote = tk.Label(root, font=('comic sans', 10))
quote.pack(padx=20, pady=20)
# root.pack_propagate(False)


def welcome_page():
    def page_two():
        label.destroy()
        button.destroy()

        second_page = tk.Frame(root, bg="#F0D5E7")
        second_page.pack(pady=15, fill="both", expand=True)

        second_page_label = tk.Label(second_page,
                                     text="Please select how you feel:",
                                     bg="#F0D5E7",
                                     font=("Segoe Print", 16))
        second_page_label.pack(pady=5, side="top")
        #adding using .pack on second_page_label lets you put it somewhere, "top" for this one but can be anywhere

        emojis = ["Happy😃", "Okay😐", "Sad😢", "Angry😡"]
        for emoji in emojis:
            mood_button = tk.Button(second_page,
                                    text=emoji,
                                    font=("Arial", 20),
                                    bg="#B78BA8",
                                    command=lambda e=emoji: record_mood(e))
            mood_button.pack(pady=5)

        #Additional Button to Show Mood Records in a pop out window
        button_show_records_image = Image.open("Mood_Record.jpg")
        button_show_records_image = ImageTk.PhotoImage(button_show_records_image)
        button_show_records = tk.Button(second_page,
                                        image=button_show_records_image,
                                        bg="#F0D5E7",
                                        width=130,
                                        height=100,
                                        command=display_mood_records)
        button_show_records.image = button_show_records_image
        button_show_records.pack(padx=5, pady=20)


        # quote = tk.Label(root, font=('comic sans', 15))
        # quote.pack(padx=20, pady=20)

        button3_image = Image.open("Affirmation.jpg")
        button3_image = ImageTk.PhotoImage(button3_image)
        button3 = tk.Button(second_page, text="Get Affirmation",
                            image=button3_image,
                            bg="#F0D5E7",
                            width=130,
                            height=100,
                            command=get_positive_affirmation)
        button3.image = button3_image
        button3.pack(padx=5, pady=20)

        def back_to_welcome():
            second_page.destroy()
            second_page_button.destroy()
            button3.destroy()
            welcome_page()

        second_page_button_image = Image.open("Flattened_Welcome.jpg")
        second_page_button_image = ImageTk.PhotoImage(second_page_button_image)
        second_page_button = tk.Button(second_page,
                                       image=second_page_button_image,
                                       bg="#F0D5E7",
                                       width=130,
                                       height=100,
                                       command=back_to_welcome)
        second_page_button.image = second_page_button_image
        second_page_button.pack(padx=5, pady=20)

    label = tk.Label(root,
                     text='Welcome\n\nto a world\n\nof positive\n\nwonder',
                     font=('Segoe Script', 22),
                     background="#F0D5E7")
    label.pack(padx=40, pady=30)

    button_image = Image.open("Enter.jpg")
    button_image = ImageTk.PhotoImage(button_image)
    button = tk.Button(root,
                       image=button_image,
                       bg="white",
                       width=130,
                       height=100,
                       command=page_two)
    button.image = button_image
    button.pack(padx=5, pady=30)


# The code below can be used to add a logo to the pages
#     logo = Image.open("mood_logo.jpg")
#     resized_logo = logo.resize((150, 100))
#     new_image = ImageTk.PhotoImage(resized_logo)
#     logo_widget = tk.Label(root, image=new_image, bg="#F0D5E7")
#     logo_widget.image = new_image
#     logo_widget.pack(side='bottom')
    

    def display_mood_records(): #Opens another window when the show mood records button is pressed that reads the text file
        try:
            with open("mood_records.txt", "r", encoding="utf-8") as file:
                records = file.read()

            records_window = tk.Toplevel(root)
            records_window.title("Mood Records")
            records_window.geometry("400x300")
            records_window.config(background="#F0D5E7")

            records_label = tk.Label(records_window,
                                     text="Mood Records",
                                     font=("Segoe Print", 25),
                                     background="#F0D5E7",
                                     foreground="black")
            records_label.pack(pady=10)

            records_text = tk.Text(records_window, wrap="word", font=("Segoe Print", 15), background="#F0D5E7",
                                   foreground="black")
            records_text.insert("1.0", records)
            records_text.pack(padx=10, pady=10, fill="both", expand=True)

        except FileNotFoundError:
            print("mood_records.txt not found")


welcome_page()
display_affirmation_with_timer()
root.mainloop()