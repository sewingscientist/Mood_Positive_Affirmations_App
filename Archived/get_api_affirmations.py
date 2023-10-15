import tkinter as tk
# from tkinter import *
import requests
from threading import Thread


def get_positive_affirmation():
    pass
    """ Allows us to access zenquotes API to retrieve a random quote.
    We can update this later to be a bit more specific on quotes returned"""

    api= 'https://zenquotes.io/api/random'
    response = requests.get(api)
    if response.status_code == 200:
        data = response.json()
        affirmation = data[0]['q']
        quote_label.config(text=affirmation)
    else:
        quote_label.config(text='Unable to fetch affirmation')


def display_affirmation_with_timer():
    get_positive_affirmation()
    # Change the delay below (in milliseconds) to set the time between affirmations
    delay = 10000  # 10 seconds (adjust this value as required)
    window.after(delay, display_affirmation_with_timer)


window = tk.Tk()
window.geometry("550x550")
window.title('Positive Affirmations For You')
window.config(background="#009973")


quote_label = tk.Label(window, text='Daily Positive Affirmations',
                       height=6,
                       pady=5,
                       fg='white',
                       bg="#009973",
                       font=('Segoe Script', 11))
quote_label.pack(padx=20, pady=20)




 # allows us to add a 'click me' button or any button
button = tk.Button(window,
                   text="Get Affirmation",
                   height=2,
                   font=('Arial', 10),
                   bg="white",
                   command=get_positive_affirmation)
button.pack(padx=10, pady=10)


display_affirmation_with_timer()
if __name__ == '__main__':
    window.mainloop()
