"""
Samuel Guttormson
Initial Upload Date: Jan 8th 2021

The following will generate evolving automaton using the pygame engine given a simple set of rules.
The main variables for the user to play with at this time are:

    Cell Grid Size: defined in creation of Automaton object

    The initial state: Three methods exist to determine initial state. These can create:
        - one live cell starting in the top middle of the grid,
        - one live cell starting in the middle of the grid,
        - random noise generating multiple live cells all over the grid, based on an intensity parameter.

    color_function(x, y): a mathematical function to determine cell colors

    rulesets(): a method called by update() that determines what the next state will look like based on the
        current state and a set of rules. General idea is to use indexing and the helper methods.

"""

import random, math, time
import numpy as np
# Viewer is a small helper class that drives the pygame renderer
from Viewer import Viewer

class Automaton:
    def __init__(self, w, h, color_func, ruleset):
        """
        :param w: respective width of cell grid
        :param h: respective height of cell grid
        :param color_func: a function that determines the color of a cell
        :param ruleset: a string that determines the ruleset to be used
        :return: A new Automaton object
        """

        #Initialize a 2d array of w*h size with 0's (empty cell grid)
        x = [[0 for i in range(w)] for j in range(h)]
        np_x = np.array(x)

        # initialization of the Automaton objects' fields
        self.width = w 
        self.height = h
        self.current_state = np_x
        self.steps = 0
        self.color_func = color_func
        self.ruleset = ruleset

        # counter is an optional feature that can be used in creation of rulesets. "worms" example demonstrates this.
        self.counter = 0 

    def initialize_top_mid(self):
        """
        Initializes cell grid to have one living cell top-mid.
        """
        self.current_state[int((self.width)/2)][0] = 255
        
    def initialize_middle(self):
        """
        Initializes cell grid to have one living cell in the middle.
        """
        self.current_state[int((self.width)/2)][int((self.height)/2)] = 255

    def initialize_with_noise(self, intensity):
        """
        :param intensity: An integer value that scales how many random cells should be revived.

        Initializes cell grid with random noise. Smaller intensity value means more live cells.
        """
        #A list containing the two choices, alive or dead
        r = [0, 255]
        #The more zeros added from intensity, the more dead cells
        for i in range(intensity):
            r.append(0)

        for (x, y), element in np.ndenumerate(self.current_state):
            self.current_state[x][y] = random.choice(r)


    def is_alive(self, x, y):
        """
        :param x: x-coordinate of cell
        :param y: y-coordinate of cell
        :returns: True if cell is alive and otherwise false 
        """
        if self.is_within_bounds(x, y):
            if (self.current_state[x][y] > 0): return True
            else: return False 

    def is_within_bounds(self, x, y):
        """
        :param x: x-coordinate of cell
        :param y: y-coordinate of cell
        :returns: True if index values are not out of bounds

        Determines if x and y are within the bounds of the cellular grid.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return True

    def update(self):
        """
        Determines what the next state will look like given the current state
        This is where rulesets are executed.
        """
        # We create a copy of the current state so that our decisions are not affected by our modifications
        state_copy = self.current_state.copy()
        
        for (x, y), element in np.ndenumerate(self.current_state):
            if self.is_alive(x, y):
                self.rulesets(x, y, element, state_copy, self.ruleset)

        self.current_state = state_copy
        return (state_copy, self.update_steps())

    def rulesets(self, x, y, element, state, ruleset):
        """ 
        :param x: x-coordinate of the cell
        :param y: y-coordinate of the cell
        :param element: the value of the cell at x, y
        :param state: a reference to a copy of the current state of the cell grid.

        A couple of example rulesets.
        """        
        # match-case would be nice here, but its a 3.10 feature (very new) so i'll use conditionals
        if ruleset == "lanes":
            if self.is_alive(x+1, y):
                self.kill_cell(state, x+2, y+1)
            if self.is_alive(x-1, y):
                self.kill_cell(state, x-2, y+1)
            self.revive_cell(state, x, y+1) 
            self.revive_cell(state, x+1, y+1)

        # Another example: worms
        elif ruleset == "worms":
            if self.counter == 4:
                self.counter = 0
            if self.is_alive(x+1, y):
                self.revive_cell(state, x+self.counter, y+1)
                self.counter+=1
            if self.is_alive(x-1, y):
                self.revive_cell(state, x-self.counter, y-1)
                self.kill_cell(state, x+self.counter, y-2)

        # Another example: a falling 3D plane. Use initialize_top_mid() for it to look as described.
        elif ruleset == "plane":
            self.revive_cell(state, x, y+1)
            self.kill_cell(state, x, y-2)
            self.revive_cell(state, x+2, y)
            self.revive_cell(state, x-2, y)
            self.kill_cell(state, x-2, y+1)
            
        else:
            print("No ruleset found for:", ruleset)

    def update_steps(self):
        """
        Increments and returns step count.
        """
        self.steps +=1
        return self.steps

    def revive_cell(self, state, x, y):
        """
        :param state: a reference to a cell grid to modify
        :params x: x-coordinate of cell
        :params y: y-coordinate of cell

        Bring the specified cell back from the dead.
        """
        if self.is_within_bounds(x, y):
            state[x][y] = self.color_func(x, y)
                
    def kill_cell(self, state, x, y):
        """
        :param state: a reference to a cell grid to modify
        :param x: x-coordinate of cell
        :param y: y-coordinate of cell

        Kills the specified cell. 
        """
        if self.is_within_bounds(x, y):
            state[x][y] = 0

# color function is defined outside of the class, so that it can be provided by the user.
# This is an example I've made with a few interesting options.
def color_function(x, y):
    """
    Pass a mathematical function optionally using x and y to
    generate a color value from 0-255
    """
    # change the color function here from the list of options
    color_func_name = "color_block"

    options = {
        "white": lambda x, y: 255,
        "red": lambda x, y: 100,
        "green": lambda x, y: 25,
        "blue": lambda x, y: 10,
        "rainbow": lambda x, y: abs(math.sin(x+y+random.randint(0,35)))*(255),
        "color_block": lambda x, y: x+y/abs(random.randint(0, y)+1)
    }
    return options[color_func_name](x, y)


# Create a new Automaton Object
new_automaton = Automaton(200, 200, color_function, "lanes")

# There are three methods to choose from for generating an initial state. 
# The example rulesets are crafted with the random noise method in mind.
new_automaton.initialize_with_noise(35)
# new_automaton.initialize_top_mid()  # use if you use ruleset "plane"

#Initializes the pygame viewer object and starts
viewer = Viewer(new_automaton.update, (750, 750))
viewer.start()