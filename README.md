# Group2_AffirmationsApp

![img_1.png](Images/logo_for_readme.png)

Install the following tools if you don't already have them: <br>
- Tkinter 
- Requests 
- Pillow (PIL) (https://pillow.readthedocs.io/en/latest/installation.html)

Open config.py replace **HOST**, **USER** and **PASSWORD** with your own 
Host, User and Password details. 

Open **SQL_set_up.sql** to set up your own database in MySQL. If needed the code is as follows:

```
CREATE DATABASE fave_affirmation;
USE fave_affirmation;
CREATE TABLE favourited (
    id INT AUTO_INCREMENT PRIMARY KEY,
    affirmation VARCHAR(255) NOT NULL
); 
```

Run **final-code.py** to open app.
