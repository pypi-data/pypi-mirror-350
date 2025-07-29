# SpecPiNk

**Spec**troscopic data reduction **Pi**peline for the **N**ord**k**uppel telescope

## Functionality
This package is currently under development and shall provide a convenient and easily accessible way to process
spectroscopic data obtained with the LISA High luminosity spectrograph (Shelyak Instruments) on the 80cm telescope
situated in the northern dome (Nordkuppel) of the Institute for Astronomy's observatory in Vienna into a science-ready form.
\
The processing shall include the application of image correction with Bias-, Dark- and Flat-Frames and the wavelength
calibration.

## User stories
\
As Alice, a Bachelor student with more interest in science than in programming, I want to check the produced science
frames of my self developed data reduction against the results of this (hopefully) very well crafted python package,
so I can hand in my lab report with some more confidence.
\
\
As Bob, who just found out about a niche case with transitional phenomena where this small telescope can actually be of
use for some serious science, I do not want to waste my time getting to know the peculiarities of the spectrograph
configuration, I only want my well defined images out of some sort of mostly pre-configured black box (this package).
However, I want some control over the final data reduction process, so I need both the correctional images (Bias, Dark,
Flat) and the science frames.
\
\
As Charly, who works on the same transitional phenoma, I do not want to just stare at the wall of the Nordkuppel while
an exposure is being made, I want some preliminary results, the details of the data reduction do not really
matter for now, I just want to use this package to get some processed science frames very fast. After all, I need to be faster than Bob.
\
\
As Dagobert, I am not in a particular rush, for I am only an amateur astronomer interested in spectroscopy. A student
friend of mine has provided me with observational data he recently obtained, but has not really explained to me how I
get something useful out of this. I want this package to produce nice science frames without having to learn all about
the mechanics of data reduction. Maybe the example given in the documentation is some sort of standard example?

## Pseudo code example (minimal)
\
\# simply importing the package
\
import specpink 
\
\
\# optional input settings file
\
input_file = ".\input" 
\
\
\# specify input directories
\
dark_dir = ".\Darks"
\
bias_dir = ".\Bias"
\
flat_dir = ".\Flats"
\
calib_dir = ".\Calibs"
\
science_dir = ".\Science"
\
\
\# specify output directories (maybe differently structured)
\
final_dir = ".\Finals" #
\
\
specpink.dothemagic(directories)
