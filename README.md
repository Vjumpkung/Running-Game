# Running-Game

A simple game with big red square and small black square moving thing. You must avoid it by jumping. Caution it has a random size and speed you have to press your button accurately.

# How to play?

- press <kbd>SPACEBAR</kbd> or <kbd>LEFTCLICK</kbd> or <kbd>↑</kbd> to jump
- press <kbd>R</kbd> to retry.

# Features

- every 5 marks the small sqaure black things will moving faster. (Maximum acceleration 25 unit)
- login and register system
- save personal best score in database (updating best score every 10 seconds)
- real time scoreboard (update every 10 seconds)

# Requirement Software and Libraries

- python 3.6 or newer with tkinter
- pygame
- bcrypt
- pymongo
- MongoDB

# Launch Instructions

    git clone https://github.com/Vjumpkung/Running-Game.git
    cd Running-Game
    pip install -r requirement.txt
    python RunningGame.py

- rename settings.json.example to settings.json and connect to MongoDB

# Known Issues

- none.

# Screenshot

[screenshot]: assets/screenshot.png
[mainmenu]: assets/main-menu.png
[mainmenu2]: assets/main-menu2.png

![][mainmenu]
![][mainmenu2]
![][screenshot]

# Reference

[Youtube](https://www.youtube.com/watch?v=AY9MnQ4x3zk)
