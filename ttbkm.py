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

    # empty list to store output
    out_list = []
    
    # add the initial state to the output list
    # if ┃ isn't present in the first layer of the init state, we can assume there are multiple rows
    if '┃' not in init_state:
        # add the rows we know are present already
        for row in init_state:
            out_list.append(row)
        prev_state = init_state[-1]
    # otherwise, just need the standard raymer row
    else:
        out_list.append(init_state)
        prev_state = init_state
    
    # if you want to save the data, path should hold name the output file
    if path:
        with open(path, 'w') as f:
            f.write(init_state + '\n')

            for i in range(t):
                cross, prev_state = braid_move(prev_state, k_right, k_above, quiet, color)
                f.write(cross + '\n')
                f.write(prev_state + '\n')
                # write to list
                out_list.append(cross)
                out.list.append(prev_state)
                # if you want to animate it, sleep is in seconds
                if sleep:
                    time.sleep(sleep)
    else:
        for i in range(t):
            cross, prev_state = braid_move(prev_state, k_right, k_above, quiet, color)
            # write to list
            out_list.append(cross)
            out_list.append(prev_state)
            # if you want to animate it, sleep is in seconds
            if sleep:
                time.sleep(sleep)
    return tuple(out_list)

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

def draw_knot(state):
    """Draw a schematic of the initial configuration before tumbling."""
    
    # create an empty list to store the whole knot
    knot_rows = []
    
    # if ┃ isn't present in the first layer of the init state, we can assume there are multiple rows
    if '┃' not in state:
        # add the rows we know are present already
        for row in state:
            knot_rows.append(list(row))
    # otherwise, just need the standard raymer row
    else:
        knot_rows.append(list(state))

    # record number of loops for later use
    loops = knot_rows[0].count('│')

    # extend rows appropriately
    # each need double the elements - assume the outer 'end' will terminate at the same level as these rows
    for row in knot_rows:
        row.extend(['│',' ']*(loops+1))

    # now we need to start adding the loops
    # first on top
    for i in range(loops + 1):
        # duplicate first row
        # NOTE: using .insert here but it is ineffecient but usable because the lists are short
        #       if this needed to be extended to very long lists, use a deque object
        knot_rows.insert(0,knot_rows[0].copy())
        # find the active point we need to draw from
        try:
            point = knot_rows[0].index('┌')
        # otherwise, this must be the first row so we need the thick active end
        except:
            point = knot_rows[0].index('┃')
        # if dealing with the first row
        if knot_rows[0][point] == '┃':
            knot_rows[0][point] = '┌'
            knot_rows[0][point+1] = '┐'
        else:
            end_point = knot_rows[0].index('┐')
            # get to the next loop
            if knot_rows[0][point-1] == ' ':
                point -= 2
            else:
                point -= 1
            knot_rows[0][point] = '┌'
            # we don't need to check on right-hand side
            end_point += 2
            knot_rows[0][end_point] = '┐'
            # now add all the horizontal markers
            for p, char in enumerate(knot_rows[0]):
                if (p > point) and (p < end_point):
                    knot_rows[0][p] = '─'
    # add loops to bottom
    for i in range(loops + 1):
        # variable to store if final row
        fin = False
        # duplicate the bottom row
        knot_rows.append(knot_rows[-1].copy())
        # find active point to draw from
        try:
            point = knot_rows[-1].index('└')
        # otherwise, we start from the center
        except:
            point = (loops * 2) - 1
        # if we already have a curve
        if knot_rows[-1][point] == '└':
            # check that it is not the last loop
            if point == 1:
                # we just do the final active end
                point = knot_rows[-1].index('┃')
                fin = True
            else:
                point -= 2
            end_point = knot_rows[-1].index('┘') + 2
        # otherwise we need the first end point
        else:
            end_point = point + 2
        # we have the start and end points now
        knot_rows[-1][point] = '└'
        knot_rows[-1][end_point] = '┘'
        for p, char in enumerate(knot_rows[-1]):
            if char != '┃':
                if (p > point) and (p < end_point):
                    knot_rows[-1][p] = '─'
                if fin:
                    if p < point:
                        knot_rows[-1][p] = ' '
            
    # finally we need to get the output
    for row in knot_rows:
        print(''.join(row))
    print('\n')
    return knot_rows
    #end = 

#def file_to_coords(path):
#    """Convert text file to list of coordinates representing knot."""
#    # we will always move the active end downwards but we can move left or right.
#    # first active end should always be vertical
#    try:
#        with open(path, 'r') as f:
#            # list to store coordinates
#            coords = []
#            # follow the active end
#            for y, line in enumerate(f):
#                # y = 0 is top
#                # first find end
#                if coords == []:
#                    for x, char in enumerate(line):
#                        # x = 0 is left
#                        # check if we have the first active end
#                        # it should always be vertical
#                        if char == '┃':
#                            # all vertical lines fall at z=0
#                            coords.append([x, y, 0])
#                else:
#                    coords.append(

# find start
# go down
# if left, go left, if right go right
# find start
# append first

def knot_to_coords(knot):
    """Convert knot string to list of coordinates representing knot."""
    # split up the text
    text = knot.split('\n')

    # work our way down moving left or right
    # first active end will always be vertical
    coords = []
    for y, line in enumerate(text):
        # y=0 is the top
        row = []
        # this is only relevant coordinate in vertical lines
        if '┃' in line:
            pos = line.index('┃')
            check = line[pos-1:pos+1]
            # check if its the final tail at the bottom of knot
            if '─' in check or '└' in check or '┘' in check: 
                coords.append([pos, y, 1])
            else:
                coords.append([pos, y, 0])
        # check for signs of mobile end
        elif '┓' in line or '┏' in line or '┛' in line or '┗' in line:
            # define left and right bounds
            try:
                left_bound = line.index('┏')
                invert = True
            except:
                left_bound = line.index('┗')
                invert = False
            try:
                right_bound = line.index('┓')
            except:
                right_bound = line.index('┛')
            # now iterate through characters and add coordinates
            for x, char in enumerate(line):
                if x >= left_bound and x <= right_bound:
                    if char in '┓┏┛┗':
                        row.append([x,y,0])
                    # the string goes over
                    elif char == '━':
                        row.append([x,y,1])
                    # the string goes under
                    elif char == '│':
                        row.append([x,y,-1])
                    else:
                        pass
            # invert row if necessary
            if invert:
                row.reverse()
                coords.extend(row)
            else:
                coords.extend(row)
        else:
            pass
    # add the bottom edge of the knot loop
    # └──────┘
    coords.append([coords[-1][0],coords[-1][1]+1,0])
    coords.append([len(text[0])-2,coords[-1][1],0])
    # now add appropriate number of loops
    for j in range(int((len(text[0])+1)/4)):
        # up-left component
        # ───┐
        #    │
        coords.append([coords[-1][0],j,0])
        # for the last segment we need to shift it
        if j == int((len(text[0])+1)/4)-1:
            coords.append([(j*2),coords[-1][1],0])
        else:
            coords.append([(j*2)+1,coords[-1][1],0])
        if j != int((len(text[0])+1)/4)-1:
            # down-right component
            # │
            # └───
            coords.append([coords[-1][0],coords[-3][1]-1,0])
            coords.append([coords[-3][0]-2,coords[-1][1],0])
    # add connection to start
    # UNNECESSARY
    #coords.append(coords[0])
    return coords

def analyze_coords(coords):
    """Use pyknotid to analyze generated knot coordinates."""

    # first make sure we have pyknotid imported
    try:
        from pyknotid.spacecurves import Knot
    except:
        print("You must have pyknotid installed for the analysis!")
        return
    # check if sympy is installed
    try:
        import sympy
    except:
        print("You must have sympy installed for the analysis!")
        return

    # make Knot object
    k=Knot(coords)
    k.plot(mode="matplotlib")
    print(input("wait"))

    # find reduced gauss_code
    gauss_code = k.gauss_code()
    gauss_code.simplify()

    # crossing number
    crossing_num = len(gauss_code)

    # alexander polynomial
    alexander_poly = str(k.alexander_polynomial(variable=sympy.Symbol("t")))
    
    print(f"Crossing number: {crossing_num}")
    print(f"Gauss code: {str(gauss_code)}")
    print(f"Alexander polynomial: {alexander_poly}")

    return (str(gauss_code), crossing_num, alexander_poly)

# ─ ┌ └ ┐ ┘

# ┆
g = generate_peppino(2)
t = t_moves(10, g, 0.5, 0.5, False, 'red',0.1,False)
print('\n\n\n')
time.sleep(1)
draw_knot(t)

knot = ''' ┌───────┐ 
 │ ┌───┐ │ 
 │ │┌┐ │ │ 
 │ │┃│ │ │ 
┏━━━┛│ │ │ 
┃│ │ │ │ │ 
┗━┓│ │ │ │ 
 │┃│ │ │ │ 
┏│┛│ │ │ │ 
┃│ │ │ │ │ 
┗│┓│ │ │ │ 
 │┃│ │ │ │ 
 │┃└─┘ │ │ 
 └┃────┘ │ 
  └──────┘ '''

print(knot)
print(knot_to_coords(knot))

knot2 = ''' 
 ┌───────┐ 
 │ ┌───┐ │ 
 │ │┌┐ │ │ 
 │ │┃│ │ │ 
┏━━━┛│ │ │ 
┃│ │ │ │ │ 
┗│┓│ │ │ │ 
 │┃│ │ │ │ 
 │┃│ │ │ │ 
 │┃│ │ │ │ 
 │┃│ │ │ │ 
 │┃│ │ │ │ 
 │┃└─┘ │ │ 
 └┃────┘ │ 
  └──────┘ '''

print(knot2)
print(knot_to_coords(knot2))

for i in range(1):
    t = t_moves(30, g, 0.5, 0.5, False, list(term_colors.keys())[i+1], 0, False)
    s = draw_knot(t)
    z = ''
    for j in s:
        z += ''.join(j) + '\n'
    print(knot_to_coords(z))
    analyze_coords(knot_to_coords(z))

