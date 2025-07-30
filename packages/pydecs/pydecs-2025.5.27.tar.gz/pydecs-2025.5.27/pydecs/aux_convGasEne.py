#!/usr/bin/env python
#---------------------------------------------------------------------------
# Copyright 2021 Takafumi Ogawa
# Licensed under the Apache License, Version2.0.
#---------------------------------------------------------------------------
# Auxiliary tool of pydecs library for converting the file from JANAF database
#---------------------------------------------------------------------------

import sys
import math
import numpy as np

kjmol2eV =1.036427e-2 # eV/(kJ/mol)

def convGasEneFromJANAF():
    firstLoop=True
    if len(sys.argv)>1:
        filename_in=sys.argv[1]
    else:
        print(f" ERROR: input-file not found")
        print(f"    usage: pydecs-convDOS-VASP [input-filename]")
        sys.exit()
    for t1 in open(filename_in):
        if firstLoop:
            print("#"+t1.strip())
            print("#Temperature [K], Free_Energy [eV]")
            firstLoop=False
        if not "." in t1:
            continue
        t2=t1.split()
        temper=float(t2[0])
        ene=-temper*float(t2[2])/1000.0+float(t2[4])
        if temper<1e-6:
            ene0=ene 
            ene=0.0
        else:
            ene=ene-ene0
        print("{:>8.2f}".format(temper)+" , "+"{:<12.8f}".format(kjmol2eV*ene))


if __name__=="__main__":
    convGasEneFromJANAF()

