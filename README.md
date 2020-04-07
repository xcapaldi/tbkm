# tbkm [terminal braid knotting model]

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Generate (and analyze) knots produced using a terminal braid knotting model.

(example knot)
(example full knot)

## Background

Raymer et al. proposed a simple knotting model to describe agitated knot formation.
Knots form at the mobile end of an open string so their model simply involved a coiled chain where one end was able to move over or under adjacent strings randomly for each time step.
This model showed similarities with their experimental data but failed to describe our subsequent work.

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
	abstract = {It is well known that a jostled string tends to become knotted; yet the factors governing the {\textquotedblleft}spontaneous{\textquotedblright} formation of various knots are unclear. We performed experiments in which a string was tumbled inside a box and found that complex knots often form within seconds. We used mathematical knot theory to analyze the knots. Above a critical string length, the probability P of knotting at first increased sharply with length but then saturated below 100\%. This behavior differs from that of mathematical self-avoiding random walks, where P has been proven to approach 100\%. Finite agitation time and jamming of the string due to its stiffness result in lower probability, but P approaches 100\% with long, flexible strings. We analyzed the knots by calculating their Jones polynomials via computer analysis of digital photos of the string. Remarkably, almost all were identified as prime knots: 120 different types, having minimum crossing numbers up to 11, were observed in 3,415 trials. All prime knots with up to seven crossings were observed. The relative probability of forming a knot decreased exponentially with minimum crossing number and M{\"o}bius energy, mathematical measures of knot complexity. Based on the observation that long, stiff strings tend to form a coiled structure when confined, we propose a simple model to describe the knot formation based on random {\textquotedblleft}braid moves{\textquotedblright} of the string end. Our model can qualitatively account for the observed distribution of knots and dependence on agitation time and string length.},
	issn = {0027-8424},
	URL = {https://www.pnas.org/content/104/42/16432},
	eprint = {https://www.pnas.org/content/104/42/16432.full.pdf},
	journal = {Proceedings of the National Academy of Sciences}
}
```

## Usage

No CLI interface has been written because you will likely want to import this module and write your own sequence of experiments.

### Setup

There are three initial configurations: raymer, peppino and twisted.
They can be generated with the generate_raymer(), generate_peppino(), generate_twised() functions respectively.

The raymer configuration represents a coil which has no initial crossings.
The peppino configuration has the terminal end of the coil lying outside the loops which means it crosses all loops before beginning the run.
The twisted configuration is the same as the peppino configuration but the loops have been twised oncewhile the terminal end remains stationary outside them.

You need to generate your initial configuration to do a run.
Each of the generator functions take only two arguments: the number of loops and the non-interacting loops.
By default non_interacting is False which means the terminal end is able to interact with any of the loops.
If you set non_interacting=integer_n, n loops will be randomly selected to inaccessible to the terminal end.
By inaccessible I mean the terminal end will always cross over them and never loop around them.
They are graphically represented by dashed lines but in the physical world this represents the terminal end only interacting with some subset of the overall coil because of confinment or rotation of the coil during agitation.
If in you set non_interacting=list/tuple, those loops will be specifically made non-interacting.
This is useful if you want to simulate a particular configuration many times.

### Individual braids

Once you have your initial configuration, you can generate a single braid using t_steps() which takes the initial state.
You can change the probabilities of going left or right and above or below adjacent strings.
In addition, you can add a delay to the output if you want to give a presenation with it.
You can also colorize the terminal end.
Finally the resulting braid can be saved to a text for for analysis later.

### Individual knots

To generate a real knot, the loops need to be closed so you can use draw_knot() to generate the full knot from a braid.

### Run model

Most often, you won't be working with individual knots.
Instead you'll want to run a given model many times, analyze the knots and save the resulting data.

You can use run_model() to do this.
It still requires an initial configuration as generated above.
This function also requires pyknotid and sympy to perform the knot analysis.
The resulting data consists of the gauss code, minimum crossing number and alexander polynomial and can be saved to a csv (along with the raw braids if desired).
