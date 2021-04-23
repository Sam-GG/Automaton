"""
Samuel Guttormson
Initial Upload Date: Jan 8th 2021

The following will generate automaton using the pygame engine given a simple set of rules.
The main variables for the user to play with at this time are:

    Cell Grid Size: defined in creation of Automaton object

    The initial state: Three methods exist to determine initial state. These can create:
        - one live cell starting in the top middle of the grid,
        - one live cell starting in the middle of the grid,
        - random noise generating multiple live cells all over the grid, based on an intensity parameter.

    color_function(x, y): a mathematical function to determine cell colors

    update(): a method that determines what the next state will look like based on the
        current state. Make use of the alive_cells list and revive and kill methods. The 
        shown example rules are very simple and can be made considerably more complex.

"""

import random, math, time
import numpy as np

from Viewer import Viewer
class Automaton:
    def __init__(self, w, h, color_func):
        """
        :params w, h: respective width and height of cell grid
        :return: A new Automaton object
        """
        #self.initial_state = np.random.random((20, 20, 3)) *255 
        #self.current_state = self.initial_state

        #Initialize a 2d array of w*h size with 0's (empty cell grid)
        x = [[0 for i in range(w)] for j in range(h)]
        np_x = np.array(x)

        self.dict = {
            'width': w,
            'height': h,
            'current_state': np_x,
            'steps': 0,
            'color_func': color_func,
            'counter': 0 
        }

    def initialize_top_mid(self):
        """
        Initializes cell grid to have one living cell top-mid.
        """
        self.dict['current_state'][int((self.dict['width'])/2)][0] = 255
        
    def initialize_middle(self):
        """
        Initializes cell grid to have one living cell in the middle.
        """
        self.dict['current_state'][int((self.dict['width'])/2)][int((self.dict['height'])/2)] = 255

    def initialize_with_noise(self, intensity):
        """
        Initializes cell grid with random noise
        :param intensity: An integer value that scales how many random cells should be revived.
        Smaller intensity value means more live cells.
        """
        #A list containing the two choices, alive or dead
        r = [0, 255]
        #The more zeros added from intensity, the more dead cells
        for i in range(intensity):
            r.append(0)
        image = self.dict['current_state']
        for (x, y), element in np.ndenumerate(image):
            image[x][y] = random.choice(r)


    def is_alive(self, cell):
        """
        :param cell: A single cell value from the state grid
        :returns: True if cell is alive and otherwise false 
        """
        if (cell > 0): return True
        else: return False 

    def is_within_bounds(self, x, y):
        """
        Determines if x and y are within the bounds of the cellular grid
        :params x, y: x and y index values
        :returns: True if index values are not out of bounds
        """
        if x in range(0, self.dict['width']) and y in range(0, self.dict['height']):
            return True

    def update(self):
        """
        Determines what the next state will look like given the current state
        This is where rulesets are created.
        """
        image = self.dict['current_state']
        
        for (x, y), element in np.ndenumerate(image):
            if self.is_alive(element):
                ###
                #DEFINE RULESET HERE
                #alive_cells is a list containing tuples of coordinates for all the currently live cells.
                #Make use of this list and kill and revive cell methods to define your ruleset. Example below:

                #An Example: 
                # if self.is_within_bounds(x+1, y):
                #     if self.is_alive(image[x+1][y]):
                #         self.revive_cell(image, x+2, y+1)
                # if self.is_within_bounds(x-1, y):
                #     if self.is_alive(image[x-1][y]):
                #         self.revive_cell(image, x-2, y+1)

                #Another example: worms
                if self.dict['counter'] == 3:
                    self.dict['counter'] = 0
                if self.is_within_bounds(x+1, y):
                    if self.is_alive(image[x+1][y]):
                        self.revive_cell(image, x+self.dict['counter'], y+1)
                        self.dict['counter']+=1
                if self.is_within_bounds(x-1, y):
                    if self.is_alive(image[x-1][y]):
                        self.revive_cell(image, x-self.dict['counter'], y-1)
                        self.kill_cell(image, x+self.dict['counter'], y-2)
        
        #time.sleep(1)
        return (image, self.update_steps())

    def update_steps(self):
        self.dict['steps'] +=1
        return self.dict['steps']

    def revive_cell(self, image, x, y):
        """
        Play god and bring the specified cell back from the dead
        :param image: a reference to a cell grid to modify
        :params x, y: x and y coordinates of the dead cell in the provided cell grid
        """
        if self.is_within_bounds(x, y):
            image[x][y] = self.dict['color_func'](x, y)
                
    def kill_cell(self, image, x, y):
        """
        Kills the specified cell 
        :param image: a reference to a cell grid to modify
        :params x, y: x and y coordinates of the living cell in the provided cell grid
        """
        if self.is_within_bounds(x, y):
            image[x][y] = 0


######################################
#DEFINE COLOR ASSIGNMENT FUNCTION HERE
def color_function(x, y):
    """
    Pass a mathematical function optionally using x and y to
    generate a color value from 0-255
    """
    #setting a return of 255 defaults automaton to simple black and white (dead and alive)
    #return 255
    return abs(math.sin(x+y+random.randint(0,35)))*(255)
    #return x+y/abs(random.randint(0, y)+1)
######################################

#Create a new Automaton Object
new_automaton = Automaton(100, 100, color_function)

#There are three methods to choose from for generating an initial state:
new_automaton.initialize_with_noise(10)
#new_automaton.initialize_middle()
#new_automaton.initialize_top_mid()

#Initializes the pygame viewer object and starts
viewer = Viewer(new_automaton.update, (800, 800))
viewer.start()