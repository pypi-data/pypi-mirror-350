#!/usr/bin/env python
#---------------------------------------------------------------------------
# Copyright 2021 Takafumi Ogawa
# Licensed under the Apache License, Version2.0.
#---------------------------------------------------------------------------
# Auxiliary tool of pydecs library for producing inpydecs_dos.csv file
#---------------------------------------------------------------------------
import os,sys
import datetime
import matplotlib.pyplot as plt
import math 

def convDOSfromVASP():
    print(" Preparing \"inpydecs_dos.csv\" from VASP-output files in the current directory.")
    print(" Parsed files: DOSCAR, OUTCAR, EIGENVAL")
    if not os.path.exists("OUTCAR"):
        print("ERROR::file_not_found: OUTCAR")
        sys.exit()
    if not os.path.exists("EIGENVAL"):
        print("ERROR::file_not_found: EIGANVAL")
        sys.exit()
    if not os.path.exists("DOSCAR"):
        print("ERROR::file_not_found: DOSCAR")
        sys.exit()


    fin=open("OUTCAR")
    l1=fin.readline()
    NEDOS=-1
    NIONS=-1
    ISPIN=-1
    LNONCOLLINEAR=-1
    natoms=[]
    elems=[]
    NBANDS=-1
    NKPTS=-1
    volume=-1
    while l1:
        if "number of dos" in l1:
            l2=l1.split()
            NEDOS=int(l2[5])
            NIONS=int(l2[-1])
        if "ISPIN" in l1:
            l2=l1.split()
            ISPIN=int(l2[2])
        if "LNONCOLLINEAR" in l1:
            l2=l1.split()
            LNONCOLLINEAR=l2[2]
        if "ions per type" in l1:
            l2=l1.split()
            for t2 in l2[4:]:
                natoms.append(int(t2))
        if "POSCAR =" in l1:
            l2=l1.split()
            for t2 in l2[2:]:
                elems.append(t2)
        if "NKPTS" in l1 and "NBANDS" in l1:
            l2=l1.split()
            NKPTS=int(l2[3])
            NBANDS=int(l2[-1])
        if "direct lattice vectors" in l1:
            #l2=fin.readline().split()
            #latt1=[float(t2) for t2 in l2[:3]]
            #l2=fin.readline().split()
            #latt2=[float(t2) for t2 in l2[:3]]
            #l2=fin.readline().split()
            #latt3=[float(t2) for t2 in l2[:3]]
            #out23=[latt2[1]*latt3[2]-latt2[2]*latt3[1],
            #       latt2[2]*latt3[0]-latt2[0]*latt3[2],
            #       latt2[0]*latt3[1]-latt2[1]*latt3[0]]
            #volume=out23[0]*latt1[0]+out23[1]*latt1[1]+out23[2]*latt1[2]
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
            out23=[latt_list[1][1]*latt_list[2][2]-latt_list[1][2]*latt_list[2][1],
                   latt_list[1][2]*latt_list[2][0]-latt_list[1][0]*latt_list[2][2],
                   latt_list[1][0]*latt_list[2][1]-latt_list[1][1]*latt_list[2][0]]
            volume=out23[0]*latt_list[0][0]+out23[1]*latt_list[0][1]+out23[2]*latt_list[0][2]
        l1=fin.readline()
    NSPIN=-1
    if LNONCOLLINEAR=="T":
        NSPIN=3
    if LNONCOLLINEAR=="F":
        NSPIN=ISPIN
    fin=open("EIGENVAL")
    for i1 in range(6):
        l1=fin.readline()
    E_VBM=-1.0e10
    E_CBM= 1.0e6
    for i1 in range(NKPTS):
        l1=fin.readline()
        l1=fin.readline()
        for i2 in range(NBANDS):
            l2=fin.readline().split()
            elist=[float(t2) for t2 in l2[1:1+NSPIN]]
            occlist=[float(t2) for t2 in l2[1+NSPIN:1+2*NSPIN]]
            for i3,occ3 in enumerate(occlist):
                if occ3 >0.5:
                    if E_VBM<elist[i3]:
                        E_VBM=elist[i3]
                elif occ3<0.1:
                    if E_CBM>elist[i3]:
                        E_CBM=elist[i3]
    fin=open("DOSCAR")
    for i1 in range(6):
        l1=fin.readline()
    enelist=[]
    doslist=[]
    l1=fin.readline()
    for i1 in range(NEDOS-1):
        l2=fin.readline().split()
        enelist.append(float(l2[0]))
        dsum=0.0
        for d1 in l2[1:1+NSPIN]:
            dsum+=float(d1)
        doslist.append(dsum)
    E_gap=E_CBM-E_VBM

    fnout_dos = "inpydecs_dos.csv"
    fout=open(fnout_dos,"w")
    fout.write("##############################\n")
    fout.write("# Produced by pydecs-aux-tool\n")
    dt1=str(datetime.datetime.today())
    fout.write("# Time = "+dt1[:dt1.rfind(":")]+"\n")
    fout.write("# ELEMENTS = ")
    for e1 in elems:
        fout.write(e1+" ")
    fout.write("\n")
    fout.write("# NATOMS = ")
    natoms_tot=0
    for n1 in natoms:
        fout.write(str(n1)+" ")
        natoms_tot+=n1
    fout.write("\n")
    # fout.write("# NATOMStot = "+str(natoms_tot)+"\n")
    fout.write("# Volume = "+str(volume)+" [A^3]\n")
    fout.write("# EVBM = "+str(E_VBM)+" [eV]\n")
    fout.write("# ECBM = "+str(E_CBM)+" [eV]\n")
    fout.write("# Egap = "+str(E_gap)+" [eV]\n")
    fout.write("# NEDOS = "+str(len(enelist))+"\n")
    # fout.write("# NEDOS = "+str(NEDOS-1)+"\n")
    fout.write("##############################\n")
    fout.write("# energy,dos\n")
    for i2,e2 in enumerate(enelist):
        fout.write(str(e2)+","+str(doslist[i2])+"\n")
    fout.close()
    print(" Finished: Output filename = "+fnout_dos) 
    print("-"*100)

    plt.figure(figsize=(7,6))
    plt.tick_params(axis="x",direction="in",top=True)
    plt.tick_params(axis="y",direction="in",right=True)
    plt.plot(enelist,doslist,"k-",linewidth=2.0)
    plt.xlim([enelist[0],enelist[-1]])
    #plt.ylim([min(charge_list)*1.1,max(charge_list)*1.1])
    plt.axvline(E_VBM,color="tab:red",ls="--",lw=1.5)
    plt.axvline(E_CBM,color="tab:red",ls="--",lw=1.5)
    plt.xlabel(r"$\mathrm{Energy\ [eV]}$",size=14)
    plt.ylabel(r"$\mathrm{Dinsity\ of\ states\ [/cell]}$",size=14)
    plt.savefig("inpydecs_dos.png",dpi=200,bbox_inches="tight")
    plt.close()

if __name__=="__main__":
    convDOSfromVASP()

