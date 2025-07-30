#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Copyright 2021 Takafumi Ogawa
# Licensed under the Apache License, Version2.0.
#-----------------------------------------------------------------------------
# pydecs-solver module
#-----------------------------------------------------------------------------
import os
import sys
import copy
import numpy as np
from scipy import optimize
from scipy import interpolate

from pydecs.defects import Defects
from pydecs.host import Host
from pydecs.inout import plot_Edef_eFermi

class LineOptError(Exception):
    pass

class DefectEqSolver:

    def calc_defEne_single(self,temperature_in,chempots_in,eFermi_in):
        self.defects.update_defect_energies_densities(temperature_in,chempots_in,eFermi_in)
        (dens_hole,dens_elec)=self.host.calc_electronic_carrier_densities(temperature_in,eFermi_in)
        qtot_out=dens_hole-dens_elec
        for dt1 in self.defects.get_defect_types():
            qtot_out+=self.defects.get_charge(dt1)*self.defects.get_defect_density(dt1)
        return qtot_out

    def calc_defEne_wrt_eFermi(self,temperature_in,chempots_in,emin,emax,edel):
        enum=int(np.floor((emax-emin)/edel))
        energy_list=np.linspace(emin,emax,enum)
        qtot_list=[]
        defect_energy_list={}
        for dt1 in self.defects.get_defect_types():
            defect_energy_list[dt1]=[]
        for eF1 in energy_list:
            qtot=self.calc_defEne_single(temperature_in,chempots_in,eF1)
            qtot_list.append(qtot)
            for dt1 in defect_energy_list.keys():
                defect_energy_list[dt1].append(self.defects.get_defect_energy(dt1))
        return (energy_list,qtot_list,defect_energy_list)

    def output_defEne_wrt_eFermi(self,temperature_in,chempots_in,root_outfiles,plot_params_in):
        if not "Edef_x_lower_limit" in plot_params_in.keys():
            plot_params_in["Edef_x_lower_limit"]=0.0
        if not "Edef_x_upper_limit" in plot_params_in.keys():
            plot_params_in["Edef_x_upper_limit"]=self.host.get_Egap()
        if plot_params_in["Edef_x_upper_limit"]<plot_params_in["Edef_x_lower_limit"]:
            print(" ERROR:: emax is less than emin in eFermi search.")
            print("   Please check the input file")
            print("   plot.Edef_x_lower_limit and plot.Edef_x_upper_limit")
            sys.exit()
        if not "Edef_x_delta" in plot_params_in.keys():
            plot_params_in["Edef_x_delta"]=(plot_params_in["Edef_x_upper_limit"]-plot_params_in["Edef_x_lower_limit"])/100.0
        (energy_list,qtot_list,defect_energy_list)=self.calc_defEne_wrt_eFermi(temperature_in,chempots_in,
            plot_params_in["Edef_x_lower_limit"],plot_params_in["Edef_x_upper_limit"],plot_params_in["Edef_x_delta"])
        fnout_csv=root_outfiles+"_Edef_eFermi.csv"
        fout=open(fnout_csv,"w")
        fout.write("# Egap = "+str(self.host.get_Egap())+"\n")
        str1="line_color,"
        for dt1 in defect_energy_list.keys():
            str1+=","+self.defects.get_line_color(dt1)
        fout.write(str1+"\n")
        str1="line_style,"
        for dt1 in defect_energy_list.keys():
            str1+=","+self.defects.get_line_style(dt1)
        fout.write(str1+"\n")
        str1="line_width,"
        for dt1 in defect_energy_list.keys():
            str1+=","+str(self.defects.get_line_width(dt1))
        fout.write(str1+"\n")
        str1="Fermi_level,Total_charge"
        for dt1 in defect_energy_list.keys():
            def_label=self.defects.get_label(dt1)
            str1+=","+def_label
        fout.write(str1+"\n")
        for i1,e1 in enumerate(energy_list):
            fout.write(str(e1)+","+str(qtot_list[i1]))
            for dt1 in defect_energy_list.keys():
                fout.write(","+str(defect_energy_list[dt1][i1]))
            fout.write("\n")
        fout.close()
        plot_Edef_eFermi(fnout_csv,root_outfiles,plot_params_in)

    def opt_defEne_wrt_eFermi(self,temperature_in,chempots_in,emin,emax,edel):
        (energy_list,qtot_list,defect_energy_list)=self.calc_defEne_wrt_eFermi(temperature_in,chempots_in,emin,emax,edel)
        q_min=1.0e10
        eFermiQ0=-1.0e10
        for ie1,e1 in enumerate(energy_list):
            q1=np.fabs(qtot_list[ie1])
            if q1<q_min:
                q_min=q1
                eFermiQ0=e1
        qtotQ0=self.calc_defEne_single(temperature_in,chempots_in,eFermiQ0)
        return (eFermiQ0,qtotQ0)

    def reset_id_loop_eFermi(self):
        self.id_loop_eFermi=1
        return

    def opt_eFermi_for_chempots(self,temperature_in,chempots_in,opt_params_in,root_outfiles):
        if not "opt_eFermi_type" in opt_params_in.keys():
            opt_params_in["opt_eFermi_type"]="root_scalar"
            # opt_params_in["opt_eFermi_type"]="single_search+root_scalar"
        if not "opt_eFermi_tol" in opt_params_in.keys():
            opt_params_in["opt_eFermi_tol"]=1e-10
        if not "opt_eFermi_emin" in opt_params_in.keys():
            opt_params_in["opt_eFermi_emin"]=self.host.get_Egap()*0.001
        if not "opt_eFermi_emax" in opt_params_in.keys():
            opt_params_in["opt_eFermi_emax"]=self.host.get_Egap()*0.999
        if not "opt_eFermi_edel" in opt_params_in.keys():
            opt_params_in["opt_eFermi_edel"]=self.host.get_Egap()*0.01
        if not "opt_eFermi_output_detail" in opt_params_in.keys():
            opt_params_in["opt_eFermi_output_detail"]=False
        if not "opt_eFermi_output_atlast" in opt_params_in.keys():
            opt_params_in["opt_eFermi_output_atlast"]=False

        if opt_params_in["opt_eFermi_output_detail"]:
            fnout_detail=root_outfiles+"_Edef_detail.txt"
            option_open="a"
            if self.id_loop_eFermi==1:
                option_open="w"
            fout1=open(fnout_detail,option_open)
            fout1.write(f" [opt_eFermi] id_loop_eFermi = {self.id_loop_eFermi:>3}\n")
            fout1.write(f" [opt_eFermi] id_loop_Nsites = {self.id_loop_Nsites:>3}\n")
            str1=""
            i_cnt=1
            for at1,cp1 in chempots_in.items():
                str1+=f" mu_{at1:<2} = {cp1:20.15f} ;"
                if i_cnt%3==0:
                    str1=str1[:-1]+"\n"
                i_cnt+=1
            str1=str1[:-1]+"\n"
            fout1.write(str1)
            fout1.write("    Fermi_level    |    Total charge    |\n")

        def func_eFermi_local(eF_in):
            res_qtot=self.calc_defEne_single(temperature_in,chempots_in,eF_in)
            if opt_params_in["opt_eFermi_output_detail"]:
                fout1.write(f" {eF_in:17.14f} |  {res_qtot:17.10e} |\n")
            return res_qtot
        if opt_params_in["opt_eFermi_type"]=="single_search":
            (res_eF,res_qtot)=self.opt_defEne_wrt_eFermi(temperature_in,chempots_in,
                    opt_params_in["opt_eFermi_emin"],opt_params_in["opt_eFermi_emax"],
                    opt_params_in["opt_eFermi_edel"])
        elif opt_params_in["opt_eFermi_type"]=="single_search+root_scalar":
            (res_eF0,res_qtot0)=self.opt_defEne_wrt_eFermi(temperature_in,chempots_in,
                    opt_params_in["opt_eFermi_emin"],opt_params_in["opt_eFermi_emax"],
                    opt_params_in["opt_eFermi_edel"])
            res_eF=optimize.brentq(func_eFermi_local,res_eF0-2.0*opt_params_in["opt_eFermi_edel"],
                                    res_eF0+2.0*opt_params_in["opt_eFermi_edel"])
            res_qtot=self.calc_defEne_single(temperature_in,chempots_in,res_eF)
        elif opt_params_in["opt_eFermi_type"]=="root_scalar":
            try:
                res_eF=optimize.root_scalar(func_eFermi_local,bracket=[opt_params_in["opt_eFermi_emin"],
                            opt_params_in["opt_eFermi_emax"]],method="ridder")
            except ValueError:
                print(" WARNING(opt_eFermi):: Failed to find Fermi level satisfying chage neutrality condition.")
                return(None,None)
            #res_eF=optimize.root_scalar(func_eFermi_local,bracket=[opt_params_in["opt_eFermi_emin"],
            #                opt_params_in["opt_eFermi_emax"]],method="brenth")
            res_eF=res_eF.root
            res_qtot=self.calc_defEne_single(temperature_in,chempots_in,res_eF)
        else:
            print(" WARNING:: unknown optimization parameter opt_eFermi_tpye: "+opt_params_in["opt_eFermi_type"])
        if res_qtot>opt_params_in["opt_eFermi_tol"]:
            print(" WARNING(opt_eFermi):: qtot is larger than tolerant value.")
            print("    qtot="+str(res_qtot)+" ;  tolerance(qtot) = "+str(opt_params_in["opt_eFermi_tol"]))
        if opt_params_in["opt_eFermi_output_detail"]:
            fout1.write("-"*100+"\n")
            fout1.close()
        if opt_params_in["opt_eFermi_output_atlast"]:
            self.output_defEne_wrt_eFermi(temperature_in,chempots_in,root_outfiles,opt_params_in["opt_eFermi_edel"])
        self.id_loop_eFermi+=1
        return (res_eF,res_qtot)

    def update_Nsites_defective(self):
        self.host.reset_Nsites_defective()
        for dt1 in self.defects.get_defect_types():
            Nsites_dt1=self.defects.get_occ_sites(dt1)
            dens1=self.defects.get_defect_density(dt1)
            for s1,n1 in Nsites_dt1.items():
                self.host.add_Nsite_defective(s1,-dens1*n1)
        return
    
    def calc_residual_Nsites(self,Nsites_prev,Nsites_new):
        residuals_out={}
        residual_rms=0.0
        for s1,n1 in Nsites_prev.items():
            n2=Nsites_new[s1]
            residuals_out[s1]=n2-n1
            residual_rms+=(n1-n2)**2
        residuals_out["RMS"]=residual_rms
        return residuals_out

    def reset_id_loop_Nsites(self):
        self.id_loop_Nsites=1
        return

    def outstr_Nsites_head(self,chempot_in):
        str_out=f" [opt_Nsites] id_loop_Nsites = {self.id_loop_Nsites:>3}\n"
        i_cnt=1
        for at1,cp1 in chempot_in.items():
            str_out+=f" mu_{at1:<2} = {cp1:20.15f} ;"
            if i_cnt%3==0:
                str_out=str_out[:-1]+"\n"
            i_cnt+=1
        str_out=str_out[:-1]+"\n"
        str_out+=f"       eFermi       |   qtot   | "
        for s1,n1 in self.host.get_Nsites_perfect().items():
            s2="dNs_"+s1
            str_out+=f"{s2:<9}| "
        str_out+=f"RMS(dNs) |"
        return str_out

    def outstr_Nsites(self,eF,qtot,residuals_Nsites):
        str_out=f"  {eF:17.14f} | {qtot:+8.1e} | "
        for s1,n1 in residuals_Nsites.items():
            str_out+=f"{n1:+8.1e} | "
        return str_out

    def opt_Nsites_for_chempots(self,temperature_in,chempots_in,opt_params_in,root_outfiles,plot_params_in={}):
        if not "opt_Nsites_fixed_at_perfect" in opt_params_in.keys():
            opt_params_in["opt_Nsites_fixed_at_perfect"]=False
        if not "opt_Nsites_tol" in opt_params_in.keys():
            opt_params_in["opt_Nsites_tol"]=1e-10
        if not "opt_Nsites_maxloop" in opt_params_in.keys():
            opt_params_in["opt_Nsites_maxloop"]=1000
        if not "opt_Nsites_output" in opt_params_in.keys():
            opt_params_in["opt_Nsites_output"]="both"
        if not "opt_Nsites_output_Edef_atlast" in opt_params_in.keys():
            opt_params_in["opt_Nsites_output_Edef_atlast"]=True
        if opt_params_in["opt_Nsites_output"]=="both":
            bool_output_std=True
            bool_output_file=True
        elif opt_params_in["opt_Nsites_output"]=="file":
            bool_output_std=False
            bool_output_file=True
        elif opt_params_in["opt_Nsites_output"]=="std":
            bool_output_std=True
            bool_output_file=False
        elif opt_params_in["opt_Nsites_output"]=="none":
            bool_output_std=False
            bool_output_file=False
        if root_outfiles=="NONE":
            bool_output_file=False

        if bool_output_file:
            fn_out=root_outfiles+"_Nsites_loop.txt"
            option_open="a"
            if self.id_loop_Nsites==1:
                option_open="w"
            else:
                if not os.path.exists(fn_out):
                    option_open="w"
            fout1=open(fn_out,mode=option_open)
        def outdata_local(str_out):
            if bool_output_std:
                print(str_out)
            if bool_output_file:
                fout1.write(str_out+"\n")

        self.host.reset_Nsites_defective()
        outdata_local(self.outstr_Nsites_head(chempots_in))
        if opt_params_in["opt_Nsites_fixed_at_perfect"]:
            (res_eF,res_qtot)=self.opt_eFermi_for_chempots(temperature_in,chempots_in,opt_params_in,root_outfiles)
        else:
            residualRMS_Nsites=opt_params_in["opt_Nsites_tol"]*2.0
            Nsites_previous=self.host.get_Nsites_perfect()
            i_loop=1
            while residualRMS_Nsites>opt_params_in["opt_Nsites_tol"] and i_loop<opt_params_in["opt_Nsites_maxloop"]:
                (res_eF,res_qtot)=self.opt_eFermi_for_chempots(temperature_in,chempots_in,opt_params_in,root_outfiles)
                if self.defects.check_minus_defect_energy():
                    print(" ERROR(opt_Nsites):: Densities cannot be obtained for negative defect formation energies.")
                    print("    You can check these by setting 'just_plot_Edef = True' in the input file (inpydecs.toml).")
                    # print("   Check output-files: *_Edef_eFermi.*  ")
                    return None
                self.update_Nsites_defective()
                Nsites_new=self.host.get_Nsites_defective()
                residuals_Nsites=self.calc_residual_Nsites(Nsites_previous,Nsites_new)
                residualRMS_Nsites=residuals_Nsites["RMS"]
                outdata_local(self.outstr_Nsites(res_eF,res_qtot,residuals_Nsites))
                Nsites_previous=copy.deepcopy(Nsites_new)
                i_loop+=1
            if i_loop==opt_params_in["opt_Nsites_maxloop"]:
                print(" WARNING(opt_Nsites):: Nsites_loop reached maxloop:"+str(i_loop))
        data_defect_densities=self.produce_outheader_density(temperature_in,chempots_in,res_eF,res_qtot,self.host.get_Egap(),self.host.get_Volume())
        # fnout_csv=root_outfiles+"_defect_densities.csv"
        # self.output_density_data(data_defect_densities,fnout_csv)
        if opt_params_in["opt_Nsites_output_Edef_atlast"]:
            self.output_defEne_wrt_eFermi(temperature_in,chempots_in,root_outfiles,plot_params_in)
            self.calc_defEne_single(temperature_in,chempots_in,res_eF)
        self.id_loop_Nsites+=1
        outdata_local("-"*100)
        if bool_output_file:
            fout1.close()
        return data_defect_densities

    #def output_density_data(self,data_in,out_filename):
    #    fout=open(out_filename,"w")
    #    for i1 in range(len(data_in[0])):
    #        str1=""
    #        for d1 in data_in:
    #            str1+=str(d1[i1])+","
    #        fout.write(str1[:-1]+"\n")
    #    fout.close()
    #    return

    def produce_outheader_density(self,temperature_in,chempots_in,eFermi_in,qtot_in,Egap,Vol):
        outdata_all=[]
        outdata_all.append([" Egap = "+str(Egap),"line_color","line_style","line_width","condition","this_dir"])
        outdata_all.append([" Volume = "+str(Vol),"","","","temperature",temperature_in])
        (Natoms_def,Natoms_host)= self.defects.calc_Natoms()
        elems_list=[]
        for s1 in self.host.get_siteList():
            es1=self.host.get_atom_at_site(s1)
            if not es1 in elems_list and es1!="NONE":
                elems_list.append(es1)
        for e1,nat1 in Natoms_def.items():
            if not e1 in elems_list:
                elems_list.append(e1)
        for e1 in elems_list:
            cp1=chempots_in[e1]
            outdata_all.append(["","","","","chempot_"+e1,cp1])
        for e1 in elems_list:
            nat1=Natoms_def[e1]
            outdata_all.append(["","","","","Natom_"+e1,nat1])
        for e1 in elems_list:
            nat1=Natoms_def[e1]
            nat2=Natoms_host[e1]
            outdata_all.append(["","","","","delta_Natom_"+e1,nat1-nat2])
        for s1 in self.host.get_siteList():
            outdata=["","","",""]
            outdata.append("Nsite_"+s1)
            outdata.append(self.host.get_Nsite_defective(s1))
            outdata_all.append(outdata)
        for s1 in self.host.get_siteList():
            outdata=["","","",""]
            outdata.append("delta_Nsite_"+s1)
            outdata.append(self.host.get_Nsite_defective(s1)-self.host.get_Nsite_perfect(s1))
            outdata_all.append(outdata)
        outdata_all.append(["","","","","Fermi_level",eFermi_in])
        outdata_all.append(["","","","","Total_charge",qtot_in])
        outdata_all.append(["","k","-","1.5","density_Hole",self.host.get_hole_density()])
        outdata_all.append(["","k","--","1.5","density_Electron",self.host.get_electron_density()])
        for dt1 in self.defects.get_defect_types():
            outdata=[""]
            outdata.append(self.defects.get_line_color(dt1))
            outdata.append(self.defects.get_line_style(dt1))
            outdata.append(self.defects.get_line_width(dt1))
            outdata.append("density_"+self.defects.get_label(dt1))
            outdata.append(self.defects.get_defect_density(dt1))
            outdata_all.append(outdata)
        for dt1 in self.defects.get_defect_types():
            outdata=[""]
            outdata.append(self.defects.get_line_color(dt1))
            outdata.append(self.defects.get_line_style(dt1))
            outdata.append(self.defects.get_line_width(dt1))
            outdata.append("energy_"+self.defects.get_label(dt1))
            outdata.append(self.defects.get_defect_energy(dt1))
            outdata_all.append(outdata)
        return outdata_all


    def opt_steady_line_minimization(self,func_resid,vect_grad,cp0,step_size,fout=None,tol_in=1e-7,maxiter=1000):
        fout.write(f" ------ Starting stepwise minimization with step size of {step_size} -----\n")
        residArray0=func_resid(cp0)
        if residArray0 is None:
            return (None,None)
        # resid0=np.max(np.fabs(residArray0))
        # resid0=np.sqrt(np.square(residArray0).mean(axis=0))
        resid0=np.linalg.norm(residArray0)
        cp1=[]
        for i1,v1 in enumerate(vect_grad):
            cp1.append(cp0[i1]+step_size*v1)
        i_loop=0
        while i_loop<maxiter:
            residArray1=func_resid(cp1)
            if residArray1 is None:
                return (None,None)
            resid1=np.max(np.fabs(residArray1))
            # resid1=np.sqrt(np.square(residArray1).mean(axis=0))
            resid1=np.linalg.norm(residArray1)
            if resid1>resid0:
                break
            else:
                cp2=[]
                for i1,v1 in enumerate(vect_grad):
                    cp2.append(cp1[i1]+step_size*v1)
                cp0=cp1
                residArray0=residArray1
                resid0=resid1
                cp1=cp2
            i_loop+=1
        print("finished: stepwise minimization")
        fout.write(" ------ Starting golden minimization -----\n")
        print(" [opt_Natoms] Starting minimization")
        def func_resid_local(x_in):
            cp2=[]
            for i1 in range(len(cp0)):
                cp2.append(x_in*cp0[i1]+(1.0-x_in)*cp1[i1])
            residArray2=func_resid(cp2)
            if residArray2 is None:
                raise LineOptError("Minimization error!")
            # resid2=np.max(np.fabs(residArray2))
            # resid2=np.sqrt(np.square(residArray2).mean(axis=0))
            resid2=np.linalg.norm(residArray2)
            return resid2
        try:
            # res3=optimize.minimize_scalar(func_resid_local,bracket=(0.0,1.0),method="golden",tol=tol_in,options={'xtol':tol_in})
            res3=optimize.minimize_scalar(func_resid_local,bracket=(0.0,1.0),method="golden",tol=1e-5,options={'xtol':1e-10})
        except LineOptError:
            return(None,None)
        cp3=[]
        for i1 in range(len(cp0)):
            cp3.append(res3.x*cp0[i1]+(1.0-res3.x)*cp1[i1])
        residArray3=func_resid(cp3)
        if residArray3 is None:
            return (None,None)
        resid3=np.max(np.fabs(residArray3))
        # resid3=np.sqrt(np.square(residArray3).mean(axis=0))
        resid3=np.linalg.norm(residArray3)
        print("finished: opt_steady_line_minimization")
        return(cp3,residArray3)

    def opt_chempot_multi(self,func_resid,func_grad,cp0,delta_cp,damping_rate,fout,tol,maxiter):
        cp2=copy.copy(cp0)
        delta_cp2=delta_cp
        residArray2=func_resid(cp2)
        if residArray2 is None:
            return (None,None)
        vgrad2=func_grad(residArray2)
        resid2=np.max(np.fabs(residArray2))
        resid2=np.linalg.norm(residArray2)
        CGalgo="PR" ### PR may be best
        for iloop1 in range(maxiter):
            ###### CG
            if iloop1%(len(cp0)*2)==0:
                cgvect2=copy.copy(vgrad2)
            else:
                cgvect1=copy.copy(cgvect2)
                cgfact1=0.0
                cgfact2=0.0
                ## Fletcher-Reeves
                if CGalgo=="FR":
                    for i1 in range(len(cp0)):
                        cgfact2+=vgrad2[i1]**2
                        cgfact1+=vgrad1[i1]**2
                ## Polak-Ribiere
                elif CGalgo=="PR":
                    for i1 in range(len(cp0)):
                        cgfact2+=vgrad2[i1]*(vgrad2[i1]-vgrad1[i1])
                        cgfact1+=vgrad1[i1]**2
                ## Hestenes-Stiefel
                elif CGalgo=="HS":
                    for i1 in range(len(cp0)):
                        cgfact2+=vgrad2[i1]*(vgrad2[i1]-vgrad1[i1])
                        cgfact1-=cgvect1[i1]*(vgrad2[i1]-vgrad1[i1])
                ## Dai-Yuan
                elif CGalgo=="DY":
                    for i1 in range(len(cp0)):
                        cgfact2+=vgrad2[i1]**2
                        cgfact1-=cgvect1[i1]*(vgrad2[i1]-vgrad1[i1])
                #######################
                betaCG2=cgfact2/cgfact1
                if CGalgo=="PR" and betaCG2<0.0:
                    betaCG2=0.0
                cgvect2=[]
                for i1 in range(len(cp0)):
                    cgvect2.append(vgrad2[i1]+betaCG2*cgvect1[i1])
            vgrad1=copy.copy(vgrad2)
            cgvect2abs=0.0
            for i1,v1 in enumerate(cgvect2):
                cgvect2abs+=v1**2
            cgvect2abs=cgvect2abs**0.5
            cgvect3=[]
            for i1,v1 in enumerate(cgvect2):
                cgvect3.append(v1/cgvect2abs)
            fout.write(f" ----- New search starting ({iloop1+1}) -----\n")
            fout.write(f" ----- Gradient for the line search = {cgvect3} -----\n")
            (cp3,residArray2)=self.opt_steady_line_minimization(func_resid,cgvect3,cp2,delta_cp2,fout,0.01*tol,maxiter)
            if residArray2 is None:
                return (None,None)
            if damping_rate=="DividedByNsteps":
                delta_cp2=delta_cp/(iloop1+2.0)
            else:
                delta_cp2*=damping_rate
            cp2=cp3
            vgrad2=func_grad(residArray2)
            # resid2=np.max(np.fabs(residArray2))
            resid2=np.linalg.norm(residArray2)
            if resid2<tol:
                break
        print("finished: opt_chempot_multi")
        return(cp2,residArray2)

    def opt_Natoms(self,temperature_in,chempots_in,Natoms_target_in,
                   opt_params_in,root_outfiles,plot_params_in):
        if not "opt_Natoms_tol" in opt_params_in.keys():
            opt_params_in["opt_Natoms_tol"]=1e-4
        if not "opt_Natoms_maxloop" in opt_params_in.keys():
            opt_params_in["opt_Natoms_maxloop"]=1000
        if not "opt_Natoms_output" in opt_params_in.keys():
            opt_params_in["opt_Natoms_output"]="both"
        if not "opt_Natoms_output_every_step" in opt_params_in.keys():
            opt_params_in["opt_Natoms_output_every_step"]=False
        if not "opt_Natoms_delta_chempot" in opt_params_in.keys():
            opt_params_in["opt_Natoms_delta_chempot"]=0.1
        if not "opt_Natoms_delta_chempot_damping_rate" in opt_params_in.keys():
            opt_params_in["opt_Natoms_delta_chempot_damping_rate"]="DividedByNsteps"

        self.reset_id_loop_Nsites()
        self.reset_id_loop_eFermi()
        Natoms_elem_list=[]
        Natoms_target_list=[]
        Natoms_chempot0_list=[]
        Natoms_chempot_results_list=[]
        for nat1 in Natoms_target_in:
            Natoms_elem_list.append(nat1["element"])
            Natoms_target_list.append(nat1["target_Natoms"])
            Natoms_chempot0_list.append(nat1["chempot_init"])

        bool_output_std=False
        bool_output_file=False
        if opt_params_in["opt_Natoms_output"]=="both":
            bool_output_std=True
            bool_output_file=True
        elif opt_params_in["opt_Natoms_output"]=="file":
            bool_output_file=True
        elif opt_params_in["opt_Natoms_output"]=="std":
            bool_output_std=True
        if bool_output_file:
            fout1=open(root_outfiles+"_Natoms_loop.txt","w")
            str1=" [Natoms] \n"
            str1+=" Atoms with constant chemical potential: "
            for at1,cp1 in chempots_in.items():
                str1+=f"{at1} ,"
            str1=str1[:-1]+"\n"
            i_cnt=1
            for at1,cp1 in chempots_in.items():
                str1+=f" mu_{at1:<2} = {cp1:20.15f} ;"
                if i_cnt%3==0:
                    str1=str1[:-1]+"\n"
                i_cnt+=1
            str1=str1[:-1]+"\n"
            for ie1,e1 in enumerate(Natoms_elem_list):
                str1+=f" target_Nat({e1}) =  {Natoms_target_list[ie1]}\n"
            str1=str1[:-1]+"\n"
            fout1.write(str1)
            str_outlabel=""
            for e1 in Natoms_elem_list:
                str_outlabel+=f"   mu_{e1:<3}          |   Nat_{e1:<3}         |    delNat_{e1:<3}      |"
            str_outlabel+=f"    max(residual)   |"
            fout1.write(str_outlabel+"\n")
        if opt_params_in["opt_Natoms_output_every_step"]:
            opt_params_in["opt_Nsites_output_Edef_atlast"]=True
        else:
            opt_params_in["opt_Nsites_output_Edef_atlast"]=False
        def output_local(cp_new,Nat_new,delNat_new):
            str1=""
            # resid_new=np.sqrt(np.square(delNat_new).mean(axis=0))
            # resid_new=np.max(np.fabs(delNat_new))
            resid_new=np.linalg.norm(delNat_new)
            for ie1,e1 in enumerate(Natoms_elem_list):
                str1+=f" {cp_new[ie1]:17.14f} | {Nat_new[ie1]:17.14f} | {delNat_new[ie1]:18.11e} |"
            str1+=f" {resid_new:18.11e} |"
            if bool_output_std:
                print(" [Natoms] "+str_outlabel)
                print(" [Natoms] "+str1)
                print("-"*100)
            if bool_output_file:
                fout1.write(str1+"\n")
        print(" [opt_Natoms] Starting")
        def func_resid_fixNatoms(cp_in):
            cp1=copy.deepcopy(chempots_in)
            for icp1,cp_in1 in enumerate(cp_in):
                cp1[Natoms_elem_list[icp1]]=cp_in1
            out_defect_densities=self.opt_Nsites_for_chempots(temperature_in,cp1,opt_params_in,root_outfiles)
            if out_defect_densities is None:
                return None
            del_nat_array=[]
            nat_array=[]
            nat_dict=self.defects.get_Natoms_list()
            for icp1,cp_in1 in enumerate(cp_in):
                nat2=nat_dict[Natoms_elem_list[icp1]]
                nat3=Natoms_target_list[icp1]
                del_nat_array.append(nat2-nat3)
                nat_array.append(nat2)
            output_local(cp_in,nat_array,del_nat_array)
            return del_nat_array
        def func_grads_fixNatoms(residArray_in):
            jacob1=self.defects.get_Jacobian(Natoms_elem_list,temperature_in)
            vect_grads=np.zeros(len(Natoms_elem_list))
            a1=1.0/(np.linalg.norm(residArray_in)**0.5)
            for ie1,e1 in enumerate(Natoms_elem_list):
                for ie2,e2 in enumerate(Natoms_elem_list):
                    vect_grads[ie1]-=a1*residArray_in[ie2]*jacob1[ie2][ie1]
            return vect_grads
        (Natoms_chempot_results_list,res_delNat)=self.opt_chempot_multi(
                func_resid_fixNatoms,func_grads_fixNatoms,
                Natoms_chempot0_list,opt_params_in["opt_Natoms_delta_chempot"],
                opt_params_in["opt_Natoms_delta_chempot_damping_rate"],
                fout1,opt_params_in["opt_Natoms_tol"],
                opt_params_in["opt_Natoms_maxloop"])
        if Natoms_chempot_results_list is None:
            return None
        print(" [opt_Natoms] Finished")
        cp_list=copy.deepcopy(chempots_in)
        for iat1,nat1 in enumerate(Natoms_elem_list):
            cp_list[nat1]=Natoms_chempot_results_list[iat1]
        # (res_eF,res_qtot)=self.opt_eFermi_for_chempots(temperature_in,cp_list,opt_params_in,root_outfiles)
        # self.output_defEne_wrt_eFermi(temperature_in,cp_list,root_outfiles,plot_params_in)
        # out_defect_densities=self.produce_outheader_density(temperature_in,cp_list,res_eF,res_qtot,self.host.get_Egap(),self.host.get_Volume())
        # opt_params_in["opt_Nsites_output_Edef_atlast"]=bk_opt_Nsites_output_Edef_atlast
        opt_params_in["opt_Nsites_output_Edef_atlast"]=True
        out_defect_densities=self.opt_Nsites_for_chempots(temperature_in,cp_list,opt_params_in,root_outfiles,plot_params_in)
        if bool_output_file:
            fout1.close()
        return out_defect_densities

    def __init__(self,input_params_host,elements_in,input_paths_in,densform_in,root_outfiles):
        self.host=Host(input_params_host,input_paths_in,root_outfiles)
        self.defects=Defects(self.host,elements_in,input_paths_in,densform_in,root_outfiles)
        self.reset_id_loop_Nsites()
        self.reset_id_loop_eFermi()
        self.chempots_fixNatoms="NONE"
        return

    def opt_coordinator(self,eq_cond_in,solver_params_in,root_outfiles,plot_params_in):
        if not "opt_Natoms_chempot_init" in solver_params_in.keys():
            solver_params_in["opt_Natoms_chempot_init"]="fix"
        temp=eq_cond_in["T"]
        chempots={}
        for l1, v1 in eq_cond_in.items():
            if "chempot_" in l1:
                e1=l1.split("_")[1].strip()
                chempots[e1]=v1
        if "espot" in eq_cond_in.keys():
            self.host.set_espot(eq_cond_in["espot"])
            self.defects.set_espot(eq_cond_in["espot"])
        if not "just_plot_Edef" in solver_params_in:
            solver_params_in["just_plot_Edef"]=False
        if solver_params_in["just_plot_Edef"]:
            print(" [solver] Just plotting Edef")
            if "fix_Natoms" in eq_cond_in.keys():
                print("   WARNING: fix_Natoms detected.")
                print("   chemical potentials set to [eq.fix_Natoms.chempot_init] values.")
                for fix1 in eq_cond_in["fix_Natoms"]:
                    chempots[fix1["element"]]=fix1["chempot_init"]
            self.output_defEne_wrt_eFermi(temp,chempots,root_outfiles,plot_params_in)
            return None

        bool_fixNatoms=False
        self.eqlabel_fixNatoms="NONE"
        for k1 in eq_cond_in.keys():
            if k1=="fix_Natoms":
                bool_fixNatoms=True
                self.eqlabel_fixNatoms="fix_Natoms"
            elif k1=="fix_Natoms_linked":
                bool_fixNatoms=True
                self.eqlabel_fixNatoms="fix_Natoms_linked"
        if bool_fixNatoms:
            if solver_params_in["opt_Natoms_chempot_init"]=="update" and self.chempots_fixNatoms!="NONE":
                for ie1,eq1 in enumerate(eq_cond_in[self.eqlabel_fixNatoms]):
                    e1=eq1["element"]
                    eq1["chempot_init"]=self.chempots_fixNatoms[e1]
            defect_densities=self.opt_Natoms(temp,chempots,eq_cond_in[self.eqlabel_fixNatoms],solver_params_in,root_outfiles,plot_params_in)
            if defect_densities is None:
                return None
            if solver_params_in["opt_Natoms_chempot_init"]=="update":
                self.chempots_fixNatoms={}
                for ie1,eq1 in enumerate(eq_cond_in[self.eqlabel_fixNatoms]):
                    e1=eq1["element"]
                    for d1 in defect_densities:
                        if d1[-2]=="chempot_"+e1:
                            self.chempots_fixNatoms[e1]=float(d1[-1])
        else:
            defect_densities=self.opt_Nsites_for_chempots(temp,chempots,solver_params_in,root_outfiles,plot_params_in)
        
        return defect_densities
