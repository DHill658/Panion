# virtual pet game/program

import pygame
from pygame.locals import *
import sys
import sqlite3
import random
import math
import ast


ALPHABET = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

WIDTH = 800
HEIGHT = 800

BED_START = [-190, -100]
BALL_START = [0, -70]
WATER_START = [280, -120]
FOOD_START = [450, -70]

FPS = 60


class Game:
    def __init__(self):
        self.running = False
        self.startrun = True
        self.paused = False
        self.interactables = []
        self.decorations = []
        self.pets = []
        self.menus = []
        self.clocks = []
        self.secs = 0
        self.mins = 0
        self.hours = 0
        self.text_active = False
        self.pet_data = ["", "cat"]
        self.MAIN_SURF = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Panion")
        pygame.display.set_icon(pygame.image.load("assets/icon.png"))

        pygame.init()
        self.startup()
        self.run()

    def __str__(self):
        """
        Prints all the information for the class in a readable format
        :return: All attributes within the class
        """
        return "GAME CLASS - \nRunning: " + str(self.running) + "\nInteractables: " + str(self.interactables) + "\nDecorations: " + str(self.decorations) + "\nPets: " + str(self.pets) + "\nMenus: " + str(self.menus) + "\nClocks: " + str(self.clocks)

    def clear_screen(self):
        """
        Clears the screen for new objects to be drawn
        :return: None
        """
        self.MAIN_SURF.fill((220, 200, 210))

    def redraw(self):
        """
        Redraws everything on the screen
        :return: None
        """
        self.clear_screen()
        [dm.draw() for dm in self.menus[0].get_decorations()]
        [b.draw() for b in self.menus[0].get_buttons()]
        [i.draw() for i in self.interactables]
        [d.draw() for d in self.decorations]
        [t.draw() for t in self.menus[0].get_text()]
        [p.draw() for p in self.pets]

    def menu(self, menu):
        """
        Creates an instance of Menu with specific buttons based on the type
        :param menu: the type of menu, which dictates the buttons within it
        :return: None
        """
        self.menus.append(Menu(menu, self.MAIN_SURF, self))

    def run(self):
        """
        Contains the main game loop
        :return: None
        """
        self.running = True
        # start the game clock
        self.add_clock()
        self.create_visual_clock()
        # main game loop
        while self.running:
            # check for events
            self.event_handler()
            # change real time to 'game time'
            self.correct_time()
            # try to change the time, won't change if game is paused
            try:
                exception = self.decorations[5]
                # if the minutes have changed
                if self.secs == 0:
                    # change the minutes to display the new minutes
                    mins = self.split(self.mins)
                    min1 = self.decorations[4]
                    min2 = self.decorations[5]
                    min1.set_display(mins[0])
                    min2.set_display(mins[1])
                    min1.set_sprite(pygame.image.load(min1.format_image(min1.get_display())))
                    min2.set_sprite(pygame.image.load(min2.format_image(min2.get_display())))
                    for z in range(4, 6):
                        deco = self.decorations[z].get_sprite()
                        self.decorations[z].set_sprite(pygame.transform.scale(deco, (deco.get_width() // 3, deco.get_height() // 3)))
                    [self.decorations[y].draw() for y in range(0, 6)]

                    # if the hours have changed
                    if self.mins == 0:
                        # change everything to display correctly
                        hours = self.split(self.hours)
                        hour1 = self.decorations[2]
                        hour2 = self.decorations[3]
                        min1 = self.decorations[4]
                        min2 = self.decorations[5]
                        hour1.set_display(hours[0])
                        hour2.set_display(hours[1])
                        min1.set_display(mins[0])
                        min2.set_display(mins[1])
                        hour1.set_sprite(pygame.image.load(hour1.format_image(hour1.get_display())))
                        hour2.set_sprite(pygame.image.load(hour2.format_image(hour2.get_display())))
                        min1.set_sprite(pygame.image.load(min1.format_image(min1.get_display())))
                        min2.set_sprite(pygame.image.load(min2.format_image(min2.get_display())))
                        for z in range(2, 6):
                            deco = self.decorations[z].get_sprite()
                            self.decorations[z].set_sprite(pygame.transform.scale(deco, (deco.get_width() // 3, deco.get_height() // 3)))
                        [self.decorations[y].draw() for y in range(0, 6)]

                if self.mins % 30 == 0 or self.mins == 0:
                    # check for emotion changes every thirty seconds
                    self.pets[0].process_emotion(self.pets[0].change_emotion())
                if self.mins == 0 and self.secs == 0:
                    # change all of these statistics every minute
                    self.pets[0].set_stat("hunger", self.pets[0].get_stat("hunger") - 1)
                    self.pets[0].set_stat("thirst", self.pets[0].get_stat("thirst") - 1)
                    self.pets[0].set_stat("energy", self.pets[0].get_stat("energy") - 1)

            # if paused, do nothing
            except IndexError:
                pass

            # checking for repeated actions
            for event in self.pets[0].get_times():
                # if the current time is the same and the event is locked in
                if (event[1] >= 2) and (self.hours == event[2][0]) and (self.mins == event[2][1]) and (self.secs - 17 <= event[2][2] <= self.secs + 17):
                    if event[0] == "eat":
                        food = self.menus[0].get_buttons()[3]
                        position = food.get_pos()
                        position = [position[0] + food.get_sprite().get_width(), position[1] + food.get_sprite().get_height()]
                        food.clicked(position)
                    elif event[0] == "drink":
                        drink = self.menus[0].get_buttons()[4]
                        position = drink.get_pos()
                        position = [position[0] + drink.get_sprite().get_width(), position[1] + drink.get_sprite().get_height()]
                        drink.clicked(position)
                    elif event[0] == "sleep":
                        bed = self.menus[0].get_buttons()[1]
                        position = bed.get_pos()
                        position = [position[0] + bed.get_sprite().get_width(), position[1] + bed.get_sprite().get_height()]
                        bed.clicked(position)

            self.clocks[0].tick(FPS)

            pygame.display.update()
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
        self.menu("start")
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
                # end the program
                self.end()
            # if the mouse is clicked (on the up of the click)
            elif event.type == MOUSEBUTTONUP:
                none_clicked = True
                # if a text box is active
                if self.text_active:
                    # de-activate the text box
                    self.text_active = False
                    if self.menus[0].get_text():
                        sprite = pygame.image.load(self.menus[0].get_text()[0].format_image("textbox"))
                        self.menus[0].get_text()[0].set_sprite(pygame.transform.scale(sprite, (int(sprite.get_width() * 0.75), int(sprite.get_height() * 0.75))))
                        self.redraw()
                        self.menus[0].get_text()[0].text_render()
                # for all text boxes in the current menu...
                for text in self.menus[0].get_text():
                    # create a rect at the same position as the text box
                    rect = text.get_sprite().get_rect().move(text.get_pos())
                    # check if the mouse is there
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        none_clicked = False
                        # if it is, run clicked() for the text box
                        text.clicked(pygame.mouse.get_pos())
                # for all the buttons in the current menu...
                for button in self.menus[0].get_buttons():
                    # create a rect at the same position as the button
                    rect = button.get_sprite().get_rect().move(button.get_pos())
                    # check if the mouse is there
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        none_clicked = False
                        # if it is, run clicked() for that button
                        button.clicked(pygame.mouse.get_pos())
                # for all the pets currently in use...
                for pet in self.pets:
                    # create a rect at their position
                    rect = pet.get_sprite().get_rect().move(pet.get_pos())
                    # check if the mouse is there
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        none_clicked = False
                        # if it is, run clicked() for that pet
                        pet.clicked(pygame.mouse.get_pos())
                if none_clicked and self.running:
                    if not self.pets[0].get_ball_active() and not self.paused:
                        self.pets[0].travel(pygame.mouse.get_pos())
                    elif not self.paused:
                        point = pygame.mouse.get_pos()
                        self.add_decoration("ball")
                        ball = self.decorations[len(self.decorations) - 1]
                        ball.set_sprite(pygame.transform.scale(ball.get_sprite(), (int(ball.get_sprite().get_width() * 2), int(ball.get_sprite().get_height() * 2))))
                        point_ball_c = [point[0] - ball.get_sprite().get_width()//2, point[1] - ball.get_sprite().get_height()//2]
                        ball.set_pos(point_ball_c)
                        ball.set_pos([ball.get_pos()[0], ball.get_pos()[1] - 70])
                        ball.draw()
                        pygame.display.update()
                        # drop the ball
                        while ball.get_pos() != list(point_ball_c):
                            ball.set_pos([ball.get_pos()[0], ball.get_pos()[1] + 7])
                            self.redraw()
                            pygame.display.update()
                        # move the pet to the ball and get the parameters used for that motion
                        reverse = self.pets[0].travel(point)
                        # flip the parameters
                        reverse = [-(reverse[0]) + WIDTH//2, -(reverse[1]) + HEIGHT//2]
                        # remove the ball
                        del self.decorations[len(self.decorations) - 1]
                        # change the pet's sprite to hold the ball
                        self.pets[0].set_sprite(pygame.image.load(self.pets[0].format_image(self.pets[0].get_animal() + "spriteball")))
                        self.redraw()
                        # return the pet to its original position
                        self.pets[0].travel(reverse)
                        # change the pet's sprite back to normal
                        self.pets[0].set_sprite(pygame.image.load(self.pets[0].format_image(self.pets[0].get_animal() + "sprite")))
                        self.redraw()

            # if a key is pressed
            elif event.type == KEYDOWN:
                # if a text box is active
                if self.text_active:
                    # if the letter is valid
                    if event.unicode in ALPHABET:
                        # add it to the text box's content
                        self.menus[0].get_text()[0].add_content(event.unicode)
                    # if the key is a backspace
                    elif event.key == K_BACKSPACE:
                        # remove a character
                        self.menus[0].get_text()[0].remove_content()
                        # redraw the screen
                        self.redraw()
                    # re-render the text
                    self.menus[0].get_text()[0].text_render()
                    # if the key pressed is escape
                    if event.key == K_ESCAPE:
                        # de-activate the text box
                        self.text_active = False
                        sprite = pygame.image.load(self.menus[0].get_text()[0].format_image("textbox"))
                        self.menus[0].get_text()[0].set_sprite(pygame.transform.scale(sprite, (int(sprite.get_width() * 0.75), int(sprite.get_height() * 0.75))))
                        self.redraw()
                        self.menus[0].get_text()[0].text_render()
                else:
                    if event.key == K_b and self.running and not self.paused:
                        self.menus[0].get_buttons()[2].clicked(pygame.mouse.get_pos())

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
            c.execute('UPDATE pets SET Happiness = ' + str(i.get_stat("happiness")) +
                      ', Hunger = ' + str(i.get_stat("hunger")) + ', Comfort = ' + str(i.get_stat("comfort")) + ', Anger = ' +
                      str(i.get_stat("hunger")) + ', Thirst = ' + str(i.get_stat("thirst")) + ', Energy = ' + str(i.get_stat("energy")) +
                      ', Hours = ' + str(self.correct_time()[0]) + ', Mins = ' + str(self.correct_time()[1]) + ', Secs = ' +
                      str(self.correct_time()[2]) + ', Times = "' + str(i.get_times()) + '" WHERE Name = "' + i.get_name() + '";')
        conn.commit()
        conn.close()
        # quit pygame
        pygame.quit()
        # quit the window
        sys.exit()

    @staticmethod
    def split(number):
        """
        Splits a one or two digit number into two separate numbers
        :param number: the given number
        :return: [num1, num2]
        """
        if number < 10:
            return [0, number]
        num1 = str(number)[0]
        num2 = str(number)[1]
        return [num1, num2]

    def create_visual_clock(self):
        """
        Creates the visual clock
        :return: None
        """
        # add the clock
        self.add_decoration("clock")
        deco = self.decorations[0].get_sprite()
        self.decorations[0].set_sprite(pygame.transform.scale(deco, (deco.get_width() // 2, deco.get_height() // 2)))
        self.decorations[0].set_pos([-40, 700])
        self.decorations[0].draw()
        self.add_decoration("colon")
        deco = self.decorations[1].get_sprite()
        self.decorations[1].set_sprite(pygame.transform.scale(deco, (deco.get_width() // 2, deco.get_height() // 2)))
        self.decorations[1].set_pos([100, 695])
        self.decorations[1].draw()
        # add the starting numbers on the clock
        hours = self.split(self.hours)
        mins = self.split(self.mins)
        [self.add_decoration(i) for i in hours]
        [self.add_decoration(x) for x in mins]
        for z in range(2, 6):
            deco = self.decorations[z].get_sprite()
            self.decorations[z].set_sprite(pygame.transform.scale(deco, (deco.get_width() // 3, deco.get_height() // 3)))
        self.decorations[2].set_pos([20, 715])
        self.decorations[3].set_pos([70, 715])
        self.decorations[4].set_pos([160, 715])
        self.decorations[5].set_pos([210, 715])
        [self.decorations[y].draw() for y in range(2, 6)]

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
        self.interactables.append(Interactable(display, action, self.MAIN_SURF, self))

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
    
    def get_decorations(self):
        """
        Returns self.decorations
        :return: self.decorations
        """
        return self.decorations

    def add_decoration(self, display):
        """
        Adds a new instance of the Decorative class to the array self.decorations
        :param display: What the Decorative is/what it looks like
        :return: None
        """
        self.decorations.append(Decorative(display, self.MAIN_SURF, self))

    def remove_decoration(self, index):
        """
        Removes a specific instance of Decorative class
        :param index: The desired instance
        :return: None
        """
        self.decorations.remove(index)

    def remove_decorations(self):
        """
        Clears self.decorations
        :return: None
        """
        self.decorations.clear()

    def get_pet(self, index):
        """
        Returns a specific instance of the Pet class
        :param index: The index of the desired instance
        :return: Instance of the Pet class
        """
        return self.pets[index]

    def get_pets(self):
        """
        Returns the whole of self.pets
        :return: self.pets
        """
        return self.pets

    def add_pet(self, name, animal):
        """
        Adds a new instance of the Pet class to the array self.pets
        :param name: Name of the pet
        :param animal: What animal the pet is
        :return: None
        """
        self.pets.append(Pet(name, animal, self.MAIN_SURF, self))

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

    def remove_menus(self):
        """
        Remove all instances of the Menu class
        :return: None
        """
        self.menus.clear()

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

    def get_time(self):
        """
        Returns [self.hours, self.mins, self.secs]
        :return: [self.hours, self.mins, self.secs]
        """
        return [self.hours, self.mins, self.secs]

    def set_time(self, time):
        """
        Sets the values of self.hours, self.mins, and self.secs
        :param time: array containing self.hours, self.mins, self.secs
        :return: None
        """
        self.hours = time[0]
        self.mins = time[1]
        self.secs = time[2]

    def set_running(self, boolean):
        """
        Sets the value of running to the given boolean
        :param boolean: Given boolean value
        :return: None
        """
        self.running = boolean

    def set_startrun(self, boolean):
        """
        Sets the value of startrun to the given boolean
        :param boolean: Given boolean value
        :return: None
        """
        self.startrun = boolean

    def get_surf(self):
        """
        Returns the surface that the Game class is using (MAIN_SURF)
        :return: self.MAIN_SURF
        """
        return self.MAIN_SURF

    def get_startrun(self):
        """
        Returns the startrun attribute
        :return: self.startrun
        """
        return self.startrun

    def get_running(self):
        """
        Returns the running attribute
        :return: self.running
        """
        return self.running

    def get_text_active(self):
        """
        Returns self.text_active
        :return: self.text_active
        """
        return self.text_active

    def set_text_active(self, boolean):
        """
        Sets the value of self.text_active to the given boolean
        :param boolean: the given boolean
        :return: None
        """
        self.text_active = boolean

    def get_pet_data(self):
        """
        Returns self.pet_data
        :return: self.pet_data
        """
        return self.pet_data

    def set_pet_data(self, index, value):
        """
        Sets the value of the given index in self.pet_data to the given value
        :param index: The given index
        :param value: The given value
        :return: None
        """
        self.pet_data[index] = value

    def swap_paused(self):
        """
        Swaps the value of self.paused
        :return: None
        """
        self.paused = not self.paused


class Menu:
    def __init__(self, menu, surface, game_inst):
        self.menu = menu
        self.buttons = []
        self.decorations = []
        self.text = []
        self.surface = surface
        self.game_inst = game_inst
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
            self.add_button("buttonhelp")
            # change the size of all the buttons
            for i in range(len(self.buttons)):
                button = self.buttons[i].get_sprite()
                self.buttons[i].set_sprite(pygame.transform.scale(button, (int(button.get_width() * 0.4), int(button.get_height() * 0.4))))
            # change the size of the logo
            deco = self.decorations[0].get_sprite()
            self.decorations[0].set_sprite(pygame.transform.scale(deco, (deco.get_width() // 2, deco.get_height() // 2)))
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
                button = self.buttons[i].get_sprite()
                self.buttons[i].set_sprite(pygame.transform.scale(button, (int(button.get_width() * 0.4), int(button.get_height() * 0.4))))
            # scaling the text box
            text = self.text[0].get_sprite()
            self.text[0].set_sprite(pygame.transform.scale(text, (int(text.get_width() * 0.75), int(text.get_height() * 0.75))))
            # set positions of all menu parts
            self.buttons[0].set_pos([100, 575])
            self.buttons[1].set_pos([400, 575])
            self.text[0].set_pos([WIDTH//2 - self.text[0].get_sprite().get_width()//2, HEIGHT//2])
            # drawing all parts of the menu
            self.game_inst.set_text_active(False)
            self.buttons[0].draw()
            self.buttons[1].draw()
            self.text[0].draw()
        elif self.menu == "petchoice":
            # add all parts of the menu
            self.add_decoration("choosepet")
            self.add_decoration("arrow")
            self.add_button("catsprite")
            self.add_button("dogsprite")
            self.add_button("ducksprite")
            self.add_button("buttonnext")
            # scaling of buttons
            button = self.buttons[3].get_sprite()
            self.buttons[3].set_sprite(pygame.transform.scale(button, (int(button.get_width() * 0.4), int(button.get_height() * 0.4))))
            # scaling the text
            deco = self.decorations[0].get_sprite()
            self.decorations[0].set_sprite(pygame.transform.scale(deco, (deco.get_width() // 2, deco.get_height() // 2)))
            # x value for centering buttons
            x = WIDTH//2 - self.buttons[3].get_sprite().get_width()//2
            # set positions of all menu parts
            self.decorations[0].set_pos([WIDTH//2 - self.decorations[0].get_sprite().get_width()//2, 60])
            self.decorations[1].set_pos([WIDTH//4 - self.decorations[1].get_sprite().get_width()//2 - 19, 175])
            self.buttons[0].set_pos([WIDTH//4 - self.buttons[0].get_sprite().get_width()//2, HEIGHT//2 - 55])
            self.buttons[1].set_pos([WIDTH//2 - self.buttons[1].get_sprite().get_width()//2, HEIGHT//2 - 20])
            self.buttons[2].set_pos([WIDTH - WIDTH//4 - self.buttons[0].get_sprite().get_width()//2, HEIGHT//2 - 40])
            self.buttons[3].set_pos([x, 600])
            # drawing all parts of the menu
            self.decorations[0].draw()
            self.decorations[1].draw()
            self.buttons[0].draw()
            self.buttons[1].draw()
            self.buttons[2].draw()
            self.buttons[3].draw()
        elif self.menu == "namepet":
            # add all parts of the menu
            self.add_decoration(self.game_inst.get_pet_data()[1] + "sprite")
            self.add_text()
            self.add_button("buttondone")
            # scale the buttons
            for i in range(len(self.buttons)):
                button = self.buttons[i].get_sprite()
                self.buttons[i].set_sprite(pygame.transform.scale(button, (int(button.get_width() * 0.4), int(button.get_height() * 0.4))))
            # scale text
            text = self.text[0].get_sprite()
            self.text[0].set_sprite(pygame.transform.scale(text, (int(text.get_width() * 0.75), int(text.get_height() * 0.75))))
            # set positions of all parts of menu
            self.buttons[0].set_pos([WIDTH//2 - self.buttons[0].get_sprite().get_width()//2, HEIGHT - 200])
            self.decorations[0].set_pos([WIDTH//2 - self.decorations[0].get_sprite().get_width()//2, HEIGHT - 550])
            self.text[0].set_pos([WIDTH//2 - self.text[0].get_sprite().get_width()//2, HEIGHT - (300 + self.text[0].get_sprite().get_height()//2)])
            # draw all parts of menu
            self.buttons[0].draw()
            self.decorations[0].draw()
            self.text[0].draw()
        elif self.menu == "pause":
            # add all parts of the menu
            self.add_decoration("paused")
            self.add_button("buttonresume")
            self.add_button("buttonhelp")
            self.add_button("buttonquit")
            # scale the buttons
            for i in range(len(self.buttons)):
                button = self.buttons[i].get_sprite()
                self.buttons[i].set_sprite(pygame.transform.scale(button, (int(button.get_width() * 0.4), int(button.get_height() * 0.4))))
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
        elif self.menu == "help":
            # add all parts of menu
            self.add_decoration("help")
            self.add_decoration("helptext")
            self.add_button("buttondone")
            # scale the buttons
            for i in self.buttons:
                i.set_sprite(pygame.transform.scale(i.get_sprite(), (int(i.get_sprite().get_width() * 0.4), int(i.get_sprite().get_height() * 0.4))))
            # scale help text
            deco = self.decorations[0].get_sprite()
            self.decorations[0].set_sprite(pygame.transform.scale(deco, (int(deco.get_width() * 0.4), int(deco.get_height() * 0.4))))
            deco = self.decorations[1].get_sprite()
            self.decorations[1].set_sprite(pygame.transform.scale(deco, (int(deco.get_width() * 0.25), int(deco.get_height() * 0.25))))
            # set positions of all parts of menu
            self.decorations[0].set_pos([WIDTH//2 - self.decorations[0].get_sprite().get_width()//2, 20])
            self.decorations[1].set_pos([WIDTH//2 - self.decorations[1].get_sprite().get_width()//2, 100])
            self.buttons[0].set_pos([WIDTH//2 - self.buttons[0].get_sprite().get_width()//2, 600])
            # draw all parts of menu
            self.decorations[0].draw()
            self.decorations[1].draw()
            self.buttons[0].draw()
        elif self.menu == "playscreen":
            # add all parts of menu
            self.add_decoration("background")
            self.add_button("buttonpause")
            self.add_button("bed")
            self.add_button("ball")
            self.add_button("foodbowl")
            self.add_button("watertank")
            # scale everything
            deco = self.decorations[0].get_sprite()
            self.decorations[0].set_sprite(pygame.transform.scale(deco, (int(deco.get_width() * 0.75), int(deco.get_height() * 0.75))))
            button = self.buttons[0].get_sprite()
            self.buttons[0].set_sprite(pygame.transform.scale(button, (int(button.get_width() * 0.2), int(button.get_height() * 0.2))))
            bed = self.buttons[1].get_sprite()
            ball = self.buttons[2].get_sprite()
            food = self.buttons[3].get_sprite()
            water = self.buttons[4].get_sprite()
            self.buttons[1].set_sprite(pygame.transform.scale(bed, (int(bed.get_width() * 2), int(bed.get_height() * 2))))
            self.buttons[2].set_sprite(pygame.transform.scale(ball, (int(ball.get_width() * 2), int(ball.get_height() * 2))))
            self.buttons[3].set_sprite(pygame.transform.scale(food, (int(food.get_width() * 4), int(food.get_height() * 4))))
            self.buttons[4].set_sprite(pygame.transform.scale(water, (int(water.get_width() * 4), int(water.get_height() * 4))))
            # set positions of all parts of menu
            self.decorations[0].set_pos([WIDTH//2 - self.decorations[0].get_sprite().get_width()//2, HEIGHT//2 - self.decorations[0].get_sprite().get_height()//2])
            self.buttons[0].set_pos([-25, 3])
            self.buttons[1].set_pos(BED_START)
            self.buttons[2].set_pos(BALL_START)
            self.buttons[3].set_pos(FOOD_START)
            self.buttons[4].set_pos(WATER_START)
            self.game_inst.get_pets()[0].set_pos([WIDTH//2 - self.game_inst.get_pets()[0].get_sprite().get_width()//2, HEIGHT//2 - self.game_inst.get_pets()[0].get_sprite().get_height()//2])
            # draw all parts of menu
            self.decorations[0].draw()
            [i.draw() for i in self.buttons]
            self.game_inst.get_pets()[0].draw()
        elif self.menu == "playthirst":
            # add all parts of menu
            self.add_decoration("background")
            self.add_button("buttonpause")
            self.add_decoration("thirst")
            self.add_button("bed")
            self.add_button("ball")
            self.add_button("foodbowl")
            self.add_button("watertank")
            # scale everything
            deco = self.decorations[0].get_sprite()
            self.decorations[0].set_sprite(pygame.transform.scale(deco, (int(deco.get_width() * 0.75), int(deco.get_height() * 0.75))))
            button = self.buttons[0].get_sprite()
            self.buttons[0].set_sprite(pygame.transform.scale(button, (int(button.get_width() * 0.2), int(button.get_height() * 0.2))))
            deco_pic = self.decorations[1].get_sprite()
            self.decorations[1].set_sprite(pygame.transform.scale(deco_pic, (deco_pic.get_width() * 4, deco_pic.get_height() * 4)))
            bed = self.buttons[1].get_sprite()
            ball = self.buttons[2].get_sprite()
            food = self.buttons[3].get_sprite()
            water = self.buttons[4].get_sprite()
            self.buttons[1].set_sprite(pygame.transform.scale(bed, (int(bed.get_width() * 2), int(bed.get_height() * 2))))
            self.buttons[2].set_sprite(pygame.transform.scale(ball, (int(ball.get_width() * 2), int(ball.get_height() * 2))))
            self.buttons[3].set_sprite(pygame.transform.scale(food, (int(food.get_width() * 4), int(food.get_height() * 4))))
            self.buttons[4].set_sprite(pygame.transform.scale(water, (int(water.get_width() * 4), int(water.get_height() * 4))))
            # set positions of all parts of menu
            self.decorations[0].set_pos([WIDTH // 2 - self.decorations[0].get_sprite().get_width() // 2, HEIGHT // 2 - self.decorations[0].get_sprite().get_height() // 2])
            self.decorations[1].set_pos([740, 5])
            self.buttons[0].set_pos([-25, 3])
            self.buttons[1].set_pos(BED_START)
            self.buttons[2].set_pos(BALL_START)
            self.buttons[3].set_pos(FOOD_START)
            self.buttons[4].set_pos(WATER_START)
            self.game_inst.get_pets()[0].set_pos([WIDTH // 2 - self.game_inst.get_pets()[0].get_sprite().get_width() // 2, HEIGHT // 2 - self.game_inst.get_pets()[0].get_sprite().get_height() // 2])
            # draw all parts of menu
            self.decorations[0].draw()
            self.decorations[1].draw()
            [i.draw() for i in self.buttons]
            self.game_inst.get_pets()[0].draw()
        elif self.menu == "playhungry":
            # add all parts of the menu
            self.add_decoration("background")
            self.add_button("buttonpause")
            self.add_decoration("hunger")
            self.add_button("bed")
            self.add_button("ball")
            self.add_button("foodbowl")
            self.add_button("watertank")
            # scale everything
            deco = self.decorations[0].get_sprite()
            self.decorations[0].set_sprite(pygame.transform.scale(deco, (int(deco.get_width() * 0.75), int(deco.get_height() * 0.75))))
            button = self.buttons[0].get_sprite()
            self.buttons[0].set_sprite(pygame.transform.scale(button, (int(button.get_width() * 0.2), int(button.get_height() * 0.2))))
            deco_pic = self.decorations[1].get_sprite()
            self.decorations[1].set_sprite(pygame.transform.scale(deco_pic, (deco_pic.get_width() * 5, deco_pic.get_height() * 5)))
            bed = self.buttons[1].get_sprite()
            ball = self.buttons[2].get_sprite()
            food = self.buttons[3].get_sprite()
            water = self.buttons[4].get_sprite()
            self.buttons[1].set_sprite(pygame.transform.scale(bed, (int(bed.get_width() * 2), int(bed.get_height() * 2))))
            self.buttons[2].set_sprite(pygame.transform.scale(ball, (int(ball.get_width() * 2), int(ball.get_height() * 2))))
            self.buttons[3].set_sprite(pygame.transform.scale(food, (int(food.get_width() * 4), int(food.get_height() * 4))))
            self.buttons[4].set_sprite(pygame.transform.scale(water, (int(water.get_width() * 4), int(water.get_height() * 4))))
            # set positions for all parts of menu
            self.decorations[0].set_pos([WIDTH // 2 - self.decorations[0].get_sprite().get_width() // 2, HEIGHT // 2 - self.decorations[0].get_sprite().get_height() // 2])
            self.decorations[1].set_pos([720, 5])
            self.buttons[0].set_pos([-25, 3])
            self.buttons[1].set_pos(BED_START)
            self.buttons[2].set_pos(BALL_START)
            self.buttons[3].set_pos(FOOD_START)
            self.buttons[4].set_pos(WATER_START)
            self.game_inst.get_pets()[0].set_pos([WIDTH // 2 - self.game_inst.get_pets()[0].get_sprite().get_width() // 2, HEIGHT // 2 - self.game_inst.get_pets()[0].get_sprite().get_height() // 2])
            # draw all parts of menu
            self.decorations[0].draw()
            self.decorations[1].draw()
            [i.draw() for i in self.buttons]
            self.game_inst.get_pets()[0].draw()
        elif self.menu == "playmaln":
            # add all parts of the menu
            self.add_decoration("background")
            self.add_button("buttonpause")
            self.add_decoration("thirst")
            self.add_decoration("hunger")
            self.add_button("bed")
            self.add_button("ball")
            self.add_button("foodbowl")
            self.add_button("watertank")
            # scale the buttons
            button = self.buttons[0].get_sprite()
            self.buttons[0].set_sprite(pygame.transform.scale(button, (int(button.get_width() * 0.2), int(button.get_height() * 0.2))))
            # scale the decorations
            deco = self.decorations[0].get_sprite()
            self.decorations[0].set_sprite(pygame.transform.scale(deco, (int(deco.get_width() * 0.75), int(deco.get_height() * 0.75))))
            deco_pic1 = self.decorations[1].get_sprite()
            deco_pic2 = self.decorations[2].get_sprite()
            self.decorations[1].set_sprite(pygame.transform.scale(deco_pic1, (deco_pic1.get_width() * 4, deco_pic1.get_height() * 4)))
            self.decorations[2].set_sprite(pygame.transform.scale(deco_pic2, (deco_pic2.get_width() * 5, deco_pic2.get_height() * 5)))
            bed = self.buttons[1].get_sprite()
            ball = self.buttons[2].get_sprite()
            food = self.buttons[3].get_sprite()
            water = self.buttons[4].get_sprite()
            self.buttons[1].set_sprite(pygame.transform.scale(bed, (int(bed.get_width() * 2), int(bed.get_height() * 2))))
            self.buttons[2].set_sprite(pygame.transform.scale(ball, (int(ball.get_width() * 2), int(ball.get_height() * 2))))
            self.buttons[3].set_sprite(pygame.transform.scale(food, (int(food.get_width() * 4), int(food.get_height() * 4))))
            self.buttons[4].set_sprite(pygame.transform.scale(water, (int(water.get_width() * 4), int(water.get_height() * 4))))
            # set positions for all parts of menu
            self.decorations[0].set_pos([WIDTH // 2 - self.decorations[0].get_sprite().get_width() // 2, HEIGHT // 2 - self.decorations[0].get_sprite().get_height() // 2])
            self.buttons[0].set_pos([-25, 3])
            self.decorations[1].set_pos([740, 5])
            self.decorations[2].set_pos([670, 1])
            self.buttons[1].set_pos(BED_START)
            self.buttons[2].set_pos(BALL_START)
            self.buttons[3].set_pos(FOOD_START)
            self.buttons[4].set_pos(WATER_START)
            # draw all parts of menu
            self.buttons[0].draw()
            self.decorations[0].draw()
            self.decorations[1].draw()
            self.decorations[2].draw()
            [i.draw() for i in self.buttons]
            self.game_inst.get_pets()[0].draw()

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
        self.buttons.append(Interactable(button, button, self.surface, self.game_inst))

    def get_decorations(self):
        """
        Returns the self.decorations array
        :return: self.decorations
        """
        return self.decorations

    def add_decoration(self, decoration):
        """
        Adds an instance of the decorations class to self.decorations
        :param decoration: Type of new decoration
        :return: None
        """
        self.decorations.append(Decorative(decoration, self.surface, self.game_inst))

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
        self.text.append(Text(self.surface, self.game_inst))


class Item:
    def __init__(self, surface, game_inst):
        self.sprite = ""
        self.position = [0, 0]
        self.surface = surface
        self.game_inst = game_inst

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
        # if not a button...
        if "button" not in str(image):
            # return with a normal path
            return "assets/" + str(image) + ".png"
        # if there are no current pets
        if not self.game_inst.get_pets():
            # random button
            ends = ["cat", "dog", "duck"]
            return "assets/" + str(image) + random.choice(ends) + ".png"
        # if there is a current pet, use this pet's buttons
        return "assets/" + str(image) + str(self.game_inst.get_pet(0).get_animal()) + ".png"

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
    def __init__(self, name, animal, surface, game_inst):
        super().__init__(surface, game_inst)
        self.name = name
        self.animal = animal
        self.sprite = pygame.image.load(self.format_image(self.animal + "sprite"))
        self.stats = {"happiness": 5, "hunger": 5, "comfort": 5, "anger": 5, "thirst": 5, "energy": 5}
        self.emotion = "happy"
        self.times = []

        self.pause_time = [7, 0, 0]

        self.ball_active = False

    def __str__(self):
        """
        Prints all the information for the class in a readable format
        :return: All attributes of the class
        """
        return "PET CLASS - \nSprite: " + str(self.sprite) + "\nPosition: " + str(self.position) + "\nName: " + str(self.name) + "\nAnimal: " + str(self.animal) + "\nStats: " + str(self.stats) + "\nEmotion: " + str(self.emotion) + "\nTimes: " + str(self.times)

    def travel(self, pos):
        """
        Moves the Pet to a specified position
        :param pos: Specified position
        :return: [x, y]
        """
        # gets the difference between the coords of the pet and the mouse
        x = pos[0] - WIDTH//2
        y = pos[1] - HEIGHT//2
        background = self.game_inst.get_menus()[0].get_decorations()[0]
        buttons = self.game_inst.get_menus()[0].get_buttons()
        # gets the angle of travel
        angle = math.atan2(abs(y), abs(x))
        # gets the x value of a triangle of hypotenuse 1 and angle 'angle'
        xDiff = math.cos(angle)
        # gets the y value of a triangle of hypotenuse 1 and angle 'angle'
        yDiff = math.sin(angle)
        # gets the distance of travel
        distance = math.hypot(x, y)
        # flips the x or y if the mouse is 'behind' the pet in each direction
        if x < 0:
            xDiff = -xDiff
        if y < 0:
            yDiff = -yDiff

        # checks if the pet is at/past the edge and makes sure they are within the bounds
        if background.get_pos()[0] < -(background.get_sprite().get_width()-WIDTH//2):
            # right

            difference = -(background.get_sprite().get_width()-WIDTH//2) - background.get_pos()[0]
            background.set_pos([background.get_pos()[0] + difference, background.get_pos()[1]])
            for c in range(1, len(buttons)):
                buttons[c].set_pos([buttons[c].get_pos()[0] + difference, buttons[c].get_pos()[1]])

        if background.get_pos()[1] < -(background.get_sprite().get_height()-HEIGHT//2):
            # bottom

            difference = -(background.get_sprite().get_height()-HEIGHT//2) - background.get_pos()[1]
            background.set_pos([background.get_pos()[0], background.get_pos()[1] + difference])
            for c in range(1, len(buttons)):
                buttons[c].set_pos([buttons[c].get_pos()[0], buttons[c].get_pos()[1] + difference])

        if background.get_pos()[0] > WIDTH//2:
            # left

            difference = background.get_pos()[0] - WIDTH//2
            background.set_pos([background.get_pos()[0] - difference, background.get_pos()[1]])
            for c in range(1, len(buttons)):
                buttons[c].set_pos([buttons[c].get_pos()[0] - difference, buttons[c].get_pos()[1]])

        if background.get_pos()[1] > HEIGHT//2:
            # top
            # background.set_pos([background.get_pos()[0], background.get_pos()[1] - (yDiff // yDiff)])
            # for x in range(1, len(buttons)):
            #     buttons[x].set_pos([buttons[x].get_pos()[0], buttons[x].get_pos()[1]])
            # y_edge = True

            difference = background.get_pos()[1] - HEIGHT // 2
            background.set_pos([background.get_pos()[0], background.get_pos()[1] - difference])
            for c in range(1, len(buttons)):
                buttons[c].set_pos([buttons[c].get_pos()[0], buttons[c].get_pos()[1] - difference])

        # loops for the distance (divided by a factor)
        for a in range(int(distance)//20):

            # if the pet is within the bounds, move them
            if (WIDTH//2 >= background.get_pos()[0] >= -(background.get_sprite().get_width()-WIDTH//2)) and (HEIGHT//2 >= background.get_pos()[1] >= -(background.get_sprite().get_height()-HEIGHT//2)):
                # background.set_pos([background.get_pos()[0] - (xDiff * 20), background.get_pos()[1] - (yDiff * 20)])
                background.set_pos([background.get_pos()[0] - (xDiff * 20), background.get_pos()[1] - (yDiff * 20)])

                for d in range(1, len(buttons)):
                    buttons[d].set_pos([buttons[d].get_pos()[0] - (xDiff * 20), buttons[d].get_pos()[1] - (yDiff * 20)])

                if self.ball_active and len(self.game_inst.get_decorations()) >= 7:
                    ball = self.game_inst.get_decorations()[len(self.game_inst.get_decorations()) - 1]
                    ball.set_pos([ball.get_pos()[0] - (xDiff * 20), ball.get_pos()[1] - (yDiff * 20)])
            # redraw all parts of the screen
            self.game_inst.redraw()
            # update the display
            pygame.display.update()
        return [x, y]

    def change_emotion(self):
        """
        Decides what emotion the pet should be in based on their statistics
        :return: The new emotion
        """
        t_emotion = self.emotion
        if self.stats["thirst"] <= 3 and self.stats["hunger"] <= 3:
            t_emotion = "malnourished"
        elif self.stats["thirst"] <= 3:
            t_emotion = "thirsty"
        elif self.stats["hunger"] <= 3:
            t_emotion = "hungry"
        elif self.stats["energy"] <= 3:
            t_emotion = "tired"
        elif self.stats["anger"] <= 3:
            t_emotion = "angry"
        elif self.stats["comfort"] <= 3:
            t_emotion = "uncomfortable"
        elif self.stats["happiness"] <= 3:
            t_emotion = "unhappy"
        elif self.stats["happiness"] >= 6:
            t_emotion = "happy"
        else:
            t_emotion = "neutral"
        return t_emotion

    def process_emotion(self, emotion):
        """
        Does all of the things that need to be done upon an emotion change
        :return: None
        """
        # check which emotion is given, and perform the desired actions based on that
        if emotion == self.emotion:
            pass
        elif emotion == "malnourished":
            self.emotion = emotion
            back_pos = self.game_inst.get_menus()[0].get_decorations()[0].get_pos()
            inter_pos = []
            [inter_pos.append(x.get_pos()) for x in self.game_inst.get_menus()[0].get_buttons()]
            self.game_inst.remove_menus()
            self.game_inst.menu("playmaln")
            self.game_inst.get_menus()[0].get_decorations()[0].set_pos(back_pos)
            [self.game_inst.get_menus()[0].get_buttons()[y].set_pos(inter_pos[y]) for y in range(len(self.game_inst.get_menus()[0].get_buttons()))]
            self.game_inst.redraw()
        elif emotion == "thirsty":
            self.emotion = emotion
            back_pos = self.game_inst.get_menus()[0].get_decorations()[0].get_pos()
            inter_pos = []
            [inter_pos.append(x.get_pos()) for x in self.game_inst.get_menus()[0].get_buttons()]
            self.game_inst.remove_menus()
            self.game_inst.menu("playthirst")
            self.game_inst.get_menus()[0].get_decorations()[0].set_pos(back_pos)
            [self.game_inst.get_menus()[0].get_buttons()[y].set_pos(inter_pos[y]) for y in range(len(self.game_inst.get_menus()[0].get_buttons()))]
            self.game_inst.redraw()
        elif emotion == "hungry":
            self.emotion = emotion
            back_pos = self.game_inst.get_menus()[0].get_decorations()[0].get_pos()
            inter_pos = []
            [inter_pos.append(x.get_pos()) for x in self.game_inst.get_menus()[0].get_buttons()]
            self.game_inst.remove_menus()
            self.game_inst.menu("playhungry")
            self.game_inst.get_menus()[0].get_decorations()[0].set_pos(back_pos)
            [self.game_inst.get_menus()[0].get_buttons()[y].set_pos(inter_pos[y]) for y in range(len(self.game_inst.get_menus()[0].get_buttons()))]
            self.game_inst.redraw()
        elif emotion == "tired":
            self.emotion = emotion
            back_pos = self.game_inst.get_menus()[0].get_decorations()[0].get_pos()
            inter_pos = []
            [inter_pos.append(x.get_pos()) for x in self.game_inst.get_menus()[0].get_buttons()]
            self.game_inst.remove_menus()
            self.game_inst.menu("playscreen")
            self.game_inst.get_menus()[0].get_decorations()[0].set_pos(back_pos)
            [self.game_inst.get_menus()[0].get_buttons()[y].set_pos(inter_pos[y]) for y in range(len(self.game_inst.get_menus()[0].get_buttons()))]
            self.sprite = pygame.image.load(self.format_image(self.animal + "spritetired"))
            self.game_inst.redraw()
        elif emotion == "angry":
            self.emotion = emotion
            back_pos = self.game_inst.get_menus()[0].get_decorations()[0].get_pos()
            inter_pos = []
            [inter_pos.append(x.get_pos()) for x in self.game_inst.get_menus()[0].get_buttons()]
            self.game_inst.remove_menus()
            self.game_inst.menu("playscreen")
            self.game_inst.get_menus()[0].get_decorations()[0].set_pos(back_pos)
            [self.game_inst.get_menus()[0].get_buttons()[y].set_pos(inter_pos[y]) for y in range(len(self.game_inst.get_menus()[0].get_buttons()))]
            self.sprite = pygame.image.load(self.format_image(self.animal + "spriteangry"))
            self.game_inst.redraw()
        elif emotion == "uncomfortable":
            self.emotion = emotion
            back_pos = self.game_inst.get_menus()[0].get_decorations()[0].get_pos()
            inter_pos = []
            [inter_pos.append(x.get_pos()) for x in self.game_inst.get_menus()[0].get_buttons()]
            self.game_inst.remove_menus()
            self.game_inst.menu("playscreen")
            self.game_inst.get_menus()[0].get_decorations()[0].set_pos(back_pos)
            [self.game_inst.get_menus()[0].get_buttons()[y].set_pos(inter_pos[y]) for y in range(len(self.game_inst.get_menus()[0].get_buttons()))]
            self.sprite = pygame.image.load(self.format_image(self.animal + "spriteuncomfortable"))
            self.game_inst.redraw()
        elif emotion == "unhappy":
            self.emotion = emotion
            back_pos = self.game_inst.get_menus()[0].get_decorations()[0].get_pos()
            inter_pos = []
            [inter_pos.append(x.get_pos()) for x in self.game_inst.get_menus()[0].get_buttons()]
            self.game_inst.remove_menus()
            self.game_inst.menu("playscreen")
            self.game_inst.get_menus()[0].get_decorations()[0].set_pos(back_pos)
            [self.game_inst.get_menus()[0].get_buttons()[y].set_pos(inter_pos[y]) for y in range(len(self.game_inst.get_menus()[0].get_buttons()))]
            self.sprite = pygame.image.load(self.format_image(self.animal + "spriteunhappy"))
            self.game_inst.redraw()
        elif emotion == "happy":
            self.emotion = emotion
            back_pos = self.game_inst.get_menus()[0].get_decorations()[0].get_pos()
            inter_pos = []
            [inter_pos.append(x.get_pos()) for x in self.game_inst.get_menus()[0].get_buttons()]
            self.game_inst.remove_menus()
            self.game_inst.menu("playscreen")
            self.game_inst.get_menus()[0].get_decorations()[0].set_pos(back_pos)
            [self.game_inst.get_menus()[0].get_buttons()[y].set_pos(inter_pos[y]) for y in range(len(self.game_inst.get_menus()[0].get_buttons()))]
            self.sprite = pygame.image.load(self.format_image(self.animal + "spritehappy"))
            self.game_inst.redraw()
        elif emotion == "neutral":
            self.emotion = emotion
            back_pos = self.game_inst.get_menus()[0].get_decorations()[0].get_pos()
            inter_pos = []
            [inter_pos.append(x.get_pos()) for x in self.game_inst.get_menus()[0].get_buttons()]
            self.game_inst.remove_menus()
            self.game_inst.menu("playscreen")
            self.game_inst.get_menus()[0].get_decorations()[0].set_pos(back_pos)
            [self.game_inst.get_menus()[0].get_buttons()[y].set_pos(inter_pos[y]) for y in range(len(self.game_inst.get_menus()[0].get_buttons()))]
            self.sprite = pygame.image.load(self.format_image(self.animal + "sprite"))
            self.game_inst.redraw()

    def sleep(self):
        """
        Causes the pet to sleep
        :return: None
        """
        # change the pet to 'sleeping'
        self.sprite = pygame.image.load(self.format_image(self.animal + "spritesleep"))
        # set the pet's energy to 10
        self.set_stat("energy", 10)
        # change the background to night time
        self.game_inst.get_menus()[0].get_decorations()[0].set_sprite(pygame.image.load(self.format_image("backgroundnight")))
        deco = self.game_inst.get_menus()[0].get_decorations()[0].get_sprite()
        self.game_inst.get_menus()[0].get_decorations()[0].set_sprite(pygame.transform.scale(deco, (int(deco.get_width() * 0.75), int(deco.get_height() * 0.75))))
        # create a dark cover to dim the display
        dark = pygame.Surface((WIDTH, HEIGHT))
        dark.fill(0)
        dark.set_alpha(100)
        self.game_inst.redraw()
        self.surface.blit(dark, (0, 0))
        pygame.display.update()
        # wait 3.5 seconds
        pygame.time.delay(3500)
        # change sprite and background back to normal and redraw (also gets rid of tint)
        self.sprite = pygame.image.load(self.format_image(self.animal + "sprite"))
        self.game_inst.get_menus()[0].get_decorations()[0].set_sprite(pygame.image.load(self.format_image("background")))
        deco = self.game_inst.get_menus()[0].get_decorations()[0].get_sprite()
        self.game_inst.get_menus()[0].get_decorations()[0].set_sprite(pygame.transform.scale(deco, (int(deco.get_width() * 0.75), int(deco.get_height() * 0.75))))
        # set the time to 7:00 am
        self.game_inst.set_time([6, 59, 980])
        self.game_inst.redraw()
        pygame.display.update()

    def clicked(self, pos):
        """
        Runs the chosen functions whenever the object is clicked,
        :return: None
        """
        # set the sprite to the 'petting' sprite
        self.set_sprite(pygame.image.load(self.format_image(self.animal + "spritepetting")))
        self.game_inst.redraw()
        pygame.display.update()
        # wait for half a second
        pygame.time.delay(500)
        # add 1 to happiness stat
        self.set_stat("happiness", self.get_stat("happiness") + 1)
        # change back to the current emotion
        self.set_sprite(pygame.image.load(self.format_image(self.animal + "sprite")))
        self.process_emotion(self.change_emotion())
        self.game_inst.redraw()
        pygame.display.update()

    def get_times(self):
        """
        Gets all of the repeated times with all information related to them
        :return: self.times array
        """
        return self.times

    def set_times(self, times):
        """
        Sets the value of self.times to a given value
        :return: None
        """
        self.times = times

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

    def check_repeat(self, time, action):
        """
        Checks to see if actions are repeated every game tick
        :return: None
        """
        done = False
        # checking all of the previous actions
        for event in self.times:
            # if the action is the same, the counter has 2 or less events, and at least one time
            if event[0] == action and event[1] == 1:
                # if the given time is within 15 mins either side of the previous action(s)
                if time[0] == event[2][0] and (event[2][1] - 5) <= time[1] <= (event[2][1] + 5):
                    # add the time
                    event.append(time)
                    # add to the counter
                    event[1] += 1
                    done = True
                # if the event is old and has not repeated
                else:
                    # remove it
                    self.times.remove(event)
        # if there are no matching events
        if not done:
            # add it to the list
            self.times.append([action, 1, time])

    def set_time(self, time):
        """
        Sets the time of day to a specific value (used for restarting with an old pet)
        :return: None
        """
        self.game_inst.set_time(time)

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
        if value <= 0:
            self.stats[stat] = 0
        elif value >= 10:
            self.stats[stat] = 10
        else:
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

    def set_ball_active(self, boolean):
        """
        Sets the value of self.ball_active
        :param boolean: boolean value to be set
        :return: None
        """
        self.ball_active = boolean

    def get_ball_active(self):
        """
        Returns the value of self.ball_active
        :return: self.ball_active
        """
        return self.ball_active

    def set_pause_time(self, value):
        """
        Sets self.pause_time to the given value
        :param value: the given value
        :return: None
        """
        self.pause_time = value

    def get_pause_time(self):
        """
        Returns self.pause_time
        :return: self.pause_time
        """
        return self.pause_time


class Interactable(Item):
    def __init__(self, display, action, surface, game_inst):
        super().__init__(surface, game_inst)
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
        if self.action == "watertank":
            # change the sprite to have a white outline to show activity
            self.set_sprite(pygame.image.load(self.format_image("watertankselected")))
            self.set_sprite(pygame.transform.scale(self.get_sprite(), (int(self.get_sprite().get_width() * 4), int(self.get_sprite().get_height() * 4))))
            self.game_inst.redraw()
            # go to the water
            self.game_inst.get_pet(0).travel(pos)
            # set thirst stat to full
            self.game_inst.get_pet(0).set_stat("thirst", 10)
            # change the sprite to be inactive again
            self.set_sprite(pygame.image.load(self.format_image("watertank")))
            self.set_sprite(pygame.transform.scale(self.get_sprite(), (int(self.get_sprite().get_width() * 4), int(self.get_sprite().get_height() * 4))))
            self.game_inst.redraw()
            # check for repeat actions
            self.game_inst.get_pet(0).check_repeat(self.game_inst.correct_time(), "drink")
            # change emotions
            self.game_inst.get_pet(0).process_emotion(self.game_inst.get_pet(0).change_emotion())
        if self.action == "foodbowl":
            # change the sprite to have a white outline to show activity
            self.set_sprite(pygame.image.load(self.format_image("foodbowlselected")))
            self.set_sprite(pygame.transform.scale(self.get_sprite(), (int(self.get_sprite().get_width() * 4), int(self.get_sprite().get_height() * 4))))
            self.game_inst.redraw()
            # go to the food
            self.game_inst.get_pet(0).travel(pos)
            # set hunger stat to full
            self.game_inst.get_pet(0).set_stat("hunger", 10)
            # change the sprite to be inactive again
            self.set_sprite(pygame.image.load(self.format_image("foodbowl")))
            self.set_sprite(pygame.transform.scale(self.get_sprite(), (int(self.get_sprite().get_width() * 4), int(self.get_sprite().get_height() * 4))))
            self.game_inst.redraw()
            # check for repeat actions
            self.game_inst.get_pet(0).check_repeat(self.game_inst.correct_time(), "eat")
            # change emotions
            self.game_inst.get_pet(0).process_emotion(self.game_inst.get_pet(0).change_emotion())
        if self.action == "bed":
            # change the sprite to have a white outline to show activity
            self.set_sprite(pygame.image.load(self.format_image("bedselected")))
            self.set_sprite(pygame.transform.scale(self.get_sprite(), (int(self.get_sprite().get_width() * 2), int(self.get_sprite().get_height() * 2))))
            self.game_inst.redraw()
            # go to bed
            self.game_inst.get_pet(0).travel(pos)
            # check for repeat actions
            self.game_inst.get_pet(0).check_repeat(self.game_inst.correct_time(), "sleep")
            # sleep
            self.game_inst.get_pet(0).sleep()
            # change the sprite to be inactive again
            self.set_sprite(pygame.image.load(self.format_image("bed")))
            self.set_sprite(pygame.transform.scale(self.get_sprite(), (int(self.get_sprite().get_width() * 2), int(self.get_sprite().get_height() * 2))))
            self.game_inst.redraw()
        if self.action == "ball":
            # swap 'ball_active'
            self.game_inst.get_pet(0).set_ball_active(not self.game_inst.get_pet(0).get_ball_active())
            # swap sprite between active and not
            if self.game_inst.get_pet(0).get_ball_active():
                self.set_sprite(pygame.image.load(self.format_image("ballselected")))
                self.set_sprite(pygame.transform.scale(self.get_sprite(), (int(self.get_sprite().get_width() * 2), int(self.get_sprite().get_height() * 2))))
                self.game_inst.redraw()
            else:
                self.set_sprite(pygame.image.load(self.format_image("ball")))
                self.set_sprite(pygame.transform.scale(self.get_sprite(), (int(self.get_sprite().get_width() * 2), int(self.get_sprite().get_height() * 2))))
                self.game_inst.redraw()
        # if a sprite is clicked
        if "sprite" in self.action:
            # if the main game is not running (i.e. if the pet is being selected)
            if not self.game_inst.get_running():
                if self.action == "catsprite":
                    # set the current pet to cat
                    self.game_inst.set_pet_data(1, "cat")
                    # place the arrow above the cat
                    arrow = self.game_inst.get_menus()[0].get_decorations()[1]
                    arrow.set_pos([WIDTH//4 - arrow.get_sprite().get_width()//2 - 19, 175])
                    arrow.draw()
                    self.game_inst.redraw()
                elif self.action == "dogsprite":
                    # set the current pet to dog
                    self.game_inst.set_pet_data(1, "dog")
                    # place the arrow above the dog
                    arrow = self.game_inst.get_menus()[0].get_decorations()[1]
                    arrow.set_pos([WIDTH // 2 - arrow.get_sprite().get_width() // 2, 175])
                    arrow.draw()
                    self.game_inst.redraw()
                elif self.action == "ducksprite":
                    # set the current pet to duck
                    self.game_inst.set_pet_data(1, "duck")
                    # place the arrow above the duck
                    arrow = self.game_inst.get_menus()[0].get_decorations()[1]
                    arrow.set_pos([WIDTH // 4 + WIDTH // 2 - arrow.get_sprite().get_width() // 2, 175])
                    arrow.draw()
                    self.game_inst.redraw()
                else:
                    pass
            else:
                pass
        if "button" in self.action:
            self.button(self.action)

    def button(self, action):
        """
        Performs the desired action of a button
        :param action: The desired action
        :return: None
        """
        if action == "buttonpause":
            self.game_inst.remove_menus()
            self.game_inst.clear_screen()
            self.game_inst.swap_paused()
            self.game_inst.get_pet(0).set_pause_time(self.game_inst.get_time())
            self.game_inst.remove_decorations()
            self.game_inst.menu("pause")
        elif action == "buttonplay":
            invalid = False
            # if there's no new pet
            if not self.game_inst.get_pet_data()[0]:
                # connect to the database
                conn = sqlite3.connect('pets.db')
                c = conn.cursor()
                names = c.execute('SELECT Name FROM pets;').fetchall()
                for n in range(len(names)):
                    names[n] = names[n][0]

                try:
                    # if the entered name is in the database
                    if self.game_inst.get_menus()[0].get_text()[0].get_content() in names:
                        # get all of that pet's data
                        data = c.execute('SELECT * FROM pets WHERE Name="' + self.game_inst.get_menus()[0].get_text()[0].get_content() + '";').fetchall()
                        # create an instance of Pet with that data
                        self.game_inst.add_pet(data[0][0], data[0][1])
                        self.game_inst.get_pet(0).set_stat("happiness", data[0][2])
                        self.game_inst.get_pet(0).set_stat("hunger", data[0][3])
                        self.game_inst.get_pet(0).set_stat("comfort", data[0][4])
                        self.game_inst.get_pet(0).set_stat("anger", data[0][5])
                        self.game_inst.get_pet(0).set_stat("thirst", data[0][6])
                        self.game_inst.get_pet(0).set_stat("energy", data[0][7])
                        self.game_inst.set_time([data[0][8], data[0][9], data[0][10]])
                        # changes the times list from a string (how it is stored in the db) to a list
                        fix_times = ast.literal_eval(data[0][11])
                        self.game_inst.get_pet(0).set_times(fix_times)
                        conn.close()
                    else:
                        # deletes old error messages
                        if self.game_inst.get_decorations():
                            self.game_inst.remove_decoration(self.game_inst.get_decoration(0))
                        # adds an error message
                        self.game_inst.add_decoration("inuse")
                        # scales, positions, and draws the error message
                        deco = self.game_inst.get_decoration(0)
                        deco.set_sprite(pygame.transform.scale(deco.get_sprite(), (int(deco.get_sprite().get_width() * 0.25), int(deco.get_sprite().get_height() * 0.25))))
                        deco.set_pos([WIDTH // 2 - deco.get_sprite().get_width() // 2, 20])
                        deco.set_pos([WIDTH // 2 - deco.get_sprite().get_width() // 2, 20])
                        deco.draw()
                        # redraws the screen, including the text in the text box
                        self.game_inst.redraw()
                        self.game_inst.get_menus()[0].get_text()[0].text_render()
                        invalid = True
                except IndexError:
                    invalid = True
                    self.game_inst.remove_menus()
                    self.game_inst.clear_screen()
                    pause_time = self.game_inst.get_pet(0).get_pause_time()
                    pause_time = [pause_time[0], pause_time[1], pause_time[2] - 20]
                    self.game_inst.set_time(pause_time)
                    self.game_inst.create_visual_clock()
                    self.game_inst.menu("playscreen")

            # valid pet name, so go!
            if not invalid:
                if self.game_inst.get_decorations():
                    self.game_inst.remove_decoration(self.game_inst.get_decoration(0))
                self.game_inst.set_startrun(False)
                self.game_inst.set_running(True)
                self.game_inst.remove_menus()
                self.game_inst.clear_screen()
                self.game_inst.menu("playscreen")
                self.game_inst.add_clock()
        elif action == "buttonnew":
            self.game_inst.remove_menus()
            self.game_inst.clear_screen()
            self.game_inst.menu("petchoice")
        elif action == "buttonold":
            self.game_inst.remove_menus()
            self.game_inst.clear_screen()
            self.game_inst.menu("oldpet")
        elif action == "buttonquit":
            self.game_inst.set_running(False)
        elif action == "buttonnext":
            self.game_inst.remove_menus()
            self.game_inst.clear_screen()
            self.game_inst.menu("namepet")
        elif action == "buttondone":
            # if the game was already running
            if self.game_inst.get_running():
                # go back to the normal game
                self.button("buttonplay")
            # in the start menu
            else:
                # if there's a text box (i.e. are currently naming pet)
                if self.game_inst.get_menus()[0].get_text():
                    # set the pet's name to the currently entered one
                    name = self.game_inst.get_menus()[0].get_text()[0].get_content()
                    self.game_inst.set_pet_data(0, name)
                    # connect to the database
                    conn = sqlite3.connect('pets.db')
                    # create a cursor within the db
                    c = conn.cursor()
                    # get all names from the database
                    names = c.execute('SELECT Name FROM pets;').fetchall()
                    conn.close()
                    # format the names
                    for n in range(len(names)):
                        names[n] = names[n][0]
                    # if the chosen name has already been used
                    if self.game_inst.get_pet_data()[0] in names:
                        # deletes old error messages
                        if self.game_inst.get_decorations():
                            self.game_inst.remove_decoration(self.game_inst.get_decoration(0))
                        # adds an error message
                        self.game_inst.add_decoration("warning")
                        # scales, positions, and draws the error message
                        deco = self.game_inst.get_decoration(0)
                        deco.set_sprite(pygame.transform.scale(deco.get_sprite(), (int(deco.get_sprite().get_width() * 0.25), int(deco.get_sprite().get_height() * 0.25))))
                        deco.set_pos([WIDTH//2 - deco.get_sprite().get_width()//2, 20])
                        deco.draw()
                        # redraws the screen, including the text in the text box
                        self.game_inst.redraw()
                        self.game_inst.get_menus()[0].get_text()[0].text_render()
                    # if the chosen name has not already been used
                    else:
                        if self.game_inst.get_menus()[0].get_text()[0].get_content() != "":
                            # connect to the database
                            conn = sqlite3.connect('pets.db')
                            c = conn.cursor()
                            # add data as entry in database
                            c.execute('INSERT INTO pets VALUES ("' + self.game_inst.get_pet_data()[0] + '", "' + self.game_inst.get_pet_data()[1] +
                                      '", 5, 5, 5, 5, 5, 5, 0, 0, 0, "[]");')
                            conn.commit()
                            conn.close()
                            # start playing game
                            if self.game_inst.get_decorations():
                                self.game_inst.remove_decoration(self.game_inst.get_decoration(0))
                            self.game_inst.add_pet(self.game_inst.get_pet_data()[0], self.game_inst.get_pet_data()[1])
                            conn.close()
                            self.game_inst.get_pets()[0].draw()
                            self.button("buttonplay")
                # else on settings menu in beginning
                else:
                    # go back to start
                    self.game_inst.remove_menus()
                    self.game_inst.clear_screen()
                    self.game_inst.menu("start")
        elif action == "buttonresume":
            self.game_inst.swap_paused()
            self.game_inst.set_running(True)
            self.button("buttonplay")
        elif action == "buttonback":
            self.game_inst.remove_menus()
            self.game_inst.clear_screen()
            # deletes old error messages
            if self.game_inst.get_decorations():
                self.game_inst.remove_decoration(self.game_inst.get_decoration(0))
            self.game_inst.menu("start")
        elif action == "buttonhelp":
            self.game_inst.remove_menus()
            self.game_inst.clear_screen()
            self.game_inst.menu("help")

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
    def __init__(self, display, surface, game_inst):
        super().__init__(surface, game_inst)
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
    def __init__(self, surface, game_inst):
        super().__init__(surface, game_inst)
        self.content = ""
        self.font = pygame.font.Font(None, 72)
        self.TXT_SURFACE = self.font.render(self.content, True, pygame.Color("black"))
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
        self.game_inst.set_text_active(True)
        self.sprite = pygame.image.load(self.format_image("textboxactive"))
        self.sprite = pygame.transform.scale(self.sprite, (int(self.sprite.get_width() * 0.75), int(self.sprite.get_height() * 0.75)))
        self.game_inst.redraw()
        self.text_render()

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

    def add_content(self, content):
        """
        Appends characters to self.content
        :param content: content to be added
        :return: None
        """
        self.content += content
        if len(self.content) > 10:
            self.remove_content()

    def remove_content(self):
        """
        Removes a character from self.content
        :return: None
        """
        self.content = self.content[:-1]

    def text_render(self):
        """
        Re-renders the text
        :return: None
        """
        self.TXT_SURFACE = self.font.render(self.content, True, pygame.Color("black"))
        self.game_inst.get_surf().blit(self.TXT_SURFACE, (self.position[0] + 20, self.position[1] + 90))


game = Game()
