import h5py
import numpy as np
import pandas as pd

from ..core.experiment import MappingExperiment
from ..core.map import MapsStack
from ..composite.channels import CompositeChannels
from ..composite.composite import CompositeMap
from ..point_analysis.points import EDSPoints

"""This module provides functions to save trated dataset from EDXIA.
For example, it can be used to save the denoised maps,
or the representative points"""


DS_STACK_NAME = "stack"
DS_COMPOSITE_NAME = "composite"
DS_POINTS_NAME = "points"
DS_EXTRA_NAME = "extras"


DS_EXP_NAME = "experiment"


def save_dataset(filepath, exp, stack=None, composite=None, points=None, extras=None, override=True):
    """This function save a set of treated data into a hdf5 file."""

    if override:
        mode = "w"
    else:
        mode = "x"
    h5f = h5py.File(filepath, mode)
    save_experiment(h5f, exp)
    if stack is not None:
        save_stack(h5f, stack)
    if composite is not None:
        save_composite(h5f, composite)
    if points is not None:
        save_points(h5f, points)
    if extras is not None:
        save_extras(h5f, extras)
    h5f.close()

def save_experiment(h5file, exp):
    h5file.attrs["components"] = np.array(exp.list_components, dtype="S")
    h5file.attrs[DS_EXP_NAME] = np.array([exp.pattern,exp.label], dtype="S")

def save_stack(h5file, stack):
    dset =   h5file.create_dataset(DS_STACK_NAME, data=stack.maps)
    dset.attrs["components"] = np.array(stack.components, dtype="S")

def save_composite(h5file, composite):
    channels = composite.channels
    dset = h5file.create_dataset(DS_COMPOSITE_NAME, data=composite.map)
    dset.attrs["components"] = np.array(channels.components, dtype="S")
    dset.attrs["factors"]  = np.array(channels.factors)

def save_points(h5file, points):
    dset = h5file.create_dataset(DS_POINTS_NAME, data=points.df.values)
    dset.attrs["columns"] = np.array(points.df.columns, dtype="S")

def save_extras(h5file, extras):
    grp = h5file.create_group(DS_EXTRA_NAME)
    for name, dmap in extras.items():
        grp.create_dataset(name, data=dmap)

def read_dataset(filepath):
    """Read a set of edxia data from a hdf5 file"""
    h5f = h5py.File(filepath, "r")
    exp = read_experiment(h5f)

    if DS_STACK_NAME in h5f.keys():
        stack  = read_stack(h5f, exp)
    else:
        stack = None
    if DS_COMPOSITE_NAME in h5f.keys():
        composite = read_composite(h5f, exp)
    else:
        composite = None
    if DS_POINTS_NAME in h5f.keys():
        points = read_points(h5f, exp)
    else:
        points = None
    if DS_EXTRA_NAME in h5f.keys():
        extras = read_extras(h5f)
    else:
        extras = None
    h5f.close()

    return stack, composite, points, extras

# -----------------------------------------------------------------------------


def read_experiment(h5file):
    """Read an experiment from an open hdf5 file"""
    data = h5file.attrs[DS_EXP_NAME]
    pattern = bytes(data[0]).decode()
    label = bytes(data[1]).decode()
    comp = h5file.attrs["components"].tolist()
    components = [bytes(c).decode() for c in comp]

    exp = MappingExperiment(pattern, label, components=components)
    return exp

def read_stack(hf5file, exp):
    """Read a stack object from an open hdf5 file"""
    dset = hf5file[DS_STACK_NAME]
    comp = dset.attrs["components"].tolist()
    components = [bytes(c).decode() for c in comp]
    stack = MapsStack(components, dset.shape, exp)
    stack.maps = dset[:]
    return stack

def read_composite(hf5file, exp):
    """Read a composite object from an open hdf5 file"""
    dset = hf5file[DS_COMPOSITE_NAME]
    comp= dset.attrs["components"].tolist()
    components = [bytes(c).decode() for c in comp]
    factors = dset.attrs["factors"].tolist()
    channels = CompositeChannels(components, factors)
    composite = CompositeMap(dset[:], channels, exp)
    return composite

def read_points(hf5file, exp):
    """Read a points object from an open hdf5 file"""
    dset = hf5file["points"]
    col = dset.attrs["columns"]
    columns = [bytes(c).decode() for c in col]
    points = pd.DataFrame(data=dset[:], columns=columns)
    pts =  EDSPoints(points, exp)
    return pts

def read_extras(h5file):
    extras = {}
    grp = h5file[DS_EXTRA_NAME]
    for name in grp.keys():
        dset = grp[name]
        extras[name] = dset[:]
    return extras
