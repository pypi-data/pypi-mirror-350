#!/usr/bin/env python
#---------------------------------------------------------------------------
# Copyright 2021 Takafumi Ogawa
# Licensed under the Apache License, Version2.0.
#---------------------------------------------------------------------------
# pydecs-io module
#---------------------------------------------------------------------------
import os
import sys
import shutil
import copy
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import toml

from pydecs.common import product_local

"""
def parse_composition_list(comp_in):
    comp1=[]
    ic0=0
    for ic1,c1 in enumerate(comp_in):
        if ic1!=0 and c1.isupper():
            comp1.append(comp_in[ic0:ic1])
            ic0=ic1
    comp1.append(comp_in[ic0:])
    atomList=[]
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
        atomList.append((elem1,int(num1)))
    return atomList
"""

def parse_composition_list(comp_in):
    comp1=[]
    ic0=0
    for ic1,c1 in enumerate(comp_in):
        if ic1!=0 and c1.isupper():
            comp1.append(comp_in[ic0:ic1])
            ic0=ic1
    comp1.append(comp_in[ic0:])
    atomList=[]
    for c1 in comp1:
        elem1=""
        num1=""
        i2=0
        while i2<len(c1):
            c2 = c1[i2]
            if c2=="[":
                elem1+=c2
                i2+=1
                c2 = c1[i2]
                while c2!="]":
                    elem1+=c2
                    i2+=1
                    c2 = c1[i2]
            if c2.isdigit():
                num1+=c2
            else:
                elem1+=c2
            i2+=1
        if len(num1)==0:
            num1="1"
        atomList.append((elem1,int(num1)))
    return atomList




def conv_legend_label(label_def1,str_for_Vac_in,legend_KV_in,duplication_in):
    if label_def1=="Hole":
        if legend_KV_in:
            label_legend=r"$h^{\bullet}$"
        else:
            label_legend=r"$h^{+}$"
        label_legend_noQ=label_legend
    elif label_def1=="Electron":
        if legend_KV_in:
            label_legend=r"$e^{\,\prime}$"
        else:
            label_legend="$e^{-}$"
        label_legend_noQ=label_legend
    else:
        label_def2=label_def1[1:label_def1.rfind("]")]
        label_def4=""
        for t1 in label_def2.split("+"):
            t2=t1.split("_")
            t3=parse_composition_list(t2[0])
            t4atoms=""
            if len(t3)==1 and t3[0][1]==1:
                t4atoms=t3[0][0]
                if t4atoms=="Vac":
                    t4atoms=str_for_Vac_in
            else:
                for t5 in t3:
                    if t5[0]=="Vac":
                        t5[0]=str_for_Vac_in
                    if t5[1]==1:
                        t4atoms+="{"+t5[0]+"}"
                    else:
                        t4atoms+="{"+t5[0]+"}_{"+str(t5[1])+"}"
                t4atoms="("+t4atoms+")"
            t3=parse_composition_list(t2[1])
            t4sites=""
            if len(t3)==1 and t3[0][1]==1:
                t4sites=t3[0][0]
            else:
                for t5 in t3:
                    if t5[1]==1:
                        t4sites+="{"+t5[0]+"}"
                    else:
                        t4sites+="{"+t5[0]+"}_{"+str(t5[1])+"}"
            label_def4+="{"+t4atoms+"}_{"+t4sites+"}+"
        label_def4=label_def4[:-1]
        if "+" in label_def4:
            label_def4=r"\left["+label_def4+r"\right]"
        label_charge=label_def1[label_def1.find("{")+1:label_def1.find("}")]
        label_charge_int=int(label_charge)
        ##### Space-filling commands: \! = -3/18em, \; = +5/18em,  \: = +4/18em, \, =+3/18 em
        if legend_KV_in:
            label_charge="?"
            if label_charge_int==0:
                label_charge=r"\times"
            elif label_charge_int<0:
                label_charge=r"\;\!"
                for i1 in range(abs(label_charge_int)):
                    label_charge+=r"\prime"
            else:
                label_charge=r"\!\!\;\bullet"
                for i1 in range(abs(label_charge_int)-1):
                    label_charge+=r"\!\!\!\!\bullet"
        else:
            if label_charge_int==-1:
                label_charge="-"
            elif label_charge_int==1:
                label_charge="+"
            elif label_charge_int>1:
                label_charge=label_charge+"\!\!+"
            elif label_charge_int<-1:
                label_charge=label_charge[1:]+r"\!\!-"
        label_id=label_def1[label_def1.find("(")+1:label_def1.find(")")]
        label_legend=r"\mathrm{"+label_def4+"^{"+label_charge+"}}"
        label_legend_noQ=label_legend[:label_legend.find("^")]+"}"
        if duplication_in:
            label_legend=label_legend+"("+label_id+")"
            label_legend_noQ=label_legend_noQ+"("+label_id+")"
        label_legend="$"+label_legend+"$"
        label_legend_noQ="$"+label_legend_noQ+"$"
    return label_legend,label_legend_noQ


class InputParamsToml:

    def __init__(self,filename_in="inpydecs.toml"):
        if not os.path.exists(filename_in):
            print(" ERROR: File not found: "+filename_in)
            sys.exit()
        print(" Reading input file: "+filename_in)
        try:
            self.input_parameters=toml.load(filename_in)
        except Exception as e:
            print(" ERROR: Check TOML-format in the input file")
            print("  => "+str(e))
            sys.exit()
        self.input_paths=["./"]
        self.outfiles_header="outpydecs"
        if "io" in self.input_parameters.keys():
            p1=self.input_parameters["io"]
            if "input_paths" in p1.keys():
                self.input_paths=p1["input_paths"]
            if "input_paths" in p1.keys():
                self.outfiles_header=p1["outfiles_header"]
        self.densform="v1"
        if "solver" in self.input_parameters.keys():
            if "densform" in self.input_parameters["solver"].keys():
                self.densform=self.input_parameters["solver"]["densform"]
        for i1,p1 in enumerate(self.input_paths):
            if p1[-1]!="/":
                self.input_paths[i1]=p1+"/"
        str1=f"  input_paths = [\""
        for p1 in self.input_paths:
            str1=str1+f"{p1}\", \""
        print(str1[:-3]+"]")
        print("  outfiles_header = "+self.outfiles_header)
        print("-"*100)

    def get_input_parameters(self):
        return self.input_parameters

    def get_input_paths(self):
        return self.input_paths
    
    def get_root_outfiles(self):
        return self.outfiles_header

    def get_densform(self):
        return self.densform

def plot_Edef_eFermi(filename_in,root_outfiles,plot_params_in={}):
    if not "format" in plot_params_in.keys():
        plot_params_in["format"]=["png"]
    if not "dpi" in plot_params_in.keys():
        plot_params_in["dpi"]=100
    if not "figsize_x_cm" in plot_params_in.keys():
        plot_params_in["figsize_x_cm"]=9.0
    if not "figsize_y_cm" in plot_params_in.keys():
        plot_params_in["figsize_y_cm"]=8.0
    plot_params_in["figsize_x_inch"]=plot_params_in["figsize_x_cm"]/2.54
    plot_params_in["figsize_y_inch"]=plot_params_in["figsize_y_cm"]/2.54
    if not "label_size" in plot_params_in.keys():
        plot_params_in["label_size"]=10
    if not "ticks_size" in plot_params_in.keys():
        plot_params_in["ticks_size"]=8
    if not "ticks_pad" in plot_params_in.keys():
        plot_params_in["ticks_pad"]=4.0
    if not "str_replacing_Vac" in plot_params_in.keys():
        plot_params_in["str_replacing_Vac"]="V"
    if not "legend_KV" in plot_params_in.keys():
        plot_params_in["legend_KV"]=False
    if not "Edef_x_lower_limit" in plot_params_in.keys():
        plot_params_in["Edef_x_lower_limit"]=0.0
    if not "Edef_x_upper_limit" in plot_params_in.keys():
        plot_params_in["Edef_x_upper_limit"]="BAND_GAP"
    if not "Edef_xlabel" in plot_params_in.keys():
        plot_params_in["Edef_xlabel"]=r"$\varepsilon_\mathrm{F}-\varepsilon_\mathrm{VBM}\ \mathrm{[eV]}$"
    if not "Edef_y_lower_limit" in plot_params_in.keys():
        plot_params_in["Edef_y_lower_limit"]=0.0
    if not "Edef_y_upper_limit" in plot_params_in.keys():
        plot_params_in["Edef_y_upper_limit"]=3.0
    if not "Edef_xtick_labels" in plot_params_in.keys():
        plot_params_in["Edef_xtick_labels"]="NONE"
    if not "Edef_ytick_labels" in plot_params_in.keys():
        plot_params_in["Edef_ytick_labels"]="NONE"
    if not "Edef_ylabel" in plot_params_in.keys():
        plot_params_in["Edef_ylabel"]=r"$\mathrm{Defect\ formation\ energy\ [eV]}$"
    if not "Edef_zero_line" in plot_params_in.keys():
        plot_params_in["Edef_zero_line"]=True
    if not "Edef_bands_fill" in plot_params_in.keys():
        plot_params_in["Edef_bands_fill"]=True
    if not os.path.exists(filename_in):
        print(" ERROR: file not found: "+filename_in)
        sys.exit()
    fin=open(filename_in).readlines()
    for l1 in fin:
        if "Fermi_level" in l1:
            labels=l1.split(",")
            num_data=len(labels)
        if l1.strip()[0]!="#":
            continue
        if "Egap" in l1:
            Egap=float(l1.split(",")[0].split("=")[1].strip())
    if plot_params_in["Edef_x_upper_limit"]=="BAND_GAP":
        plot_params_in["Edef_x_upper_limit"]=Egap
    eFermi_list=[]
    charge_list=[]
    defects_list=[]
    for lab1 in labels[2:]:
        dict1={"label":lab1.strip(),"defect_energy":[]}
        dict1["charge"]=lab1.split("{")[1].split("}")[0]
        if float(dict1["charge"])>0:
            dict1["charge"]="+"+dict1["charge"]
        def_label1=lab1.split("[")[1].split("]")[0]
        duplication1=False
        for lab2 in labels[2:]:
            if lab1==lab2:
                continue
            if lab1[:lab1.rfind("(")]==lab2[:lab2.rfind("(")]:
                duplication1=True
        leg1,leg1_noQ=conv_legend_label(lab1,plot_params_in["str_replacing_Vac"],plot_params_in["legend_KV"],duplication1)
        dict1["label_for_legend"]=leg1_noQ
        dict1["label_for_legend_withQ_withID"]=leg1
        lab3=lab1[:lab1.rfind("^")]+lab1[lab1.rfind("}"):]
        dict1["label_withoutQ"]=lab3.strip()
        defects_list.append(dict1)
    for l1 in fin:
        if l1.strip()[0]=="#":
            continue
        l2=l1.split(",")
        mode2=""
        if l2[0]=="line_color":
            mode2=l2[0]
        elif l2[0]=="line_style":
            mode2=l2[0]
        elif l2[0]=="line_width":
            mode2=l2[0]
        elif l2[0]=="Fermi_level":
            mode2="label"
        else:
            mode2="data"
        if mode2=="data":
            eFermi_list.append(float(l2[0]))
            charge_list.append(float(l2[1]))
        for i3,v3 in enumerate(l2[2:]):
            if mode2=="line_color":
                defects_list[i3]["line_color"]=v3.strip()
            elif mode2=="line_style":
                defects_list[i3]["line_style"]=v3.strip()
            elif mode2=="line_width":
                defects_list[i3]["line_width"]=v3.strip()
            elif mode2=="data":
                defects_list[i3]["defect_energy"].append(float(v3))
    #### Plotting Total_charge
    plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
    plt.tick_params(axis="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
    plt.plot(eFermi_list,charge_list,"k-",linewidth=2.0)
    plt.axhline(0.0,color="k",ls=":",lw=1.0)
    plt.yscale("symlog",linthresh=10**-20)
    plt.xlim([plot_params_in["Edef_x_lower_limit"],plot_params_in["Edef_x_upper_limit"]])
    plt.ylim([min(charge_list)*1.1,max(charge_list)*1.1])
    plt.ylabel(r"$\mathrm{Total\ charge\ [e/cell]}$",size=plot_params_in["label_size"])
    plt.xlabel(r"$\varepsilon_\mathrm{F}-\varepsilon_\mathrm{VBM}\ \mathrm{[eV]}$",size=plot_params_in["label_size"])
    if plot_params_in["Edef_xtick_labels"]!="NONE":
        plt.xticks(plot_params_in["Edef_xtick_labels"])
    for f1 in plot_params_in["format"]:
        plt.savefig(root_outfiles+"_Edef_Qtot."+f1,dpi=plot_params_in["dpi"])
    plt.close()
    
    eFermi_balanced = 1e10
    charge_balanced = 1e10
    for ie1,e1 in enumerate(eFermi_list):
        chg1=np.fabs(charge_list[ie1])
        if chg1<charge_balanced:
            charge_balanced=chg1
            eFermi_balanced=e1
    #### Determining plot-range
    lowestEf_line=[]
    for i1,e1 in enumerate(eFermi_list):
        emin=1e20
        for d2 in defects_list:
            e2=d2["defect_energy"][i1]
            if e1<emin:
                emin=e1
        lowestEf_line.append(emin)
    max_lowestEf=max(lowestEf_line)
    if max_lowestEf<0.0:
        print(" WARNING(plot_Edef_eFermi)::There is not positive-cros point of Edef.")
        if plot_params_in["Edef_y_upper_limit"]=="AUTO":
            print("    Edef_y_upper_limit is set to 3.0 eV.")
            plot_params_in["Edef_y_upper_limit"]=3.0
    if plot_params_in["Edef_y_upper_limit"]=="AUTO":
        plot_params_in["Edef_y_upper_limit"]=max_lowestEf*2.0
    #### Screening defect species for plotting
    defects_list_screened=[]
    for d1 in defects_list:
        elist1=d1["defect_energy"]
        bool_plot=False
        for i1,eF1 in enumerate(eFermi_list):
            e2=elist1[i1]
            if eF1>plot_params_in["Edef_x_lower_limit"] and eF1<plot_params_in["Edef_x_upper_limit"]\
                    and e2>plot_params_in["Edef_y_lower_limit"] and e2<plot_params_in["Edef_y_upper_limit"]:
                bool_plot=True
        if bool_plot:
            defects_list_screened.append(d1)
    #### Plotting defect-energies without bundling
    fig1=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
    fig2legend=plt.figure(figsize=(plot_params_in["figsize_x_inch"]*0.5,plot_params_in["figsize_x_inch"]*0.5),constrained_layout=True)
    ax1=fig1.add_subplot(111)
    ax1.tick_params(axis="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
    lines=[]
    legends=[]
    for d1 in defects_list_screened:
        l1,=ax1.plot(eFermi_list,d1["defect_energy"],c=d1["line_color"],ls=d1["line_style"],lw=d1["line_width"])
        lines.append(l1)
        legends.append(d1["label_for_legend_withQ_withID"])
    if plot_params_in["Edef_zero_line"]:
        if np.abs(plot_params_in["Edef_y_lower_limit"])>1e-10:
            ax1.axhline(0.0,color="k",ls=":",lw=1.0)
        ax1.axvline(eFermi_balanced,color="k",ls=":",lw=1.0)
    ax1.set_xlim([plot_params_in["Edef_x_lower_limit"],plot_params_in["Edef_x_upper_limit"]])
    ax1.set_ylim([plot_params_in["Edef_y_lower_limit"],plot_params_in["Edef_y_upper_limit"]])
    if plot_params_in["Edef_bands_fill"]:
        if plot_params_in["Edef_x_lower_limit"]<0.0:
            ax1.axvspan(plot_params_in["Edef_x_lower_limit"],0.0,color="gray",alpha=0.2,linewidth=0)
        if plot_params_in["Edef_x_upper_limit"]>Egap:
            ax1.axvspan(Egap,plot_params_in["Edef_x_upper_limit"],color="gray",alpha=0.2,linewidth=0)
    ax1.set_xlabel(plot_params_in["Edef_xlabel"],size=plot_params_in["label_size"])
    ax1.set_ylabel(plot_params_in["Edef_ylabel"],size=plot_params_in["label_size"])
    if plot_params_in["Edef_xtick_labels"]!="NONE":
        ax1.set_xticks(plot_params_in["Edef_xtick_labels"])
    if plot_params_in["Edef_ytick_labels"]!="NONE":
        ax1.set_yticks(plot_params_in["Edef_ytick_labels"])
    num_data=len(defects_list_screened)
    ncol_df=int(np.floor(float(num_data)**0.5))
    fig2legend.legend(lines,legends,ncol=ncol_df,borderaxespad=0,fontsize=plot_params_in["label_size"],
        edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0)
    for f1 in plot_params_in["format"]:
        fig1.savefig(root_outfiles+"_Edef_separated_main."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        fig2legend.savefig(root_outfiles+"_Edef_separated_legend."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
    plt.close(fig1)
    plt.close(fig2legend)

    #### Bundling the same defect-type with a different charge
    defects_list_Qmerged={}
    for d1 in defects_list:
        k1=d1["label_withoutQ"]
        q1=d1["charge"]
        if not k1 in defects_list_Qmerged.keys():
            def1={}
            def1["defect_energy"]=np.zeros(len(eFermi_list))+1e100
            def1["charge_list"]=np.zeros(len(eFermi_list))
            def1["label_for_legend"]=d1["label_for_legend"]
            def1["line_color"]=d1["line_color"]
            def1["line_style"]="-"
            def1["line_width"]=d1["line_width"]
            defects_list_Qmerged[k1]=def1
 
    for i1,eF1 in enumerate(eFermi_list):
        for d1 in defects_list:
            k1=d1["label_withoutQ"]
            e1=d1["defect_energy"][i1]
            q1=d1["charge"]
            e2=defects_list_Qmerged[k1]["defect_energy"][i1]
            if e1<e2:
                defects_list_Qmerged[k1]["defect_energy"][i1]=e1
                defects_list_Qmerged[k1]["charge_list"][i1]=q1
    #### Calculating charge-transition levels
    transition_levels={}
    for k1,d1 in defects_list_Qmerged.items():
        transition_levels[k1]=[]
        elist=d1["defect_energy"]
        qlist=d1["charge_list"]
        for i1,eF1 in enumerate(eFermi_list):
            if i1==0:
                q_prev=qlist[0]
                e_prev=elist[0]
                eF_prev=eF1
                continue
            q_new=qlist[i1]
            e_new=elist[i1]
            if q_new!=q_prev:
                tl1={}
                tl1["q_prev"]=q_prev
                tl1["q_new"]=q_new
                tl1["Fermi_level"]=(eF1+eF_prev)*0.5
                tl1["defect_energy"]=(e_new+e_prev)*0.5
                transition_levels[k1].append(tl1)
            q_prev=q_new
            e_prev=e_new
            eF_prev=eF1
    fout=open(root_outfiles+"_Edef_transition_levels.csv","w")
    fout.write("defect_type,q_prev,q_new,Fermi_level,defect_energy\n")
    for k1,tl1 in transition_levels.items():
        for tl2 in tl1:
            fout.write(k1+",")
            fout.write(str(tl2["q_prev"])+",")
            fout.write(str(tl2["q_new"])+",")
            fout.write(str(tl2["Fermi_level"])+",")
            fout.write(str(tl2["defect_energy"])+"\n")
    fout.close()
    #### Screening defect species for plotting
    defects_list_Qmerged_screened={}
    for k1,d1 in defects_list_Qmerged.items():
        elist1=d1["defect_energy"]
        bool_plot=False
        for i1,eF1 in enumerate(eFermi_list):
            e2=elist1[i1]
            if eF1>plot_params_in["Edef_x_lower_limit"] and eF1<plot_params_in["Edef_x_upper_limit"]\
                    and e2>plot_params_in["Edef_y_lower_limit"] and e2<plot_params_in["Edef_y_upper_limit"]:
                bool_plot=True
        if bool_plot:
            defects_list_Qmerged_screened[k1]=d1

    #### Plotting defect-energies with bundling
    fig1=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
    fig2legend=plt.figure(figsize=(plot_params_in["figsize_x_inch"]*0.5,plot_params_in["figsize_x_inch"]*0.5),constrained_layout=True)
    ax1=fig1.add_subplot(111)
    ax1.tick_params(axis="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
    lines=[]
    legends=[]
    for k1,d1 in defects_list_Qmerged_screened.items():
        l1,=ax1.plot(eFermi_list,d1["defect_energy"],c=d1["line_color"],ls=d1["line_style"],lw=d1["line_width"])
        lines.append(l1)
        legends.append(d1["label_for_legend"])
        if k1 in transition_levels.keys():
            xlist_tl=[]
            ylist_tl=[]
            for tl2 in transition_levels[k1]:
                xlist_tl.append(tl2["Fermi_level"])
                ylist_tl.append(tl2["defect_energy"])
            ax1.plot(xlist_tl,ylist_tl,"o",mfc="w",mec=d1["line_color"])
    if plot_params_in["Edef_zero_line"]:
        if np.abs(plot_params_in["Edef_y_lower_limit"])>1e-10:
            ax1.axhline(0.0,color="k",ls=":",lw=1.0)
        ax1.axvline(eFermi_balanced,color="k",ls=":",lw=1.0)
    ax1.set_xlim([plot_params_in["Edef_x_lower_limit"],plot_params_in["Edef_x_upper_limit"]])
    ax1.set_ylim([plot_params_in["Edef_y_lower_limit"],plot_params_in["Edef_y_upper_limit"]])
    if plot_params_in["Edef_bands_fill"]:
        if plot_params_in["Edef_x_lower_limit"]<0.0:
            ax1.axvspan(plot_params_in["Edef_x_lower_limit"],0.0,color="gray",alpha=0.2,linewidth=0)
        if plot_params_in["Edef_x_upper_limit"]>Egap:
            ax1.axvspan(Egap,plot_params_in["Edef_x_upper_limit"],color="gray",alpha=0.2,linewidth=0)
    ax1.set_xlabel(plot_params_in["Edef_xlabel"],size=plot_params_in["label_size"])
    ax1.set_ylabel(plot_params_in["Edef_ylabel"],size=plot_params_in["label_size"])
    if plot_params_in["Edef_xtick_labels"]!="NONE":
        ax1.set_xticks(plot_params_in["Edef_xtick_labels"])
    if plot_params_in["Edef_ytick_labels"]!="NONE":
        ax1.set_yticks(plot_params_in["Edef_ytick_labels"])
    num_data=len(defects_list_Qmerged_screened)
    ncol_df=int(np.floor(float(num_data)**0.5))
    fig2legend.legend(lines,legends,ncol=ncol_df,borderaxespad=0,fontsize=plot_params_in["label_size"],
        edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0)
    for f1 in plot_params_in["format"]:
        fig1.savefig(root_outfiles+"_Edef_Qmerged_main."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        fig2legend.savefig(root_outfiles+"_Edef_Qmerged_legend."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
    plt.close(fig1)
    plt.close(fig2legend)
    return

def output_eqcond(eqcond_list_in,root_outfiles_in):
    fout1=open(root_outfiles_in+"_eqconditions.csv","w")
    str1="condition, "
    for k1,v1 in eqcond_list_in[0].items():
        if k1.find("P_")==0:
            k2="pressure_"+k1.split("_")[1].strip()
            str1+=f"{k2}, "
        elif k1=="T":
            str1+=f"temperature, "
        elif k1=="fix_Natoms":
            for v2 in v1:
                k2=f"fix_Natoms_{v2['element']}"
                str1+=f"{k2}, "
        elif k1=="fix_Natoms_linked":
            for v2 in v1:
                k2=f"fix_Natoms_linked_{v2['element']}"
                str1+=f"{k2}, "
        else:
            str1+=f"{k1}, "
    fout1.write(str1[:-2]+"\n")
    for ieq1,eqc1 in enumerate(eqcond_list_in):
        str1=f"{ieq1+1:04}, "
        for k1,v1 in eqc1.items():
            if k1=="fix_Natoms":
                for v2 in v1:
                    v3=f"{v2['target_Natoms']}"
                    str1+=f"{v3}, "
            elif k1=="fix_Natoms_linked":
                for v2 in v1:
                    v3=f"{v2['target_Natoms']}"
                    str1+=f"{v3}, "
            else:
                str1+=f"{v1}, "
        fout1.write(str1[:-2]+"\n")
    fout1.close()

def output_density_with_eqcond(dens_in,eqcond_in,out_filename):
    add_list=[]
    for eq1,v1 in eqcond_in.items():
        if eq1.find("P_")==0:
            gas1=eq1.split("_")[1].strip()
            add1=["","","","","pressure_"+gas1,v1]
            add_list.append(add1)
        elif eq1.find("lambda_")==0 or eq1=="espot":
            add1=["","","","",eq1,v1]
            add_list.append(add1)
        elif eq1.find("fix_Natoms")==0:
            for v2 in v1:
                eq2=eq1+"_"+v2["element"]
                add1=["","","","",eq2,v2["target_Natoms"]]
                add_list.append(add1)
    dens_list=dens_in[:2]+add_list+dens_in[2:]
    if not os.path.exists(out_filename):
        fout=open(out_filename,"w")
        for i1 in range(len(dens_list[0])-1):
            str1=""
            for d1 in dens_list:
                str1+=str(d1[i1])+","
            fout.write(str1[:-1]+"\n")
    else:
        fout=open(out_filename,"a")
    str1=""
    for d1 in dens_list:
        str1+=str(d1[-1])+","
    fout.write(str1[:-1]+"\n")
    fout.close()
    return

def plot_defect_densities(plot_params_in={}):
    if "outfiles_header" in plot_params_in.keys():
        root_outfiles=plot_params_in["outfiles_header"]
    else:
        root_outfiles="plot"
    fnout_plot=plot_params_in["outfiles_header"]+"_plotdens.txt"
    fout1=open(fnout_plot,"w")
    print(" Starting plot_defect_densities")
    fout1.write(" Starting plot_defect_densities\n")
    ####################
    if "input_filename" in plot_params_in.keys():
        filename_in=plot_params_in["input_filename"]
    else:
        filename_in="out_densities.csv"
    if not os.path.exists(filename_in):
        print(f" ERROR(plot_defect_densities):: density file not found: {filename_in}")
        fout1.write(f" ERROR(plot_defect_densities):: density file not found: {filename_in}\n")
        sys.exit()
    if not "format" in plot_params_in.keys():
        plot_params_in["format"]=["png"]
    if not "dpi" in plot_params_in.keys():
        plot_params_in["dpi"]=100
    if not "figsize_x_cm" in plot_params_in.keys():
        plot_params_in["figsize_x_cm"]=9.0
    if not "figsize_y_cm" in plot_params_in.keys():
        plot_params_in["figsize_y_cm"]=8.0
    plot_params_in["figsize_x_inch"]=plot_params_in["figsize_x_cm"]/2.54
    plot_params_in["figsize_y_inch"]=plot_params_in["figsize_y_cm"]/2.54
    if not "label_size" in plot_params_in.keys():
        plot_params_in["label_size"]=10
    if not "ticks_size" in plot_params_in.keys():
        plot_params_in["ticks_size"]=8
    if not "ticks_pad" in plot_params_in.keys():
        plot_params_in["ticks_pad"]=4.0
    if not "str_replacing_Vac" in plot_params_in.keys():
        plot_params_in["str_replacing_Vac"]="V"
    if not "legend_KV" in plot_params_in.keys():
        plot_params_in["legend_KV"]=False

    if not "dens_merge" in plot_params_in.keys():
        plot_params_in["dens_merge"]=False
    if not "dens_merge_sites" in plot_params_in.keys():
        plot_params_in["dens_merge_sites"]=False
    if plot_params_in["dens_merge_sites"]==True and plot_params_in["dens_merge"]==False:
        print("!"*100)   
        print(f" WARNING(plot_defect_densities):: When dens_merge_sites is set to true,")
        print(f"                                  it is recommended to also set dens_merge to true.")
        print("!"*100)   
        fout1.write(f"!"*100+"\n")
        fout1.write(f" WARNING(plot_defect_densities):: When dens_merge_sites is set to true,\n")
        fout1.write(f"                                  it is recommended to also set dens_merge to true.\n")
        fout1.write(f"!"*100+"\n")
    if not "dens_unit_cm3" in plot_params_in.keys():
        plot_params_in["dens_unit_cm3"]=False
    if not "dens_scale" in plot_params_in.keys():
        plot_params_in["dens_scale"]=1.0
    if not "dens_xaxis_parameter" in plot_params_in.keys():
        plot_params_in["dens_xaxis_parameter"]="NONE"
    if not "dens_xaxis_log" in plot_params_in.keys():
        plot_params_in["dens_xaxis_log"]="NONE"
    if not "dens_x_upper_limit" in plot_params_in.keys():
        plot_params_in["dens_x_upper_limit"]="NONE"
    if not "dens_x_lower_limit" in plot_params_in.keys():
        plot_params_in["dens_x_lower_limit"]="NONE"
    if not "dens_xlabel" in plot_params_in.keys():
        plot_params_in["dens_xlabel"]="NONE"
    if not "dens_xtick_labels" in plot_params_in.keys():
        plot_params_in["dens_xtick_labels"]="NONE"
    if not "dens_yaxis_log" in plot_params_in.keys():
        plot_params_in["dens_yaxis_log"]=True
    if not "dens_y_upper_limit" in plot_params_in.keys():
        plot_params_in["dens_y_upper_limit"]="Auto"
    if plot_params_in["dens_y_upper_limit"]=="Auto":
        plot_params_in["dens_y_upper_limit_auto"]=True
    else:
        plot_params_in["dens_y_upper_limit_auto"]=False
    if not "dens_y_lower_limit" in plot_params_in.keys():
        plot_params_in["dens_y_lower_limit"]="Auto"
    if plot_params_in["dens_y_lower_limit"]=="Auto":
        plot_params_in["dens_y_lower_limit_auto"]=True
    else:
        plot_params_in["dens_y_lower_limit_auto"]=False
    if not "dens_y_rangefactor_auto" in plot_params_in.keys():
        plot_params_in["dens_y_rangefactor_auto"]=1.0e7
    if not "dens_ylabel" in plot_params_in.keys():
        if plot_params_in["dens_unit_cm3"]:
            plot_params_in["dens_ylabel"]=r"$\mathrm{Defect\ density\ [cm^{-3}]}$"
        else:
            print("   Scale factor for plotting = "+str(plot_params_in["dens_scale"]))
            print("     Size-dependent quantities (e.g. densities) in summarized plots are devided by this value.")
            fout1.write("   Scale factor for plotting = "+str(plot_params_in["dens_scale"])+"\n")
            fout1.write("     Size-dependent quantities (e.g. densities) in summarized plots are devided by this value.\n")
            plot_params_in["dens_ylabel"]=r"$\mathrm{Defect\ density\ [/scaled\ cell]}$"
    if not "Edef_x_lower_limit" in plot_params_in.keys():
        plot_params_in["Edef_x_lower_limit"]=0.0
    if not "Edef_x_upper_limit" in plot_params_in.keys():
        plot_params_in["Edef_x_upper_limit"]="BandGap"
    if not "Edef_y_lower_limit" in plot_params_in.keys():
        plot_params_in["Edef_y_lower_limit"]=0.0
    if not "Edef_y_upper_limit" in plot_params_in.keys():
        plot_params_in["Edef_y_upper_limit"]=3.0
    if not "Edef_ylabel" in plot_params_in.keys():
        plot_params_in["Edef_ylabel"]=r"$\mathrm{Defect\ formation\ energy\ [eV]}$"
    if not "Edef_zero_line" in plot_params_in.keys():
        plot_params_in["Edef_zero_line"]=True
    if not "Edef_bands_fill" in plot_params_in.keys():
        plot_params_in["Edef_bands_fill"]=True
    ####################
    fin=open(filename_in).readlines()
    l1=fin.pop(0).strip()
    t1=l1.split(",")
    Egap=-1.0
    Volume=-1.0
    if t1[0].split("=")[0].strip()=="Egap":
        Egap=float(t1[0].split("=")[1].strip())
    if t1[1].split("=")[0].strip()=="Volume":
        Volume=float(t1[1].split("=")[1].strip())
        tocm3=1.0e24/Volume
    if Egap<0.0 or Volume<0.0:
        print("Error: invalid format at line 1 in the input file.")
        sys.exit()
    ####################
    datalist0={}
    key_list0=[]
    for l1 in fin:
        l2=l1.split(",")
        if l2[0].strip()=="condition":
            for k2 in l2[1:]:
                key_list0.append(k2.strip())
                datalist0[k2.strip()]={}
                datalist0[k2.strip()]["values"]=[]
    for l1 in fin:
        l2=l1.split(",")
        if l2[0].strip()=="condition":
            continue
        elif l2[0].strip()=="line_color":
            for i2,v2 in enumerate(l2[1:]):
                datalist0[key_list0[i2]]["line_color"]=v2.strip()
        elif l2[0].strip()=="line_style":
            for i2,v2 in enumerate(l2[1:]):
                datalist0[key_list0[i2]]["line_style"]=v2.strip()
        elif l2[0].strip()=="line_width":
            for i2,v2 in enumerate(l2[1:]):
                datalist0[key_list0[i2]]["line_width"]=v2.strip()
        else:
            for i2,v2 in enumerate(l2[1:]):
                datalist0[key_list0[i2]]["values"].append(float(v2.strip()))
    if plot_params_in["dens_xaxis_parameter"]!="NONE":
        if not plot_params_in["dens_xaxis_parameter"] in key_list0:
            print(f" ERROR(plot)::"+plot_params_in["dens_xaxis_parameter"]+" is not found." )
            fout1.write(f" ERROR(plot)::"+plot_params_in["dens_xaxis_parameter"]+" is not found.\n" )
            sys.exit()
    ####################
    print("  Reading equilibrium conditions")
    fout1.write("  Reading equilibrium conditions\n")
    parameters_list1={}
    parameters_list2={}
    datalist1={}
    for k1,d1 in datalist0.items():
        if "fix_Natoms_" in k1:
            d2=np.array(d1["values"])/plot_params_in["dens_scale"]
        else:
            d2=d1["values"]
        d3=[]
        for d4 in d2:
            if d4 not in d3:
                d3.append(d4)
        if k1.find("temperature")==0 or k1.find("pressure_")==0 or k1.find("lambda_")==0 or k1.find("fix_Natoms_")==0 or k1.find("espot")==0:
            parameters_list1[k1]=d2
            parameters_list2[k1]=d3
        elif  k1.find("chempot_")==0:
            parameters_list1[k1]=d2
            parameters_list2[k1]=d3
            datalist1[k1]=d1
        else:
            datalist1[k1]=d1
    for k1,v1 in parameters_list2.items():
        str_out=f"   {k1}: "
        strl1=len(str_out)
        for v2 in v1:
            if len(str_out)>90:
                print(str_out)
                fout1.write(str_out+"\n")
                str_out=strl1*" "
            if "pressure" in k1 or "fix_Natoms" in k1:
                str_out+=f"{v2:8.2e}, "
            else:
                str_out+=f"{v2:7.2f}, "
        print(f"{str_out[:-2]}")
        fout1.write(f"{str_out[:-2]}\n")
    if plot_params_in["dens_xaxis_parameter"]=="NONE":
        num_max=-1
        param_max=""
        for k1,v1 in parameters_list1.items():
            n1=len(set(v1))
            if n1>num_max:
                num_max=n1
                param_max=k1
        plot_params_in["dens_xaxis_parameter"]=param_max
    print("   dens_xaixs_parameter = "+str(plot_params_in["dens_xaxis_parameter"]))
    fout1.write(f"   dens_xaixs_parameter = "+str(plot_params_in["dens_xaxis_parameter"])+"\n")
    bool_fixNatoms_linked=False
    if plot_params_in["dens_xaxis_parameter"].find("fix_Natoms_linked")==0:
        bool_fixNatoms_linked=True
    if plot_params_in["dens_xlabel"]=="NONE":
        if plot_params_in["dens_xaxis_parameter"]=="temperature":
            plot_params_in["dens_xlabel"]=r"Temperature [K]"
        elif plot_params_in["dens_xaxis_parameter"].find("pressure_")==0:
            g1=plot_params_in["dens_xaxis_parameter"].split("_")[1].strip()
            g2=parse_composition_list(g1)
            g4="$\\mathrm{"
            for (at2,nat2) in g2:
                if nat2==1:
                    g4=g4+at2
                else:
                    g4=g4+at2+"_{"+str(nat2)+"}"
            g4=g4+"}$"
            plot_params_in["dens_xlabel"]=f"Pressure ({g4}) [Pa]"
        elif plot_params_in["dens_xaxis_parameter"].find("lambda_")==0:
            lab1=plot_params_in["dens_xaxis_parameter"].split("_")[1].strip()
            plot_params_in["dens_xlabel"]="$\lambda$"+f" ({lab1})"
        elif plot_params_in["dens_xaxis_parameter"].find("chempot_")==0:
            lab1=plot_params_in["dens_xaxis_parameter"].split("_")[-1].strip()
            plot_params_in["dens_xlabel"]=r"$\mu_\mathrm{"+f"{lab1}"+r"}$ [eV]"
        elif plot_params_in["dens_xaxis_parameter"].find("fix_Natoms_")==0:
            lab1=plot_params_in["dens_xaxis_parameter"].split("_")[-1].strip()
            plot_params_in["dens_xlabel"]="$N_\mathrm{atom}$"+f" ({lab1})"
        elif plot_params_in["dens_xaxis_parameter"]=="espot":
            plot_params_in["dens_xlabel"]=r"$\phi$ [V]"
        else:
            print(f" ERROR(plot)::'dens_xaxis_parameter' cannot be defined for "+str(plot_params_in["dens_xaxis_parameter"]))
            fout1.write(f" ERROR(plot)::'dens_xaxis_parameter' cannot be defined for "+str(plot_params_in["dens_xaxis_parameter"])+"\n")
            sys.exit()
    if plot_params_in["dens_xaxis_log"]=="NONE":
        if plot_params_in["dens_xaxis_parameter"].find("pressure_")==0:
            plot_params_in["dens_xaxis_log"]=True
        else:
            plot_params_in["dens_xaxis_log"]=False

    parameters_list_main=[]
    parameters_list_exclmain={}
    lambda_including=[]
    fix_Natoms_linked_including=[]
    for k1,v1 in parameters_list2.items():
        if k1.find("lambda_")==0:
            lambda_including.append(k1)
        if k1.find("fix_Natoms_linked_")==0:
            fix_Natoms_linked_including.append(k1)
    cnt_lambda = len(lambda_including)-1
    bool_fix_Natoms_linked = False
    if len(fix_Natoms_linked_including) > 1:
        bool_fix_Natoms_linked = True
    for k1,v1 in parameters_list2.items():
        if k1==plot_params_in["dens_xaxis_parameter"]:
            parameters_list_main=v1
        else:
            if plot_params_in["dens_xaxis_parameter"].find("chempot_")==0:
                if k1.find("pressure_")==0 or k1.find("fix_Natoms_")==0 \
                        or k1.find("lambda_")==0:
                    continue
                if k1.find("chempot_")==0 and len(lambda_including)==1:
                    continue
                if k1.find("chempot_")==0 and cnt_lambda>0:
                    cnt_lambda-=1
                    continue
            else:
                if k1.find("chempot_")==0:
                    continue
                if k1.find("lambda_")==0 and cnt_lambda>0:
                    cnt_lambda-=1
                    continue
                if k1.find("fix_Natoms_linked_")==0:
                    if plot_params_in["dens_xaxis_parameter"].find("fix_Natoms_linked_")==0:
                        continue
                    if bool_fix_Natoms_linked:
                        bool_fix_Natoms_linked = False
                        parameters_list_exclmain[k1]=v1
                        continue
                    else:
                        continue
            parameters_list_exclmain[k1]=v1
    # print(parameters_list_exclmain)
    # print(parameters_list_main)

    if len(parameters_list_main)<=3:
        print(f" WARNING(plot)::Num. of dens_xaxis_parameter values is very small!")
        fout1.write(f" WARNING(plot)::Num. of dens_xaxis_parameter values is very small!\n")
    if plot_params_in["dens_x_lower_limit"]=="NONE":
        plot_params_in["dens_x_lower_limit"]=min(parameters_list_main)
    if plot_params_in["dens_x_upper_limit"]=="NONE":
        plot_params_in["dens_x_upper_limit"]=max(parameters_list_main)
    eq_conditions=[]
    eq_conditions_labels=[]
    for k1,v1 in parameters_list_exclmain.items():
        if bool_fixNatoms_linked and k1.find("fix_Natoms_")==0:
            continue
        if len(eq_conditions)==0:
            eq_conditions=v1
        else:
            eq_conditions=product_local(eq_conditions,v1)
        eq_conditions_labels.append(k1)
    fout_conditions=open(root_outfiles+"_plotdens_eqconditions.csv","w")
    str_out=f"ID_eqcond, "
    for ieq1,lab1 in enumerate(eq_conditions_labels):
        str_out+=f"{lab1}, "
    fout_conditions.write(str_out[:-2]+"\n")
    if len(eq_conditions_labels)==1 and isinstance(eq_conditions[0],float):
        tmp1=[]
        for t1 in eq_conditions:
            tmp1.append([t1])
        eq_conditions=tmp1
    for ieq1,eq1 in enumerate(eq_conditions):
        str_out=f"{ieq1+1:0>4}, "
        for eq2 in eq1:
            str_out+=f"{eq2}, "
        fout_conditions.write(str_out[:-2]+"\n")
    fout_conditions.close()
    ####################
    dirname=f"{root_outfiles}_plotdens_data"
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
    os.makedirs(dirname)
    os.chdir(dirname)
    default_color=("crimson","mediumblue","forestgreen","orange","deepskyblue","lime",
                   "darksalmon","aqua","olive","magenta","turquoise","midnightblue",
                   "rosybrown","cornflowerblue","lightslategray","navajowhite","tan")
    for ieq1,eq1 in enumerate(eq_conditions):
        ieq2=ieq1+1
        ieq2_str=f"{ieq2:0>4}"
        dirname=f"eqcond_{ieq2_str}"
        print("-"*100)
        print(f"  Starting plot-densities ({ieq1+1}/{len(eq_conditions)}) at {dirname}")
        fout1.write("-"*100+"\n")
        fout1.write(f"  Starting plot-densities ({ieq1+1}/{len(eq_conditions)}) at {dirname}\n")
        os.makedirs(dirname)
        os.chdir(dirname)
        ### Preparing data
        datalist2={}
        for k1,d1 in datalist1.items():
            datalist2[k1]=copy.deepcopy(d1)
            datalist2[k1]["values"]=[]
            if k1.find("density_")!=0 and k1.find("energy_")!=0:
                continue
            label_def1=k1[k1.find("_")+1:]
            duplication1=False
            for k2 in datalist1.keys():
                label_def2=k2[k2.find("_")+1:]
                if label_def1==label_def2:
                    continue
                if label_def1[:label_def1.rfind("(")]==label_def2[:label_def2.rfind("(")]:
                    duplication1=True
            leg1,leg1_noQ=conv_legend_label(label_def1,plot_params_in["str_replacing_Vac"],plot_params_in["legend_KV"],duplication1)
            datalist2[k1]["label_legend_wQ"]=leg1
            datalist2[k1]["label_legend"]=leg1_noQ
        for ip1 in range(len(parameters_list1[plot_params_in["dens_xaxis_parameter"]])):
            bool_eq1=True
            for ieq3,veq3 in enumerate(eq1):
                v2=parameters_list1[eq_conditions_labels[ieq3]][ip1]
                if bool_fixNatoms_linked and eq_conditions_labels[ieq3].find("fix_Natoms_")==0:
                    continue
                if not math.isclose(v2,veq3,rel_tol=1e-9):
                    bool_eq1=False
            if bool_eq1:
                for k1,d1 in datalist1.items():
                    datalist2[k1]["values"].append(datalist1[k1]["values"][ip1])
        ### Plot-chempot
        fig=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]))
        ax=fig.add_subplot(111)
        ax.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        icolor=0
        for k1,d1 in datalist2.items():
            if k1.find("chempot_")==0:
                e1=k1.split("_")[1].strip()
                if len(d1["line_color"])==0:
                    d1["line_color"]=default_color[icolor]
                    icolor+=1
                    if icolor==len(default_color):
                        icolor=0
                if len(d1["line_style"])==0:
                    d1["line_style"]="-"
                if len(d1["line_width"])==0:
                    d1["line_width"]=1.5
                ax.plot(parameters_list_main,d1["values"],label=e1,c=d1["line_color"],
                           ls=d1["line_style"],lw=d1["line_width"])
        if plot_params_in["dens_xaxis_log"]:
            ax.set_xscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax.set_xticks(plot_params_in["dens_xtick_labels"])
        ax.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        ax.set_ylabel(r"$\mathrm{Chemical\ potential,\ }\mu_\mathrm{atom}\ \mathrm{[eV]}$",size=plot_params_in["label_size"])
        ax.legend(loc=0,fontsize=plot_params_in["ticks_size"],edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0)
        fig.savefig(root_outfiles+"_chempots."+plot_params_in["format"][0],dpi=plot_params_in["dpi"],bbox_inches="tight")
        locs1,labels1=plt.xticks()
        labels2=[]
        for i1,l1 in enumerate(locs1):
            l2=labels1[i1]
            l3=l2.get_text()
            if "10^{0}" in l3:
                l3='$\\mathdefault{1}$'
            labels2.append(l3)
        plt.xticks(locs1,labels2)
        ax.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        for f1 in plot_params_in["format"]:
            fig.savefig(root_outfiles+"_chempots."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig)
        ### Plot-Nsite
        fig=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]))
        ax=fig.add_subplot(111)
        ax.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        icolor=0
        for k1,d1 in datalist2.items():
            if k1.find("Nsite_")==0:
                e1=k1.split("_")[1].strip()
                if len(d1["line_color"])==0:
                    d1["line_color"]=default_color[icolor]
                    icolor+=1
                    if icolor==len(default_color):
                        icolor=0
                if len(d1["line_style"])==0:
                    d1["line_style"]="-"
                if len(d1["line_width"])==0:
                    d1["line_width"]=1.5
                d2=np.array(d1["values"])/plot_params_in["dens_scale"]
                ax.plot(parameters_list_main,d2,label=e1,c=d1["line_color"],ls=d1["line_style"],lw=d1["line_width"])
        if plot_params_in["dens_xaxis_log"]:
            ax.set_xscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax.set_xticks(plot_params_in["dens_xtick_labels"])
        ax.ticklabel_format(axis="y",useOffset=True,useMathText=True)
        ax.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        ax.set_ylabel(r"$N_\mathrm{site}\ \mathrm{[/scaled\ cell]}$",size=plot_params_in["label_size"])
        ax.legend(fontsize=plot_params_in["ticks_size"],edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0,ncol=10,bbox_to_anchor=(0.0, 1.1),loc="lower left")
        plt.xticks(locs1,labels2)
        ax.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        for f1 in plot_params_in["format"]:
            fig.savefig(root_outfiles+"_Nsites."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig)
        ### Plot-deltaNsite
        fig=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]))
        ax=fig.add_subplot(111)
        ax.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        icolor=0
        for k1,d1 in datalist2.items():
            if k1.find("delta_Nsite_")==0:
                e1=k1.split("_")[-1].strip()
                if len(d1["line_color"])==0:
                    d1["line_color"]=default_color[icolor]
                    icolor+=1
                    if icolor==len(default_color):
                        icolor=0
                if len(d1["line_style"])==0:
                    d1["line_style"]="-"
                if len(d1["line_width"])==0:
                    d1["line_width"]=1.5
                d2=np.array(d1["values"])/plot_params_in["dens_scale"]
                ax.plot(parameters_list_main,d2,label=e1,c=d1["line_color"],ls=d1["line_style"],lw=d1["line_width"])
        if plot_params_in["dens_xaxis_log"]:
            ax.set_xscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax.set_xticks(plot_params_in["dens_xtick_labels"])
        ax.ticklabel_format(axis="y",useOffset=True,useMathText=True)
        ax.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        ax.set_ylabel(r"$\delta N_\mathrm{site}\ \mathrm{[/scaled\ cell]}$",size=plot_params_in["label_size"])
        ax.legend(fontsize=plot_params_in["ticks_size"],edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0,ncol=10,bbox_to_anchor=(0.0, 1.1),loc="lower left")
        plt.xticks(locs1,labels2)
        ax.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        for f1 in plot_params_in["format"]:
            fig.savefig(root_outfiles+"_Nsites_delta."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig)
        ### Plot-Natom
        fig=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]))
        ax=fig.add_subplot(111)
        ax.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        icolor=0
        for k1,d1 in datalist2.items():
            if k1.find("Natom_")==0:
                e1=k1.split("_")[1].strip()
                if len(d1["line_color"])==0:
                    d1["line_color"]=default_color[icolor]
                    icolor+=1
                    if icolor==len(default_color):
                        icolor=0
                if len(d1["line_style"])==0:
                    d1["line_style"]="-"
                if len(d1["line_width"])==0:
                    d1["line_width"]=1.5
                d2=np.array(d1["values"])/plot_params_in["dens_scale"]
                ax.plot(parameters_list_main,d2,label=e1,c=d1["line_color"],ls=d1["line_style"],lw=d1["line_width"])
        if plot_params_in["dens_xaxis_log"]:
            ax.set_xscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax.set_xticks(plot_params_in["dens_xtick_labels"])
        ax.ticklabel_format(axis="y",useOffset=True,useMathText=True)
        ax.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        ax.set_ylabel(r"$N_\mathrm{atom}\ \mathrm{[/scaled\ cell]}$",size=plot_params_in["label_size"])
        ax.legend(loc=0,fontsize=plot_params_in["ticks_size"],edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0)
        plt.xticks(locs1,labels2)
        ax.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        for f1 in plot_params_in["format"]:
            fig.savefig(root_outfiles+"_Natoms."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig)
        ### Plot-deltaNsite
        # fig=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
        fig=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]))
        ax=fig.add_subplot(111)
        ax.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        icolor=0
        for k1,d1 in datalist2.items():
            if k1.find("delta_Natom_")==0:
                e1=k1.split("_")[-1].strip()
                if len(d1["line_color"])==0:
                    d1["line_color"]=default_color[icolor]
                    icolor+=1
                    if icolor==len(default_color):
                        icolor=0
                if len(d1["line_style"])==0:
                    d1["line_style"]="-"
                if len(d1["line_width"])==0:
                    d1["line_width"]=1.5
                d2=np.array(d1["values"])/plot_params_in["dens_scale"]
                ax.plot(parameters_list_main,d2,label=e1,c=d1["line_color"],ls=d1["line_style"],lw=d1["line_width"])
        if plot_params_in["dens_xaxis_log"]:
            ax.set_xscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax.set_xticks(plot_params_in["dens_xtick_labels"])
        ax.ticklabel_format(axis="y",useOffset=True,useMathText=True)
        ax.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        ax.set_ylabel(r"$\delta N_\mathrm{atom}\ \mathrm{[/scaled\ cell]}$",size=plot_params_in["label_size"])
        ax.legend(loc=0,fontsize=plot_params_in["ticks_size"],edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0)
        plt.xticks(locs1,labels2)
        ax.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        for f1 in plot_params_in["format"]:
            fig.savefig(root_outfiles+"_Natoms_delta."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig)
        ### Plot-eFermi
        fig=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]))
        ax=fig.add_subplot(111)
        ax.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        icolor=0
        for k1,d1 in datalist2.items():
            if k1.find("Fermi_level")==0:
                if len(d1["line_color"])==0:
                    d1["line_color"]=default_color[icolor]
                    icolor+=1
                    if icolor==len(default_color):
                        icolor=0
                if len(d1["line_style"])==0:
                    d1["line_style"]="-"
                if len(d1["line_width"])==0:
                    d1["line_width"]=1.5
                ax.plot(parameters_list_main,d1["values"],c=d1["line_color"],
                           ls=d1["line_style"],lw=d1["line_width"])
        if plot_params_in["dens_xaxis_log"]:
            ax.set_xscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax.set_xticks(plot_params_in["dens_xtick_labels"])
        ax.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        if plot_params_in["Edef_x_upper_limit"]=="BandGap":
            if plot_params_in["dens_xaxis_parameter"]=="espot":
                plot_params_in["Edef_x_upper_limit"]=-1.0*min(parameters_list_main)+Egap
            else:
                plot_params_in["Edef_x_upper_limit"]=Egap
        if plot_params_in["dens_xaxis_parameter"]=="espot":
            if plot_params_in["Edef_x_lower_limit"]>-1.0*max(parameters_list_main):
                plot_params_in["Edef_x_lower_limit"]=-1.0*max(parameters_list_main)
        ax.set_ylim([plot_params_in["Edef_x_lower_limit"],plot_params_in["Edef_x_upper_limit"]])
        if plot_params_in["dens_xaxis_parameter"]=="espot":
            x1=parameters_list_main[0]
            x2=parameters_list_main[-1]
            y1=-x1
            y2=-x2
            yl=plot_params_in["Edef_x_lower_limit"]
            yu=plot_params_in["Edef_x_upper_limit"]
            ax.plot([x1,x2],[y1,y2],color="k",ls="-",lw=2)
            ax.plot([x1,x2],[y1+Egap*0.5,y2+Egap*0.5],color="k",ls="--",lw=1)
            ax.plot([x1,x2],[y1+Egap,y2+Egap],color="k",ls="-",lw=2)
            ax.fill_between([x1,x2],[y1,y2],[yl,yl],color="gray",alpha=0.2,linewidth=0)
            ax.fill_between([x1,x2],[y1+Egap,y2+Egap],[yu,yu],color="gray",alpha=0.2,linewidth=0)
        else:
            ax.axhline(Egap*0.5,color="k",linestyle="--",linewidth=1)
            if plot_params_in["Edef_bands_fill"]:
                if plot_params_in["Edef_x_lower_limit"]<0.0:
                    ax.axhspan(plot_params_in["Edef_x_lower_limit"],0.0,color="gray",alpha=0.2,linewidth=0)
                if plot_params_in["Edef_x_upper_limit"]>Egap:
                    ax.axhspan(Egap,plot_params_in["Edef_x_upper_limit"],color="gray",alpha=0.2,linewidth=0)
        ax.set_ylabel(r"$\mathrm{Fermi\ level\ [eV]}$",size=plot_params_in["label_size"])
        plt.xticks(locs1,labels2)
        ax.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        for f1 in plot_params_in["format"]:
            fig.savefig(root_outfiles+"_FermiLevel."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig)
        ### Plot-total-charge
        fig=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]))
        ax=fig.add_subplot(111)
        ax.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        icolor=0
        for k1,d1 in datalist2.items():
            if k1.find("Total_charge")==0:
                if len(d1["line_color"])==0:
                    d1["line_color"]=default_color[icolor]
                    icolor+=1
                    if icolor==len(default_color):
                        icolor=0
                if len(d1["line_style"])==0:
                    d1["line_style"]="-"
                if len(d1["line_width"])==0:
                    d1["line_width"]=1.5
                d2=np.array(d1["values"])/plot_params_in["dens_scale"]
                ax.plot(parameters_list_main,d2,c=d1["line_color"],ls=d1["line_style"],lw=d1["line_width"])
        if plot_params_in["dens_xaxis_log"]:
            ax.set_xscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax.set_xticks(plot_params_in["dens_xtick_labels"])
        ax.axhline(0.0,color="k",ls=":",lw=1.0)
        ax.set_yscale("symlog",linthresh=10**-20)
        ax.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        ax.set_ylabel(r"$\mathrm{Total\ charge\ [e/scaled\ cell]}$",size=plot_params_in["label_size"])
        plt.xticks(locs1,labels2)
        ax.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        for f1 in plot_params_in["format"]:
            fig.savefig(root_outfiles+"_TotalCharage."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig)
        ### Plot-energy
        ###-- Screening defect species for plotting
        defects_list_screened={}
        for k1,d1 in datalist2.items():
            if k1.find("energy_")==0:
                dlist1=d1["values"]
                bool_plot=False
                for i1,p1 in enumerate(parameters_list_main):
                    d2=dlist1[i1]
                    if p1>=plot_params_in["dens_x_lower_limit"] and p1<=plot_params_in["dens_x_upper_limit"]\
                        and d2>plot_params_in["Edef_y_lower_limit"] and d2<plot_params_in["Edef_y_upper_limit"]:
                        bool_plot=True
                if bool_plot:
                    defects_list_screened[k1]=d1
        ###-- Plotting defect-energies without bundling
        fig1=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
        fig2legend=plt.figure(figsize=(plot_params_in["figsize_x_inch"]*0.5,plot_params_in["figsize_x_inch"]*0.5),constrained_layout=True)
        ax1=fig1.add_subplot(111)
        ax1.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        lines=[]
        legends=[]
        for k1,d1 in defects_list_screened.items():
            l1,=ax1.plot(parameters_list_main,d1["values"],c=d1["line_color"],ls=d1["line_style"],lw=d1["line_width"])
            lines.append(l1)
            legends.append(d1["label_legend_wQ"])
        if plot_params_in["Edef_zero_line"]:
            if np.abs(plot_params_in["Edef_y_lower_limit"])>1e-10:
                ax1.axhline(0.0,color="k",ls=":",lw=1.0)
        if plot_params_in["dens_xaxis_log"]:
            ax1.set_xscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax1.set_xticks(plot_params_in["dens_xtick_labels"])
        ax1.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        ax1.set_ylabel(plot_params_in["Edef_ylabel"],size=plot_params_in["label_size"])
        ax1.set_ylim([plot_params_in["Edef_y_lower_limit"],plot_params_in["Edef_y_upper_limit"]])
        ax1.set_xticks(locs1)  
        ax1.set_xticklabels(labels2)  
        ax1.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        num_data=len(defects_list_screened)
        ncol_df=int(np.floor(float(num_data)**0.5))
        fig2legend.legend(lines,legends,ncol=ncol_df,borderaxespad=0,fontsize=plot_params_in["label_size"],
            edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0)
        for f1 in plot_params_in["format"]:
            fig1.savefig(root_outfiles+"_defectFormEnergies_separated."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
            fig2legend.savefig(root_outfiles+"_defectFormEnergies_separated_legend."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig1)
        plt.close(fig2legend)
#######################################################################################
#######################################################################################
#######################################################################################
#######################################################################################
        ### Plot-density
        #### Marge same defect species
        datalist3={}
        for k1,d1 in datalist2.items():
            if k1.find("density_")==0:
                d1["values"]=np.array(d1["values"])
                datalist3[k1]=d1
        datalist4={}
        if plot_params_in["dens_merge"]:
            print("-"*50)
            print("  Defect densities are merged among same species (dens_merge = true)")
            print("         and plotted without (#) in legend")
            fout1.write("-"*50+"\n")
            fout1.write("  Defect densities are merged among same species (dens_merge = true)\n")
            fout1.write("         and plotted without (#) in legend\n")
            for k1,d1 in datalist3.items():
                if k1=="density_Hole" or k1=="density_Electron":
                    datalist4[k1]=d1
                    continue
                defid1=int(k1[k1.rfind("(")+1:k1.rfind(")")])
                d1copy=copy.deepcopy(d1)
                k12 = k1[:k1.rfind("(")]
                if defid1!=1:
                    continue
                bool_add2=False
                for k2,d2 in datalist3.items():
                    if k1==k2 or k2=="density_Hole" or k2=="density_Electron":
                        continue
                    defid2=int(k2[k2.rfind("(")+1:k2.rfind(")")])
                    k22=k2[:k2.rfind("(")]
                    if k12==k22:
                        print(f"    {k2} is added to {k1}")
                        fout1.write(f"    {k2} is added to {k1}\n")
                        d1copy["values"]+=d2["values"]
                        bool_add2=True
                if bool_add2:
                    label1=d1["label_legend_wQ"]
                    label1=label1[:label1.rfind("(")]+"$"
                    d1copy["label_legend_wQ"]=label1
                datalist4[k1]=d1copy
        else:
            datalist4=datalist3
        datalist5={}
        if plot_params_in["dens_merge_sites"]:
            print("-"*50)
            print("  Defect densities are merged among the same defects on different sites (dens_merge_sites = true)")
            print("         and plotted without [#] of defect_type in legend")
            fout1.write("-"*50+"\n")
            fout1.write("  Defect densities are merged among same species on different sites (dens_merge_sites = true)\n")
            fout1.write("         and plotted without [#] of defect_type in legend\n")
            keylist6=[]
            for k1,d1 in datalist4.items():
                if k1=="density_Hole" or k1=="density_Electron":
                    datalist5[k1]=d1
                    continue
                d1copy=copy.deepcopy(d1)
                k12 = copy.copy(k1)
                t51 = k12[:k12.find("[")+1]
                t52 = k12[k12.find("[")+1:k12.rfind("]")]
                t53 = k12[k12.rfind("]"):]
                while "[" in t52:
                    t52=t52[:t52.find("[")]+t52[t52.find("]")+1:]
                k12 = t51+t52+t53
                if k12 in keylist6:
                    continue
                bool_add2=False
                for k2,d2 in datalist4.items():
                    if k1==k2 or k2=="density_Hole" or k2=="density_Electron":
                        continue
                    k22=copy.copy(k2)
                    t51 = k22[:k22.find("[")+1]
                    t52 = k22[k22.find("[")+1:k22.rfind("]")]
                    t53 = k22[k22.rfind("]"):]
                    while "[" in t52:
                        t52=t52[:t52.find("[")]+t52[t52.find("]")+1:]
                    k22 = t51+t52+t53
                    if k12==k22:
                        print(f"    {k2} is added to {k1}")
                        fout1.write(f"    {k2} is added to {k1}\n")
                        d1copy["values"]+=d2["values"]
                        bool_add2=True
                if bool_add2:
                    label1=d1["label_legend_wQ"]
                    t52=label1
                    t61 = ""
                    t63 = ""
                    if "left[" in t52 and "right]" in t52:
                        t61 = t52[:t52.find("left[")+5]
                        t62 = t52[t52.find("left[")+5:t52.find("right]")-1]
                        t63 = t52[t52.find("right]")-1:]
                    else:
                        t62 = t52
                    while "[" in t62:
                        t62=t62[:t62.find("[")]+t62[t62.find("]")+1:]
                    label2=t61+t62+t63
                    d1copy["label_legend_wQ"]=label2
                    keylist6.append(k12)
                datalist5[k1]=d1copy
        else:
            datalist5=datalist4
        datalist4=datalist5
        #### Screening defect species for plotting
        for k1,d1 in datalist4.items():
            if plot_params_in["dens_unit_cm3"]:
                d1["values"]=d1["values"]*tocm3
            else:
                d1["values"]=d1["values"]/plot_params_in["dens_scale"]
        dens_highest1=0.0
        for k1,d1 in datalist4.items():
            dlist1=d1["values"]
            for i1,p1 in enumerate(parameters_list_main):
                dmax1=max(dlist1)
                if dens_highest1<dmax1:
                    dens_highest1=dmax1
        dens_highest2=dens_highest1*10.0
        if plot_params_in["dens_y_upper_limit_auto"]:
            plot_params_in["dens_y_upper_limit"]=dens_highest2
            print(f"  Automatically set dens_y_upper_limit")
            print(f"    dens_y_uppder_limit = {dens_highest2}")
            fout1.write(f"  Automatically set dens_y_upper_limit\n")
            fout1.write(f"    dens_y_uppder_limit = {dens_highest2}\n")
        if plot_params_in["dens_y_lower_limit_auto"]:
            dens_lowest1=dens_highest2/plot_params_in["dens_y_rangefactor_auto"]
            plot_params_in["dens_y_lower_limit"]=dens_lowest1
            print(f"  Automatically set dens_y_lower_limit")
            print(f"    dens_y_lower_limit = {dens_lowest1}")
            fout1.write(f"  Automatically set dens_y_lower_limit\n")
            fout1.write(f"    dens_y_lower_limit = {dens_lowest1}\n")
        if dens_highest2<plot_params_in["dens_y_lower_limit"]:
            dens_lowest1=dens_highest2/plot_params_in["dens_y_rangefactor_auto"]
            plot_params_in["dens_y_lower_limit"]=dens_lowest1
            print(f"  WARNING(plot):: Lower limit of density-axis is updated due to their tiny amounts.")
            print(f"    dens_y_lower_limit = {dens_lowest1}")
            fout1.write(f"  WARNING(plot):: Lower limit of density-axis is updated due to their tiny amounts.\n")
            fout1.write(f"    dens_y_lower_limit = {dens_lowest1}\n")
        defects_list_screened={}
        for k1,d1 in datalist4.items():
            dlist1=d1["values"]
            bool_plot=False
            for i1,p1 in enumerate(parameters_list_main):
                d2=dlist1[i1]
                if p1>=plot_params_in["dens_x_lower_limit"] and p1<=plot_params_in["dens_x_upper_limit"]\
                    and d2>plot_params_in["dens_y_lower_limit"] and d2<plot_params_in["dens_y_upper_limit"]:
                    bool_plot=True
            if bool_plot:
                defects_list_screened[k1]=d1
        #### Plotting defect-densities 
        fig1=plt.figure(figsize=(plot_params_in["figsize_x_inch"],plot_params_in["figsize_y_inch"]),constrained_layout=True)
        fig2legend=plt.figure(figsize=(plot_params_in["figsize_x_inch"]*0.5,plot_params_in["figsize_x_inch"]*0.5),constrained_layout=True)
        ax1=fig1.add_subplot(111)
        ax1.tick_params(axis="both",which="both",direction="in",top=True,right=True,labelsize=plot_params_in["ticks_size"],pad=plot_params_in["ticks_pad"])
        lines=[]
        legends=[]
        for k1,d1 in defects_list_screened.items():
            l1,=ax1.plot(parameters_list_main,d1["values"],c=d1["line_color"],ls=d1["line_style"],lw=d1["line_width"])
            lines.append(l1)
            legends.append(d1["label_legend_wQ"])
        if plot_params_in["dens_xaxis_log"]:
            ax1.set_xscale("log")
        ax1.set_ylim([plot_params_in["dens_y_lower_limit"],plot_params_in["dens_y_upper_limit"]])
        ax1.set_xlabel(plot_params_in["dens_xlabel"],size=plot_params_in["label_size"])
        ax1.set_ylabel(plot_params_in["dens_ylabel"],size=plot_params_in["label_size"])
        ax1.set_xticks(locs1)  
        ax1.set_xticklabels(labels2)  
        ax1.set_xlim([plot_params_in["dens_x_lower_limit"],plot_params_in["dens_x_upper_limit"]])
        if plot_params_in["dens_yaxis_log"]:
            ax1.set_yscale("log")
        if plot_params_in["dens_xtick_labels"]!="NONE":
            ax1.set_xticks(plot_params_in["dens_xtick_labels"])
        num_data=len(defects_list_screened)
        ncol_df=int(np.floor(float(num_data)**0.5))
        if len(lines)>0:
            fig2legend.legend(lines,legends,ncol=ncol_df,borderaxespad=0,fontsize=plot_params_in["label_size"],
            edgecolor="k",labelspacing=0.4,columnspacing=0.5,fancybox=False,framealpha=1.0)
        for f1 in plot_params_in["format"]:
            fig1.savefig(root_outfiles+"_defectDensities_separated."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
            fig2legend.savefig(root_outfiles+"_defectDensities_separated_legend."+f1,dpi=plot_params_in["dpi"],bbox_inches="tight")
        plt.close(fig1)
        plt.close(fig2legend)
        os.chdir("../")
    print("-"*100)
    fout1.write("-"*100+"\n")
    return
