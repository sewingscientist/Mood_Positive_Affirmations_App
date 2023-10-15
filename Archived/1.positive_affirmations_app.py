import tkinter as tk
from mood_tracker import record_mood


root = tk.Tk()

# changes the size of the pop-up box
root.geometry("470x550")
root.title('Positive Affirmations For You')
root.config(background="#009973")
# the welcome label
def welcome_page():
    def page_two():
        """This function allows the user to enter the second page of the app"""
        label.destroy()
        button.destroy()

        second_page = tk.Label(root,
                               text="Please select how you feel:",
                               bg="#009973",
                               font=("Segoe Print", 14))
        second_page.pack(pady=15)

        emojis = ["😃", "😐", "😢", "😡"]
        for emoji in emojis:
            mood_button = tk.Button(second_page,
                                    text=emoji,
                                    font=("Arial", 20),
                                    bg='white',
                                    command=lambda e=emoji: record_mood(e))
            mood_button.pack(pady=5)

        def back_to_welcome():
            second_page.destroy()
            second_page_button.destroy()
            welcome_page()
        second_page_button = tk.Button(second_page,
                                       text="Back to welcome",
                                       font=('Arial', 11),
                                       bg="white", width=13,
                                       command=back_to_welcome)
        second_page_button.pack(padx=5, pady=40)

    # allows us to add a 'click me' button or any button
        button3 = tk.Button(second_page,
                            text="Get Affirmation",
                            font=('Arial', 10),
                            bg="#91D8E4")
                            # command=get_positive_affirmation
        button3.pack(padx=5, pady=5)

    label = tk.Label(root,
                     text='Welcome\n\nto a world\n\nof positive\n\nwonder',
                     font=('Segoe Script', 22),
                     background="#009973")
    label.pack(padx=40, pady=30)

    # the enter button on welcome page
    button = tk.Button(root,
                       text="Enter",
                       font=('Arial', 15),
                       bg="white", width=12, command=page_two)
    button.pack(padx=5, pady=30)

welcome_page()
root.mainloop()  # places a window on computer screen