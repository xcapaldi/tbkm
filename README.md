# tbkm [terminal braid knotting model]

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Generate (and analyze) knots with a terminal braid knotting model.
Knot are drawn completely in the terminal using unicode box-drawing characters and as such, the raw data can be saved as text files.

If you use this project in your own research, please cite us (as well as pyknotid which is the analytical backend):

**Xavier Capaldi. tbkm - terminal braid knotting model. https://github.com/xcapaldi/tbkm, 2020. Accessed YYYY-MM-DD.**

bibtex format:

```bibtex
@Misc{tbkm,
  author = {Xavier Capaldi},
  title = {tbkm - terminal braid knotting model},
  howpublished = {\url{https://github.com/xcapaldi/tbkm}},
  note = {Accessed YYYY-MM-DD},
  year = 2020,
}
```

![Demo](pictures/demo.png?raw=true "Demo")

## Background

Raymer et al. proposed a simple knotting model to describe agitated knot formation.
Knots form at the mobile end of an open string so their model involved a coiled chain where one end was able to move over or under adjacent strands randomly for each time step.
This model showed similarities with their experimental data but fails to describe our subsequent work.
Please check their original publication for details:

```
@article {raymer2007spontaneous,
  author = {Raymer, Dorian M. and Smith, Douglas E.},
  title = {Spontaneous knotting of an agitated string},
  volume = {104},
  number = {42},
  pages = {16432--16437},
  year = {2007},
  doi = {10.1073/pnas.0611320104},
  publisher = {National Academy of Sciences},
  issn = {0027-8424},
  URL = {https://www.pnas.org/content/104/42/16432},
  eprint = {https://www.pnas.org/content/104/42/16432.full.pdf},
  journal = {Proceedings of the National Academy of Sciences}
}
```

## Requirements

If you only want to generate unicode braids and knots, you don't need to install anything.

The analysis however is performed using (Pyknotid)[https://github.com/SPOCKnots/pyknotid] and [Sympy](https://github.com/sympy/sympy).
Please check out their respective pages and cite them if you use this project for your research.

## Usage (examples below)

```
usage: tbkm.py [-h] -l LOOPS [-i INACTIVE]
               [-I [SPEC_INACTIVE [SPEC_INACTIVE ...]]] [-r RIGHT] [-a ABOVE]
               -m MOVES [-q]
               [-c {red,green,yellow,blue,magenta,cyan,white,random}]
               [-d DELAY] [-p PATH] [-n RUNS] [-s]
               {raymer,peppino,twist} {braid,knot,analyze,model}

generate (and analyze) knots with a terminal braid knotting model

positional arguments:
  {raymer,peppino,twist}
                        select the initial configuration of coil and its
                        terminal end
  {braid,knot,analyze,model}
                        generate single braid, braid + closed knot, braid +
                        closed knot + analysis or perform multiple runs

optional arguments:
  -h, --help            show this help message and exit
  -l LOOPS, --loops LOOPS
                        <required> number of loops
  -i INACTIVE, --inactive INACTIVE
                        number of random loops which are inaccessible to the
                        terminal end (it will always pass over them)
  -I [SPEC_INACTIVE [SPEC_INACTIVE ...]], --spec_inactive [SPEC_INACTIVE [SPEC_INACTIVE ...]]
                        specific loops (from left) which are inaccessible to
                        the terminal end (it will always pass over them)
  -r RIGHT, --right RIGHT
                        probability of terminal end moving right (default 0.5)
  -a ABOVE, --above ABOVE
                        probability of terminal end crossing above adjacent
                        loop instead of below (default 0.5)
  -m MOVES, --moves MOVES
                        <Required> number of moves the terminal end will make
  -q, --quiet           suppress display of braid(s) or knot
  -c {red,green,yellow,blue,magenta,cyan,white,random}, --color {red,green,yellow,blue,magenta,cyan,white,random}
                        display terminal end in selected color
  -d DELAY, --delay DELAY
                        delay (in seconds) between each move of the terminal
                        end
  -p PATH, --path PATH  path of directory (model) or file (braid/knot) to save
                        generated data
  -n RUNS, --runs RUNS  number of times to run the braid knotting model
  -s, --save_braids     save individual braid files produced during analysis
```

### Initial configuration: {raymer, peppino, twist}

There are three initial configurations: raymer, peppino and twist.

#### raymer
The raymer configuration represents a coil which has no initial crossings.

![Raymer configuration](pictures/raymer.png?raw=true "Raymer configuration")

#### peppino
The peppino configuration has the terminal end of the coil lying outside the loops which means it crosses all loops before beginning the run.

![Peppino configuration](pictures/peppino.png?raw=true "Peppino configuration")

#### twist
The twisted configuration is the same as the peppino configuration but the loops have been twised once while the terminal end remains stationary outside of them.

![Twist configuration](pictures/twist.png?raw=true "twist configuration")

#### -l LOOPS, --loops LOOPS

*required*

This parameter determines how many loops are in your coil.
In the braid model they are represented as thin vertical lines which lie parallel to the terminal end.

#### -i INACTIVE, --inactive INACTIVE

Number of loops (randomly selected) which are inaccessible to the terminal end (it will always pass over them).
By inaccessible, I mean the terminal end will always cross over them and never loop around them.
They are graphically represented by dashed lines but in the physical world this represents the terminal end only interacting with some subset of the overall coil because of confinment or rotation of the coil during agitation.
If this parameter is used in a model (with multiple runs), the inactive loops will only be selected randomly once.
If you want randomly selected loops for each run, check the section on scripting at the end of this document.

#### -I [SPEC_INACTIVE [SPEC_INACTIVE ...]], --spec_inactive [SPEC_INACTIVE [SPEC_INACTIVE ...]]

Specific loops (from left) which are inaccessible to the terminal end (it will always pass over them).
Because this takes a list without delimiters as input, it must be the last flag in your command.

Example: -I 1 3 5  ->  the first, third and fifth loop from the left will be inaccessible

### Action {braid, knot, analyze, model}

Several different actions can be performed after selected the initial configuration.
Each action is dependend upon the previous step.
In other words, *braid* form a braid, *knot* forms a braid and then a knot, . . .
I suggest you read about the options for the desired action and those that come before it.

#### braid

A braid is formed by the terminal end.
With each step it moves forward and either left or right and above or below.
Obviously it's mobility is limited at the leftmost or rightmost positions.

##### -m MOVES, --moves MOVES

*required*

This is the number of moves the terminal end will make.
This operation is fast so you can easily generate very long braids if desired (that doesn't mean it will be fast to perform the analysis).

##### -r RIGHT, --right RIGHT

Probability of the terminal end moving to the right.
Default value is *0.5*.

##### -a ABOVE, --above ABOVE

Probability of the terminal end crossing above instead of the below the adjacent string.
Default value is *0.5*.

##### -q, --quiet

Suppress display of braid(s) or knot.

##### -c {red,green,yellow,blue,magenta,cyan,white,random}, --color {red,green,yellow,blue,magenta,cyan,white,random}↩

The terminal end is displayed thicker than the loops by default but you can additionally color it as long as your terminal supports color.
By default, if this flag is unused, no color will be added.
With this flag, you can color it red, green, yellow, blue, magenta, cyan or white.
Additionally you can select random colors.
When producing a lot of braids using *model* with *-c random* each braid will have a different color.
The colors are not saved to the data files.

##### -d DELAY, --delay DELAY

A delay (in seconds) can be added between each movement of the terminal end.
This significantly slows down data generation and analysis so I recommend only using it if you are presenting.

##### -p PATH, --path PATH

You can specify a path to a file where the braid data will be saved (as a text file).
The extension is not added by default so you can add any extension you prefer.

When used with *model* this is the path to the CSV file where the analysis results are saved.
If the *--save_braids* flag is used as well, a directory of the same name (minus the .csv extension) will be made to hold the raw braid data.

##### knot

Braids are displayed as several adjacent strands with the terminal end.
In reality they represent a knot which has to be a closed loop.
*knot* will first generate a braid and then add the necessary closures and display the result to you.
It is only useful for visualizing the knot and we don't save the data in this form since it is easily constructed from the braid data.

##### analyze

First a braid is formed, then the knot is drawn and finally Pyknotid and Sympy are used to performed the knot analysis and present the results to you.

You can read more about the analysis process in the [Pyknotid ReadTheDocs](https://pyknotid.readthedocs.io/en/latest/).
In essence, Reidemeister moves are performed repeatedly to determine the simplified knot structure.
The Gauss code, minimum crossing number and Alexander polynomial will be presented.

This process is computationally intensive and for complex knots can take a long time.

##### model

Most often, you won't be working with individual knots.
Instead you'll want to run a given model many times, analyze the knots and save the resulting data.
*model* generates multiple knots and can save the analysis results to a CSV file as described previously.

###### -n RUNS, --runs RUNS

#required*

Number of knots to generate and analyze with the given parameters.

###### -s, --save_braids

If this flag is given (along with *-p*), a directory with the same name as the CSV file (minus extension) will be created and each generated braid will be saved within.

## Examples

Generate a single braid (Raymer) with 3 loops and 5 steps in yellow:

```
python tbkm.py raymer -l 3 braid -m 5 -c yellow
```

![Example 1](pictures/example_1.png?raw=true "Example 1")

Generate a single braid (Peppino) with 5 loops (2 are inaccessible) and 10 steps in blue:

```
python tbkm.py peppino -l 5 -i 2 braid -m 10 -c blue
```

![Example 2](pictures/example_2.png?raw=true "Example 2")

Generate a knot (twist) with 5 loops (1st and 3rd loop inaccessible) and 5 steps:

```
python tbkm.py twist -l 5 knot -m 5 -I 1 3
```

![Example 3](pictures/example_3.png?raw=true "Example 3")

Generate a knot (Peppino) with 3 loops and 5 steps  and analyze the result:

```
python tbkm.py peppino -l 3 analyze -m 5
```
Output:

```
Crossing number: 8
Gauss code: 1+a,2+a,3+a,4-a,5+c,6-a,7+a,8+a,3-a,4+a,2-a,5-c,8-a,1-a,6+a,7-a
Alexander polynomial: t**5 - t**4 + t**3 - t**2 + t
```

Generate 10 knots (twist), each with 4 loops and 5 steps in random colors.
Save the analysis and raw data:

```
python tbkm.py twist -l 4 model -m 5 -n 10 -c random -d 0.05 -p demo.csv -s
```
Output:

```
gauss,                           crossingnum, alexander
"1+a,2+a,3+a,8-a,9-a,10-a,11+a,
 3-a,8+a,2-a,9+a,1-a,10+a,11-a", 7,           t**6 - t**5 + t**4 - 2*t**2 + 2*t
----,                            0,           1
----,                            0,           1
"3+a,10-a,11+a,3-a,10+a,11-a",   3,           -t - (1 - t)**2
----,                            0,           1
----,                            0,           1
"1+a,2+a,9-a,10-a,11+a,2-a,9+a,
 1-a,10+a,11-a",                 5,           -t**4 + t**3 - t**2 + t - 1
----,                            0,           1
----,                            0,           1
----,                            0,           1
```

## Scripting

The last line of tbkm.py calls the command line interface (cli()).
You can simply comment that line and then import tbkm as a module.

Here is an example to produce 6300 knots with varying parameters and save the results:

```python
import tbkm

loops = [2,3,4,5,6,7,8,9,10]
steps = [5,10,15,20,25,30,50]

for coil in loops:
    for tumble in steps:
        if coil < 10:
            coilstr = '0' + str(coil)
        else:
            coilstr = str(coil)

        if tumble < 10:
            tumblestr = '00' + str(tumble)
        elif tumble < 100:
            tumblestr = '0' + str(tumble)
        else:
            tumblestr = str(tumble)
        filename="../../sim/raymer_4-max/" + coilstr + "-strands_" + tumblestr + "-moves.csv"

        tbkm.write_header(filename)

        if coil > 4:
            cut = coil - 4
        else:
            cut = False

        for i in range(100):
            config = tbkm.generate_raymer(coil, non_interacting=cut)

            braid = tbkm.t_steps(tumble, config, color='yellow')
            knot = tbkm.draw_knot(braid, quiet=True)
            coords = tbkm.knot_to_coords(knot)
            analysis = tbkm.analyze_coords(coords, path=filename)

            print(f"{coil} loops - {tumble} steps --> [{i+1}/100]")
```

## License

This work is released under the MIT license.
