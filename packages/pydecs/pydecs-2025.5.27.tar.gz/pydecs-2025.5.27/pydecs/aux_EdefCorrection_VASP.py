#!/usr/bin/env python
#---------------------------------------------------------------------------
# Copyright 2022 Takafumi Ogawa
# Licensed under the Apache License, Version2.0.
#---------------------------------------------------------------------------
# Auxiliary tool of pydecs library for calculating correction term
#  for defect formation energy
#---------------------------------------------------------------------------
import os,sys,copy
import numpy as np
# import scipy as sp
from scipy.special import erfc
import datetime
import toml
import matplotlib.pyplot as plt


def parseOUTCAR(OUTCAR_in,foutlog):
    foutlog.write(50*"="+"\n")
    foutlog.write("  parsing "+OUTCAR_in+"\n")
    if not os.path.exists(OUTCAR_in):
        print("ERROR::file_not_found: "+OUTCAR_in)
        sys.exit()
    latt_list=[]
    NIONS  = -1
    natoms = []
    elems = []
    zvals = []
    posi_list=[]
    pots_list=[]
    NELECT=-10
    fin=open(OUTCAR_in)
    l1=fin.readline()
    while l1:
        if len(elems)==0:
            while len(l1.strip())>4 and "POTCAR:" in l1:
                l2=l1.split()
                if "_" in l2[2]:
                    e2=l2[2].split("_")[0]
                else:
                    e2=l2[2].strip()
                elems.append(e2)
                l1=fin.readline()
        if "direct lattice vectors" in l1:
            latt_list=[]
            for i1 in range(3):
                l1=fin.readline()
                latt0=[]
                for t1 in l1.split()[:3]:
                    for t2 in t1.split():
                        if t2.rfind("-")>0:
                            t3=float(t2[t2.rfind("-"):])
                            latt0.append(t3)
                            t3=t2[:t2.rfind("-")]
                            if t3.rfind("-")>0:
                                t4=float(t3[t3.rfind("-"):])
                                latt0.append(t4)
                                t4=float(t3[:t3.rfind("-")])
                                latt0.append(t4)
                            else:
                                latt0.append(float(t3))
                        else:
                            t3=float(t2)
                            latt0.append(t3)
                latt_list.append(latt0[:3])
        if "NIONS" in l1:
            NIONS=int(l1.split("=")[-1].strip())
        if "ions per type" in l1:
            natstr1=l1.split("=")[-1].strip()
            natoms=[ int(t1) for t1 in natstr1.split()]
            if sum(natoms)!=NIONS:
                if len(natstr1)%4!=0:
                    iadd1=4-len(natstr1)%4
                    natstr1=iadd1*"0"+natstr1
                natoms=[ int(natstr1[i1:i1+4]) for i1 in range(0,len(natstr1),4)]
        if "ZVAL" in l1 and l1.find("ZVAL")<10:
            zvals=[ float(t1) for t1 in l1.split("=")[-1].split()]
        if "NELECT" in l1:
            NELECT=float(l1.split()[2])
        if "POSITION" in l1 and "TOTAL-FORCE" in l1:
            posi_list=[]
            l1=fin.readline()
            for i1 in range(sum(natoms)):
                l1=fin.readline()
                p2=[ float(t1) for t1 in l1.split()[:3]]
                posi_list.append(p2)
        if "average (electrostatic) potential at core" in l1:
            l1=fin.readline()
            l1=fin.readline()
            n1=0
            if len(pots_list)>0:
                pots_list=[]
            while n1<sum(natoms):
                l1=fin.readline()
                l2=[]
                for t2 in l1.split():
                    if "-" in t2:
                        l2.append(float(t2[t2.find("-"):]))
                for t2 in l2:
                    n1+=1
                    pots_list.append(float(t2))
        l1=fin.readline()
    NELECT_neutral=0.0
    for i1,n1 in enumerate(natoms):
        NELECT_neutral+=n1*zvals[i1]
    charge_cell=NELECT_neutral-NELECT
    if len(pots_list)!=sum(natoms):
        print("Error: missing electrostatic potentials in the OUTCAR")
        sys.exit()
    posi_list2=[]
    latt_inv=np.linalg.inv(latt_list)
    for p1 in posi_list:
        p2=np.dot(p1,latt_inv)
        posi_list2.append(p2)
    ######################
    tstr="  elements = "
    for e1 in elems:
        tstr+=e1+" "
    tstr+="\n"
    tstr+="  ions per type = "
    for n1 in natoms:
        tstr+=str(n1)+" "
    tstr+="\n"
    tstr+="  num. of valence electrons per type = "
    for n1 in zvals:
        tstr+=str(n1)+" "
    tstr+="\n"
    tstr+="  num. of electrons in cell = "+str(NELECT)+"\n"
    tstr+="  num. of electrons in neutral cell = "+str(NELECT_neutral)+"\n"
    tstr+="  charge of cell = "+str(charge_cell)+"\n"
    tstr+="  len(potentials) = "+str(len(pots_list))+"\n"
    foutlog.write(tstr)
    foutlog.flush()
    ######################
    return (np.array(latt_list),natoms,elems,posi_list2,pots_list,charge_cell)

class Ewpot_real:
    def __init__(self,latt_vect_in,dielectric_tensor_in,NumEwReal_in,foutlog):
        self.NumEwReal=NumEwReal_in
        self.latt_vect=latt_vect_in
        self.dielectric_tensor=dielectric_tensor_in
        self.dielectric_tensor_inv=np.linalg.inv(dielectric_tensor_in)
        self.rootdetdieinv=1.0/(np.linalg.det(self.dielectric_tensor)**0.5)
        latt_vect_entire=np.array(latt_vect_in)*NumEwReal_in**2
        cent_vect=[0.0,0.0,0.0]
        for i1 in range(3):
            for i2 in range(3):
                cent_vect[i1]+=0.5*latt_vect_entire[i2][i1]
        cross1=np.cross(latt_vect_in[0],latt_vect_in[1])
        cross1=cross1/np.linalg.norm(cross1)
        r1=np.abs(np.dot(cent_vect,cross1))
        cross1=np.cross(latt_vect_in[1],latt_vect_in[2])
        cross1=cross1/np.linalg.norm(cross1)
        r2=np.abs(np.dot(cent_vect,cross1))
        cross1=np.cross(latt_vect_in[2],latt_vect_in[0])
        cross1=cross1/np.linalg.norm(cross1)
        r3=np.abs(np.dot(cent_vect,cross1))
        self.Rmax=min([r1,r2,r3])
        griddist_list1=[]
        gridvect_list1=[]
        Rmax2=self.Rmax**2
        for ic1 in range(-NumEwReal_in,NumEwReal_in+1):
            for ic2 in range(-NumEwReal_in,NumEwReal_in+1):
                for ic3 in range(-NumEwReal_in,NumEwReal_in+1):
                    gridpoint=[ic1,ic2,ic3]
                    gridvect=[0.0,0.0,0.0]
                    for i1 in range(3):
                        for i2 in range(3):
                            gridvect[i2]+=gridpoint[i1]*latt_vect_in[i1][i2]
                    r_grid=gridvect[0]**2+gridvect[1]**2+gridvect[2]**2
                    if r_grid<Rmax2:
                        gridvect_list1.append(gridvect)
                        griddist_list1.append(r_grid**0.5)
        args1=np.argsort(griddist_list1)
        self.griddist=np.array([ griddist_list1[i1] for i1 in args1])
        self.gridvect=np.array([ gridvect_list1[i1] for i1 in args1])
        foutlog.write(50*"="+"\n")
        foutlog.write("  Preparing Ewald calc. (real part) \n")
        foutlog.write("    Nmax_grid = "+str(self.NumEwReal)+"\n")
        foutlog.write("    Rmax_real = "+str(self.Rmax)+"\n")
        foutlog.write("    NumSamplingPoints_real = "+str(len(self.griddist))+"\n")
        foutlog.flush()
        self.alpha=None

    def calc_Ewpot_real(self,alpha_in,foutlog,alpha_max=3.0,alpha_num=100,alpha_tol=1e-20):
        foutlog.write(50*"="+"\n")
        foutlog.write("  Calculating real-space term of Ewald energy\n")
        foutlog.write("  Determining screening parameter: alpha\n")
        foutlog.flush()
        t1=np.dot(self.dielectric_tensor_inv,self.latt_vect)
        t2=np.dot(self.latt_vect.transpose(),t1)
        alpha_estimated=np.pi**0.5/(np.linalg.norm(t2)**0.5)
        if np.isreal(alpha_in):
            self.alpha=alpha_in
            foutlog.write("    alpha is set from input to be: "+str(self.alpha)+"\n")
        elif alpha_in=="Estimate1":
            self.alpha=alpha_estimated
            foutlog.write("    alpha is estimated to be: "+str(self.alpha)+"\n")
        elif alpha_in=="Search":
            alpha_list=np.linspace(0.0,alpha_max,alpha_num)
            pot_list=[]
            potlast_list=[]
            for a1 in alpha_list:
                pot1=0.0
                for iv1,v1 in enumerate(self.gridvect):
                    d1=self.griddist[iv1]
                    if d1<1e-5:
                        continue
                    t1=np.dot(self.dielectric_tensor_inv,v1)
                    t2=np.dot(v1.transpose(),t1)**0.5
                    t3=self.rootdetdieinv*self.rootdetdieinv*erfc(a1*t2)/t2
                    pot1+=t3
                pot_list.append(pot1)
                potlast_list.append(t3/pot_list[0])
            for ia1,a1 in enumerate(alpha_list):
                if potlast_list[ia1] < alpha_tol:
                    self.alpha=a1
                    break
            for ia1,a1 in enumerate(alpha_list):
                if a1>alpha_estimated:
                    pot_estimated=pot_list[ia1]
                    break
            plt.close()
            plt.subplot(2,1,1)
            plt.tick_params(axis="both",direction="in",top=True,right=True)
            plt.plot(alpha_list,pot_list,lw=2.0,c="k")
            plt.yscale("log")
            plt.axvline(alpha_estimated,c="b",lw=2.0,ls="--")
            plt.text(alpha_estimated+alpha_max*0.01,pot_estimated,f"alpha_estimated = {alpha_estimated:.4}",color="b")
            plt.xlim([0.0,alpha_max])
            plt.ylabel("Normalized Epot_real")
            plt.subplot(2,1,2)
            plt.tick_params(axis="both",direction="in",top=True,right=True)
            plt.plot(alpha_list,potlast_list,c="k")
            plt.yscale("log")
            plt.xlim([alpha_list[0],alpha_list[-1]])
            plt.ylim([alpha_tol**2,max(potlast_list)])
            plt.axvline(alpha_estimated,c="b",lw=2.0,ls="--")
            plt.axhline(alpha_tol,c="r",lw=2.0,ls=":")
            plt.text(self.alpha+alpha_max*0.01,alpha_tol*10,"tol = "+str(alpha_tol),color="r")
            plt.text(alpha_max*0.01,alpha_tol**2*100,f"alpha_searched = {self.alpha:.4}",color="r")
            plt.scatter([self.alpha],[alpha_tol],marker="o",edgecolors="fuchsia",linewidth=1,facecolor="pink",s=80)
            plt.xlabel("alpha")
            plt.ylabel("Contribution of \nthe outermost grid-point \n to the normalized Epot_real \n scaled by the value at alpha=0.0")
            plt.savefig("outfig_Ewald_real_alphaSearch.png",bbox_inches='tight',dpi=500)
            foutlog.write("    alpha is determined through systematic calculations to be : "+str(self.alpha)+"\n")
        foutlog.flush()
        
        # foutlog.write("  Calculating Ew_pot_real with alpha = "+str(self.alpha)+"\n")
        pot_list=[]
        for iv1,v1 in enumerate(self.gridvect):
            d1=self.griddist[iv1]
            if d1<1e-5:
                pot_list.append(0.0)
                continue
            t1=np.dot(self.dielectric_tensor_inv,v1)
            t2=np.dot(v1.transpose(),t1)**0.5
            t3=self.rootdetdieinv*erfc(self.alpha*t2)/t2
            pot_list.append(pot_list[-1]+t3)
        pot_list=np.array(pot_list)
        Epot_real=pot_list[-1]
        plt.close()
        plt.tick_params(axis="both",direction="in",top=True,right=True)
        plt.plot(self.griddist,(pot_list-Epot_real)/Epot_real,lw=2.0,c="k")
        # plt.axhline(0.0,c="r",lw=2.0,ls=":")
        # plt.axhline(Ewpot_real,c="r",lw=2.0,ls=":")
        plt.yscale("symlog",linthresh=1e-30)
        # plt.xscale("log")
        plt.ylabel("Convergence of Epot_real")
        plt.xlabel("Radius for summation in real space")
        plt.savefig("outfig_Ewald_real_analysis.png",bbox_inches='tight',dpi=500)
        return Epot_real


    def calcpot_atom(self,relvect_in):
        pot1=0.0
        for iv1,v1 in enumerate(self.gridvect):
            v2=v1-relvect_in
            if np.linalg.norm(v2)<1e-10:
                print("  Warning!!!!!!")
            t1=np.dot(self.dielectric_tensor_inv,v2)
            t2=np.dot(v2.transpose(),t1)**0.5
            if np.abs(t2)>1e-10:
                t3=self.rootdetdieinv*erfc(self.alpha*t2)/t2
                pot1+=t3
        return pot1


class Ewpot_recip:
    def __init__(self,latt_vect_in,dielectric_tensor_in,alpha_in,Nmax_recip_in,foutlog):
        self.latt_vect=latt_vect_in
        self.dielectric_tensor=dielectric_tensor_in
        self.alpha=alpha_in
        self.NumEwRecip=Nmax_recip_in
        self.volume=np.abs(np.dot(np.cross(latt_vect_in[0],latt_vect_in[1]),latt_vect_in[2]))
        self.recip_vect=np.array([2.0*np.pi*np.cross(latt_vect_in[1],latt_vect_in[2]),
                2.0*np.pi*np.cross(latt_vect_in[2],latt_vect_in[0]),
                2.0*np.pi*np.cross(latt_vect_in[0],latt_vect_in[1])])/self.volume
        recip_vect_all=self.recip_vect*self.NumEwRecip
        cent_vect=[0.0,0.0,0.0]
        for i1 in range(3):
            for i2 in range(3):
                cent_vect[i1]+=0.5*recip_vect_all[i2][i1]
        cross1=np.cross(recip_vect_all[0],recip_vect_all[1])
        cross1=cross1/np.linalg.norm(cross1)
        r1=np.abs(np.dot(cent_vect,cross1))
        cross1=np.cross(recip_vect_all[1],recip_vect_all[2])
        cross1=cross1/np.linalg.norm(cross1)
        r2=np.abs(np.dot(cent_vect,cross1))
        cross1=np.cross(recip_vect_all[2],recip_vect_all[0])
        cross1=cross1/np.linalg.norm(cross1)
        r3=np.abs(np.dot(cent_vect,cross1))
        self.Kmax=min([r1,r2,r3])
        foutlog.write(50*"="+"\n")
        foutlog.write("  Preparing Ewald calc. (reciprocal part) \n")
        foutlog.write("    Nmax_grid = "+str(self.NumEwRecip)+"\n")
        foutlog.write("    Kmax_recip = "+str(self.Kmax)+"\n")
        foutlog.write("  Calculating Epot_recip  \n")
        foutlog.flush()
        griddist_list1=[]
        gridvect_list1=[]
        gridpot_list1=[]
        coeff1=4.0*np.pi/self.volume
        coeff2=-1.0/4.0/self.alpha**2
        for ic1 in range(-self.NumEwRecip,self.NumEwRecip+1):
            for ic2 in range(-self.NumEwRecip,self.NumEwRecip+1):
                for ic3 in range(-self.NumEwRecip,self.NumEwRecip+1):
                    gridpoint=[ic1,ic2,ic3]
                    gridvect=np.zeros(3)
                    for i1 in range(3):
                        for i2 in range(3):
                            gridvect[i2]+=gridpoint[i1]*self.recip_vect[i1][i2]
                    r_grid=(gridvect[0]**2+gridvect[1]**2+gridvect[2]**2)**0.5
                    if r_grid<1e-6:
                        continue
                    if r_grid<self.Kmax:
                        griddist_list1.append(r_grid)
                        gridvect_list1.append(gridvect)
                        t1=np.dot(self.dielectric_tensor,gridvect)
                        t2=np.dot(gridvect.transpose(),t1)
                        t3=coeff1*np.exp(coeff2*t2)/t2
                        gridpot_list1.append(t3)
        args1=np.argsort(griddist_list1)
        self.griddist=np.array([ griddist_list1[i1] for i1 in args1])
        self.gridvect=np.array([ gridvect_list1[i1] for i1 in args1])
        self.gridpot=np.array([ gridpot_list1[i1] for i1 in args1])
        foutlog.write("    NumSamplingPoints_recip = "+str(len(self.griddist))+"\n")
        foutlog.write("  Calculating Ew_pot_recip with alpha = "+str(self.alpha)+"\n")
        foutlog.flush()
        gridpot_accum=[self.gridpot[0]]
        for i1 in range(1,len(self.gridpot)):
            gridpot_accum.append(gridpot_accum[i1-1]+self.gridpot[i1])
        self.Ewpot=gridpot_accum[-1]
        
        plt.close()
        plt.tick_params(axis="both",direction="in",top=True,right=True)
        plt.plot(self.griddist,(gridpot_accum-self.Ewpot)/self.Ewpot,lw=2.0,c="k")
        # plt.axhline(0.0,c="r",lw=2.0,ls=":")
        plt.yscale("symlog",linthresh=1e-30)
        plt.ylabel("Convergence of Epot_recip")
        plt.xlabel("Radius for summation in reciprocal space")
        plt.savefig("outfig_Ewald_recip_analysis.png",bbox_inches='tight',dpi=500)
        foutlog.flush()

    def calcpot_atom(self,relvect_in):
        pot1=0.0
        for i1 in range(len(self.gridpot)):
            pot1+=self.gridpot[i1]*np.exp((0.0+1.0j)*np.dot(self.gridvect[i1],relvect_in))
        if pot1.imag>1e-10:
            print("  Warning: pot_recip of an atom has a large imaginary component.")
            print("    imag(pot_recip) = "+str(pot1.imag))
        return pot1.real


str_input="""#########################################
### Input for pydecs-EdefCorrection-VASP
#########################################

### This block must be set
  pathOUTCAR_bulk   = "OUTCAR_bulk"
  pathOUTCAR_defect = "OUTCAR_def"
  dielectric_tensor = [1.0,2.0,3.0]


#########################################
###  Bellows are optional!

### Tolerance for atomic-position shifts during relaxation
#   rtol_vac = 1.2

### When explicitly setting the defect position and charge states
#   defect_position_direct = [0.0,0.0,0.0]
#   charge_state = -1

### Settings Ewald-summation parameters

#   Ewald_alpha = "Search"      #<- Searching (default)
#   Ewald_alpha = "Estimated"   #<- Estimated parameter by  sqrt(pi)/L
#   Ewald_alpha = 0.2           #<- Direct setting

#   Ewald_real_Nmax = 10     
#   Ewald_recip_Nmax = 10

#   Ewald_alphaSearch_max = 4.0      # Maximum alpha in the searching algorithm
#   Ewald_alphaSearch_num = 100      # Dividing number of alpha in the searching algorithm
#   Ewald_alphaSearch_tol = 1e-20    # Energy tolerance in the searching algorithm
"""

def calcEdefCorrectionVASP():
    filename_in="inpydecs_Edef.toml"
    if not os.path.exists(filename_in):
        print("  Input-file not_found: "+filename_in)
        print("  Creating the input-file, please set the following part at the minimum. ")
        print("    pathOUTCAR_bulk   = \"OUTCAR_bulk\" ")
        print("    pathOUTCAR_defect = \"OUTCAR_def\" ")
        print("    dielectric_tensor = [1.0,2.0,3.0] ")
        fout=open("inpydecs_Edef.toml","w")
        fout.write(str_input)
        fout.close()
        sys.exit()
    
    input_parameters=toml.load(filename_in)
    fn_outlog="out_pydecs_Edef.txt"
    foutlog=open(fn_outlog,"w")
    foutlog.write("  Starting pydecs-EdefCorrection-VASP\n")
    print("  Starting pydecs-EdefCorrection-VASP")
    print("  Results are written in the output file: "+fn_outlog)
    print(50*"=")
    dt1=str(datetime.datetime.today())
    dt2=dt1[:dt1.rfind(":")]
    foutlog.write("     at "+str(dt2)+"\n")
    
    foutlog.write(50*"="+"\n")
    foutlog.write("  Input file: "+filename_in+"\n")
    foutlog.write("  Output file: "+fn_outlog+"\n")

    foutlog.write(50*"="+"\n")
    if "dielectric_tensor" in input_parameters:
        dielectric_tensor0=input_parameters["dielectric_tensor"]
    else:
        print("  ERROR:: dielectric_tensor is not found in the input file")
        sys.exit()
    dielectric_tensor=np.array([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
    if len(dielectric_tensor0)==1:
        dielectric_tensor[0][0]=dielectric_tensor0[0]
        dielectric_tensor[1][1]=dielectric_tensor0[0]
        dielectric_tensor[2][2]=dielectric_tensor0[0]
    elif len(dielectric_tensor0)==3:
        dielectric_tensor[0][0]=dielectric_tensor0[0]
        dielectric_tensor[1][1]=dielectric_tensor0[1]
        dielectric_tensor[2][2]=dielectric_tensor0[2]
    elif len(dielectric_tensor0)==9:
        dielectric_tensor[0][0]=dielectric_tensor0[0]
        dielectric_tensor[0][1]=dielectric_tensor0[1]
        dielectric_tensor[0][2]=dielectric_tensor0[2]
        dielectric_tensor[1][0]=dielectric_tensor0[3]
        dielectric_tensor[1][1]=dielectric_tensor0[4]
        dielectric_tensor[1][2]=dielectric_tensor0[5]
        dielectric_tensor[2][0]=dielectric_tensor0[6]
        dielectric_tensor[2][1]=dielectric_tensor0[7]
        dielectric_tensor[2][2]=dielectric_tensor0[8]
    else:
        print("  ERROR:: vecter length of dielectric_tensor should be 1, 3, or 9")
        sys.exit()

    foutlog.write("  dielectric_tesor\n")
    for i1 in range(3):
        str1="    "
        for i2 in range(3):
            str1+=str(dielectric_tensor[i1][i2])+" , "
        foutlog.write(str1[:-2]+"\n")
    
    pathOUTCAR_bulk=input_parameters["pathOUTCAR_bulk"]
    pathOUTCAR_defect=input_parameters["pathOUTCAR_defect"]
    # readingOUTCAR
    (latt_bulk,natoms_bulk,elems_bulk,posi_bulk,pot_bulk,qcell_bulk)=parseOUTCAR(pathOUTCAR_bulk,foutlog)
    (latt_def,natoms_def,elems_def,posi_def,pot_def,qcell_def)=parseOUTCAR(pathOUTCAR_defect,foutlog)
    # sys.exit()
    foutlog.write(50*"="+"\n")
    # check lattice
    for i1 in range(3):
        for i2 in range(3):
            d1=abs(latt_bulk[i1][i2]-latt_def[i1][i2])
            if d1>0.000001:
                print("  ERROR:: Lattice mismatch between bulk and defect cells")
                print("  Lattice vecter of bulk cell")
                print(latt_bulk)
                print("  Lattice vecter of defect cell")
                print("  Defect",latt_def)
                sys.exit()
    foutlog.write("  Lattice vectors are identical between bulk and defect cells.\n")
    for i1 in range(3):
        str1="    "
        for i2 in range(3):
            str1+=str(latt_bulk[i1][i2])+"  "
        foutlog.write(str1+"\n")
    # set charge_state
    if abs(qcell_bulk)>0.00001:
        print("  ERROR:: Charge of bulk cell is not neutral")
        sys.exit()
    charge_state=qcell_def
    # foutlog.write("  charge_state (from OUTCAR) = "+str(qcell_def)+"\n")
    if "charge_state" in input_parameters:
        print("  WARNING:: charge_state is overwitten by input file")
        foutlog.write("  WARNING::  charge_state is overwitten by input file\n")
        charge_state=input_parameters["charge_state"]
        if charge_state != qcell_def:
            print("  WARNING:: charge_state in input is not equal to charge in defect cell")
            foutlog.write("  WARNING:: charge_state in input is not equal to charge in defect cell\n")
    foutlog.write("  charge_state (adopted) = "+str(charge_state)+"\n")
    if np.fabs(charge_state)<1e-10:
        print("  ERROR:: Electrostatic energy cannot be calculated because charge_state is zero!")
        foutlog.write("  ERROR:: Electrostatic energy cannot be calculated because charge_state is zero!\n")
        sys.exit()
    # making elemslist
    elemslist_bulk=[]
    for i1,n1 in enumerate(natoms_bulk):
        for i2 in range(n1):
            elemslist_bulk.append(elems_bulk[i1])
    elemslist_def=[]
    for i1,n1 in enumerate(natoms_def):
        for i2 in range(n1):
            elemslist_def.append(elems_def[i1])
    ### Determining defect position
    rtol_vac=1.2
    if "rtol_vac" in input_parameters:
        rtol_vac=input_parameters["rtol_vac"]
    def0_id=[]
    def0_posi=[]
    def0_elems=[]
    potdiff=[]
    for i1 in range(sum(natoms_def)):
        potdiff.append(None)
    for ip1,p1 in enumerate(posi_bulk):
        rdiff_list=[]
        for ip2,p2 in enumerate(posi_def):
            pdiff1=[p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]]
            rdiff2min=1e10
            for s0 in [-1,0,1]:
                for s1 in [-1,0,1]:
                    for s2 in [-1,0,1]:
                        pdiff3=[pdiff1[0]+s0,pdiff1[1]+s1,pdiff1[2]+s2]
                        pdiff2=[0.0,0.0,0.0]
                        for i1 in range(3):
                            for i2 in range(3):
                                pdiff2[i2]+=pdiff3[i1]*latt_def[i1][i2]
                        rdiff2=(pdiff2[0]**2+pdiff2[1]**2+pdiff2[2]**2)**0.5
                        if rdiff2<rdiff2min:
                            rdiff2min=rdiff2
            rdiff_list.append(rdiff2min)
        # print(rdiff_list)
        args_rdiff=np.argsort(rdiff_list)
        if min(rdiff_list)>rtol_vac:
            def0_posi.append(copy.copy(p1))
            def0_elems.append("Vac_"+elemslist_bulk[ip1])
            continue
        e1=elemslist_bulk[ip1]
        pot1=pot_bulk[ip1]
        for ip2 in args_rdiff:
            # ip2=args_rdiff[0]
            e2=elemslist_def[ip2]
            pot2=pot_def[ip2]
            if e1!=e2:
                def0_id.append(ip2)
                def0_posi.append(copy.copy(posi_def[ip2]))
                deflabel=e2+"_"+e1
                def0_elems.append(deflabel)
            else:
                if potdiff[ip2]==None:
                    potdiff[ip2]=pot1-pot2
                    break
            # potdiff[ip1]=pot1-pot2
    plt.axhline(0.0,c="k",lw=2.0,ls=":")
    if None in potdiff:
        interstitial_indexes=[i1 for i1,pot1 in enumerate(potdiff) if (pot1==None and i1 not in def0_id)]
        for ip2 in interstitial_indexes:
            e2=elemslist_def[ip2]
            def0_posi.append(copy.copy(posi_def[ip2]))
            deflabel=e2+"_int"
            def0_elems.append(deflabel)
    ### output defects
    foutlog.write(50*"="+"\n")
    posi_def0=[]
    if "defect_position_direct" in input_parameters:
        print("  WARNING::  defect position is overwritten by defect_position_direct param.")
        foutlog.write("  WARNING:: defect position is overwritten by defect_position_direct param.\n")
        p1=input_parameters["defect_position_direct"]
        if len(p1)==1:
            foutlog.write("    Set as the positino for atom-id: "+str(p1[0])+"\n")
            posi_def0=posi_bulk[p1[0]-1]
        else:
            posi_def0=p1
    else:
        foutlog.write("  List of detected defects\n")
        averaged_posi=None
        if len(def0_elems)==0:
            print("  Error:: no defect is detected.")
            print("    Please try to adjust rtol_vac-parameter in the input file")
            foutlog.write("  Error:: no defect is detected\n")
            foutlog.write("    Try to adjust rtol_vac-parameter in the input file\n")
            sys.exit()
        if len(def0_elems)>1:
            print("  Warning:: complex defects are detected.")
            foutlog.write("    Warning:: complex defects are detected.\n")
            foutlog.write("      When this is unexpected, ...\n")
            foutlog.write("      (1) check the structure for confirming your expection.\n")
            foutlog.write("      (2) try to adjust rtol_vac-parameter in the input file.\n")
        foutlog.write("    The number of defects = "+str(len(def0_elems))+"\n")
        foutlog.write("    Defect_position_direct("+def0_elems[0]+") = "+str(def0_posi[0][0])+" "+str(def0_posi[0][1])+" "+str(def0_posi[0][2])+"\n")
        averaged_posi=[0.0,0.0,0.0] 
        p1=def0_posi[0]
        for id2 in range(1,len(def0_elems)):
            p2=def0_posi[id2]
            foutlog.write("    Defect_position_direct("+def0_elems[id2]+") = "+str(p2[0])+" "+str(p2[1])+" "+str(p2[2])+"\n")
            pdiff1=[p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]]
            rdiff2min=1e10
            for s0 in [-1,0,1]:
                for s1 in [-1,0,1]:
                    for s2 in [-1,0,1]:
                        pdiff3=[pdiff1[0]+s0,pdiff1[1]+s1,pdiff1[2]+s2]
                        pdiff2=[0.0,0.0,0.0]
                        for i1 in range(3):
                            for i2 in range(3):
                                pdiff2[i2]+=pdiff3[i1]*latt_def[i1][i2]
                        rdiff2=(pdiff2[0]**2+pdiff2[1]**2+pdiff2[2]**2)**0.5
                        if rdiff2<rdiff2min:
                            rdiff2min=rdiff2
                            pdiff3min=copy.copy(pdiff3)
            for i1 in range(3):
                averaged_posi[i1]+=pdiff3min[i1]
        for i1 in range(3):
            averaged_posi[i1]=p1[i1]+averaged_posi[i1]/len(def0_elems)
        if len(def0_elems)>1:
            foutlog.write("    Defect_position_direct(ave.) = "+str(averaged_posi[0])+" "+str(averaged_posi[1])+" "+str(averaged_posi[2])+"\n")
        posi_def0=averaged_posi
    foutlog.write("  Defect_position_direct(adopted) = "+str(posi_def0[0])+" "+str(posi_def0[1])+" "+str(posi_def0[2])+"\n")
    print("  Defect_position_direct(adopted) = "+str(posi_def0[0])+" "+str(posi_def0[1])+" "+str(posi_def0[2]))
    # foutlog.write(50*"="+"\n")
    foutlog.flush()
    ##### rdist from defect
    rdist=[]
    for ip2,p2 in enumerate(posi_def):
        if potdiff[ip2]==None:
            rdist.append(0.0)
        else:
            pdiff1=[p2[0]-posi_def0[0],p2[1]-posi_def0[1],p2[2]-posi_def0[2]]
            rdiff2min=1e10
            for s0 in [-1,0,1]:
                for s1 in [-1,0,1]:
                    for s2 in [-1,0,1]:
                        pdiff3=[pdiff1[0]+s0,pdiff1[1]+s1,pdiff1[2]+s2]
                        pdiff2=[0.0,0.0,0.0]
                        for i1 in range(3):
                            for i2 in range(3):
                                pdiff2[i2]+=pdiff3[i1]*latt_def[i1][i2]
                        rdiff2=(pdiff2[0]**2+pdiff2[1]**2+pdiff2[2]**2)**0.5
                        if rdiff2<rdiff2min:
                            rdiff2min=rdiff2
                            pdiff3min=copy.copy(pdiff3)
            rdist.append(rdiff2min)
    rmax=np.max(rdist)

    #### calc point-charge potential and energy
    Ewald_real_Nmax=3
    if "Ewald_real_Nmax" in input_parameters:
        Ewald_real_Nmax=input_parameters["Ewald_real_Nmax"]
    Ewald_recip_Nmax=6
    if "Ewald_recip_Nmax" in input_parameters:
        Ewald_recip_Nmax=input_parameters["Ewald_recip_Nmax"]
    epot_real=Ewpot_real(latt_bulk,dielectric_tensor,Ewald_real_Nmax,foutlog)
    alpha="Search"
    if "Ewald_alpha" in input_parameters:
        alpha=input_parameters["Ewald_alpha"]
    alpha_max=5.0
    alpha_num=100
    alpha_tol=1e-20
    if "Ewald_alphaSearch_max" in input_parameters:
        alpha_max=input_parameters["Ewald_alphaSearch_max"]
    if "Ewald_alphaSearch_num" in input_parameters:
        alpha_num=input_parameters["Ewald_alphaSearch_num"]
    if "Ewald_alphaSearch_tol" in input_parameters:
        alpha_tol=input_parameters["Ewald_alphaSearch_tol"]
    # eps_vacuum=8.9541878128e-12 #F/m=C/(V*m)
    eps_vacuum=8.85418781762039e-12 #F/m=C/(V*m)
    charge_elem=1.602176634e-19 # C
    coeff1=charge_elem*charge_state/(4.0*np.pi*eps_vacuum)/1e-10
    coeff2=0.5*coeff1*charge_state
    Ereal=coeff2*epot_real.calc_Ewpot_real(alpha,foutlog,alpha_max,alpha_num,alpha_tol)
    epot_recip=Ewpot_recip(latt_bulk,dielectric_tensor,epot_real.alpha,Ewald_recip_Nmax,foutlog)
    Erecip=coeff2*epot_recip.Ewpot
    Ebg=-coeff2*np.pi/(epot_recip.volume*epot_real.alpha**2)
    Eself=-2.0*coeff2*epot_real.alpha*epot_real.rootdetdieinv/(np.pi**0.5)
    Etot=Ereal+Erecip+Ebg+Eself # [eV]
    foutlog.write(50*"="+"\n")
    foutlog.write("  Ecorr[point charge] = "+str(Etot)+" [eV] \n")
    foutlog.write(f"     Ereal  = {Ereal:16.12f} [eV] \n")
    foutlog.write(f"     Erecip = {Erecip:16.12f} [eV] \n")
    foutlog.write(f"     Ebg    = {Ebg:16.12f} [eV] \n")
    foutlog.write(f"     Eself  = {Eself:16.12f} [eV] \n")
    foutlog.flush()
    
    #### calc point-charge potential for each atom
    foutpot=open("out_pot.csv","w")
    foutpot.write("# atom-id, element, distance from defect position, potential difference in DFT, potential of point-charge system, difference between DFT and model potentials, alignment-like term\n")
    pot_Model=[]
    pot_residual=[]
    for ip1,p1 in enumerate(posi_def):
        flag_defsite=False
        for ip0,p0 in enumerate(def0_posi):
            pdiff1=np.array([p1[0]-p0[0],p1[1]-p0[1],p1[2]-p0[2]])
            rdiff2min=1e10
            for s0 in [-1,0,1]:
                for s1 in [-1,0,1]:
                    for s2 in [-1,0,1]:
                        pdiff3=[pdiff1[0]+s0,pdiff1[1]+s1,pdiff1[2]+s2]
                        pdiff2=[0.0,0.0,0.0]
                        for i1 in range(3):
                            for i2 in range(3):
                                pdiff2[i2]+=pdiff3[i1]*latt_def[i1][i2]
                        rdiff2=(pdiff2[0]**2+pdiff2[1]**2+pdiff2[2]**2)**0.5
                        if rdiff2<rdiff2min:
                            rdiff2min=rdiff2
                            pdiff3min=copy.copy(pdiff3)
            relvect=np.dot(pdiff3min,latt_def)
            r_relvect=np.linalg.norm(relvect)
            if r_relvect<1e-10:
                flag_defsite=True
        if flag_defsite:
            pot_Model.append(None)
            pot_residual.append(None)
            continue
        pdiff1=np.array([p1[0]-posi_def0[0],p1[1]-posi_def0[1],p1[2]-posi_def0[2]])
        rdiff2min=1e10
        for s0 in [-1,0,1]:
            for s1 in [-1,0,1]:
                for s2 in [-1,0,1]:
                    pdiff3=[pdiff1[0]+s0,pdiff1[1]+s1,pdiff1[2]+s2]
                    pdiff2=[0.0,0.0,0.0]
                    for i1 in range(3):
                        for i2 in range(3):
                            pdiff2[i2]+=pdiff3[i1]*latt_def[i1][i2]
                    rdiff2=(pdiff2[0]**2+pdiff2[1]**2+pdiff2[2]**2)**0.5
                    if rdiff2<rdiff2min:
                        rdiff2min=rdiff2
                        pdiff3min=copy.copy(pdiff3)
        relvect=np.dot(pdiff3min,latt_def)
        r_relvect=np.linalg.norm(relvect)
        pot_real=epot_real.calcpot_atom(relvect)
        pot_recip=epot_recip.calcpot_atom(relvect)
        pottot=coeff1*(pot_real+pot_recip+Ebg/coeff2)
        pot_Model.append(pottot)
        pot_residual.append(potdiff[ip1]-pottot)
        str1=str(ip1+1)+","+elemslist_def[ip1]+","+str(rdist[ip1])
        str1+=","+str(potdiff[ip1])+","+str(pottot)
        str1+=","+str(pot_residual[ip1])+","+str(-1.0*pot_residual[ip1]*charge_state)
        foutpot.write(str1+"\n")
    foutpot.close()

    args1=np.argsort(-np.array(rdist))
    rdist_sorted=np.array([ rdist[i1] for i1 in args1])
    pot_residual_sorted=np.array([ pot_residual[i1] for i1 in args1])
    potacc=0.0
    pot_alignment_sorted=[]
    foutpot=open("out_alighment_sorted.csv","w")
    foutpot.write("# distance from defect position, alignment-like term, averaged alignment-like term for atoms with a larger distance than the first-colomn distance\n")
    for ip1,pot1 in enumerate(pot_residual_sorted):
        if pot1 is None:
            potacc+=0.0
            pot2=None
        else:
            potacc+=pot1
            pot2=-1.0*pot1*charge_state
        pot_alignment_sorted.append(-1.0*potacc/(ip1+1.0)*charge_state)
        if pot1 is not None:
            str1=str(rdist_sorted[ip1])+","+str(pot2)+","+str(pot_alignment_sorted[ip1])
            foutpot.write(str1+"\n")
    foutpot.close()
    r_alignmentTerm=0.5*max([np.linalg.norm(latt_def[0]),
        np.linalg.norm(latt_def[1]),np.linalg.norm(latt_def[2])])
    alignmentTerm=None
    for ir1,r1 in enumerate(rdist_sorted):
        if r1<r_alignmentTerm:
            alignmentTerm=pot_alignment_sorted[ir1]
            break
    plt.close()
    plt.figure(figsize=(4,8))
    plt.subplot(3,1,1)
    plt.tick_params(axis="both",direction="in",top=True,right=True)
    plt.scatter(rdist,potdiff,marker="s")
    plt.scatter(rdist,pot_Model,marker="o")
    plt.axhline(0.0,c="k",lw=1.0,ls="--")
    plt.ylabel("$\Delta$V [eV]")
    plt.xlim([0,rmax+1])
    plt.legend(["DFT","Model"])
    plt.subplot(3,1,2)
    plt.tick_params(axis="both",direction="in",top=True,right=True)
    plt.scatter(rdist,pot_residual,marker="^")
    plt.xlim([0,rmax+1])
    plt.axhline(0.0,c="k",lw=1.0,ls="--")
    plt.ylabel("Difference in potential [eV]")
    plt.subplot(3,1,3)
    plt.tick_params(axis="both",direction="in",top=True,right=True)
    plt.scatter(rdist_sorted,pot_alignment_sorted,marker="o",s=20,color="b")
    plt.plot(rdist_sorted,pot_alignment_sorted,"--",color="c")
    plt.axhline(0.0,c="k",lw=1.0,ls="--")
    plt.axvline(r_alignmentTerm,c="r",lw=2.0,ls=":")
    plt.axhline(alignmentTerm,c="r",lw=2.0,ls=":")
    plt.xlim([0,rmax+1])
    plt.xlabel("Distance from defect site [$\mathrm{\AA}$]")
    plt.ylabel("Potential alighment [eV]")
    plt.savefig("outfig_Epot_alignments.png",bbox_inches='tight',dpi=500)
    
    foutlog.write(50*"="+"\n")
    foutlog.write("  Minimum R for alignment-like term = "+str(r_alignmentTerm)+"\n")
    foutlog.write("  Alignment-like term = "+str(alignmentTerm)+"\n")
    foutlog.write(50*"="+"\n")
    foutlog.write("  Ecorr = -E_PointCharge + E_alignment\n")
    foutlog.write("        = "+str(-Etot+alignmentTerm)+"\n")
    
    foutlog.write(50*"="+"\n")
    foutlog.close()
    for l1 in open(fn_outlog):
        print(l1[:-1])
    

if __name__=="__main__":
    calcEdefCorrectionVASP()



