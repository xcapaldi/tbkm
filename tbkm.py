#  ttbkm
#  Tumbled Braid Knotting Model

#    ┃│ │ │
#    ┗━┓│ │
#     │┃│ │
#     │┗│┓│

import random
import time
import csv
import argparse
from subprocess import call
from os import name
from os import mkdir
from shutil import get_terminal_size

term_colors = {
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37",
}


def braid_step(prev_state, k_right=0.5, k_above=0.5, quiet=False, color=False):
    """Given the previous braid step (forward component) as a string, generate the next braid step.

    Keyword arguments:
    prev_state -- previous braid step (forward component) as a string
    k_right -- probability of active end moving to the right (default 0.5)
    k_above -- probability of active end moving over an adjacent loop (default 0.5)
    quiet -- suppress output (default False)
    color -- color active end in terminal with one of black, red, green, yellow, blue, magenta, cyan or white (default False)
    """

    # find the mobile end of the string
    end = prev_state.index("┃")

    # check if the end is already at a boundary
    # it's at left boundary
    if end == 0:
        # can only go right
        right = True
    # it's at right boundary
    elif end == len(prev_state) - 1:
        # can only go left
        right = False
    # check if there are interactable strands on the left
    elif "│" not in prev_state[1:end]:
        # can only go right
        right = True
    elif "│" not in prev_state[end:]:
        # can only go left
        right = False
    # otherwise there will be strands on either side
    else:
        # decide direction
        right = random.random() <= k_right

    # decide above/below
    above = random.random() <= k_above

    # construct braid move (two lines)
    # first copy previous
    cross = list(prev_state)
    if right:
        # find next interactable loop
        target = end + prev_state[end:].index("│")
        # add turn
        cross[end] = "┗"
        # add cross over loop
        cross[target + 1] = "┓"
        # add horizontal movement
        if above:
            cross[end + 1 : target + 1] = ["━"] * len(cross[end + 1 : target + 1])
        else:
            for i, element in enumerate(cross):
                if i < target and i > end:
                    if element in " ┆":
                        cross[i] = "━"
    else:
        # find next interactable loop
        check_region = list(prev_state[:end])
        # we want to find the first element from the end, not from the beginning
        check_region.reverse()
        target = end - check_region.index("│") - 1
        # add turn
        cross[end] = "┛"
        # add cross over loop
        cross[target - 1] = "┏"
        if above:
            cross[target:end] = ["━"] * len(cross[target:end])
        else:
            for i, element in enumerate(cross):
                if i > target and i < end:
                    if element in " ┆":
                        cross[i] = "━"
    # now take forward step
    step = list(prev_state)
    step[end] = " "
    if right:
        step[target + 1] = "┃"
    else:
        step[target - 1] = "┃"

    # check if output should not be displayed
    if not quiet:
        # color mobile end
        if color in term_colors:
            c_cross = "".join(cross)
            for char in ["┗", "┓", "┛", "┏", "━"]:
                c_cross = c_cross.replace(
                    char, "\033[" + term_colors[color] + "m" + char + "\033[0m"
                )
            c_step = "".join(step)
            c_step = c_step.replace(
                "┃", "\033[" + term_colors[color] + "m┃" + "\033[0m"
            )
            print(c_cross)
            print(c_step)
        else:
            print("".join(cross))
            print("".join(step))
    return ("".join(cross), "".join(step))


def t_steps(
    t,
    init_state,
    k_right=0.5,
    k_above=0.5,
    quiet=False,
    color=False,
    sleep=False,
    path=False,
):
    """Take t braid steps from initial state.

    Keyword arguments:
    init_state -- initial starting configuration of braid (all rows)
    k_right -- probability of active end moving to the right (default 0.5)
    k_above -- probability of active end moving over an adjacent loop (default 0.5)
    quiet -- suppress output (default False)
    color -- color active end in terminal with one of black, red, green, yellow, blue, magenta, cyan or white (default False)
    sleep -- time in seconds to delay between displaying each braid step (default False)
    path -- file in which you want to save the output braid (default False)
    """

    # empty list to store output
    out_list = []

    # add the initial state to the output list
    # if ┃ isn't present in the first layer of the init state, we can assume there are multiple rows
    if "┃" not in init_state:
        # add the rows we know are present already
        for row in init_state:
            if not quiet:
                print(row)
            out_list.append(row)
        prev_state = init_state[-1]
    # otherwise, just need the standard raymer row
    else:
        print(init_state)
        out_list.append(init_state)
        prev_state = init_state

    # if you want to save the data, path should hold name the output file
    if path:
        with open(path, "w") as f:
            # write the initial state
            for row in out_list:
                f.write(row + "\n")
            for i in range(t):
                cross, prev_state = braid_step(
                    prev_state, k_right, k_above, quiet, color
                )
                f.write(cross + "\n")
                f.write(prev_state + "\n")
                # write to list
                out_list.append(cross)
                out_list.append(prev_state)
                # if you want to animate it, sleep is in seconds
                if sleep:
                    time.sleep(sleep)
    else:
        for i in range(t):
            cross, prev_state = braid_step(prev_state, k_right, k_above, quiet, color)
            # write to list
            out_list.append(cross)
            out_list.append(prev_state)
            # if you want to animate it, sleep is in seconds
            if sleep:
                time.sleep(sleep)
    return tuple(out_list)


def generate_blank(loops, non_interacting=False):
    """Generate row of desired width with only loops and spaces.

    Keyword arguments:
    non_interacting -- loops which the active end cannot interact with (default False)
                    -- if False, all loops are interactable
                    -- if Integer (n), n loops randomly selected to be non-interactive
                    -- if List (j,k,l), loops j, k and l (from left) are non-interactive
    """

    # create an empty list with enough room for the mobile end, loops, and spaces
    spaces = (loops * 2) + 1

    row = [0] * spaces
    # start filling elements of initialization
    for i in range(spaces):
        # even lines have spaces
        if (i % 2) == 0:
            row[i] = " "
        # odd lines have loops
        else:
            row[i] = "│"
    if not non_interacting:
        return row
    elif type(non_interacting) is int:
        # check that the number of non-interacting loops is less than number of loops
        if non_interacting > loops - 1:
            print("non-interacting loops must be fewer than total loops")
            return
        else:
            # select random loops
            while row.count("┆") < non_interacting:
                row[2 * (random.randint(1, loops)) - 1] = "┆"
    elif type(non_interacting) is list or type(non_interacting) is tuple:
        # check that there are not too many non-interacting loops
        if len(non_interacting) > loops - 1:
            print("non-interacting loops must be fewer than total loops")
            return
        for j in non_interacting:
            # check is any element fall outside of loop
            if j > loops:
                print("non-interacting loop is outside loop index")
                return
            # check that there are not duplicates
            if non_interacting.count(j) > 1:
                print("duplicates in list of non-interacting loops")
                return
        # passes all checks, replace appropriate elements
        for loop in non_interacting:
            row[2 * loop - 1] = "┆"
    else:
        # incorrect input
        print("non_interacting needs to be an integer, list, tuple or False")
        return
    return row


def generate_raymer(loops, non_interacting=False):
    """Generate initial configuration to start braid moves where active end remains inside the loops.
    
    Format: ' │ │ │┃'
    
    Keyword arguments:
    non_interacting -- loops which the active end cannot interact with (default False)
                    -- if False, all loops are interactable
                    -- if Integer (n), n loops randomly selected to be non-interactive
                    -- if List (j,k,l), loops j, k and l (from left) are non-interactive
    """

    init = generate_blank(loops, non_interacting)
    # the inner line holds the mobile end
    init[-1] = "┃"

    return "".join(init)


def generate_peppino(loops, non_interacting=False):
    """Generate initial configuration to start braid moves where the active end has crossed outside the loops.

    Format: ' │ │ │┃'
            '┏━━━━━┛'
            '┃│ │ │ '
    
    Keyword arguments:
    non_interacting -- loops which the active end cannot interact with (default False)
                    -- if False, all loops are interactable
                    -- if Integer (n), n loops randomly selected to be non-interactive
                    -- if List (j,k,l), loops j, k and l (from left) are non-interactive
    """

    spaces = (loops * 2) + 1

    # row 1
    row_1 = generate_blank(loops, non_interacting)
    # the inner line holds the mobile end
    row_1[-1] = "┃"

    # row 2
    # the string crosses to the outside
    row_2 = ["━"] * spaces
    # draw the initial curve
    row_2[-1] = "┛"
    # now the mobile end is at the outside
    row_2[0] = "┏"

    # row 3
    # copy the first row
    row_3 = row_1.copy()
    # switch the first and last elements
    row_3[0] = "┃"
    row_3[-1] = " "

    return ("".join(row_1), "".join(row_2), "".join(row_3))


def generate_twist(loops, non_interacting=False):
    """Generate initial configuration to start braid moves where the active end has crossed outside the loops and they have an initial twist.

    Format: ' │ │ │┃'
            '┏━━━━━┛'
            '┃│ │ │ '
            '┗━┓│ │ '
            ' │┃│ │ '
            '┏│┛│ │ '
            '┃│ │ │ '
    
    Keyword arguments:
    non_interacting -- loops which the active end cannot interact with (default False)
                    -- if False, all loops are interactable
                    -- if Integer (n), n loops randomly selected to be non-interactive
                    -- if List (j,k,l), loops j, k and l (from left) are non-interactive
    """

    # we can use the peppino generator for the first part of this configuration
    # we just add the additional lines

    spaces = (loops * 2) + 1

    row_1, row_2, row_3 = generate_peppino(loops, non_interacting)

    if row_3[1] == "┆":
        first_loop = "┆"
    else:
        first_loop = "│"
    # row 4
    row_4 = list(row_3)
    # add first crossing
    row_4[0] = "┗"
    row_4[1] = "━"
    row_4[2] = "┓"

    # row 5
    row_5 = list(row_3)
    row_5[0] = " "
    row_5[1] = first_loop
    row_5[2] = "┃"

    # row 6
    row_6 = list(row_3)
    row_6[0] = "┏"
    row_6[1] = first_loop
    row_6[2] = "┛"

    # row 7
    row_7 = list(row_3)

    return (
        row_1,
        row_2,
        row_3,
        "".join(row_4),
        "".join(row_5),
        "".join(row_6),
        "".join(row_7),
    )


def draw_knot(state, quiet=False):
    """Draw a full 2D representation of the braid as a knot.
    
    Keyword arguments:
    state -- string of single initial state or tuple or list containing many rows of an initial state or a fully generated braid
    quiet -- suppress output (default False)
    """

    # create an empty list to store the whole knot
    knot_rows = []

    # if ┃ isn't present in the first layer of the init state, we can assume there are multiple rows
    if "┃" not in state:
        # add the rows we know are present already
        for row in state:
            knot_rows.append(list(row))
    # otherwise, just need the standard raymer row
    else:
        knot_rows.append(list(state))

    # record number of loops for later use
    loops = knot_rows[0].count("│") + knot_rows[0].count("┆")

    # extend rows appropriately
    # each need double the elements - assume the outer 'end' will terminate at the same level as these rows
    for row in knot_rows:
        row.extend(["│", " "] * (loops + 1))

    # now we need to start adding the loops
    # first on top
    for i in range(loops + 1):
        # duplicate first row
        # NOTE: using .insert here but it is ineffecient but usable because the lists are short
        #       if this needed to be extended to very long lists, use a deque object
        knot_rows.insert(0, knot_rows[0].copy())
        # find the active point we need to draw from
        try:
            point = knot_rows[0].index("┌")
        # otherwise, this must be the first row so we need the thick active end
        except:
            point = knot_rows[0].index("┃")
        # if dealing with the first row
        if knot_rows[0][point] == "┃":
            knot_rows[0][point] = "┌"
            knot_rows[0][point + 1] = "┐"
        else:
            end_point = knot_rows[0].index("┐")
            # get to the next loop
            if knot_rows[0][point - 1] == " ":
                point -= 2
            else:
                point -= 1
            knot_rows[0][point] = "┌"
            # we don't need to check on right-hand side
            end_point += 2
            knot_rows[0][end_point] = "┐"
            # now add all the horizontal markers
            for p, char in enumerate(knot_rows[0]):
                if (p > point) and (p < end_point):
                    knot_rows[0][p] = "─"
    # add loops to bottom
    for i in range(loops + 1):
        # variable to store if final row
        fin = False
        # duplicate the bottom row
        knot_rows.append(knot_rows[-1].copy())
        # find active point to draw from
        try:
            point = knot_rows[-1].index("└")
        # otherwise, we start from the center
        except:
            point = (loops * 2) - 1
        # if we already have a curve
        if knot_rows[-1][point] == "└":
            # check that it is not the last loop
            if point == 1:
                # we just do the final active end
                point = knot_rows[-1].index("┃")
                fin = True
            else:
                point -= 2
            end_point = knot_rows[-1].index("┘") + 2
        # otherwise we need the first end point
        else:
            end_point = point + 2
        # we have the start and end points now
        knot_rows[-1][point] = "└"
        knot_rows[-1][end_point] = "┘"
        for p, char in enumerate(knot_rows[-1]):
            if char != "┃":
                if (p > point) and (p < end_point):
                    knot_rows[-1][p] = "─"
                if fin:
                    if p < point:
                        knot_rows[-1][p] = " "
    # finally we need to get the output
    knot_str = ""
    for row in knot_rows:
        knot_str += "".join(row) + "\n"
    # print output
    if not quiet:
        print(knot_str)
    return knot_str


def knot_to_coords(knot):
    """Convert knot string to list of coordinates representing knot in 3D space."""
    # split up the text
    text = knot.split("\n")

    # because of a bug in pyknotid
    # crossings won't be detected if the nodes are
    # directly above/below each other
    # only the active end crosses above or below
    # so we shift each point in x and y by a modifier amount
    mod = 0.01
    # work our way down moving left or right
    # first active end will always be vertical
    coords = []
    for y, line in enumerate(text):
        # y=0 is the top
        row = []
        # this is only relevant coordinate in vertical lines
        if "┃" in line:
            pos = line.index("┃")
            check = line[pos - 1 : pos + 1]
            # check if its the final tail at the bottom of knot
            if "─" in check or "└" in check or "┘" in check:
                coords.append([pos + mod, y + mod, 1])
            else:
                coords.append([pos + mod, y + mod, 0])
        # check for signs of mobile end
        elif "┓" in line or "┏" in line or "┛" in line or "┗" in line:
            # define left and right bounds
            try:
                left_bound = line.index("┏")
                invert = True
            except:
                left_bound = line.index("┗")
                invert = False
            try:
                right_bound = line.index("┓")
            except:
                right_bound = line.index("┛")
            # now iterate through characters and add coordinates
            for x, char in enumerate(line):
                if x >= left_bound and x <= right_bound:
                    if char in "┓┏┛┗":
                        row.append([x + mod, y + mod, 0])
                    # the string goes over
                    elif char == "━":
                        row.append([x + mod, y + mod, 1])
                    # the string goes under
                    elif char == "│":
                        row.append([x + mod, y + mod, -1])
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
    coords.append([coords[-1][0], coords[-1][1] + 1, 0])
    coords.append([len(text[0]) - 2, coords[-1][1], 0])
    # now add appropriate number of loops
    for j in range(int((len(text[0]) + 1) / 4)):
        # up-left component
        # ───┐
        #    │
        coords.append([coords[-1][0], j, 0])
        # for the last segment we need to shift it
        if j == int((len(text[0]) + 1) / 4) - 1:
            coords.append([(j * 2), coords[-1][1], 0])
        else:
            coords.append([(j * 2) + 1, coords[-1][1], 0])
        if j != int((len(text[0]) + 1) / 4) - 1:
            # down-right component
            # │
            # └───
            coords.append([coords[-1][0], coords[-3][1] - 1, 0])
            coords.append([coords[-3][0] - 2, coords[-1][1], 0])
    # add connection to start
    # UNNECESSARY
    # coords.append(coords[0])
    return coords


def analyze_coords(coords, path=False, quiet=False):
    """Use pyknotid to analyze generated knot coordinates.
    
    Keyword arguments:
    coords -- list of coordinates in the form [x,y,z]
    path -- path to csv in which gauss_code, crossing number and alexander polynomial will be appended (default False)
    quiet -- suppress output (default False)
    """

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
    k = Knot(coords, verbose=False, add_closure=True)

    # find reduced gauss_code
    gauss_code = k.gauss_code()
    gauss_code.simplify()

    # crossing number
    crossing_num = len(gauss_code)

    # alexander polynomial
    alexander_poly = str(k.alexander_polynomial(variable=sympy.Symbol("t")))

    results = (str(gauss_code), crossing_num, alexander_poly)

    if not quiet:
        print(f"Crossing number: {crossing_num}")
        print(f"Gauss code: {str(gauss_code)}")
        print(f"Alexander polynomial: {alexander_poly}")

    # to save the data, path should hold name the output file
    if path:
        with open(path, "a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(results)

    return results


def write_header(path):
    """Initialize csv file with appropriate header for knot data."""

    # warning, will overwrite the file if it already exists
    with open(path, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(("gauss", "crossingnum", "alexander"))

    return


def run_model(
    runs,
    t,
    init_config,
    k_right=0.5,
    k_above=0.5,
    quiet=False,
    color="random",
    sleep=False,
    save_braids=False,
    path=False,
):
    """Run multiple tumbling models and optionally save the data.

    Keyword arguments:
    init_state -- initial starting configuration of braid (all rows)
    k_right -- probability of active end moving to the right (default 0.5)
    k_above -- probability of active end moving over an adjacent loop (default 0.5)
    quiet -- suppress output (default False)
    color -- color active end in terminal with one of red, green, yellow, blue, magenta, cyan or white
             if random, each run will display with a random color from those listed above (default random)
    sleep -- time in seconds to delay between displaying each braid step (default False)
    save_braids -- boolean to save each braid as a textfile in a subdirectory with the same name as the csv in path (default False)
    path -- csv file in which you want to save the output analysis data (default False)
    """

    # record start time
    start_time = time.time()

    # determine command to run when clearing output
    if name == "nt":
        clear_cmd = "cls"
    else:
        clear_cmd = "clear"

    # clear screen initially
    ret_code = call(clear_cmd)

    # get available space for progress bar
    columns, lines = get_terminal_size()
    columns = columns - 17 - 2 * len(str(runs))

    # initialize path where braids are saved
    braid_path = False
    if save_braids:
        if not path:
            print(
                "You must include the path to a file if you want to save the individual braids!."
            )
            return
        else:
            if "." in path:
                ext = path.index(".") + 1
                braid_dir = path[:-ext]
                mkdir(braid_dir)
            else:
                braid_dir = path
                mkdir(braid_dir)

    if path:
        with open(path, "w") as csvfile:
            writer = csv.writer(csvfile)
            # write header
            writer.writerow(("gauss", "crossingnum", "alexander"))
            # generate data
            for run in range(runs):
                # if we can see whole braid, show progress at top
                if lines - 40 >= t:
                    bot_print = False
                    progress = int(columns * ((run + 1) / runs))
                    print("\n")
                    print(
                        f"[{'█'*progress}{'-'*(columns-progress)}] {run+1}/{runs} {round(((run+1)/runs)*100)}% {round(time.time()-start_time,1)}s"
                    )
                    print("\n")
                else:
                    print("\n")
                    bot_print = True
                # random colors each run if desired
                if color == "random":
                    active_color = random.choice(list(term_colors.keys()))
                # define where each braid should be saved
                if save_braids:
                    braid_path = braid_dir + "/" + str(run + 1) + ".txt"
                # generate braid
                braid = t_steps(
                    t,
                    init_config,
                    k_right=k_right,
                    k_above=k_above,
                    quiet=quiet,
                    color=active_color,
                    sleep=sleep,
                    path=braid_path,
                )
                # show progress at bottom of terminal
                if bot_print:
                    print("\n")
                    progress = int(columns * ((run + 1) / runs))
                    print(
                        f"[{'█'*progress}{'-'*(columns-progress)}] {run+1}/{runs} {round(((run+1)/runs)*100)}% {round(time.time()-start_time,1)}s"
                    )
                knot = draw_knot(braid, quiet=True)
                coords = knot_to_coords(knot)
                gauss_code, crossing_num, alexander_poly = analyze_coords(
                    coords, path=False, quiet=True
                )
                # write data
                writer.writerow((gauss_code, crossing_num, alexander_poly))
                # clear screen
                ret_code = call(clear_cmd)
    else:
        # generate data
        for run in range(runs):
            # if we can see whole braid, show progress at top
            if lines - 40 >= t:
                bot_print = False
                progress = int(columns * ((run + 1) / runs))
                print("\n")
                print(
                    f"[{'█'*progress}{'-'*(columns-progress)}] {run+1}/{runs} {round(((run+1)/runs)*100)}% {round(time.time()-start_time,1)}s"
                )
                print("\n")
            else:
                print("\n")
                bot_print = True
            # random colors each run if desired
            if color == "random":
                active_color = random.choice(list(term_colors.keys()))
            # generate braid
            braid = t_steps(
                t,
                init_config,
                k_right=k_right,
                k_above=k_above,
                quiet=quiet,
                color=active_color,
                sleep=sleep,
                path=braid_path,
            )
            # show progress at bottom of terminal
            if bot_print:
                print("\n")
                progress = int(columns * ((run + 1) / runs))
                print(
                    f"[{'█'*progress}{'-'*(columns-progress)}] {run+1}/{runs} {round(((run+1)/runs)*100)}% {round(time.time()-start_time,1)}s"
                )
            knot = draw_knot(braid, quiet=True)
            coords = knot_to_coords(knot)
            gauss_code, crossing_num, alexander_poly = analyze_coords(
                coords, path=False, quiet=True
            )
            # clear screen
            ret_code = call(clear_cmd)
    # clear screen
    ret_code = call(clear_cmd)
    # print results
    print(f"tbkm: {runs} runs completed in {round(time.time()-start_time,1)}s")

    return


# parse commandline input
def cli():
    parser = argparse.ArgumentParser(
        description="generate (and analyze) knots with a terminal braid knotting model"
    )
    parser.add_argument(
        "select",
        choices=["braid", "knot", "analyze", "model"],
        help="generate single braid, braid + closed knot, braid + closed knot + analysis or perform multiple runs",
    )
    parser.add_argument(
        "configuration",
        choices=["raymer", "peppino", "twist"],
        help="select the initial configuration of coil and its terminal end",
    )

    parser.add_argument(
        "-l", "--loops", type=int, help="<required> number of loops", required=True
    )
    parser.add_argument(
        "-i",
        "--inactive",
        type=int,
        help="number of random loops which are inaccessible to the terminal end (it will always pass over them)",
    )
    parser.add_argument(
        "-I",
        "--spec_inactive",
        nargs="*",
        type=int,
        help="specific loops (from left) which are inaccessible to the terminal end (it will always pass over them)",
    )

    parser.add_argument(
        "-r",
        "--right",
        default=0.5,
        type=float,
        help="probability of terminal end moving right (default 0.5)",
    )
    parser.add_argument(
        "-a",
        "--above",
        default=0.5,
        type=float,
        help="probability of terminal end crossing above adjacent loop instead of below (default 0.5)",
    )
    parser.add_argument(
        "-m",
        "--moves",
        type=int,
        help="<Required> number of moves the terminal end will make",
        required=True,
    )
    parser.add_argument(
        "-q",
        "--quiet",
        help="suppress display of braid(s) or knot",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--color",
        choices=[
            "red",
            "green",
            "yellow",
            "blue",
            "magenta",
            "cyan",
            "white",
            "random",
        ],
        help="display terminal end in selected color",
        default=False,
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        help="delay (in seconds) between each move of the terminal end",
        default=False,
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="path of directory (model) or file (braid/knot) to save generated data",
        default=False,
    )

    parser.add_argument(
        "-n", "--runs", type=int, help="number of times to run the braid knotting model"
    )
    parser.add_argument(
        "-s",
        "--save_braids",
        help="save individual braid files produced during analysis",
        action="store_true",
    )

    args = parser.parse_args()

    # check rate inputs
    if args.right < 0 or args.right > 1:
        print("the rate of crossing to the right must be between 0 and 1")
        return
    if args.above < 0 or args.above > 1:
        print("the rate of crossing above must be between 0 and 1")
        return

    # check that number of runs has been specified with the model
    if args.select == "model" and not args.runs:
        print("specify number of runs to perform with the model")
        return

    # pick random color if not using model
    if args.select != "model" and args.color == "random":
        color = random.choice(list(term_colors.keys()))
    else:
        color = args.color

    # Save non-interacting values
    if not args.inactive:
        if not args.spec_inactive:
            inactive = False
        else:
            inactive = args.spec_inactive
    else:
        inactive = args.inactive

    # generate the initial configuration
    if args.configuration == "raymer":
        init_config = generate_raymer(args.loops, non_interacting=inactive)
    elif args.configuration == "peppino":
        init_config = generate_peppino(args.loops, non_interacting=inactive)
    elif args.configuration == "twist":
        init_config = generate_twist(args.loops, non_interacting=inactive)

    # braid
    if args.select == "braid":
        braid = t_steps(
            args.moves,
            init_config,
            k_right=args.right,
            k_above=args.above,
            quiet=args.quiet,
            color=color,
            sleep=args.delay,
            path=args.path,
        )
        return
    # knot
    elif args.select == "knot":
        braid = t_steps(
            args.moves,
            init_config,
            k_right=args.right,
            k_above=args.above,
            quiet=args.quiet,
            color=color,
            sleep=args.delay,
            path=args.path,
        )
        knot = draw_knot(braid, quiet=args.quiet)
    # analyze
    elif args.select == "analyze":
        braid = t_steps(
            args.moves,
            init_config,
            k_right=args.right,
            k_above=args.above,
            quiet=args.quiet,
            color=color,
            sleep=args.delay,
            path=args.path,
        )
        knot = draw_knot(braid, quiet=args.quiet)
        coords = knot_to_coords(knot)
        analysis = analyze_coords(coords, path=False, quiet=args.quiet)
    # model
    elif args.select == "model":
        run_model(
            args.runs,
            args.moves,
            init_config,
            k_right=args.right,
            k_above=args.above,
            quiet=args.quiet,
            color=color,
            sleep=args.delay,
            save_braids=args.save_braids,
            path=args.path,
        )

    return


# start the cli interface
# comment out this line if you just want to import the module for scripting
cli()
