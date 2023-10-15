import tkinter as tk
import requests
import webbrowser
from PIL import Image, ImageTk
from mood_tracker import record_mood
from DatabaseSetup import DatabaseSetup, DbConnectionError


db_manager = DatabaseSetup()

bk_ground = "#F0D5E7"

# Creates pop up window
root = tk.Tk()
root.geometry("550x450")
root.title('Positive Affirmations')
root.iconbitmap('download.icon.jpg')
root.config(background=bk_ground)


# Creates individual home page
def home_page():
    home_frame = tk.Frame(main_frame, bg=bk_ground)
    lb = tk.Label(home_frame, text="""Welcome to""", font=('Segoe Script', 25), bg=bk_ground)
    lb.pack()
    home_frame.pack(pady=20)

    # This creates the mood logo on the homepage
    logo = Image.open("../Images/mood_logo.jpg")
    resized_logo = logo.resize((400, 350))
    new_image = ImageTk.PhotoImage(resized_logo)
    lb = tk.Label(home_frame, image=new_image, bg=bk_ground)
    logo_widget = tk.Label(lb, bg=bk_ground)
    logo_widget.image = new_image
    lb.pack(padx=65)


# Creates individual about page with text
def about_page():
    about_frame = tk.Frame(main_frame, bg=bk_ground)

    about_header = Image.open("../Images/Aboutheader.jpg")
    resized_about = about_header.resize((200, 150))
    about_image = ImageTk.PhotoImage(resized_about)

    lb = tk.Label(about_frame, image=about_image, bg=bk_ground)
    lb.image = about_image
    lb.pack(padx=10)

    lb = tk.Label(about_frame, text="""

    Your daily tool for a brighter perspective on life.\n
    Get daily affirmations and monitor your mood.\n
    Read uplifting affirmations and track your mood using the mood page. \n
    Monitor emotions and save favorite affirmations for later reflection!\n
    Positivity begins with your mindset.
    """, font=('Arial', 10), fg="#158aff", bg="#F0D5E7")
    lb.pack()
    about_frame.pack(pady=10)


# API generating affirmation
def get_positive_affirmation():
    api = 'https://zenquotes.io/api/random'
    response = requests.get(api)

    if response.status_code == 200:
        data = response.json()
        if data and data[0].get('q'):
            affirmation = data[0]['q']
            quote_label.config(text=affirmation, wraplength=300,
                               font=("Segoe Print", 10),
                               bg=bk_ground)  # Adjust the wrap-length value as needed. Quotes won't be longer than this
            return affirmation
    else:
        return 'Unable to fetch affirmation'


# Saves to MySQL and shows in the Python console it was saved to SQL
def save_affirmation():
    affirmation_text = get_positive_affirmation()
    db_manager.insert_into_database('fave_affirmation', affirmation_text)
    print("Affirmation inserted into database: ", affirmation_text)


# Creates individual affirmation page with affirmation and button
def affirmation_page():
    global quote_label
    affirmation_frame = tk.Frame(main_frame, bg=bk_ground)

    dailyaff_header = Image.open("../Images/Dailyaffheader.jpg")
    resized_about = dailyaff_header.resize((200, 150))
    dailyaff_image = ImageTk.PhotoImage(resized_about)

    lb = tk.Label(affirmation_frame, image=dailyaff_image, bg=bk_ground)
    lb.image = dailyaff_image
    lb.pack(padx=5)

    quote_label = tk.Label(affirmation_frame, text='Click the button to get your daily affirmation',
                           height=6,
                           fg='black',
                           font=('Arial', 12),
                           bg=bk_ground,
                           wraplength=300)  # Adjust the wrap-length value as needed
    quote_label.pack(padx=10, pady=10)

    button_frame = tk.Frame(affirmation_frame, bg=bk_ground)

    get_positive_affirmation_button = tk.Button(affirmation_frame,
                                                text="Get Affirmation",
                                                height=4,
                                                font=('Arial', 12),
                                                bg="#158aff",
                                                command=get_positive_affirmation)
    get_positive_affirmation_button.pack(side=tk.LEFT, padx=5, pady=5)

    save_affirmation_button = tk.Button(affirmation_frame,
                                        text="Save Affirmation",
                                        height=4,
                                        font=('Arial', 12),
                                        bg="#158aff",
                                        command=save_affirmation)
    save_affirmation_button.pack(side=tk.RIGHT, padx=5, pady=5)

    button_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    affirmation_frame.pack(pady=20)


# Creates individual mood page with Text and emoji buttons. Title to be replaced with bobbies cloud
def mood_page():
    def record_selected_mood(selected_mood):
        record_mood(selected_mood)

    mood_frame = tk.Frame(main_frame, bg=bk_ground)

    feeling_header = Image.open("../Images/Feelingheader.jpg")
    resized_about = feeling_header.resize((200, 160))
    feeling_image = ImageTk.PhotoImage(resized_about)

    lb = tk.Label(mood_frame, image=feeling_image, bg=bk_ground)
    lb.image = feeling_image
    lb.pack(padx=5)

    emojis = ["Happy 😃", "Okay 😐", "Sad 😢", "Angry 😡"]
    for emoji in emojis:
        mood_button = tk.Button(mood_frame, text=emoji, font=("Arial", 16), bg="#158aff",
                                command=lambda e=emoji: record_selected_mood(e))
        mood_button.pack(pady=5)

    mood_frame.pack(pady=5)


# Creates individual page for where the mood database will go
def mood_record_page():
    mood_record_frame = tk.Frame(main_frame, bg=bk_ground)
    # Load and resize the header image
    moodrec_header = Image.open("../Images/Moodrecheader.jpg")
    resized_about = moodrec_header.resize((200, 150))
    moodrec_image = ImageTk.PhotoImage(resized_about)

    lb = tk.Label(mood_record_frame, image=moodrec_image, bg=bk_ground)
    lb.image = moodrec_image
    lb.pack(padx=5)

    # This Creates a Reset button
    reset_button = tk.Button(mood_record_frame,
                             text="Reset",
                             bg="#F0D5E7",
                             command=lambda: reset_mood_records(mood_text))
    reset_button.pack()

    # This creates a Text widget to display mood records with word wrapping
    mood_text = tk.Text(mood_record_frame, wrap=tk.WORD, font=("Arial", 12), bg=bk_ground)
    mood_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # This creates a vertical scrollbar for the Text widget
    scrollbar = tk.Scrollbar(mood_record_frame, command=mood_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # This configures the Text widget to work with the scrollbar
    mood_text.config(yscrollcommand=scrollbar.set)

    try:
        # This code tries to open and read the mood_records.txt file
        with open("mood_records.txt", "r", encoding="utf-8") as file:
            mood_content = file.read()
    except FileNotFoundError:
        mood_content = "No mood data available."

    # This inserts mood records the content into the Text widget
    mood_text.insert(tk.END, mood_content)
    mood_record_frame.pack(pady=20)


# This function allows for the reset of the mood records
def reset_mood_records(mood_text=None):
    if mood_text:
        mood_text.delete(1.0, tk.END)
        with open("mood_records.txt", "w", encoding="utf-8") as file:
            file.write("")


# Creates individual page where saved affirmation db will go
def saved_affirmations_page():
    saved_affirmations_frame = tk.Frame(main_frame, bg=bk_ground)

    myaff_header = Image.open("../Images/Myaffsheader.jpg")
    resized_about = myaff_header.resize((200, 160))
    myaff_image = ImageTk.PhotoImage(resized_about)

    lb = tk.Label(saved_affirmations_frame, image=myaff_image, bg=bk_ground)
    lb.image = myaff_image
    lb.pack(padx=5)

    all_saved_affirmations = db_manager.view_all_affirmations('fave_affirmation')
    if all_saved_affirmations:
        affirmation_text = "\n".join(all_saved_affirmations)
        affirmation_textbox = tk.Text(saved_affirmations_frame,
                                      font=('Arial', 12),
                                      bg=bk_ground,
                                      wrap=tk.WORD,  # Wrap text at word boundaries
                                      width=50,
                                      height=10)  # You can adjust the height as needed
        affirmation_textbox.insert(tk.END, affirmation_text)
        affirmation_textbox.pack(padx=20, pady=20)

    else:
        no_affirmations_label = tk.Label(saved_affirmations_frame,
                                         text="No saved affirmations",
                                         font=('Arial', 12),
                                         bg=bk_ground)
        no_affirmations_label.pack(padx=20, pady=20)

    saved_affirmations_frame.pack(pady=20)


# Creates individual support with text.
def help_page():
    home_frame = tk.Frame(main_frame, bg=bk_ground)

    webbrowser.open("https://www.helpguide.org/find-help.htm")

    safespace_header = Image.open("../Images/Safespaceheader.jpg")
    resized_about = safespace_header.resize((200, 150))
    safespace_image = ImageTk.PhotoImage(resized_about)

    lb = tk.Label(home_frame, image=safespace_image, bg=bk_ground)
    lb.image = safespace_image
    lb.pack(padx=5)

    lb = tk.Label(home_frame, text="Remember,\njust one positive\nthought is capable\nof shaping "
                                   "your\nentire day...", font=('Segoe Script', 20), fg="#158aff", bg=bk_ground)
    lb.pack()
    home_frame.pack(pady=20)


# Hides indicators when not selected (the blue line on the sidebar which shows when buttons are selected)
def hide_indicators():
    home_indicate.config(bg=bk_ground)
    about_indicate.config(bg=bk_ground)
    affirmation_indicate.config(bg=bk_ground)
    mood_indicate.config(bg=bk_ground)
    mood_record_indicate.config(bg=bk_ground)
    saved_affirmations_indicate.config(bg=bk_ground)
    help_indicate.config(bg=bk_ground)


# deletes page contents when a new button is clicked on so that the new pages content is showing
def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()


# Crates indicators (the blue tabs)
def indicate(lb, page):
    hide_indicators()
    lb.config(bg="#158aff")
    delete_pages()
    page()


options_frame = tk.Frame(root, bg=(bk_ground))

# Creating buttons below (button name, font, colours, connection to indicator tab and page):
# Home button creation
home_button = tk.Button(options_frame, text="Home",
                        font=("Bold", 15),
                        fg="#158aff", bd=0, bg=bk_ground,
                        command=lambda: indicate(home_indicate, home_page))

# Placement of home tab
home_button.place(x=10, y=0)

# Indicator bar on sidebar
home_indicate = tk.Label(options_frame, text=" ", bg=bk_ground)
home_indicate.place(x=3, y=0, width=5, height=40)

# About button
about_button = tk.Button(options_frame, text="About", font=("Bold", 15),
                         fg="#158aff", bd=0, bg=bk_ground,
                         command=lambda: indicate(about_indicate, about_page))

# Placement of about tab
about_button.place(x=10, y=50)

# Indicator bar on sidebar
about_indicate = tk.Label(options_frame, text=" ", bg=bk_ground)
about_indicate.place(x=3, y=50, width=5, height=40)

# Affirmation tab
affirmation_button = tk.Button(options_frame, text="Affirmation", font=("Bold", 15),
                               fg="#158aff", bd=0, bg=bk_ground,
                               command=lambda: indicate(affirmation_indicate, affirmation_page))
# Tab location on sidebar
affirmation_button.place(x=10, y=100)

# Indicator bar on sidebar
affirmation_indicate = tk.Label(options_frame, text=" ", bg=bk_ground)
affirmation_indicate.place(x=3, y=100, width=5, height=40)

# Mood tab
Mood_button = tk.Button(options_frame, text="Mood", font=("Bold", 15),
                        fg="#158aff", bd=0, bg=bk_ground, command=lambda: indicate(mood_indicate, mood_page))
# Mood tab placement on sidebar
Mood_button.place(x=10, y=150)

# Indicator on sidebar
mood_indicate = tk.Label(options_frame, text=" ", bg=bk_ground)
mood_indicate.place(x=3, y=150, width=5, height=40)

# Mood tracker tab
mood_record_button = tk.Button(options_frame, text="My Mood", font=("Bold", 15),
                               fg="#158aff", bd=0, bg=bk_ground,
                               command=lambda: indicate(mood_record_indicate, mood_record_page))

# Mood tracker tab placement
mood_record_button.place(x=10, y=200)

# Mood tracker indicator placement
mood_record_indicate = tk.Label(options_frame, text=" ", bg=bk_ground)
mood_record_indicate.place(x=3, y=200, width=5, height=40)

# Saved affirmations tab
saved_affirmations_button = tk.Button(options_frame, text="❤", font=("Bold", 25),
                                      fg="#158aff", bd=0, bg=bk_ground,
                                      command=lambda: indicate(saved_affirmations_indicate, saved_affirmations_page))
# Saved affirmations tab placement
saved_affirmations_button.place(x=10, y=250)

# Saved affirmations indicator location
saved_affirmations_indicate = tk.Label(options_frame, text=" ", bg=bk_ground)
saved_affirmations_indicate.place(x=3, y=250, width=5, height=50)

# Help tab
help_button = tk.Button(options_frame, text="Support", font=("Bold", 15),
                        fg="#158aff", bd=0, bg=bk_ground,
                        command=lambda: indicate(help_indicate, help_page))

# Help button placement
help_button.place(x=10, y=310)

# Help indicator location
help_indicate = tk.Label(options_frame, text=" ", bg=bk_ground)
help_indicate.place(x=3, y=310, width=5, height=40)

# Keeps the sidebar to the left
options_frame.pack(side=tk.LEFT)
options_frame.pack_propagate(False)
options_frame.configure(width=120, height=400, background=bk_ground)

# Black boarder within box. Can change thickness and colour
main_frame = tk.Frame(root, highlightbackground="#158aff",
                      highlightthickness=2)

# Creates margin and main frame below
main_frame.pack(side=tk.LEFT)
main_frame.pack_propagate(False)
main_frame.configure(height=400, width=500, background=bk_ground)

root.mainloop()

if __name__ == '__main__':
    try:
        root.mainloop()
    except DbConnectionError:
        print("Database connection error")
