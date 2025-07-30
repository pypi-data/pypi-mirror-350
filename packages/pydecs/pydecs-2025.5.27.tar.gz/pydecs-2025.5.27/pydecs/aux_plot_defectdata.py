#!/usr/bin/env python
#---------------------------------------------------------------------------
# Copyright 2021 Takafumi Ogawa
# Licensed under the Apache License, Version2.0.
#---------------------------------------------------------------------------
# Auxiliary tool of pydecs library for plotting defect-data
#---------------------------------------------------------------------------
import os,sys
import numpy as np
import datetime

from pydecs.inout  import InputParamsToml
from pydecs.inout  import plot_defect_densities

def plot_defect_data():
    print(f"-"*100)
    print(f" Starting plot-densities tool of pydecs")
    fnin_toml="inpydecs.toml"
    if len(sys.argv)>1:
        fnin_toml=sys.argv[1]
    print(f"-"*100)
    print(f" Input toml-file = {fnin_toml}")
    if not os.path.exists(fnin_toml):
        print(f" ERROR:: file not-found: {fnin_toml}")
        print(f"-"*100)
        sys.exit()
    intoml=InputParamsToml(fnin_toml)
    inparams=intoml.get_input_parameters()
    if not "plot" in inparams:
        print(" ERROR(plot):: plot-block is not found in the toml-input file")
    root_outfiles=intoml.get_root_outfiles()
    dirname_root=f"{root_outfiles}_outdata"
    if os.path.exists(dirname_root):
        os.chdir(dirname_root)
    if not "outfiles_header" in inparams["plot"]:
        inparams["plot"]["outfiles_header"]=root_outfiles
    if not "input_filename" in inparams["plot"]:
        inparams["plot"]["input_filename"]=root_outfiles+"_densities.csv"
    print(f"  outfiles_header for plot-densities = {inparams['plot']['outfiles_header']}")
    print(f"  input_filename  for plot-densities = {inparams['plot']['input_filename']}")
    print(f"-"*100)
    plot_defect_densities(inparams["plot"])
    print("*"*100)
    print(f" Finished!")
    print("*"*100)

if __name__=="__main__":
    plot_defect_data()

