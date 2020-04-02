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

def t_moves(t, init_state, k_right, k_above, quiet, color, sleep):
    """Take designated number of braid moves from initial state."""

    prev_state = init_state
    for i in range(t):
        prev_state = braid_move(prev_state, k_right, k_above, quiet, color)[1]
        # if you want to animate it
        if sleep:
            time.sleep(0.05)
    return



        

