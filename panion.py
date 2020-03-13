# virtual pet game/program

import pygame
from pygame.locals import *
import sys
import sqlite3
import random


ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

WIDTH = 800
HEIGHT = 800

FPS = 60


class Game:
    def __init__(self):
        self.running = False
        self.startrun = True
        self.interactables = []
        self.decorations = []
        self.pets = []
        self.menus = []
        self.clocks = []
        self.secs = 0
        self.mins = 0
        self.hours = 0
        self.MAIN_SURF = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Panion")
        pygame.display.set_icon(pygame.image.load("assets/icon.png"))

        pygame.init()
        self.startup()

    def __str__(self):
        """
        Prints all the information for the class in a readable format
        :return: All attributes within the class
        """
        return "GAME CLASS - \nRunning: " + str(self.running) + "\nInteractables: " + str(self.interactables) + "\nDecorations: " + str(self.decorations) + "\nPets: " + str(self.pets) + "\nMenus: " + str(self.menus) + "\nClocks: " + str(self.clocks)

    def menu(self, menu):
        """
        Creates an instance of Menu with specific buttons based on the type
        :param menu: the type of menu, which dictates the buttons within it
        :return: None
        """
        self.add_menu(menu)

    def run(self):
        """
        Contains the main game loop
        :return: None
        """
        running = True
        # start the game clock
        self.add_clock()
        # main game loop
        while running:
            # check for events
            self.event_handler()
            # tick the clock
            self.clocks[0].tick(FPS)
            # change real time to 'game time' and check repeated actions
            for i in self.pets:
                i.check_repeat(self.correct_time(), "eat")
        # once main loop is finished, end the game
        self.end()

    def startup(self):
        """
        Runs the startup sequence
        :return: None
        """
        # sets the background colour
        self.MAIN_SURF.fill((220, 200, 210))
        # updates the display
        pygame.display.update()
        self.startrun = True
        # creates a start menu
        self.menu("playthirst")
        # loops starting menus until the main game loop starts
        while self.startrun:
            # checks for events
            self.event_handler()
            # updates the display
            pygame.display.update()

    def event_handler(self):
        """
        Handles all events created by the user
        :return: None
        """
        # for all the events that occur per loop:
        for event in pygame.event.get():
            # if the event is clicking the exit button:
            if event.type == QUIT:
                # stop both loops so that the program can quit
                self.startrun = False
                self.running = False

    def end(self):
        """
        Saves all pet data into the database and quits the program
        :return: None
        """
        # connect to the database
        conn = sqlite3.connect('pets.db')
        # create a cursor within the db
        c = conn.cursor()
        # loop all pets
        for i in self.pets:
            # change all values to the new values
            c.execute('UPDATE pets SET Happiness = ' + i.get_stat("happiness") +
                      ', Hunger = ' + i.get_stat("hunger") + ', Comfort = ' + i.get_stat("comfort") + ', Anger = ' +
                      i.get_stat("hunger") + ', Thirst = ' + i.get_stat("thirst") + ', Energy = ' + i.get_stat("energy") +
                      ', Hours = ' + str(self.correct_time()[0]) + ', Mins = ' + str(self.correct_time()[1]) + ', Secs = ' +
                      str(self.correct_time()[2]) + ' WHERE Name = ' + i.get_name())
        # quit pygame
        pygame.quit()
        # quit the window
        sys.exit()

    def process_click(self, pos):
        """
        Processes what clicked() method to call when a point is clicked on the screen
        :param pos: The position clicked
        :return: None
        """

    def get_interactable(self, index):
        """
        Returns a specific instance of the Interactable class
        :param index: The index of the desired instance
        :return: Instance of Interactable class
        """
        return self.interactables[index]

    def add_interactable(self, display, action):
        """
        Adds a new instance of the Interactable class to the array self.interactables
        :param display: What the Interactable is/what it looks like
        :param action: The action performed when the Interactable is clicked on
        :return: None
        """
        self.interactables.append(Interactable(display, action, self.MAIN_SURF))

    def remove_interactable(self, index):
        """
        Removes a specific instance of Interactable
        :param index: The index of the desired instance
        :return: None
        """
        self.interactables.remove(index)

    def get_decoration(self, index):
        """
        Returns a specific instance of the Decorative class
        :param index: The index of the desired instance
        :return: Instance of the Decorative class
        """
        return self.decorations[index]

    def add_decorative(self, display):
        """
        Adds a new instance of the Decorative class to the array self.decorations
        :param display: What the Decorative is/what it looks like
        :return: None
        """
        self.decorations.append(Decorative(display, self.MAIN_SURF))

    def remove_decorative(self, index):
        """
        Removes a specific instance of Decorative
        :param index: The index of the desired instance
        :return: None
        """
        self.decorations.remove(index)

    def get_pet(self, index):
        """
        Returns a specific instance of the Pet class
        :param index: The index of the desired instance
        :return: Instance of the Pet class
        """
        return self.pets[index]

    def add_pet(self, name, animal):
        """
        Adds a new instance of the Pet class to the array self.pets
        :param name: Name of the pet
        :param animal: What animal the pet is
        :return: None
        """
        self.pets.append(Pet(name, animal, self.MAIN_SURF))

    def remove_pet(self, index):
        """
        Removes a specific instance of the Pet class
        :param index: The index of the desired instance
        :return: None
        """
        self.pets.remove(index)

    def get_menu(self, index):
        """
        Returns a specific instance of the Menu class
        :param index: The index of the desired instance
        :return: Instance of the Menu class
        """
        return self.menus[index]

    def get_menus(self):
        """
        Returns the whole menu list
        :return: self.menus
        """
        return self.menus

    def add_menu(self, menu):
        """
        Adds a new instance of the Menu class to the array self.menus
        :param menu: Type of menu
        :return: None
        """
        self.menus.append(Menu(menu, self.MAIN_SURF))

    def remove_menu(self, index):
        """
        Removes a specific instance of the Menu class
        :param index: The index of the desired instance
        :return: None
        """
        self.menus.remove(index)

    def get_clock(self, index):
        """
        Returns a specific clock in self.clocks
        :param index: The index of the desired object
        :return: A PyGame Clock object
        """
        return self.clocks[index]

    def add_clock(self):
        """
        Adds a new PyGame Clock object to the array self.clocks
        :return: None
        """
        self.clocks.append(pygame.time.Clock())

    def remove_clock(self, index):
        """
        Removes a specific PyGame Clock object
        :param index: The index of the desired object
        :return: None
        """
        self.clocks.remove(index)

    def correct_time(self):
        """
        Changes the PyGame time to 'game time'
        :return: [hours, minutes, seconds]
        """
        # adds 'seconds passed' (milliseconds) since last tick to seconds
        self.secs = int((self.clocks[0].get_time()) + self.secs)
        # if a game minute has passed...
        if self.secs >= 1000:
            # reset seconds
            self.secs = 0
            # add a minute
            self.mins += 1
        # etc for mins and hours
        if self.mins >= 60:
            self.mins = 0
            self.hours += 1
        if self.hours >= 24:
            # reset clock to loop back after 24 'hours'
            self.hours = 0
        # return hours mins and secs
        return [self.hours, self.mins, self.secs]

    def swap_running(self):
        """
        Swaps the running attribute to the opposite of what it was
        :return: None
        """
        self.running = not self.running

    def swap_startrun(self):
        """
        Swaps the selfrun attribute to the opposite of what it was
        :return: None
        """
        self.startrun = not self.startrun

    def get_surf(self):
        """
        Returns the surface that the Game class is using (MAIN_SURF)
        :return: self.MAIN_SURF
        """
        return self.MAIN_SURF


class Menu:
    def __init__(self, menu, surface):
        self.menu = menu
        self.buttons = []
        self.decorations = []
        self.text = []
        self.surface = surface
        self.calc_buttons()

    def __str__(self):
        """
        Prints all the information for the class in a readable format
        :return: All attributes of the class
        """
        return "MENU CLASS - \nMenu: " + str(self.menu) + "\nButtons: " + str(self.buttons)

    def calc_buttons(self):
        """
        Works out which buttons are required for the specified type of menu, and adds these buttons using self.add_button(button)
        :return: None
        """
        if self.menu == "start":
            # add all of the parts of the menu
            self.add_decoration("logo")  # panion logo at top
            self.add_button("buttonnew")
            self.add_button("buttonold")
            self.add_button("buttonsettings")
            # change the size of all the buttons
            for i in range(len(self.buttons)):
                self.buttons[i].set_sprite(pygame.transform.rotozoom(self.buttons[i].get_sprite(), 0, 0.4))
            # change the size of the logo
            self.decorations[0].set_sprite(pygame.transform.rotozoom(self.decorations[0].get_sprite(), 0, 0.5))
            # x value for centering buttons
            x = WIDTH//2 - self.buttons[0].get_sprite().get_width()//2
            # set positions of all menu parts
            self.decorations[0].set_pos([WIDTH//2 - self.decorations[0].get_sprite().get_width()//2, 5])
            self.buttons[0].set_pos([x, 275])
            self.buttons[1].set_pos([x, 425])
            self.buttons[2].set_pos([x, 575])
            # draw all of the parts of the menu in the correct places
            self.decorations[0].draw()
            self.buttons[0].draw()
            self.buttons[1].draw()
            self.buttons[2].draw()
        elif self.menu == "oldpet":
            # add all parts of the menu
            self.add_button("buttonback")
            self.add_text()
            self.add_button("buttonplay")
            # scaling all of the buttons
            for i in range(len(self.buttons)):
                self.buttons[i].set_sprite(pygame.transform.rotozoom(self.buttons[i].get_sprite(), 0, 0.4))
            # scaling the text box
            self.text[0].set_sprite(pygame.transform.rotozoom(self.text[0].get_sprite(), 0, 0.75))
            # set positions of all menu parts
            self.buttons[0].set_pos([100, 575])
            self.buttons[1].set_pos([400, 575])
            self.text[0].set_pos([WIDTH//2 - self.text[0].get_sprite().get_width()//2, HEIGHT//2])
            # drawing all parts of the menu
            self.buttons[0].draw()
            self.buttons[1].draw()
            self.text[0].draw()
        elif self.menu == "petchoice":
            # add all parts of the menu
            self.add_decoration("choosepet")
            self.add_button("cat")
            self.add_button("dog")
            self.add_button("duck")
            self.add_button("buttonnext")
            # scaling of buttons
            self.buttons[3].set_sprite(pygame.transform.rotozoom(self.buttons[3].get_sprite(), 0, 0.4))
            # scaling the text
            self.decorations[0].set_sprite(pygame.transform.rotozoom(self.decorations[0].get_sprite(), 0, 0.5))
            # x value for centering buttons
            x = WIDTH//2 - self.buttons[3].get_sprite().get_width()//2
            # set positions of all menu parts
            self.decorations[0].set_pos([WIDTH//2 - self.decorations[0].get_sprite().get_width()//2, 60])
            self.buttons[0].set_pos([WIDTH//4 - self.buttons[0].get_sprite().get_width()//2, HEIGHT//2 - 55])
            self.buttons[1].set_pos([WIDTH//2 - self.buttons[1].get_sprite().get_width()//2, HEIGHT//2 - 20])
            self.buttons[2].set_pos([WIDTH - WIDTH//4 - self.buttons[0].get_sprite().get_width()//2, HEIGHT//2 - 40])
            self.buttons[3].set_pos([x, 600])
            # drawing all parts of the menu
            self.decorations[0].draw()
            self.buttons[0].draw()
            self.buttons[1].draw()
            self.buttons[2].draw()
            self.buttons[3].draw()
        elif self.menu == "namepet":
            # add all parts of the menu
            self.add_button("buttonsettings")
            self.add_decoration("cat")  # TODO: add extra variables when doing the clicked method that allow this to change with the chosen pet
            self.add_text()
            self.add_button("buttondone")
            # scale the buttons
            for i in range(len(self.buttons)):
                self.buttons[i].set_sprite(pygame.transform.rotozoom(self.buttons[i].get_sprite(), 0, 0.4))
            # scale text
            self.text[0].set_sprite(pygame.transform.rotozoom(self.text[0].get_sprite(), 0, 0.75))
            # set positions of all parts of menu
            self.buttons[0].set_pos([WIDTH - (160 + self.buttons[0].get_sprite().get_width()//2), 5])
            self.buttons[1].set_pos([WIDTH//2 - self.buttons[1].get_sprite().get_width()//2, HEIGHT - 200])
            self.decorations[0].set_pos([WIDTH//2 - self.decorations[0].get_sprite().get_width()//2, HEIGHT - 550])
            self.text[0].set_pos([WIDTH//2 - self.text[0].get_sprite().get_width()//2, HEIGHT - (300 + self.text[0].get_sprite().get_height()//2)])
            # draw all parts of menu
            self.buttons[0].draw()
            self.buttons[1].draw()
            self.decorations[0].draw()
            self.text[0].draw()
        elif self.menu == "pause":
            # add all parts of the menu
            self.add_decoration("paused")
            self.add_button("buttonresume")
            self.add_button("buttonsettings")
            self.add_button("buttonquit")
            # scale the buttons
            for i in range(len(self.buttons)):
                self.buttons[i].set_sprite(pygame.transform.rotozoom(self.buttons[i].get_sprite(), 0, 0.4))
            # set positions of all parts of menu
            self.decorations[0].set_pos([WIDTH//2 - self.decorations[0].get_sprite().get_width()//2, 20])
            self.buttons[0].set_pos([WIDTH//2 - self.buttons[0].get_sprite().get_width()//2, 300])
            self.buttons[1].set_pos([WIDTH//2 - self.buttons[1].get_sprite().get_width()//2, 450])
            self.buttons[2].set_pos([WIDTH//2 - self.buttons[2].get_sprite().get_width()//2, 600])
            # draw all parts of menu
            self.decorations[0].draw()
            self.buttons[0].draw()
            self.buttons[1].draw()
            self.buttons[2].draw()
        elif self.menu == "settings":
            # add all parts of menu
            self.add_decoration("settings")
            # self.add_button("volume")
            # TODO: add volume into Interactable class
            self.add_button("buttondone")
            # scale the buttons
            for i in range(len(self.buttons)):
                self.buttons[i].set_sprite(pygame.transform.rotozoom(self.buttons[i].get_sprite(), 0, 0.4))
            # scale settings text
            self.decorations[0].set_sprite(pygame.transform.rotozoom(self.decorations[0].get_sprite(), 0, 0.4))
            # x value for centering buttons
            x = WIDTH//2 - self.buttons[0].get_sprite().get_width()//2
            # set positions of all parts of menu
            self.decorations[0].set_pos([WIDTH//2 - self.decorations[0].get_sprite().get_width()//2, 20])
            self.buttons[0].set_pos([x, 600])   # change the 0 to a 1 if I include volume
            # draw all parts of menu
            self.decorations[0].draw()
            self.buttons[0].draw()
        elif self.menu == "playscreen":
            # add all parts of menu
            self.add_button("buttonpause")
            # scale the buttons
            self.buttons[0].set_sprite(pygame.transform.rotozoom(self.buttons[0].get_sprite(), 0, 0.2))
            # set positions of all parts of menu
            self.buttons[0].set_pos([-25, 3])
            # draw all parts of menu
            self.buttons[0].draw()
        elif self.menu == "playthirst":
            # add all parts of menu
            self.add_button("buttonpause")
            self.add_decoration("thirst")
            # scale the buttons
            self.buttons[0].set_sprite(pygame.transform.rotozoom(self.buttons[0].get_sprite(), 0, 0.2))
            # scale decorations
            deco_pic = self.decorations[0].get_sprite()
            self.decorations[0].set_sprite(pygame.transform.scale(deco_pic, (deco_pic.get_width() * 4, deco_pic.get_height() * 4)))
            # set positions of all parts of menu
            self.buttons[0].set_pos([-25, 3])
            self.decorations[0].set_pos([740, 5])
            # draw all parts of menu
            self.buttons[0].draw()
            self.decorations[0].draw()
        elif self.menu == "playhungry":
            # add all parts of the menu
            self.add_button("buttonpause")
            self.add_decoration("hunger")
            # scale the buttons
            # TODO: do the scales
        elif self.menu == "playmain":
            self.add_button("buttonpause")
            self.add_decoration("thirst")
            self.add_decoration("hunger")
            # TODO: place all in correct place
        else:
            pass

    def get_menu(self):
        """
        Returns the type of menu that this menu is
        :return: self.menu
        """
        return self.menu

    def set_menu(self, menu):
        """
        Sets the type of menu to the specified menu
        :param menu: The specified new menu
        :return: None
        """
        self.menu = menu

    def get_buttons(self):
        """
        Returns the self.buttons array
        :return: self.buttons
        """
        return self.buttons

    def add_button(self, button):
        """
        Adds a button to self.buttons
        :param button: Function of the new button
        :return: None
        """
        self.buttons.append(Interactable(button, button, self.surface))

    def get_decorations(self):
        """
        Returns the self.decorations array
        :return: self.decorations
        """
        return self.decorations

    def add_decoration(self, decoration):
        """
        Adds an instance of the decoratives class to self.decorations
        :param decoration: Type of new decoration
        :return: None
        """
        self.decorations.append(Decorative(decoration, self.surface))

    def get_text(self):
        """
        Returns the self.text array
        :return: self.text
        """
        return self.text

    def add_text(self):
        """
        Adds an instance of the Text class to self.text
        :return: None
        """
        self.text.append(Text(self.surface))


class Item:
    def __init__(self, surface):
        self.sprite = ""
        self.position = [0, 0]
        self.surface = surface

    def __str__(self):
        """
        Prints all the information for the class in a readable format
        :return: All attributes of the class
        """
        return "ITEM CLASS - \nSprite: " + str(self.sprite) + "\nPosition: " + str(self.position)

    def draw(self):
        """
        Draws the Item onto the screen, onto a certain surface, in a certain position
        :return: None
        """
        self.surface.blit(self.sprite, self.position)

    def format_image(self, image):
        """
        Takes a string and changes it into a file path for loading with pygame.image.load
        :return: image file path
        """
        if "button" not in image:
            return "assets/" + image + ".png"
        ends = ["cat", "dog"]
        return "assets/" + image + random.choice(ends) + ".png"

    def get_sprite(self):
        """
        Returns the value of self.sprite
        :return: self.sprite
        """
        return self.sprite

    def set_sprite(self, sprite):
        """
        Changes the display sprite for an Item
        :param sprite: The new sprite for the Item to be changed to
        :return: None
        """
        self.sprite = sprite

    def set_pos(self, pos):
        """
        Changes the position of an Item
        :param pos: The new position
        :return: None
        """
        self.position = pos

    def set_xpos(self, pos):
        """
        Changes the x position of the Item
        :param pos: x position
        :return: None
        """
        self.position[0] = pos

    def set_ypos(self, pos):
        """
        Changes the y position of the Item
        :param pos: y position
        :return: None
        """
        self.position[1] = pos

    def get_pos(self):
        """
        Returns the position of the Item i.e. self.position
        :return: The Item's position
        """
        return self.position

    def clicked(self, pos):
        """
        Runs whenever an Item is clicked on. Defaults to be empty
        :return: None
        """


class Pet(Item):
    def __init__(self, name, animal, surface):
        super().__init__(surface)
        self.name = name
        self.animal = animal
        self.sprite = pygame.image.load(self.format_image(self.animal))
        self.stats = {"happiness": 0, "hunger": 0, "comfort": 0, "anger": 0, "thirst": 0, "energy": 0}
        self.emotion = "happy"
        self.times = []

    def __str__(self):
        """
        Prints all the information for the class in a readable format
        :return: All attributes of the class
        """
        return "PET CLASS - \nSprite: " + str(self.sprite) + "\nPosition: " + str(self.position) + "\nName: " + str(self.name) + "\nAnimal: " + str(self.animal) + "\nStats: " + str(self.stats) + "\nEmotion: " + str(self.emotion) + "\nTimes: " + str(self.times)

    def move(self, pos):
        """
        Moves the Pet to a specified position
        :param pos: Specified position
        :return: None
        """

    def change_emotion(self):
        """
        Decides what emotion the pet should be in based on their statistics
        :return: The new emotion
        """

    def process_emotion(self):
        """
        Does all of the things that need to be done upon an emotion change
        :return: None
        """

    def sleep(self):
        """
        Causes the pet to sleep
        :return: None
        """

    def clicked(self, pos):
        """
        Runs the chosen functions whenever the object is clicked,
        :return: None
        """

    def get_times(self):
        """
        Gets all of the repeated times with all information related to them
        :return: self.times array
        """
        return self.times

    def add_time(self, index, time):
        """
        Adds a new repeated time to a specific index of the self.times array
        :param index: The specified index
        :param time: The time to be added
        :return: None
        """
        self.times[index].append(time)

    def remove_time(self, index):
        """
        Removes a specific repeated time/times
        :param index: The specified index
        :return: None
        """
        self.times.remove(index)

    def check_repeat(self):
        """
        Checks to see if actions are repeated every game tick
        :return: None
        """

    def set_time(self):
        """
        Sets the time of day to a specific value (used for restarting with an old pet)
        :return: None
        """

    def get_name(self):
        """
        Returns the name of the pet
        :return: self.name
        """
        return self.name

    def set_name(self, name):
        """
        Sets the name of the pet to the specified name
        :param name: The specified name
        :return: None
        """
        self.name = name

    def get_animal(self):
        """
        Returns the type of animal that the pet is
        :return: self.animal
        """
        return self.animal

    def set_animal(self, animal):
        """
        Sets the type of animal that the pet is
        :param animal: The specified animal
        :return: None
        """
        self.animal = animal

    def get_stat(self, stat):
        """
        Returns the value of the specified statistics
        :param stat: The specified statistic
        :return: self.stats[stat]
        """
        return self.stats[stat]

    def set_stat(self, stat, value):
        """
        Sets the value of a specific statistic in self.stats
        :param stat: The specified statistic
        :param value: The value to be set to
        :return: None
        """
        self.stats[stat] = value

    def get_emotion(self):
        """
        Returns the current emotion of the pet
        :return: self.emotion
        """
        return self.emotion

    def set_emotion(self, emotion):
        """
        Sets the emotion of the pet
        :param emotion: The new emotion
        :return: None
        """
        self.emotion = emotion


class Interactable(Item):
    def __init__(self, display, action, surface):
        super().__init__(surface)
        self.display = display
        self.action = action
        self.sprite = pygame.image.load(self.format_image(display))

    def __str__(self):
        """
        Prints all the information for the class in a readable format
        :return: All attributes of the class
        """
        return "INTERACTABLE CLASS - \nSprite: " + str(self.sprite) + "\nPosition: " + str(self.position) + "\nDisplay: " + str(self.display) + "\nAction: " + str(self.action)

    def clicked(self, pos):
        """
        Runs whenever an Interactable is clicked. Runs the desired function(s)
        :return: None
        """
        if self.action == "drink":
            game.get_pet(0).move(pos)
            game.get_pet(0).set_stat("thirst", 10)
            [game.remove_menu(i) for i in game.get_menus()]
            game.get_pet(0).process_emotion(game.get_pet(0).change_emotion())
        if self.action == "eat":
            game.get_pet(0).move(pos)
            game.get_pet(0).set_stat("hunger", 10)
            [game.remove_menu(i) for i in game.get_menus()]
            game.get_pet(0).process_emotion(game.get_pet(0).change_emotion())
        if "play" in self.action:
            if self.action == "playball":
                ball = True
        if "sprite" in self.action:
            if self.action == "catsprite":
                pass
            elif self.action == "dogsprite":
                pass
            elif self.action == "ducksprite":
                pass
            else:
                pass
            # TODO: include functionality for these
        if "button" in self.action:
            self.button(self.action)
        # TODO: add variables that hold information on what has been chosen in the starting menus

    def button(self, action):
        """
        Performs the desired action of a button
        :param action: The desired action
        :return: None
        """
        if action == "buttonpause":
            game.add_menu("pause")
            # TODO: paused = True
        elif action == "buttonplay":
            game.swap_startrun()
            [game.remove_menu(i) for i in game.get_menus()]
            game.add_menu("playscreen")
            game.add_clock()
            # TODO: set the clock time to the last time the user had
        elif action == "buttonnew":
            [game.remove_menu(i) for i in game.get_menus()]
            game.add_menu("petchoice")
            # TODO: create temp array of pet_info, but might have to create in add_menu()
        elif action == "buttonold":
            [game.remove_menu(i) for i in game.get_menus()]
            game.add_menu("oldpet")
        elif action == "buttonquit":
            game.swap_running()
        elif action == "buttonnext":
            [game.remove_menu(i) for i in game.get_menus()]
            game.add_menu("namepet")
        elif action == "buttondone":
            # TODO: send info about pet to DB
            self.button("buttonplay")
        elif action == "buttonresume":
            # TODO: paused = False
            self.button("buttonplay")
        elif action == "buttonback":
            [game.remove_menu(i) for i in game.get_menus()]
            game.add_menu("start")
        elif action == "buttonsettings":
            [game.remove_menu(i) for i in game.get_menus()]
            game.add_menu("settings")
        else:
            pass

    def get_display(self):
        """
        Returns self.display for the instance of Interactable
        :return: self.display
        """
        return self.display

    def set_display(self, display):
        """
        Sets self.display to the specified new display
        :param display: The specified new display
        :return: None
        """
        self.display = display

    def get_action(self):
        """
        Returns the action that the Interactable has
        :return: self.action
        """
        return self.action

    def set_action(self, action):
        """
        Sets self.action to the specified new action
        :param action: The specified new action
        :return: None
        """
        self.action = action


class Decorative(Item):
    def __init__(self, display, surface):
        super().__init__(surface)
        self.display = display
        self.sprite = pygame.image.load(self.format_image(display))

    def __str__(self):
        """
        Prints all the information for the class in a readable format
        :return: All attributes of the class
        """
        return "DECORATIVE CLASS - \nSprite: " + str(self.sprite) + "\nPosition: " + str(self.position) + "\nDisplay: " + str(self.display)

    def clicked(self, pos):
        """
        Runs whenever a Decorative is clicked. Runs the desired function(s)
        :return: None
        """

    def place_clock(self):
        """
        Draws the clock onto the screen for the player
        :return: None
        """

    def get_display(self):
        """
        Returns self.display for the Decorative
        :return: self.display
        """
        return self.display

    def set_display(self, display):
        """
        Sets the value of self.display to a specified new display
        :return: The specified new display
        """
        self.display = display


class Text(Item):
    def __init__(self, surface):
        super().__init__(surface)
        self.content = ""
        self.sprite = pygame.image.load(self.format_image("textbox"))

    def __str__(self):
        """
        Prints all the information for the class in a readable format
        :return: All attributes of the class
        """
        return "TEXT CLASS - \nSprite: " + str(self.sprite) + "\nPosition: " + str(self.position) + "\nContent: " + str(self.content)

    def clicked(self, pos):
        """
        Runs whenever a Text is clicked. Runs the desired function(s)
        :return: None
        """

    def get_content(self):
        """
        Returns self.content
        :return: self.content
        """
        return self.content

    def set_content(self, content):
        """
        Sets self.content to a specified new content
        :param content: The specified new content
        :return: None
        """
        self.content = content


game = Game()
