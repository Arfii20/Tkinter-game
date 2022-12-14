# Coursework 2 of COMP16321 by Arefin Ahammed, p28320aa

"""
The screen resolution is 1440x900

This is a classic asteroid game where the player needs to avoid hitting the asteroids to survive.
The difficulty increases at certain scores and there is only one life.
The speed of the asteroids will increase making the game harder and harder at each level.
There are "save", "load", "pause" and "restart" options while playing game.
There is a leaderboard which reflects the top 10 scores in the game.
4 different cheat codes have been added for people who want to cheat.
"""

# Image sources
# game_icon.ico source: https://www.freeiconspng.com/img/17270
# spaceship_image.png source: https://www.pngkey.com/detail/u2q8a9t4r5y3a9r5_spaceship-png-file-spaceship-png/
# asteroid_1.png source: https://www.pngwing.com/en/free-png-yoygi
# asteroid_2.png source: https://pngimg.com/image/105528
# asteroid_3.png source: https://pngimg.com/image/105498
# asteroid_4.png source: https://pngimg.com/image/105494
# main.png: https://www.pngitem.com/middle/wmmbxo_asteroids-asteroid-mining-transparent-background-asteroids-png-png/
# spreadsheet: https://upload.wikimedia.org/wikipedia/commons/2/25/LibreOffice_7.2.4.1_Calc_with_csv_screenshot.png

# options.png source: http://pixelartmaker.com/art/e996fd04f0c49f2
# start.png source: http://pixelartmaker.com/art/6a45404d913e6d1
# exit.png source: http://pixelartmaker.com/art/36cd392e6295705
# pause.png source: https://www.pixilart.com/draw/pause-button-2-22f5240ce52a5c4
# restart.png source: http://pixelartmaker.com/art/ad99f7494306997
# resume.png source: http://pixelartmaker.com/art/5be181b34875416
# leaderboard.png source: http://pixelartmaker.com/art/7cc98bfa5bbcc0b
# back.png source: http://pixelartmaker.com/art/fe696dcfb337a49
# load.png source: http://pixelartmaker.com/art/84432c853ed5006
# save.png source: http://pixelartmaker.com/art/154309787c95a2f
# cheat.png source: http://pixelartmaker.com/art/184effceebac6a0
# help.png source: http://pixelartmaker.com/art/e423fd17591bcaa

# Edited all the buttons to gray colour and made the unmentioned pictures by myself using pixelartmaker.com


from tkinter import Tk, Canvas, Button, Frame, ttk, Entry, Label
from pickle import dump, load as ld
from random import randint, shuffle
from webbrowser import open as opn
from tkinter.font import Font
from platform import system
from math import sqrt, pow
from os import getlogin
from time import sleep
from PIL import Image, ImageTk
import sqlite3


def configure_window():
    """
    Adds title, icon and fixes the size of the main window
    Makes the main window not resizable to minimise complexity.
    Fixes the geometry such that the window is always opened at the center.
    """
    window.title("Into The Space")

    # If the system is windows, ico icon is selected. Otherwise, xbm is selected.
    if system() == "Windows":
        window.iconbitmap("images/game_icon.ico")
    else:
        window.iconbitmap("@images/game_icon.xbm")

    # Disabled resizing of the window.
    window.resizable(False, False)

    "Fixing geometry so that the window opens at the center"
    # Width and height of the window.
    width = window_width
    height = window_height

    # Screen width and height.
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Determines the change of coordinates.
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2 - 20)

    # Sets the screen position.
    window.geometry(f"{width}x{height}+{x}+{y}")


# Functions about binding and unbinding.
def bind_keys():
    """
    Binds the movement keys of the spaceship.
    If arrow flag is true, arrow keys are binded.
    If arrow flag is false, wasd keys are binded.
    Also binds the cheats when called.
    """
    global arrow_flag
    if arrow_flag:
        canvas_main.bind("<Left>", move_spaceship_left)
        canvas_main.bind("<Right>", move_spaceship_right)
        canvas_main.bind("<Up>", move_spaceship_up)
        canvas_main.bind("<Down>", move_spaceship_down)
    else:
        canvas_main.bind("<a>", move_spaceship_left)
        canvas_main.bind("<d>", move_spaceship_right)
        canvas_main.bind("<w>", move_spaceship_up)
        canvas_main.bind("<s>", move_spaceship_down)
    canvas_main.bind("<Shift-Z>", cheatz_reduce_speed_default)
    canvas_main.bind("<Shift-X>", cheatx_reduce_speed_by_one)
    canvas_main.bind("<Shift-C>", cheatc_increase_score)
    canvas_main.bind("<Shift-V>", cheatv_invulnerability)


def unbind_keys():
    """
    Unbinds the movement keys of the spaceship.
    Also unbinds the cheats.
    """
    canvas_main.unbind("<Left>")
    canvas_main.unbind("<Right>")
    canvas_main.unbind("<Up>")
    canvas_main.unbind("<Down>")
    canvas_main.unbind("<a>")
    canvas_main.unbind("<d>")
    canvas_main.unbind("<w>")
    canvas_main.unbind("<s>")
    canvas_main.unbind("<Shift-Z>")
    canvas_main.unbind("<Shift-X>")
    canvas_main.unbind("<Shift-C>")
    canvas_main.unbind("<Shift-V>")


def move_spaceship_left(_):
    """
    Moves spaceship left 15 pixels everytime it is called.
    Takes an event as an argument and that is why used "_".
    """

    canvas_main.move(spaceship, -15, 0)


def move_spaceship_right(_):
    """
    Moves spaceship right 15 pixels everytime it is called.
    Takes an event as an argument and that is why used "_".
    """
    canvas_main.move(spaceship, 15, 0)


def move_spaceship_up(_):
    """
    Moves spaceship up 15 pixels everytime it is called.
    Takes an event as an argument and that is why used "_".
    """
    canvas_main.move(spaceship, 0, -15)


def move_spaceship_down(_):
    """
    Moves spaceship down 15 pixels everytime it is called.
    Takes an event as an argument and that is why used "_".
    """
    canvas_main.move(spaceship, 0, 15)


def spaceship_touches_sides():
    """
    This function unbinds movement of the spaceship if it touches the sides.
    When the player tries to go other direction, it binds the keys again.
    The bindings depend on the status of the arrow flag which either binds wasd or arrows.
   """
    # Unbinds if the spaceship touches any side.
    if spaceship_pos[0] > window_width - 100:
        canvas_main.unbind("<Right>")
        canvas_main.unbind("<d>")
    if spaceship_pos[0] < 0:
        canvas_main.unbind("<Left>")
        canvas_main.unbind("<a>")
    if spaceship_pos[1] > window_height - 100:
        canvas_main.unbind("<Down>")
        canvas_main.unbind("<s>")
    if spaceship_pos[1] < 0:
        canvas_main.unbind("<Up>")
        canvas_main.unbind("<w>")

    # Binds if it goes other direction.
    if spaceship_pos[0] < window_width - 100:
        if arrow_flag:
            canvas_main.bind("<Right>", move_spaceship_right)
        else:
            canvas_main.bind("<d>", move_spaceship_right)
    if spaceship_pos[0] > 0:
        if arrow_flag:
            canvas_main.bind("<Left>", move_spaceship_left)
        else:
            canvas_main.bind("<a>", move_spaceship_left)
    if spaceship_pos[1] < window_height - 100:
        if arrow_flag:
            canvas_main.bind("<Down>", move_spaceship_down)
        else:
            canvas_main.bind("<s>", move_spaceship_down)
    if spaceship_pos[1] > 0:
        if arrow_flag:
            canvas_main.bind("<Up>", move_spaceship_up)
        else:
            canvas_main.bind("<w>", move_spaceship_up)


def boss_key1(_):
    """
    When tab is clicked, it opens the boss.css file.
    It also pauses the game and shows all the buttons.
    Takes an event as an argument and that is why used "_".
    """
    global pause_game, game_over
    # Only works while playing the game.
    if not pause_game:
        opn("boss.css")

        pause_game = True

        # Does not show the resume button if in the game over menu.
        if not game_over:
            canvas_main.itemconfig(resume, state="normal")
            canvas_main.coords(save, load_coords[0] + 110, load_coords[1] + 50)

        # Shows the following buttons.
        normal_buttons()
        canvas_main.itemconfig(restarted, state="normal")
        canvas_main.itemconfig(save, state="normal")
        canvas_main.itemconfig(load, state="normal")

        # Hides the following objects.
        canvas_main.itemconfig(level, state="hidden")
        canvas_main.itemconfig(cheat, state="hidden")

        # Moves the load button from initial position.
        canvas_main.coords(load, load_coords[0] - 110, load_coords[1] + 50)


def boss_key2(_):
    """
    When ` is clicked, it flips to an excel image.
    It also pauses the game and resumes when clicked again.
    Takes an event as an argument and that is why used "_".
    """
    global pause_game, boss_flag
    # Only works when not playing the game
    if not boss_flag and not pause_game:
        boss_flag = True
        pause_game = True
        canvas_main.itemconfig(boss_key, state="normal")
        canvas_main.tag_raise(boss_key)
        unbind_keys()
        canvas_main.unbind("<Escape>")
        canvas_main.unbind("<Tab>")

    elif boss_flag:
        pause_game = False
        boss_flag = False
        bind_keys()
        canvas_main.bind("<Escape>", pause_menu)
        canvas_main.bind("<Tab>", boss_key1)
        canvas_main.itemconfig(boss_key, state="hidden")
        asteroids_and_collision()


# Functions about cheats.
def cheatz_reduce_speed_default(_):
    """
    When pressed Shift+Z the speed is set to 4.
    Takes an event as an argument and that is why used "_".
    """
    global asteroid_speed
    if system() == "Windows":
        asteroid_speed = 4
    else:
        asteroid_speed = 1.6
    canvas_main.itemconfig(cheat, state="normal", text="Speed set to default")
    # Raising so that any other object does not come in front of it.
    canvas_main.tag_raise(cheat)


def cheatx_reduce_speed_by_one(_):
    """
    When pressed Shift+X the speed is reduced by 1.
    Takes an event as an argument and that is why used "_".
    """
    global asteroid_speed
    if asteroid_speed > 4 and system() == "Windows":
        asteroid_speed -= 1
        canvas_main.itemconfig(cheat, state="normal", text="Spead reduced by 1")
        # Raising so that any other object does not come in front of it.
        canvas_main.tag_raise(cheat)
    elif asteroid_speed > 1.6 and system() != "Windows":
        asteroid_speed -= 0.2
        canvas_main.itemconfig(cheat, state="normal", text="Spead reduced by 1")
        # Raising so that any other object does not come in front of it.
        canvas_main.tag_raise(cheat)


def cheatc_increase_score(_):
    """
    When pressed Shift+C the score will increase by 500.
    Takes an event as an argument and that is why used "_".
    """
    global score
    score += 500
    canvas_main.itemconfig(cheat, state="normal", text="Score increased by 500")
    # Raising so that any other object does not come in front of it.
    canvas_main.tag_raise(cheat)


def cheatv_invulnerability(_):
    """
    When pressed Shift+V the collision detection will be turned off and on.
    Takes an event as an argument and that is why used "_".
    """
    global invulnerable

    # Turns on GOD Mode
    if not invulnerable:
        invulnerable = True
        canvas_main.itemconfig(cheat, state="normal", text="Invulnerability On")
        # Raising so that any other object does not come in front of it.
        canvas_main.tag_raise(cheat)

    # Turns off GOD Mode
    elif invulnerable:
        invulnerable = False
        canvas_main.itemconfig(cheat, state="normal", text="Invulnerability Off")
        # Raising so that any other object does not come in front of it.
        canvas_main.tag_raise(cheat)


# Functions about modifying buttons.
def normal_buttons():
    """Makes the exit, leaderboard and options buttons visible again."""
    canvas_main.itemconfig(options, state="normal")
    canvas_main.itemconfig(exited, state="normal")
    canvas_main.itemconfig(leaderboards, state="normal")


def hidden_buttons():
    """Hides the exit, leaderboard and options buttons."""
    canvas_main.itemconfig(exited, state="hidden")
    canvas_main.itemconfig(leaderboards, state="hidden")
    canvas_main.itemconfig(options, state="hidden")


def shift_buttons(y):
    """
    Used for changing the button positions along the y-axis.
    Changes are applied to resume, restart, exit, leaderboard and options button.
    Argument y - takes the buttons y pixels down.
    """
    canvas_main.coords(resume, resume_coords[0], resume_coords[1] + y)
    canvas_main.coords(restarted, restart_coords[0], restart_coords[1] + y)
    canvas_main.coords(exited, exit_coords[0], exit_coords[1] + y)
    canvas_main.coords(leaderboards, leaderboard_coords[0], leaderboard_coords[1] + y)
    canvas_main.coords(options, options_coords[0], options_coords[1] + y)


# Functions about setting name.
def ask_name_choice(_):
    """
    Asks the player if they want to change their name.
    Two options will be displayed saying default and change.
    Deletes the previous window's widgets.
    Takes one argument which is the event of Return press.
    """
    canvas_main.unbind("<Return>")
    canvas_main.delete(press_enter_to_continue)
    canvas_main.delete(welcome_text)
    canvas_main.delete(title_text)

    canvas_main.itemconfig(name_change_text, text="Do you want to change your name?\n"
                                                  "The default is your PC's user name",
                           state="normal")
    canvas_main.itemconfig(use_default, state="normal")
    canvas_main.itemconfig(change_name, state="normal")


def use_default_name():
    """
    If the player selects default name, it deletes the widgets
    and proceeds to the main menu as the default has been set earlier.
    """
    canvas_main.delete(name_change_text)
    canvas_main.delete(use_default)
    canvas_main.delete(change_name)
    main_menu()


def entry_clear(_):
    """Deletes the characters that are in the entry widget if called."""
    enter_name_box.delete(0, "end")


def change_name():
    """
    Makes an entry widget which takes the player name.
    Also shows a done button which takes to the next screen.
    """
    global entry_box, enter_name_box
    canvas_main.delete(name_change_text)
    canvas_main.delete(use_default)
    canvas_main.delete(change_name)

    # Create Entry box.
    enter_name_box = Entry(window, font=("OCR A Extended", 25), width=25, fg="black", bd=0)
    # Enters a default text in the entry box.
    enter_name_box.insert(0, "Enter Name")

    # Binds button-1 of mouse to it which calls a function and clears the default text
    enter_name_box.bind("<Button-1>", entry_clear)
    entry_box = canvas_main.create_window(window_width / 2, window_height / 2, window=enter_name_box)
    canvas_main.itemconfig(done, state="normal")


def done_button_click():
    """
    When the done button is clicked, the name is saved to whatever was written in the entry box.
    After assigning the value to the variable, it deletes the widgets and proceeds to main menu.
    """
    global name
    name = enter_name_box.get()
    canvas_main.delete(entry_box)
    canvas_main.delete(done)
    main_menu()


# Functions about menus.
def main_menu():
    """This function shows the 5 main menu buttons."""
    canvas_main.itemconfig(start, state="normal")
    canvas_main.itemconfig(load, state="normal")
    normal_buttons()


def pause_menu(_):
    """
    When escape is clicked, the game is paused which stop everything and displays all the buttons.
    When escape is clicked again, the game removes buttons and continues the game.
    Takes an event as an argument and that is why used "_".
    """
    global pause_game

    # Pauses the game and adds buttons and hides texts.
    if not pause_game:
        # Setting the variable to True ends the main while loop.
        pause_game = True
        canvas_main.itemconfig(main_image, state="normal")
        canvas_main.itemconfig(resume, state="normal")
        canvas_main.itemconfig(restarted, state="normal")
        canvas_main.itemconfig(save, state="normal")
        canvas_main.itemconfig(load, state="normal")
        canvas_main.tag_raise(main_image)
        normal_buttons()
        unbind_keys()

        canvas_main.itemconfig(level, state="hidden")
        canvas_main.itemconfig(cheat, state="hidden")

        # Changes coordinates of load and save so that they can be side by side.
        canvas_main.coords(save, save_coords[0] + 110, save_coords[1])
        canvas_main.coords(load, load_coords[0] - 110, load_coords[1] + 50)

    # Unpauses the game and hides buttons and shows texts.
    elif pause_game:
        # Setting the variable to false resumes the main while loop.
        pause_game = False
        canvas_main.itemconfig(resume, state="hidden")
        canvas_main.itemconfig(restarted, state="hidden")
        canvas_main.itemconfig(save, state="hidden")
        canvas_main.itemconfig(main_image, state="hidden")
        canvas_main.itemconfig(load, state="hidden")
        canvas_main.bind("<Tab>", boss_key1)
        canvas_main.bind("<q>", boss_key2)
        hidden_buttons()
        bind_keys()

        canvas_main.itemconfig(game_saved, state="hidden")
        canvas_main.itemconfig(level, state="normal")
        canvas_main.tag_raise(level)

        # Calls the falling function as long as not paused.
        asteroids_and_collision()


def resume_button_click():
    """When resume button is clicked, clears the buttons from the screen and resumes all the processes."""
    global pause_game
    canvas_main.itemconfig(resume, state="hidden")
    canvas_main.itemconfig(restarted, state="hidden")
    canvas_main.itemconfig(save, state="hidden")
    canvas_main.itemconfig(main_image, state="hidden")
    canvas_main.itemconfig(game_saved, state="hidden")
    canvas_main.itemconfig(load, state="hidden")
    hidden_buttons()
    bind_keys()
    canvas_main.bind("<q>", boss_key2)
    canvas_main.bind("<Tab>", boss_key1)
    canvas_main.itemconfig(game_saved, state="hidden")

    # Setting the variable to false resumes the main while loop.
    pause_game = False

    # Calls the function which resumes the falling of the asteroids.
    asteroids_and_collision()


def restart_game():
    """
    When restart button is clicked, this function clears all the items and
    launches the main game function which starts the game from beginning.
    """
    global restart_flag, pause_game, score, asteroid_speed, level_number, \
        bonus_on, low_speed_one_on, low_speed_default_on

    # The game only adds the score to leaderboard file iff the score unequal zero
    if score != 0:
        save_leaderboard(name, score)

    # Sets the following variables to default
    pause_game = False
    restart_flag = True
    if system() == "Windows":
        asteroid_speed = 4
    else:
        asteroid_speed = 1.6
    level_number = 1
    score = 0

    canvas_main.itemconfig(level, text="Level " + str(level_number) + "\n\nDodge the Asteroids")
    canvas_main.coords(spaceship, window_width / 2 - 40, window_height - window_height / 6)
    canvas_main.itemconfig(resume, state="hidden")
    canvas_main.itemconfig(restarted, state="hidden")
    canvas_main.itemconfig(game_over_score, state="hidden")
    canvas_main.itemconfig(game_saved, state="hidden")
    canvas_main.itemconfig(save, state="hidden")

    if bonus_on:
        canvas_main.delete(bonus_object)
        bonus_on = False

    if low_speed_one_on:
        canvas_main.delete(low_speed_one_object)
        low_speed_one_on = False

    if low_speed_default_on:
        canvas_main.delete(low_speed_default_object)
        low_speed_default_on = False

    hidden_buttons()

    canvas_main.bind("<Tab>", boss_key1)
    canvas_main.bind("<q>", boss_key2)

    # Deletes all the asteroids from the last game
    for j in asteroid:
        canvas_main.delete(j)

    main_game()


def game_over_menu():
    """
    When the game is over, this function is called.
    It displays all the required buttons and texts.
    """
    # Sets the following button states to normal
    normal_buttons()
    canvas_main.unbind("<q>")
    canvas_main.unbind("<Tab>")
    canvas_main.itemconfig(restarted, state="normal")
    canvas_main.itemconfig(load, state="normal")
    canvas_main.coords(load, window_width / 2, window_height / 2 - 50)

    # Shows the game over score and raises it above all.
    canvas_main.itemconfig(game_over_score, state="normal", text="Score: " + str(score))
    canvas_main.tag_raise(game_over_score)

    # Deletes the "GAME OVER" text.
    canvas_main.itemconfig(game_over_text, state="hidden")


# Functions about leaderboard.
def create_database_table():
    """
    This function runs when the program is run and if there is no database table,
    it creates a table with the selected name.
    If the table exists, the function has no effect.
    """
    # Connects to the database
    conn = sqlite3.connect("leaderboard_database.db")

    # Creates cursor and attempts to create a table if it does not already exist.
    curs = conn.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTS leaderboard (Name text, Score integer)")

    # Commits and closes the file after finishing all tasks.
    conn.commit()
    conn.close()


def save_leaderboard(player_name, total_score):
    """
    Takes player's name and score and stores them to the database.
    Player's name will be a string and score will be an integer.
    """
    # Connects to the database.
    conn = sqlite3.connect("leaderboard_database.db")

    # create cursor
    curs = conn.cursor()

    # Inserts the name and score to a new row on the leaderboard table.
    curs.execute("INSERT INTO leaderboard VALUES (:Name, :Score)",
                 {
                     "Name": player_name,
                     "Score": total_score
                 })

    # Commits and closes the database.
    conn.commit()
    conn.close()


def get_leaderboard_values():
    """Gets top 10 scores from the database and returns to the caller of the function."""
    # Connects to the database.
    conn = sqlite3.connect("leaderboard_database.db")

    # creates the cursor.
    curse = conn.cursor()

    # Selects all the columns and orders the table by descending score.
    curse.execute("SELECT *, oid FROM leaderboard ORDER BY Score DESC")

    # Fetches top 10 scores.
    leaders = curse.fetchmany(10)

    conn.commit()
    conn.close()

    # Returns the list of tuples to the caller.
    return leaders


def leaderboard():
    """
    Makes the leaderboard which displays the top 10 scores in descending order with player name.
    Hides all the previous widgets and uses file handling to sort and display scores.
    """
    # Unbinding the boss key
    canvas_main.unbind("<q>")
    canvas_main.unbind("<Tab>")
    canvas_main.unbind("<Escape>")
    # Packing the outer leaderboard frame.
    secondary_frame.pack(fill="both", expand=1)

    # Creating a canvas for the leaderboard.
    canvas_leaderboard = Canvas(secondary_frame, bg="black", border=0)
    canvas_leaderboard.pack(side="left", fill="both", expand=1)

    # Creating a scrollbar for the leaderboard.
    leaderboard_scrollbar = ttk.Scrollbar(secondary_frame, orient="vertical", command=canvas_leaderboard.yview)
    leaderboard_scrollbar.pack(side="right", fill="y")

    "configure the leaderboard canvas "
    canvas_leaderboard.configure(yscrollcommand=leaderboard_scrollbar.set)
    canvas_leaderboard.bind("<Configure>",
                            lambda e: canvas_leaderboard.configure(scrollregion=canvas_leaderboard.bbox("all")))

    # Adding 300 random stars to the background.
    for _ in range(300):
        # Finds random spawn positions of stars.
        optionsbg_x = randint(0, window_width)
        optionsbg_y = randint(0, window_height)

        # Selects a random size and colour of the stars
        options_size = randint(1, 5)
        options_color_chooser = randint(0, 4)
        canvas_leaderboard.create_oval(optionsbg_x, optionsbg_y, optionsbg_x + options_size, optionsbg_y + options_size,
                                       fill=color[options_color_chooser])

    # Hides the main menu buttons.
    canvas_main.itemconfig(main_image, state="hidden")
    canvas_main.itemconfig(start, state="hidden")
    canvas_main.itemconfig(load, state="hidden")
    canvas_main.itemconfig(resume, state="hidden")
    canvas_main.itemconfig(save, state="hidden")
    canvas_main.itemconfig(restarted, state="hidden")
    canvas_main.itemconfig(game_saved, state="hidden")
    hidden_buttons()

    # Displays the leaderboard text on top left
    canvas_leaderboard.create_text(60, 60, fill="white", text="Leaderboard:",
                                   font=("OCR A Extended", 40), anchor="w")

    # Gets a list of tuples containing rows of table from the database.
    leaders = get_leaderboard_values()

    # Forms a string with the first two values of the tuples which are name and score.
    print_leaders = ""
    for idx, val in enumerate(leaders, start=1):
        print_leaders += str(idx) + ". " + str(val[0]) + " - " + str(val[1]) + "\n\n"

    # Prints nothing to show here if the database is empty.
    if print_leaders == "":
        canvas_leaderboard.create_text(window_width / 2, window_height / 2, fill="white",
                                       font=("OCR A Extended", 25), text="Nothing to show here", justify="left")

    # Prints out the top 10 scores in new lines.
    else:
        canvas_leaderboard.create_text(65, 120, fill="white", font=("OCR A Extended", 25),
                                       text=print_leaders, justify="left", anchor="nw")

    canvas_main.itemconfig(backs, state="normal")


# Functions about options menu
def options_button_click():
    """
    When the options button is clicked, it creates three buttons and hides the earlier ones.
    When clicked, they call the respective functions.
    For this screen, a new frame, canvas and background stars are created.
    """
    global canvas_options
    canvas_main.unbind("<q>")
    canvas_main.unbind("<Tab>")
    canvas_main.unbind("<Escape>")
    # Packing the outer leaderboard frame.
    secondary_frame.pack(fill="both", expand=1)

    # Creating a canvas for the leaderboard.
    canvas_options = Canvas(secondary_frame, bg="black", border=0)
    canvas_options.pack(side="left", fill="both", expand=1)

    # Adding 300 starts to the new canvas.
    for _ in range(300):
        optionsbg_x = randint(0, window_width)
        optionsbg_y = randint(0, window_height)

        options_size = randint(1, 5)
        options_color_chooser = randint(0, 4)

        canvas_options.create_oval(optionsbg_x, optionsbg_y, optionsbg_x + options_size, optionsbg_y + options_size,
                                   fill=color[options_color_chooser])

    # Hides the main menu buttons.
    canvas_main.itemconfig(main_image, state="hidden")
    canvas_main.itemconfig(game_saved, state="hidden")
    canvas_main.itemconfig(start, state="hidden")
    canvas_main.itemconfig(load, state="hidden")
    canvas_main.itemconfig(resume, state="hidden")
    canvas_main.itemconfig(save, state="hidden")
    canvas_main.itemconfig(restarted, state="hidden")
    hidden_buttons()

    # Shows the options menu buttons.
    canvas_main.itemconfig(cheats, state="normal")
    canvas_main.itemconfig(helps, state="normal")
    canvas_main.itemconfig(key_binds, state="normal")
    canvas_main.itemconfig(backs, state="normal")


def cheat_codes():
    """
    Displays and tells the user what the Cheat Codes are.
    Also mentions what the boss keys are.
    """
    global options_text
    # This text is displayed when the cheat code button is clicked.
    explanation = "Reset asteroid speed to default:\nShift + z \n\n" \
                  "Reduce asteroid speed by 1:\nShift + x \n\n" \
                  "Increase score by 500:\nShift + c \n\n" \
                  "God Mode (Invulnerability):\nShift + v\n\n\n" \
                  "BOSS KEY1: <TAB> and BOSS KEY2: <Q>"
    options_text = canvas_options.create_text(window_width / 2, window_height / 3 + 100, fill="white",
                                              font=("OCR A Extended", 25), text=explanation, justify="center")

    canvas_main.itemconfig(cheats, state="hidden")
    canvas_main.itemconfig(key_binds, state="hidden")
    canvas_main.itemconfig(helps, state="hidden")
    canvas_main.itemconfig(backs, state="hidden")

    canvas_main.itemconfig(back1s, state="normal")


def help_player():
    """
    Displays text and a back button to get back to options screen.
    Explains to the player the mechanism of the game.
    """
    global options_text
    # This text is displayed when the help button is clicked
    explanation = "The player has to avoid the asteroids to earn score and survive\n\n" \
                  "The speed and level will increase every 100 scores\n\n" \
                  "Speed will keep on increasing till game over\n\n" \
                  "The game is over if the player crashes into any asteroid\n\n" \
                  "The player can use cheats if he wants to but is discouraged\n\n\n" \
                  "BOSS KEY: <TAB> and BOSS KEY2: <Q>"
    options_text = canvas_options.create_text(window_width / 2, window_height / 3 + 100, fill="white",
                                              font=("OCR A Extended", 25), text=explanation, justify="center")

    canvas_main.itemconfig(cheats, state="hidden")
    canvas_main.itemconfig(key_binds, state="hidden")
    canvas_main.itemconfig(helps, state="hidden")
    canvas_main.itemconfig(backs, state="hidden")

    canvas_main.itemconfig(back1s, state="normal")


def key_binds_options():
    """
    This function displays two buttons and hides the buttons from previous screen.
    A text is displayed which describes what happens when clicked.
    There is also a back button which hides the current buttons and takes back to options menu.
    """
    global options_text, selected_keybind
    # This text is displayed when the keybinds button is clicked
    explanation = "You can choose any of the two below key-binds\n" \
                  "to move the spaceship"

    options_text = canvas_options.create_text(window_width / 2, window_height / 3 + 50, fill="white",
                                              font=("OCR A Extended", 25), text=explanation, justify="center")

    # The text displays whichever button was clicked and which keybind was selected.
    selected_keybind = canvas_options.create_text(window_width / 2, window_height / 2 + 80, fill="white",
                                                  font=("OCR A Extended", 20), justify="center")
    canvas_options.itemconfig(selected_keybind, state="hidden")

    canvas_main.itemconfig(cheats, state="hidden")
    canvas_main.itemconfig(key_binds, state="hidden")
    canvas_main.itemconfig(helps, state="hidden")
    canvas_main.itemconfig(backs, state="hidden")

    canvas_main.itemconfig(arrows, state="normal")
    canvas_main.itemconfig(wasd, state="normal")
    canvas_main.itemconfig(back1s, state="normal")


def arrows_keybinds():
    """
    When the "arrows" button is clicked this functions sets the arrow_flag to true.
    The arrow_flag switches the key-binds from wasd to arrows
    """
    global arrow_flag
    canvas_options.itemconfig(selected_keybind, text="Arrow keys selected", state="normal")
    arrow_flag = True


def wasd_keybinds():
    """
    When the "wasd" button is clicked this functions sets the arrow_flag to false.
    The false arrow_flag switches the key-binds from arrows to wasd
    """
    global arrow_flag
    canvas_options.itemconfig(selected_keybind, text="WASD keys selected", state="normal")
    arrow_flag = False


def back_clear_to_options():
    """
    This function clears the cheat code or help screen.
    It brings back the options screen.
    It makes a back button which connects to main menu.
    """
    canvas_main.itemconfig(cheats, state="normal")
    canvas_main.itemconfig(key_binds, state="normal")
    canvas_main.itemconfig(helps, state="normal")
    canvas_main.itemconfig(backs, state="normal")

    canvas_main.itemconfig(arrows, state="hidden")
    canvas_main.itemconfig(wasd, state="hidden")
    canvas_main.itemconfig(back1s, state="hidden")
    canvas_options.itemconfig(selected_keybind, state="hidden")
    canvas_options.delete(options_text)


def back_clear():
    """
    Clears the screen and brings out the buttons after exit is clicked on.
    Configured for 3 different cases as leaderboard can be accessed from 3 places.
    """
    global secondary_frame
    for widget in secondary_frame.winfo_children():
        widget.destroy()
    canvas_main.itemconfig(cheats, state="hidden")
    canvas_main.itemconfig(key_binds, state="hidden")
    canvas_main.itemconfig(helps, state="hidden")
    canvas_main.itemconfig(backs, state="hidden")
    secondary_frame.pack_forget()
    if pause_game:
        canvas_main.itemconfig(resume, state="normal")
        canvas_main.itemconfig(save, state="normal")
        canvas_main.itemconfig(restarted, state="normal")
        canvas_main.itemconfig(load, state="normal")
        canvas_main.bind("<Escape>", pause_menu)
    elif game_over:
        game_over_menu()
        canvas_main.coords(load, window_width / 2, window_height / 2 - 50)
    else:
        canvas_main.itemconfig(start, state="normal")
        canvas_main.itemconfig(load, state="normal")
    normal_buttons()
    canvas_main.itemconfig(main_image, state="normal")
    canvas_main.tag_raise(main_image)


# Functions about save and load
def save_game():
    """
    Saves the score, speed and spaceship position for the player to load later.
    Unfortunately this does not save the asteroid positions.
    """
    global score, asteroid_speed, spaceship_pos, level_number

    # Dumps the score, speed, level number and spaceship position to a dat file.
    dump(score, open("save/score.bat", "wb"))
    dump(asteroid_speed, open("save/asteroid_speed.bat", "wb"))
    dump(level_number, open("save/level.bat", "wb"))
    dump(spaceship_pos, open("save/spaceship_pos.bat", "wb"))

    canvas_main.itemconfig(game_saved, state="normal")


def load_game():
    """
    Loads the game from last saved files and resets the on-screen widgets.
    It loads everything apart from the asteroids from last session.
    The asteroids are newly formed after this load.
    """
    global score, asteroid_speed, restart_flag, pause_game, game_over, \
        level_number, bonus_on, low_speed_one_on, low_speed_default_on

    # Loads the saved values from the bat files.
    score = ld(open("save/score.bat", "rb"))
    asteroid_speed = ld(open("save/asteroid_speed.bat", "rb"))
    level_number = ld(open("save/level.bat", "rb"))
    ship_pos = ld(open("save/spaceship_pos.bat", "rb"))
    canvas_main.coords(spaceship, ship_pos[0], ship_pos[1])

    canvas_main.itemconfig(restarted, state="hidden")
    canvas_main.itemconfig(game_over_score, state="hidden")
    canvas_main.itemconfig(resume, state="hidden")
    canvas_main.itemconfig(save, state="hidden")
    canvas_main.itemconfig(game_saved, state="hidden")
    canvas_main.itemconfig(load, state="hidden")
    canvas_main.itemconfig(level, text="")

    # If not loaded from main menu, deletes
    if pause_game or game_over:
        for j in asteroid:
            canvas_main.delete(j)
        canvas_main.delete(scoreText)

    if bonus_on:
        canvas_main.delete(bonus_object)
        bonus_on = False

    if low_speed_one_on:
        canvas_main.delete(low_speed_one_object)
        low_speed_one_on = False

    if low_speed_default_on:
        canvas_main.delete(low_speed_default_object)
        low_speed_default_on = False

    pause_game = False

    hidden_buttons()
    main_game()


def bonus_parts():
    """
    This function makes and operates the 3 bonus objects.
    First one increases 200 score and deletes itself when collected.
    Second one reduces speed by 1 and Third one sets speed to default.
    """
    global bonus_on, bonus_object, score, low_speed_one_on, low_speed_one_object, asteroid_speed, \
        low_speed_default_on, low_speed_default_object

    if not bonus_on:
        bonus = randint(0, 1000)
        if bonus == 69 or bonus == 420:
            bonus_x = randint(100, window_width - 100)

            # Placing the ovals at the random points.
            bonus_object = canvas_main.create_oval(bonus_x, -20, bonus_x + 20, 0, fill="green")
            bonus_on = True

    if bonus_on:
        canvas_main.move(bonus_object, 0, 3)

        bonus_pos = canvas_main.coords(bonus_object)
        spaceship_pos1 = canvas_main.coords(spaceship)

        bonus_score = 60 > sqrt(pow(bonus_pos[0] + 10 - spaceship_pos1[0] - 50, 2)
                                + pow(bonus_pos[1] + 10 - spaceship_pos1[1] - 50, 2))

        if bonus_score:
            score += 200
            score_txt = "Score: " + str(score)
            canvas_main.itemconfig(scoreText, text=score_txt)
            canvas_main.tag_raise(scoreText)
            canvas_main.itemconfig(cheat, state="normal", text="Score increased by 200")

            canvas_main.delete(bonus_object)
            bonus_on = False

        if bonus_pos[1] >= window_height:
            canvas_main.delete(bonus_object)
            bonus_on = False

    " Decreases the asteroid speed by 1 "
    if (asteroid_speed >= 6 and system() == "Windows") or (asteroid_speed >= 2 and system() != "Windows"):
        if not low_speed_one_on:
            low_speed_one = randint(0, 500)
            if low_speed_one == 69 or low_speed_one == 420:
                low_speed_one_x = randint(100, window_width - 100)

                # Placing the ovals at the random points.
                low_speed_one_object = canvas_main.create_oval(low_speed_one_x, -20, low_speed_one_x + 20,
                                                               0, fill="orange")
                low_speed_one_on = True

    if low_speed_one_on:
        canvas_main.move(low_speed_one_object, 0, 3)

        low_speed_one_pos = canvas_main.coords(low_speed_one_object)
        spaceship_pos2 = canvas_main.coords(spaceship)

        low_speed_one_score = 60 > sqrt(pow(low_speed_one_pos[0] + 10 - spaceship_pos2[0] - 50, 2)
                                        + pow(low_speed_one_pos[1] + 10 - spaceship_pos2[1] - 50, 2))

        if low_speed_one_score:
            if system() == "Windows":
                asteroid_speed -= 1
            else:
                asteroid_speed -= 0.2

            canvas_main.itemconfig(cheat, state="normal", text="Speed reduced by 1")

            canvas_main.delete(low_speed_one_object)
            low_speed_one_on = False

        if low_speed_one_pos[1] >= window_height:
            canvas_main.delete(low_speed_one_object)
            low_speed_one_on = False

    " Sets the asteroid speed to default "
    if (asteroid_speed >= 6 and system() == "Windows") or (asteroid_speed >= 2 and system() != "Windows"):
        if not low_speed_default_on:
            low_speed_default = randint(0, 2000)
            if low_speed_default == 69 or low_speed_default == 420:
                low_speed_default_x = randint(100, window_width - 100)

                # Placing the ovals at the random points.
                low_speed_default_object = canvas_main.create_oval(low_speed_default_x, -20, low_speed_default_x + 20,
                                                                   0, fill="red")
                low_speed_default_on = True

    if low_speed_default_on:
        canvas_main.move(low_speed_default_object, 0, 3)

        low_speed_default_pos = canvas_main.coords(low_speed_default_object)
        spaceship_pos3 = canvas_main.coords(spaceship)

        low_speed_default_score = 60 > sqrt(pow(low_speed_default_pos[0] + 10 - spaceship_pos3[0] - 50, 2)
                                            + pow(low_speed_default_pos[1] + 10 - spaceship_pos3[1] - 50, 2))

        if low_speed_default_score:
            if system() == "Windows":
                asteroid_speed = 4
            else:
                asteroid_speed = 1.6

            canvas_main.itemconfig(cheat, state="normal", text="Speed set to default")
            # Raising so that any other object does not come in front of it.
            canvas_main.tag_raise(cheat)

            canvas_main.delete(low_speed_default_object)
            low_speed_default_on = False

        if low_speed_default_pos[1] >= window_height:
            canvas_main.delete(low_speed_default_object)
            low_speed_default_on = False


# Functions running the main game
def asteroids_and_collision():
    """
    Keeps the asteroid falling loop running till the game is over.
    The collision detection and finds when game over.
    """
    global pause_game, game_over, score, asteroid_speed, spaceship_pos, \
        level_number, invulnerable, bonus_on, bonus_object, low_speed_one_on, \
        low_speed_one_object, low_speed_default_on, low_speed_default_object

    # This loop only happens if pause flag is false.
    while not pause_game:
        bonus_parts()

        x = y = [asteroid_speed] * 4
        # For 4 asteroids, the for-loop loops 4 times.
        for i in range(4):
            pos = canvas_main.coords(asteroid[i])
            # When the asteroid goes out of the window height, the asteroids are repositioned
            if pos[1] >= window_height:
                canvas_main.coords(asteroid[i], randint(50, window_width - 110), randint(-500, 0))
                score += 10
                score_txt = "Score: " + str(score)
                canvas_main.itemconfig(scoreText, text=score_txt)
                canvas_main.tag_raise(scoreText)
                # Every hundred score, level and asteroid speed increases.
                if score != 0 and score % 100 == 0:
                    if system() == "Windows":
                        asteroid_speed += 1
                    else:
                        asteroid_speed += 0.2
                    level_number += 1
                    canvas_main.itemconfig(level, state="normal",
                                           text=("Level " + str(level_number) + ": Speed increased"))
                    canvas_main.itemconfig(cheat, state="hidden")
                # Level and cheat activated texts are removed when the score reaches 40s.
                elif (score - 40) % 100 == 0:
                    canvas_main.itemconfig(level, state="hidden")
                    canvas_main.itemconfig(cheat, state="hidden")

            # Position of the asteroids and the spaceship.
            asteroid_pos = canvas_main.coords(asteroid[i])
            spaceship_pos = canvas_main.coords(spaceship)

            spaceship_touches_sides()

            if not invulnerable:

                # Collision detection system.
                game_over = 105 > sqrt(pow(asteroid_pos[0] + 10 - spaceship_pos[0], 2)
                                       + pow(asteroid_pos[1] - spaceship_pos[1], 2))

                # When game is over, the following actions are taken
                if game_over:
                    unbind_keys()
                    canvas_main.unbind("<Escape>")
                    canvas_main.unbind("<Tab>")
                    canvas_main.unbind("<q>")
                    canvas_main.itemconfig(game_over_text, state="normal")
                    canvas_main.tag_raise(game_over_text)
                    canvas_main.itemconfig(level, state="hidden")
                    canvas_main.itemconfig(cheat, state="hidden")
                    canvas_main.itemconfig(scoreText, state="hidden")
                    canvas_main.coords(load, window_width / 2, window_height / 2 - 100)

                    # Saves the game when the score is not 0
                    if score != 0:
                        # Calls the function to save the score and player name
                        save_leaderboard(name, score)

                    if bonus_on:
                        canvas_main.delete(bonus_object)
                        bonus_on = False

                    if low_speed_one_on:
                        canvas_main.delete(low_speed_one_object)
                        low_speed_one_on = False

                    if low_speed_default_on:
                        canvas_main.delete(low_speed_default_object)
                        low_speed_default_on = False

                    canvas_main.after(1000, game_over_menu)
                    break

            if i == 3:
                canvas_main.move(asteroid[i], -x[i] / 4, y[i])
            elif i == 2:
                canvas_main.move(asteroid[i], x[i] / 3, y[i])
            else:
                # Moves the asteroids down every time.
                canvas_main.move(asteroid[i], 0, y[i])

        # As long as the game is not over, loops back after 0.001 seconds.
        if not game_over:
            sleep(0.001)
            window.update()
            continue
        break


def main_game():
    """
    Initiates all the widgets and starts the main game.
    Hides the previous buttons and binds the keys to control the spaceship.
    Initials scoring system and asteroid's initial position.
    """
    global score, scoreText, restart_flag, asteroid

    shift_buttons(50)

    # Display only if the game starts from 0.
    if score == 0:
        canvas_main.itemconfig(level, text=("Level " + str(level_number) + "\n\nDodge the Asteroids"))

    # Hides the main menu buttons.
    canvas_main.itemconfig(main_image, state="hidden")
    canvas_main.itemconfig(start, state="hidden")
    canvas_main.itemconfig(load, state="hidden")
    hidden_buttons()

    # Deletes the scoreText when restarting.
    if restart_flag:
        canvas_main.delete(scoreText)
        restart_flag = False

    # Adding the spaceship.
    canvas_main.itemconfig(spaceship, state="normal")

    """ 
    Binding the keys to control spaceship and pause the game
    Binding the cheats to their binds and the boss key to TAB as well
    """
    # This function binds all the keys.
    bind_keys()
    canvas_main.bind("<Escape>", pause_menu)

    # Boss Key - TAB.
    canvas_main.bind("<Tab>", boss_key1)
    canvas_main.bind("<q>", boss_key2)
    canvas_main.focus_set()

    "Making the scoring system"
    # storing and displaying the score.
    score_text = "Score: " + str(score)

    # displaying the score on the top right.
    scoreText = canvas_main.create_text(window_width - window_width / 8, window_height / 15,
                                        fill="white", font=("OCR A Extended", 30), text=score_text)
    canvas_main.tag_raise(scoreText)

    "Stores the initial asteroid positions to a list"
    asteroid = []
    for _ in range(4):
        asteroid_x = randint(50, window_width - 110)
        asteroid_y = randint(-1000, -100)
        asteroid_select = randint(0, 3)
        asteroid.append(canvas_main.create_image(asteroid_x, asteroid_y,
                                                 image=asteroid_image[asteroid_select],
                                                 anchor="nw"))
    canvas_main.itemconfig(level, state="normal")
    canvas_main.tag_raise(level)
    asteroids_and_collision()


# Creates the main window.
window = Tk()

# Setting the width and height of the main window.
window_width = 1440
window_height = 900

# Calls the function to configure the window size and position.
configure_window()

"Defining various variables needed all over the game."
arrow_flag = True
restart_flag = False
invulnerable = False
pause_game = False
game_over = False
bonus_on = False
low_speed_one_on = False
low_speed_default_on = False
boss_flag = False
spaceship_pos = None
options_text = None
canvas_options = None
enter_name_box = None
selected_keybind = None
bonus_object = ""
low_speed_one_object = ""
low_speed_default_object = ""
name = getlogin()
asteroid = []
scoreText = ""
entry_box = ""
level_number = 1
score = 0
count = 50
if system() == "Windows":
    asteroid_speed = 4
else:
    asteroid_speed = 1.6

"Creating the Main Canvas of the game."
# Will contain most of the game
canvas_main = Canvas(window, width=window_width, height=window_height, bg="black")
canvas_main.pack(fill="both", expand=True)

"Creating a leaderboard frame."
# There is an outer frame to contain a canvas which will contain another frame.
secondary_frame = Frame(canvas_main, border=0)

"Background image of menus."
# Will be shown on title page, start, pause and game over menu.
main_menu_image = ImageTk.PhotoImage(Image.open("images/main.png"))
main_image = canvas_main.create_image(window_width / 2, window_height / 2,
                                      image=main_menu_image, anchor="center")
canvas_main.itemconfig(main_image, state="normal")

"Creating the leaderboard database if it does not exist"
create_database_table()

"""
The following are different texts that will be displayed at certain point.
Made here to reduce global variable usages.
Set to hidden for later usages when needed.
"""

# This will display the final score after the game is over.
game_over_score = canvas_main.create_text(window_width / 2, window_height / 5, fill="white",
                                          font=("OCR A Extended", 60))
canvas_main.itemconfig(game_over_score, state="hidden")

# This will show the cheat message when any cheat is activated. Modified later for different cheats.
cheat = canvas_main.create_text(window_width / 2, window_height / 2,
                                fill="white", font=("OCR A Extended", 20))
canvas_main.itemconfig(cheat, state="hidden")

# When the game is saved, this will be written at the bottom right.
game_saved = canvas_main.create_text(window_width - 100, window_height - 30, fill="white",
                                     font=("OCR A Extended", 20), text="Game Saved")
canvas_main.itemconfig(game_saved, state="hidden")

# level_number text that will be shown upper mid upon each level increment.
level = canvas_main.create_text(window_width / 2, window_height / 7, fill="white",
                                font=("OCR A Extended", 25), justify="center")
canvas_main.itemconfig(level, state="hidden")

# level_number text that will be shown upper mid upon each level increment.
name_change_text = canvas_main.create_text(window_width / 2, window_height / 2 - 100, fill="white",
                                           font=("OCR A Extended", 25), justify="center")
canvas_main.itemconfig(name_change_text, state="hidden")

# The text that will be shown when the game is over
game_over_text = canvas_main.create_text(window_width / 2, window_height / 2, fill="white",
                                         font=("OCR A Extended", 120), text="Game Over")
canvas_main.itemconfig(game_over_text, state="hidden")

"""
This will add a background of stars to the whole game.
For this, canvas shapes, ovals, are used of random sizes at random places.
Inspired from stewart's videos and modified for my needs.
"""
# Color palette of 5 different colours.
color = ["white", "#fefefe", "#dfdfdf", "#ad7f00", "#828181"]

# Made 300 starts to reduce lag as higher numbers were causing lags.
for _ in range(300):
    bg_x = randint(0, window_width)
    bg_y = randint(0, window_height)

    # randomly selecting size and colour of the ovals.
    size = randint(1, 5)
    color_chooser = randint(0, 4)

    # Placing the ovals at the random points.
    canvas_main.create_oval(bg_x, bg_y, bg_x + size, bg_y + size, fill=color[color_chooser])

""" 
The following things will be displayed when the game is launched.
This will stay till enter is pressed to move on to start menu.
"""
# text showing the title of the game in large font.
title_text = canvas_main.create_text(window_width / 2, window_height / 3 + 60,
                                     fill="white", font=("OCR A Extended", 90),
                                     text="INTO THE SPACE")

# This will great the player using the name of the user of the pc.
welcome_text = canvas_main.create_text(window_width / 2, window_height / 2 + 10,
                                       fill="white", font=("OCR A Extended", 40),
                                       text="Hello")

# This will show the text of press enter to continue to start menu.
press_enter_to_continue = canvas_main.create_text(window_width / 2, window_height / 2 + 70,
                                                  fill="white", font=("OCR A Extended", 25),
                                                  text="Please press enter to continue")

# Key binding the enter button so that player can access the start menu by clicking it.
canvas_main.bind("<Return>", ask_name_choice)
canvas_main.focus_set()

"""
The next sections are about loading, resizing and storing images to variables.
Using the images, buttons are created and the state is set to hidden to use later.
Position of the buttons are fixed using the coords function.
"""
"Use default button."
use_default_org = Image.open("images/use_default.png")
use_default_resized = use_default_org.resize((400, 75))
use_default_image = ImageTk.PhotoImage(use_default_resized)
use_default_button = Button(window, image=use_default_image, bg="black", border=0, command=use_default_name)
use_default = canvas_main.create_window(window_width / 2, window_height / 2, window=use_default_button)
canvas_main.itemconfig(use_default, state="hidden")

"Change name button."
change_name_org = Image.open("images/change_name.png")
change_name_resized = change_name_org.resize((400, 75))
change_name_image = ImageTk.PhotoImage(change_name_resized)
change_name_button = Button(window, image=change_name_image, bg="black", border=0, command=change_name)
change_name = canvas_main.create_window(window_width / 2, window_height / 2 + 100, window=change_name_button)
canvas_main.itemconfig(change_name, state="hidden")

"Done button."
done_org = Image.open("images/done.png")
done_resized = done_org.resize((200, 75))
done_image = ImageTk.PhotoImage(done_resized)
done_button = Button(window, image=done_image, bg="black", border=0, command=done_button_click)
done = canvas_main.create_window(window_width / 2, window_height / 2 + 100, window=done_button)
canvas_main.itemconfig(done, state="hidden")

"Start button."
start_org = Image.open("images/start.png")
start_resized = start_org.resize((200, 75))
start_image = ImageTk.PhotoImage(start_resized)
start_button = Button(window, image=start_image, bg="black", border=0, command=main_game)
start = canvas_main.create_window(window_width / 2, window_height / 2 - 200, window=start_button)
canvas_main.itemconfig(start, state="hidden")

"Resume button."
resume_org = Image.open("images/resume.png")
resume_resized = resume_org.resize((244, 80))
resume_image = ImageTk.PhotoImage(resume_resized)
resume_button = Button(window, image=resume_image, border=0, bg="black", command=resume_button_click)
resume = canvas_main.create_window(window_width / 2, window_height / 2 - 300, window=resume_button)
canvas_main.itemconfig(resume, state="hidden")
resume_coords = canvas_main.coords(resume)

"Restart button."
restart_org = Image.open("images/restart.png")
restart_resized = restart_org.resize((244, 80))
restart_image = ImageTk.PhotoImage(restart_resized)
restart_button = Button(window, image=restart_image, border=0, bg="black", command=restart_game)
restarted = canvas_main.create_window(window_width / 2, window_height / 2 - 200, window=restart_button)
canvas_main.itemconfig(restarted, state="hidden")
restart_coords = canvas_main.coords(restarted)

"Save button."
save_org = Image.open("images/save.png")
save_resized = save_org.resize((204, 80))
save_image = ImageTk.PhotoImage(save_resized)
save_button = Button(window, image=save_image, border=0, bg="black", command=save_game)
save = canvas_main.create_window(window_width / 2, window_height / 2 - 50, window=save_button)
canvas_main.itemconfig(save, state="hidden")
save_coords = canvas_main.coords(save)

"Load button."
load_org = Image.open("images/load.png")
load_resized = load_org.resize((204, 80))
load_image = ImageTk.PhotoImage(load_resized)
load_button = Button(window, image=load_image, border=0, bg="black", command=load_game)
load = canvas_main.create_window(window_width / 2, window_height / 2 - 100, window=load_button)
canvas_main.itemconfig(load, state="hidden")
load_coords = canvas_main.coords(load)

"Leaderboard button."
leaderboard_org = Image.open("images/leaderboard.png")
leaderboard_resized = leaderboard_org.resize((474, 80))
leaderboard_image = ImageTk.PhotoImage(leaderboard_resized)
leaderboard_button = Button(window, image=leaderboard_image, border=0, bg="black", command=leaderboard)
leaderboards = canvas_main.create_window(window_width / 2, window_height / 2, window=leaderboard_button)
canvas_main.itemconfig(leaderboards, state="hidden")
leaderboard_coords = canvas_main.coords(leaderboards)

"Options button."
options_org = Image.open("images/options.png")
options_resized = options_org.resize((240, 75))
options_image = ImageTk.PhotoImage(options_resized)
options_button = Button(window, image=options_image, bg="black", border=0, command=options_button_click)
options = canvas_main.create_window(window_width / 2, window_height / 2 + 100, window=options_button)
canvas_main.itemconfig(options, state="hidden")
options_coords = canvas_main.coords(options)

"Cheat button."
cheat_org = Image.open("images/cheat.png")
cheat_resized = cheat_org.resize((204, 75))
cheat_image = ImageTk.PhotoImage(cheat_resized)
cheat_button = Button(window, image=cheat_image, border=0, bg="black", command=cheat_codes)
cheats = canvas_main.create_window(window_width / 2, window_height / 2 - 100, window=cheat_button)
canvas_main.itemconfig(cheats, state="hidden")

"Key_binds button."
key_binds_org = Image.open("images/key_binds.png")
key_binds_resized = key_binds_org.resize((354, 80))
key_binds_image = ImageTk.PhotoImage(key_binds_resized)
key_binds_button = Button(window, image=key_binds_image, border=0, bg="black", command=key_binds_options)
key_binds = canvas_main.create_window(window_width / 2, window_height / 2, window=key_binds_button)
canvas_main.itemconfig(key_binds, state="hidden")

"Arrows button."
arrows_org = Image.open("images/arrows.png")
arrows_resized = arrows_org.resize((334, 90))
arrows_image = ImageTk.PhotoImage(arrows_resized)
arrows_button = Button(window, image=arrows_image, border=0, bg="black", command=arrows_keybinds)
arrows = canvas_main.create_window(window_width / 2 - 150, window_height / 2, window=arrows_button)
canvas_main.itemconfig(arrows, state="hidden")

"Wasd button."
wasd_org = Image.open("images/wasd.png")
wasd_resized = wasd_org.resize((254, 90))
wasd_image = ImageTk.PhotoImage(wasd_resized)
wasd_button = Button(window, image=wasd_image, border=0, bg="black", command=wasd_keybinds)
wasd = canvas_main.create_window(window_width / 2 + 150, window_height / 2, window=wasd_button)
canvas_main.itemconfig(wasd, state="hidden")

"Help button."
help_org = Image.open("images/help.png")
help_resized = help_org.resize((174, 80))
help_image = ImageTk.PhotoImage(help_resized)
help_button = Button(window, image=help_image, border=0, bg="black", command=help_player)
helps = canvas_main.create_window(window_width / 2, window_height / 2 + 100, window=help_button)
canvas_main.itemconfig(helps, state="hidden")

"Back button."
back_org = Image.open("images/Back.png")
back_resized = back_org.resize((204, 75))
back_image = ImageTk.PhotoImage(back_resized)
back_button = Button(window, image=back_image, border=0, bg="black", command=back_clear)
backs = canvas_main.create_window(window_width / 2, window_height - window_height / 7, window=back_button)
canvas_main.itemconfig(backs, state="hidden")

"Back button to options."
back1_org = Image.open("images/back.png")
back1_resized = back1_org.resize((204, 75))
back1_image = ImageTk.PhotoImage(back1_resized)
back1_button = Button(window, image=back1_image, border=0, bg="black", command=back_clear_to_options)
back1s = canvas_main.create_window(window_width / 2, window_height - window_height / 7, window=back1_button)
canvas_main.itemconfig(back1s, state="hidden")

"Exit button."
exit_org = Image.open("images/exit.png")
exit_resized = exit_org.resize((200, 70))
exit_image = ImageTk.PhotoImage(exit_resized)
exit_button = Button(window, image=exit_image, bg="black", border=0, command=window.destroy)
exited = canvas_main.create_window(window_width / 2, window_height / 2 + 200, window=exit_button)
canvas_main.itemconfig(exited, state="hidden")
exit_coords = canvas_main.coords(exited)

"Boss Key Image."
boss_key_image = ImageTk.PhotoImage(Image.open("images/bosskey.png"))
boss_key = canvas_main.create_image(window_width / 2, window_height / 2, image=boss_key_image, anchor="center")
canvas_main.itemconfig(boss_key, state="hidden")

"Spaceship."
spaceship_org = Image.open("images/spaceship_image.png")
spaceship_resized = spaceship_org.resize((100, 100))
spaceship_image = ImageTk.PhotoImage(spaceship_resized)
spaceship = canvas_main.create_image(window_width / 2 - 40,
                                     window_height - window_height / 6,
                                     image=spaceship_image, anchor="nw")
canvas_main.itemconfig(spaceship, state="hidden")

"List data structure to store asteroid images."
asteroid_image = []
for m in range(1, 5):
    asteroid_org = Image.open("images/asteroid_" + str(m) + ".png")
    asteroid_resized = asteroid_org.resize((120, 120))
    asteroid_image.append(ImageTk.PhotoImage(asteroid_resized))

# Keeps looping the gui till closed manually.
window.mainloop()
