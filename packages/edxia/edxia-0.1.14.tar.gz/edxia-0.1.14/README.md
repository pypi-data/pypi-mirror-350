# edxia

Analyse SEM-BSE and SEM-EDS maps.

[Scanning Electron Microscopy (SEM)](https://en.wikipedia.org/wiki/Scanning_electron_microscope "Wikipedia link") coupled with [Energy-Dispersive Spectroscopy (EDX)](https://en.wikipedia.org/wiki/Energy-dispersive_X-ray_spectroscopy "wikipedia link") is an imaging technique used in the cement community to learn more about the microstructure of the material.

This python package aims to offer tools to analyse and correlate this information.

## Features

- Superpixel subsampling to extract representative points from the maps
- A [Glue](http://glueviz.org/)  plugins to provide a user-friendly way to identify phases using the well-known ratios plots
- Analysis functions to measure phase distributions, also available graphically
- Python API to automate analysis
- Based on robust and well-known framework such as scipy/scikit-image/pandas

## References

- Fabien Georget, William Wilson, Karen Scrivener, Comprehensive microstructure phase characterization from quantified SEM-EDS maps in cementitious materials, *in preparation*


## Install

edxia can be installed using [pip](https://pip.pypa.io/en/stable/) or [conda](https://www.anaconda.com/distribution). 

    pip install edxia

ou

    conda install -c specmicp edxia
    
## About

This code is developed by Fabien Georget (georget "AT" ibac.rwth-aachen "dot" de)  in the [laboratory of construction materials](https://lmc.epfl.ch/) at [EPFL](https://epfl.ch). This work is part of a collaboration with William Wilson (EPFL, Sherbrooke University). 
