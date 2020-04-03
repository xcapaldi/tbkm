# Terminal Tumbled Braid Knotting Model

# want to modify rates of crossing in given direction
#                rates of crossing above and below
#                rates of initial twist
#
# compare raymer initial conditions
# versus our own
#
#

import random as r
import time

term_colors = {'black':'30','red':'31','green':'32','yellow':'33','blue':'34','magenta':'35','cyan':'36','white':'37'}

#def init_run(init_cond)



#1   ┃│ │ │
#2   ┗━┓│ │
#3    │┃│ │
#4    │┗│┓│


def braid_move(prev_state, k_right, k_above, quiet, color):
    """Make an individual braid move.""" 

    # find the mobile end of the string
    end = prev_state.index('┃')

    # check if the end is already at a boundary
    # it's at left boundary
    if end == 0:
        # can only go right
        right = True
        # decide above/below
        above = r.random() <= k_above
    # it's at right boundary
    elif end == len(prev_state) - 1:
        # can only go left
        right = False
        # decide above/below
        above = r.random() <= k_above
    # otherwise there will be strands on either side
    else:
        # decide direction
        right = r.random() <= k_right
        # decide above/below
        above = r.random() <= k_above
    
    # construct braid move (two lines)
    # first copy previous
    cross = list(prev_state)
    if right:
        cross[end] = '┗'
        cross[end+2] = '┓'
        if above:
            cross[end+1] = '━'
        else:
            cross[end+1] = '│'
    else:
        cross[end] = '┛'
        cross[end-2] = '┏'
        if above:
            cross[end-1] = '━'
        else:
            cross[end-1] = '│'
    # now take forward step
    step = list(prev_state)
    step[end] = ' '
    if right:
        step[end+2] = '┃'
    else:
        step[end-2] = '┃'

    # check if output should not be displayed
    if not quiet:
        # color mobile end
        if color in term_colors:
            c_cross = ''.join(cross)
            for char in ['┗','┓','┛','┏','━']:
                c_cross = c_cross.replace(char, '\033['+term_colors[color]+'m'+char+ '\033[0m')
            c_step = ''.join(step)
            c_step = c_step.replace('┃', '\033['+term_colors[color]+'m┃'+'\033[0m')
            print(c_cross)
            print(c_step)
        else:
            print("Not a valid color!\nUse one of: black, red, green, yellow, blue, magenta, cyan or white")
    return (''.join(cross), ''.join(step))

def t_moves(t, init_state, k_right, k_above, quiet, color, sleep, path):
    """Take designated number of braid moves from initial state."""

    # if you want to save the data, path should hold name the output file
    if path:
        with open(path, 'w') as f:
            f.write(init_state + '\n')
            prev_state = init_state

            for i in range(t):
                cross, prev_state = braid_move(prev_state, k_right, k_above, quiet, color)
                f.write(cross + '\n')
                f.write(prev_state + '\n')
                # if you want to animate it, sleep is in seconds
                if sleep:
                    time.sleep(sleep)
    else:
        prev_state = init_state
        for i in range(t):
            prev_state = braid_move(prev_state, k_right, k_above, quiet, color)[1]
            # if you want to animate it, sleep is in seconds
            if sleep:
                time.sleep(sleep)
    return

def generate_blank(loops):
    """Generate a row with only the loops and spaces."""
    
    # create an empty list with enough room for the mobile end, loops, and spaces
    spaces = (loops * 2) + 1

    row = [0] * spaces
    # start filling elements of initialization
    for i in range(spaces):
        # even lines have spaces
        if (i % 2) == 0:
            row[i] = ' '
        # odd lines have loops
        else:
            row[i] = '│'
    return row

def generate_raymer(loops):
    """Generate initial configuration to start braid moves based on Raymer's paper."""
    
    init = generate_blank(loops)
    # the inner line holds the mobile end
    init[-1] = '┃'

    return ''.join(init)


def generate_peppino(loops):
    """Generate initial configuration to start braid moves based on our configuration."""

    spaces = (loops * 2) + 1

    # row 1
    row_1 = generate_blank(loops)
    # the inner line holds the mobile end
    row_1[-1] = '┃'

    # row 2
    # the string crosses to the outside
    row_2 = ['━'] * spaces
    # draw the initial curve
    row_2[-1] = '┛'
    # now the mobile end is at the outside
    row_2[0] = '┏'
    
    # row 3
    # copy the first row
    row_3 = row_1.copy()
    # switch the first and last elements
    row_3[0] = '┃'
    row_3[-1] = ' '
    
    return (''.join(row_1), ''.join(row_2), ''.join(row_3))

def generate_twist(loops):
    """Generate initial configuration based on our model with a twist."""
    
    # we can use the peppino generator for the first part of this configuration
    # we just add the additional lines
    
    spaces = (loops * 2) + 1

    # row 4
    row_4 = generate_blank(loops)
    # add first crossing
    row_4[0] = '┗'
    row_4[1] = '━'
    row_4[2] = '┓'

    # row 5
    row_5 = generate_blank(loops)
    row_5[0] = ' '
    row_5[1] = '│'
    row_5[2] = '┃'

    # row 6
    row_6 = generate_blank(loops)
    row_6[0] = '┏'
    row_6[1] = '│'
    row_6[2] = '┛'

    # row 7
    row_7 = generate_blank(loops)
    row_7[0] = '┃'

    row_1, row_2, row_3 = generate_peppino(loops)
    
    return (row_1, row_2, row_3,''.join(row_4),''.join(row_5),''.join(row_6),''.join(row_7))
