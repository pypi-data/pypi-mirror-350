#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Copyright 2021 Takafumi Ogawa
# Licensed under the Apache License, Version2.0.
#-----------------------------------------------------------------------------
# Auxiliary tool of pydecs library for checking equilibrium phases
#-----------------------------------------------------------------------------
import os
import sys
import numpy as np
from scipy import interpolate

class ReferencePhases:

    def parse_composition(self,comp_in):
        comp1=[]
        ic0=0
        for ic1,c1 in enumerate(comp_in):
            if ic1!=0 and c1.isupper():
                comp1.append(comp_in[ic0:ic1])
                ic0=ic1
        comp1.append(comp_in[ic0:])
        atomList={}
        for c1 in comp1:
            elem1=""
            num1=""
            for c2 in c1:
                if c2.isdigit():
                    num1+=c2
                else:
                    elem1+=c2
            if len(num1)==0:
                num1="1"
            atomList[elem1]=int(num1)
        return atomList
    
    def check_host(self,phaseList_in):
        self.phase_host=""
        for ph1 in phaseList_in:
            if ph1["type"]=="solid*":
                self.phase_host=ph1
        if self.phase_host=="":
            print(" WARNING:: Host tag not found (inpydecs_phases.csv): solid*")
            return False
        return True

#    def get_host_composition(self):
#        return self.phase_host["composition"]
    def get_host(self,phaseList_in):
        if self.check_host(phaseList_in):
            return self.phase_host
        else:
            sys.exit()

    def prepare_finterp(self):
        for ph1 in self.phaseList:
            fn1=ph1["filename_delG"]
            if len(fn1)==0:
                ph1["delG_finterp"]="NONE"
                continue
            fin=open(self.filename_root+fn1)
            xlist=[]
            ylist=[]
            l1 = fin.readline()
            while l1:
                if l1.strip()[0]!="#":
                    l2=l1.split(",")
                    xlist.append(float(l2[0]))
                    ylist.append(float(l2[1]))
                l1 = fin.readline()
            finterp=interpolate.interp1d(xlist,ylist,kind="cubic")
            ph1["delG_finterp"]=finterp

    def parse_phases(self,filename_phases_in="inpydecs_phases.csv",elemsList_in="host",fout_lm=None):
        if not os.path.exists(filename_phases_in):
            print(" ERROR:: File not found: "+filename_phases_in)
            sys.exit()
        print(" Reading file: "+filename_phases_in)
        fout_lm.write(" Reading file: "+filename_phases_in+"\n")
        fin=open(filename_phases_in).readlines()
        columns=[ t1.strip() for t1 in fin[0].split(",")]
        column_names=set(["commentout","type","composition","energy_0K","filename_delG"])
        for c1 in column_names:
            if not c1 in columns:
                print(" ERROR:: Column not found: "+c1)
                sys.exit()
        phaseList0=[]
        for l1 in fin[1:]:
            l2=[ t1.strip() for t1 in l1.split(",")]
            ph0={}
            for i3,l3 in enumerate(l2):
                c3=columns[i3]
                if c3=="commentout":
                    ph0[c3]=l3
                if c3=="filename_delG":
                    ph0[c3]=l3
                if c3=="composition":
                    ph0[c3]=l3
                    ph0["composition_dict"]=self.parse_composition(l3)
                if c3=="type":
                    ph0[c3]=l3
                if c3=="energy_0K":
                    ph0[c3]=l3
            if not "composition" in ph0.keys()\
                or not "composition_dict" in ph0.keys()\
                or not "energy_0K" in ph0.keys()\
                or not "type" in ph0.keys():
                continue
            if len(ph0["commentout"])==0 and len(ph0["composition"])>0:
                if not ph0["type"] in ["gas","solid","solid*"]:
                   print(" WARNING:: Invalid type: "+(l3))
                   fout_lm.write(" WARNING:: Invalid type: "+(l3)+"\n")
                ph0["energy_0K"]=float_unicode(ph0["energy_0K"])
                phaseList0.append(ph0)
        self.check_host(phaseList0)
        comp_host=self.phase_host["composition"]
        comp_host_elems=set(self.phase_host["composition_dict"].keys())
        if elemsList_in=="host":
            slected_elems=comp_host_elems
        else:
            slected_elems=set(elemsList_in)
        print("   Host composition: "+self.phase_host["composition"])
        fout_lm.write("   Host composition: "+self.phase_host["composition"]+"\n")
        phaseList1=[]
        str1_solid="   Solids: "
        str1_gas="   Gases: "
        for ph1 in phaseList0:
            comp1_elems=set(ph1["composition_dict"].keys())
            elems_sum=slected_elems.union(comp1_elems)
            if len(elems_sum)<=len(slected_elems):
                phaseList1.append(ph1)
            if ph1["type"]=="solid":
                str1_solid+=f"{ph1['composition']}, "
            if ph1["type"]=="gas":
                str1_gas+=f"{ph1['composition']}, "
        if str1_solid[-2]==":":
            print(f"{str1_solid} None")
            fout_lm.write(f"{str1_solid} None\n")
        else:
            print(f"{str1_solid[:-2]}")
            fout_lm.write(f"{str1_solid[:-2]}\n")
        if str1_gas[-2]==":":
            print(f"{str1_gas} None")
            fout_lm.write(f"{str1_gas} None\n")
        else:
            print(f"{str1_gas[:-2]}")
            fout_lm.write(f"{str1_gas[:-2]}\n")
        self.phaseList=phaseList1
        print("-"*50)
        fout_lm.write("-"*50+"\n")

    def get_phaseList(self):
        return self.phaseList

    def __init__(self,elemsList_in="host",input_paths=["./"],fout_lm=None):
        fnin="NONE"
        for path1 in input_paths:
            if os.path.exists(path1+"inpydecs_phases.csv"):
                fnin=path1+"inpydecs_phases.csv"
                break
        if fnin=="NONE":
            print(" ERROR:: File not found: inpydecs_phases.csv")
            sys.exit()
        if "/" in fnin:
            self.filename_root=fnin[:fnin.rfind("/")+1]
        else:
            self.filename_root=""
        self.parse_phases(fnin,elemsList_in,fout_lm)

    def get_phasedata(self,comp_in):
        ph_target="NONE"
        for ph1 in self.phaseList:
            if ph1["composition"]==comp_in:
                ph_target=ph1
                return ph_target
        if ph_target=="NONE":
            print(" WARNING:: No data found for phase "+comp_in)
        return ph_target

    def get_singleFreeEnergy(self,comp_in,temp_in,press_in):
        ph1=self.get_phasedata(comp_in)
        energy1=ph1["energy_0K"]
        if "delG_finterp" not in ph1.keys():
            self.prepare_finterp()
        if ph1["delG_finterp"]!="NONE":
            energy1+=ph1["delG_finterp"](temp_in)
        if ph1["type"]=="gas":
            energy1+=(8.61733262e-5)*temp_in*np.log(press_in/1.0e5)
        return energy1
    
    def calc_atomChempots(self,temp_in,comp_press_list_in,bool_silent=False):
        if not bool_silent:
            print(" Calculating chemical potentials")
            print("   Temperature = "+str(temp_in))
            for (c1,p1) in comp_press_list_in:
                print("   Phase = "+str(c1)+" ; Pressure = "+str(p1))
        elems=[]
        atomnumsList=[]
        eneList=[]
        for (c1,p1) in comp_press_list_in:
            ph1=self.get_phasedata(c1)
            ene1=self.get_singleFreeEnergy(c1,temp_in,p1)
            c2=ph1["composition_dict"]
            atomnums2={}
            for e1,n1 in c2.items():
                if e1 not in elems:
                    elems.append(e1)
                atomnums2[e1]=float(n1)
            atomnumsList.append(atomnums2)
            eneList.append([ene1])
        coeffsList=[]
        if not bool_silent:
            print(" Constructed simultaneous linear equations")
        for iat1,at1 in enumerate(atomnumsList):
            coeffs=np.zeros(len(elems))
            for ie1,e1 in enumerate(elems):
                if e1 in at1.keys():
                    coeffs[ie1]=at1[e1]
            coeffsList.append(coeffs)
            str1="   "
            for ie1,e1 in enumerate(elems):
                str1+=str(coeffs[ie1])+" mu_"+e1+" + "
            str1=str1[:-3]
            str1+=" = "+str(eneList[iat1][0])
            if not bool_silent:
                print(str1)
        if len(comp_press_list_in)<len(elems):
            print(" ERROR:: The above equations cannot be solved.")
            sys.exit()
        coeffsList=np.matrix(coeffsList)
        coeffsList_inv=np.linalg.inv(coeffsList)
        muList1=coeffsList_inv*np.matrix(eneList)
        if not bool_silent:
            print(" Equations solved")
        muList2={}
        for ie1,e1 in enumerate(elems):
            muList2[e1]=float(muList1[ie1][0])
        for ie1,e1 in enumerate(elems):
            str1="   mu_"+e1+" = "+str(muList2[e1])
            if not bool_silent:
                print(str1)
        if not bool_silent:
            print("-"*50)
        return muList2

    def exists(self,phase_in):
        t1=self.get_phasedata(phase_in)
        if t1=="NONE":
            return False
        return True

    def issolid(self,phase_in):
        t1=self.get_phasedata(phase_in)
        if "solid" in t1["type"]:
            return True
        return False

def float_unicode(arg_str):
    return float(arg_str.replace(u"\u2212", "-"))
