#!/usr/bin/env python
#---------------------------------------------------------------------------
# Copyright 2021 Takafumi Ogawa
# Licensed under the Apache License, Version2.0.
#---------------------------------------------------------------------------
# Auxiliary tool of pydecs library for checking equilibrium phases
#---------------------------------------------------------------------------
import os,sys
import numpy as np
import datetime
from scipy.spatial import ConvexHull

from pydecs.reference_phases import ReferencePhases

def check_equilibrium_phases_0K():
    fout_rp = open("outpydecs_checked_EqPhase.txt","w")
    print("-"*60)
    print(" Checking equilibrium phases")
    print(" Parsed files: inpydecs_phases.csv")
    fout_rp.write("-"*60+"\n")
    fout_rp.write(" Checking equilibrium phases\n")
    fout_rp.write(" Parsed files: inpydecs_phases.csv\n")
    refPhase=ReferencePhases("host",["./"],fout_rp)
    phaseList=refPhase.get_phaseList()
    print("-"*60)
    fout_rp.write("-"*60+"\n")
    ph_host=refPhase.get_host(phaseList)
    comp_host=ph_host["composition"]
    atoms_host=ph_host["composition_dict"]
    elems_host=list(atoms_host.keys())
    num_elems=len(elems_host)
    pointsList = []
    compList=[]
    print(" Accounted compounds")
    fout_rp.write(" Accounted compounds\n")
    for ph1 in phaseList:
        c1=ph1["composition"]
        print("  "+c1)
        fout_rp.write("  "+c1+"\n")
        compList.append(c1)
        atoms=ph1["composition_dict"]
        ene0K=ph1["energy_0K"]
        ntot=0
        for n1 in atoms.values():
            ntot+=n1
        point1=np.zeros(num_elems)
        for e1,n1 in atoms.items():
            index_elem1=elems_host.index(e1)
            point1[index_elem1]=float(n1)/float(ntot)
        point2=point1.tolist()[:-1]
        point2.append(ene0K/float(ntot))
        pointsList.append(point2)
    convhull = ConvexHull(pointsList)
    ind_host=compList.index(comp_host)
    simpList=[]
    for simp1 in convhull.simplices:
        if ind_host in simp1:
            comp_simp=[comp_host]
            for is1 in simp1:
                c1=compList[is1]
                if c1!=comp_host:
                    comp_simp.append(c1)
            simpList.append(comp_simp)
    print("-"*60)
    print(" Simpleces list")
    fout_rp.write("-"*60+"\n")
    fout_rp.write(" Simpleces list\n")
    for simp1 in simpList:
        str1="  "
        for comp1 in simp1:
            str1+=comp1+" + "
        str1=str1[:-2]
        print(str1)
        fout_rp.write(str1+"\n")


if __name__=="__main__":
    check_equilibrium_phases_0K()



