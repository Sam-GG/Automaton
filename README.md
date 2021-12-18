# Cellular Automaton
Samuel Guttormson

Requires: pygame and numpy libraries

The following will generate a cellular automaton using the pygame engine given a simple set of rules.
The main variables for the user to play with at this time are:

    Cell Grid Size: defined in creation of Automaton object

    The initial state: Three methods exist to determine initial state. These can create:
        - one live cell starting in the top middle of the grid,
        - one live cell starting in the middle of the grid,
        - random noise generating multiple live cells all over the grid, based on an intensity parameter.

    color_function(x, y): a mathematical function to determine cell colors

    rulesets(): a method called by update() that determines what the next state will look like based on the
        current state and a set of rules. General idea is to use indexing and the helper methods.

