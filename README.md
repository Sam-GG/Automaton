# Cellular Automaton
Samuel Guttormson

The following will generate a cellular automaton using the pygame engine given a simple set of rules.
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
