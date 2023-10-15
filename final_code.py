import tkinter as tk
import requests
import webbrowser
from PIL import Image, ImageTk
from mood_tracker import record_mood
from DatabaseSetup import DatabaseSetup, DbConnectionError

# Setup app in a class - outlines the app set up which can be referred to in later code
class PositiveAffirmationsApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("550x450")
        self.root.title('Positive Affirmations')
        self.root.iconbitmap('Images/download.icon.jpg')

        self.bk_ground = "#F0D5E7"
        self.root.config(background=self.bk_ground)

        self.db_manager = DatabaseSetup()

        self.main_frame = None
        self.options_frame = None
        self.quote_label = None

        self.current_affirmation = None

        self.init_ui()

    def init_ui(self):
        self.create_options_frame()
        self.create_main_frame()
        self.create_buttons()

        self.pages = [
            self.home_page,
            self.about_page,
            self.affirmation_page,
            self.mood_page,
            self.mood_record_page,
            self.saved_affirmations_page,
            self.help_page
        ]

        self.hide_indicators()
        self.indicate(0)

        self.root.mainloop()

    def create_options_frame(self):
        self.options_frame = tk.Frame(self.root, bg=self.bk_ground, width=120)
        self.options_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.options_frame.pack_propagate(False)

    def create_main_frame(self):
        self.main_frame = tk.Frame(self.root,
                                   highlightbackground="#158aff",
                                   highlightthickness=2,
                                   width=500,
                                   bg=self.bk_ground)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.main_frame.pack_propagate(False)

    def create_buttons(self):
        button_info = [
            ("Home", self.home_page),
            ("About", self.about_page),
            ("Affirmation", self.affirmation_page),
            ("Mood", self.mood_page),
            ("My Mood", self.mood_record_page),
            ("❤", self.saved_affirmations_page),
            ("Support", self.help_page)
        ]

        self.indicators = []

        for idx, (label, command) in enumerate(button_info):
            button = tk.Button(self.options_frame, text=label, font=("Bold", 15),
                               fg="#158aff", bd=0, bg=self.bk_ground,
                               command=lambda c=command, i=idx: self.indicate(i))
            button.place(x=10, y=idx * 50)

            indicator = tk.Label(self.options_frame, text=" ", bg=self.bk_ground)
            indicator.place(x=3, y=idx * 50, width=5, height=40)
            self.indicators.append(indicator)

    def hide_indicators(self):
        for indicator in self.indicators:
            indicator.config(bg=self.bk_ground)

    def indicate(self, idx):
        self.hide_indicators()
        self.indicators[idx].config(bg="#158aff")
        self.delete_pages()
        self.pages[idx]()

    def delete_pages(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

# Creates individual home page
    def home_page(self):
        home_frame = tk.Frame(self.main_frame, bg=self.bk_ground)
        lb = tk.Label(home_frame, text="""Welcome to""", font=('Arial', 25), bg=self.bk_ground)
        lb.pack()
        home_frame.pack(pady=20)

        # This creates the mood logo on the homepage
        logo = Image.open("Images/mood_logo.jpg")
        resized_logo = logo.resize((400, 350))
        new_image = ImageTk.PhotoImage(resized_logo)
        lb = tk.Label(home_frame, image=new_image, bg=self.bk_ground)
        logo_widget = tk.Label(lb, bg=self.bk_ground)
        logo_widget.image = new_image
        lb.pack(padx=65)

    # Creates individual about page with text
    def about_page(self):
        about_frame = tk.Frame(self.main_frame, bg=self.bk_ground)

        about_header = Image.open("Images/Aboutheader.jpg")
        resized_about = about_header.resize((200, 150))
        about_image = ImageTk.PhotoImage(resized_about)

        lb = tk.Label(about_frame, image=about_image, bg=self.bk_ground)
        lb.image = about_image
        lb.pack(padx=10)

        lb = tk.Label(about_frame, text="""

        Your daily tool for a brighter perspective on life. Get\n
        daily affirmations and monitor your mood. Read uplifting\n
        affirmations and track your mood using the mood page.\n
        Monitor emotions and save favorite affirmations for\n
        later reflection. Positivity begins with your mindset!
        """, font=('Arial', 10), fg="#158aff", bg="#F0D5E7")
        lb.pack()
        about_frame.pack(pady=10)

    # Creates individual affirmation page with affirmation and button
    def affirmation_page(self):
        global quote_label
        affirmation_frame = tk.Frame(self.main_frame, bg=self.bk_ground)

        dailyaff_header = Image.open("Images/Dailyaffheader.jpg")
        resized_about = dailyaff_header.resize((200, 150))
        dailyaff_image = ImageTk.PhotoImage(resized_about)

        lb = tk.Label(affirmation_frame, image=dailyaff_image, bg=self.bk_ground)
        lb.image = dailyaff_image
        lb.pack(padx=5)

        quote_label = tk.Label(affirmation_frame, text='Click the button to get your daily affirmation',
                               height=6,
                               fg='black',
                               font=('Arial', 12),
                               bg=self.bk_ground,
                               wraplength=300)  # Adjust the wrap-length value as needed
        quote_label.pack(padx=10, pady=10)

        button_frame = tk.Frame(affirmation_frame, bg=self.bk_ground)

        get_positive_affirmation_button = tk.Button(affirmation_frame,
                                                    text="Get Affirmation",
                                                    height=4,
                                                    font=('Arial', 12),
                                                    bg="#158aff",
                                                    command=self.get_positive_affirmation)
        get_positive_affirmation_button.pack(side=tk.LEFT, padx=5, pady=5)

        save_affirmation_button = tk.Button(affirmation_frame,
                                            text="Save Affirmation",
                                            height=4,
                                            font=('Arial', 12),
                                            bg="#158aff",
                                            command=self.save_affirmation)
        save_affirmation_button.pack(side=tk.RIGHT, padx=5, pady=5)

        button_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        affirmation_frame.pack(pady=20)

    # API generating affirmation
    def get_positive_affirmation(self):
        api = 'https://zenquotes.io/api/random'
        response = requests.get(api)

        if response.status_code == 200:
            data = response.json()
            if data and data[0].get('q'):
                affirmation = data[0]['q']
                self.current_affirmation = affirmation
                quote_label.config(text=affirmation, wraplength=300,
                                   font=("Arial", 10),
                                   bg=self.bk_ground)  # Adjust the wrap-length value as needed. Quotes won't be longer than this
                return affirmation
        else:
            return 'Unable to fetch affirmation'

    # Saves to MySQL and shows in the Python console it was saved to SQL
    def save_affirmation(self):
        if self.current_affirmation:
            affirmation_text = self.current_affirmation
            self.db_manager.insert_into_database('fave_affirmation', affirmation_text)
            print("Affirmation inserted into database: ", affirmation_text)




    # Creates individual mood page with Text and emoji buttons. Title to be replaced with bobbies cloud
    def mood_page(self):
        def record_selected_mood(selected_mood):
            record_mood(selected_mood)

        mood_frame = tk.Frame(self.main_frame, bg=self.bk_ground)

        feeling_header = Image.open("Images/Feelingheader.jpg")
        resized_about = feeling_header.resize((200, 160))
        feeling_image = ImageTk.PhotoImage(resized_about)

        lb = tk.Label(mood_frame, image=feeling_image, bg=self.bk_ground)
        lb.image = feeling_image
        lb.pack(padx=5)

        emojis = ["Happy 😃", "Okay 😐", "Sad 😢", "Angry 😡"]
        for emoji in emojis:
            mood_button = tk.Button(mood_frame, text=emoji, font=("Arial", 16), bg="#158aff",
                                    command=lambda e=emoji: record_selected_mood(e))
            mood_button.pack(pady=5)

        mood_frame.pack(pady=5)

    # Creates individual page for where the mood database will go
    def mood_record_page(self):
        mood_record_frame = tk.Frame(self.main_frame, bg=self.bk_ground)
        # Load and resize the header image
        moodrec_header = Image.open("Images/Moodrecheader.jpg")
        resized_about = moodrec_header.resize((200, 150))
        moodrec_image = ImageTk.PhotoImage(resized_about)

        lb = tk.Label(mood_record_frame, image=moodrec_image, bg=self.bk_ground)
        lb.image = moodrec_image
        lb.pack(padx=5)

        # This Creates a Reset button
        reset_button = tk.Button(mood_record_frame,
                                 text="Reset",
                                 bg="#F0D5E7",
                                 command=lambda: self.reset_mood_records(mood_text))
        reset_button.pack()

        # This creates a Text widget to display mood records with word wrapping
        mood_text = tk.Text(mood_record_frame, wrap=tk.WORD, font=("Arial", 12), bg=self.bk_ground)
        mood_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # This creates a vertical scrollbar for the Text widget
        scrollbar = tk.Scrollbar(mood_record_frame, command=mood_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # This configures the Text widget to work with the scrollbar
        mood_text.config(yscrollcommand=scrollbar.set)

        try:
            # This code tries to open and read the mood_records.txt file
            with open("Archived/mood_records.txt", "r", encoding="utf-8") as file:
                mood_content = file.read()
        except FileNotFoundError:
            mood_content = "No mood data available."

        # This inserts mood records the content into the Text widget
        mood_text.insert(tk.END, mood_content)
        mood_record_frame.pack(pady=20)

    # This function allows for the reset of the mood records
    def reset_mood_records(self, mood_text=None):
        if mood_text:
            mood_text.delete(1.0, tk.END)
            with open("Archived/mood_records.txt", "w", encoding="utf-8") as file:
                file.write("")



    # Creates individual page where saved affirmation db will go
    def saved_affirmations_page(self):
        saved_affirmations_frame = tk.Frame(self.main_frame, bg=self.bk_ground)

        myaff_header = Image.open("Images/Myaffsheader.jpg")
        resized_about = myaff_header.resize((200, 160))
        myaff_image = ImageTk.PhotoImage(resized_about)

        lb = tk.Label(saved_affirmations_frame, image=myaff_image, bg=self.bk_ground)
        lb.image = myaff_image
        lb.pack(padx=5)

        all_saved_affirmations = self.db_manager.view_all_affirmations('fave_affirmation')
        if all_saved_affirmations:
            affirmation_text = "\n".join(all_saved_affirmations)
            affirmation_textbox = tk.Text(saved_affirmations_frame,
                                          font=('Arial', 12),
                                          bg=self.bk_ground,
                                          wrap=tk.WORD,  # Wrap text at word boundaries
                                          width=50,
                                          height=10)  # You can adjust the height as needed
            affirmation_textbox.insert(tk.END, affirmation_text)
            affirmation_textbox.pack(padx=20, pady=20)

        else:
            no_affirmations_label = tk.Label(saved_affirmations_frame,
                                             text="No saved affirmations",
                                             font=('Arial', 12),
                                             bg=self.bk_ground)
            no_affirmations_label.pack(padx=20, pady=20)

        saved_affirmations_frame.pack(pady=20)

    # Creates individual support with text.
    def help_page(self):
        home_frame = tk.Frame(self.main_frame, bg=self.bk_ground)

        webbrowser.open("https://www.helpguide.org/find-help.htm")

        safespace_header = Image.open("Images/Safespaceheader.jpg")
        resized_about = safespace_header.resize((200, 150))
        safespace_image = ImageTk.PhotoImage(resized_about)

        lb = tk.Label(home_frame, image=safespace_image, bg=self.bk_ground)
        lb.image = safespace_image
        lb.pack(padx=5)

        lb = tk.Label(home_frame, text="Remember,\njust one positive\nthought is capable\nof shaping "
                                       "your\nentire day...", font=('Arial', 20), fg="#158aff", bg=self.bk_ground)
        lb.pack()
        home_frame.pack(pady=20)


if __name__ == '__main__':
    try:
        app = PositiveAffirmationsApp()
    except DbConnectionError:
        print("Database connection error")
