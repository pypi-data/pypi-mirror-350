#!/usr/bin/env python
#---------------------------------------------------------------------------
# Copyright 2021 Takafumi Ogawa
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#---------------------------------------------------------------------------
# pydecs-main module
# pydecs = PYthon code for Defect Equilibria in Crystalline Solids
# Library-homepage = /https://gitlab.com/tkog/pydecs
# Citation: ***
#---------------------------------------------------------------------------
import os
import sys
import numpy as np
import shutil
import time
# from multiprocessing  import Pool
# import threading 
# from concurrent import futures
from pathos.multiprocessing import ProcessingPool

from pydecs.inout  import InputParamsToml
from pydecs.eqcond import EquilibriumConditions
from pydecs.solver import DefectEqSolver
from pydecs.inout  import output_eqcond
from pydecs.inout  import output_density_with_eqcond
from pydecs.inout  import plot_defect_densities

def pydecs_main():
    print(f"-"*100)
    print(f" Starting pydecs (PYthon code for Defect Equilibria in Crystalline Solids)")
    fnin_toml="inpydecs.toml"
    if len(sys.argv)>1:
        fnin_toml=sys.argv[1]
    print(f" Input toml file = {fnin_toml}")
    print(f"-"*100)
    if not os.path.exists(fnin_toml):
        print(f" ERROR:: file not found: {fnin_toml}")
        print(f"-"*100)
        sys.exit()
    intoml=InputParamsToml(fnin_toml)
    inparams=intoml.get_input_parameters()
    root_outfiles=intoml.get_root_outfiles()
    dirname=f"{root_outfiles}_outdata"
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
        time.sleep(0.01)
    os.makedirs(dirname)
    time.sleep(0.01)
    os.chdir(dirname)
    input_paths=[]
    for p1 in intoml.get_input_paths():
        input_paths.append(f"../{p1}")
    eqcond1=EquilibriumConditions(inparams["eq"],input_paths,root_outfiles)
    eqcond1list=eqcond1.get_eq_conditions()
    output_eqcond(eqcond1list,root_outfiles)
    elements=eqcond1.get_elements()
    solver1=DefectEqSolver(inparams["host"],elements,input_paths,intoml.get_densform(),root_outfiles)
    fnout_dens_csv=root_outfiles+"_densities.csv"
    if "solver" not in inparams.keys():
        inparams["solver"]={}
    if "num_parallel" not in inparams["solver"].keys():
        inparams["solver"]["num_parallel"]=1
    if "just_plot_Edef" not in inparams["solver"].keys():
        inparams["solver"]["just_plot_Edef"]=False
    def calc_defect_densities(ieq1):
        eqc1=eqcond1list[ieq1]
        ieq1str=f"{ieq1+1:0>4}"
        dirname=f"cond{ieq1str}"
        print(f"Eq-condition-loop ({ieq1+1}/{len(eqcond1list)}) starting at {dirname}")
        os.makedirs(dirname,exist_ok=True)
        os.chdir(dirname)
        defect_densities=solver1.opt_coordinator(eqc1,inparams["solver"],root_outfiles,inparams["plot"])
        if defect_densities is None:
            os.chdir("../")
            return None
        if not inparams["solver"]["just_plot_Edef"]:
            defect_densities[0][-1]=f"{ieq1+1:04}"
            output_density_with_eqcond(defect_densities,eqc1,fnout_dens_csv)
        os.chdir("../")
        print("*"*100)
    with ProcessingPool(inparams["solver"]["num_parallel"]) as pool1:
        pool1.map(calc_defect_densities,range(len(eqcond1list)))
    if not inparams["solver"]["just_plot_Edef"]:
        fout1=open(fnout_dens_csv,"w")
        icnt1=0
        for ieq1 in range(len(eqcond1list)):
            ieq1str=f"{ieq1+1:0>4}"
            dirname1=f"cond{ieq1str}"
            fnin1=dirname1+"/"+fnout_dens_csv
            if os.path.exists(fnin1):
                fin1=open(fnin1).readlines()
                if icnt1==0:
                    for l1 in fin1:
                        fout1.write(l1)
                else:
                    fout1.write(fin1[-1])
                icnt1+=1
        fout1.close()
        inparams["plot"]["outfiles_header"]=root_outfiles
        inparams["plot"]["input_filename"]=fnout_dens_csv
        if icnt1>1:
            print("*"*100)
            plot_defect_densities(inparams["plot"])
    print("*"*100)
    print(f" Finished!")
    print("*"*100)


if __name__=="__main__":
    pydecs_main()
