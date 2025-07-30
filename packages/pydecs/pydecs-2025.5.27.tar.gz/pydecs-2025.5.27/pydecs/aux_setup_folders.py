#!/usr/bin/env python3
import toml
import glob
import os
import sys
import copy
import shutil
import argparse

elems_valences = {
    "H":  "+1; 0/-1",
    "He": "0",
    "Li": "+1; 0",
    "Be": "0",
    "B":  "+3; +2/+1/0",
    "C":  "+4/+2/-4; +3/+1/0/-1/-2/-3",
    "N":  "-3; 0/-1/-2/-3",
    "O":  "-2; -1/0",
    "F":  "-1",
    "Ne": "0",
    "Na": "+1; 0",
    "Mg": "+2; +1/0",
    "Al": "+3; +2/+1/0",
    "Si": "+4; +3//0",
    "P":  "+5; +4//0",
    "S":  "+6; +4//0",
    "Cl": "-1; 0",
    "Ar": "0",
    "K":  "+1; 0",
    "Ca": "+2; +1/0",
    "Sc": "+3; +2/+1/0",
    "Ti": "+4/+3; +2/+1/0",
    "V":  "+5; +4/+3/+2/+1/0",
    "Cr": "+3; +2/+1/0",
    "Mn": "+4/+2; +1/0",
    "Fe": "+3/+2; +1/0",
    "Co": "+3/+2; +4/+1/0",
    "Ni": "+2/+3; +1/0",
    "Cu": "+2/+1; 0",
    "Zn": "+2; +1/0",
    "Ga": "+3; +2//0",
    "Ge": "+4; +3/+2/+1/0",
    "As": "+3/+5; +4/+2/+1/0",
    "Se": "-2; -1/0",
    "Br": "-1; 0",
    "Kr": "0",
    "Rb": "+1; 0",
    "Sr": "+2; +1/0",
    "Y":  "+3; +2//0",
    "Zr": "+4; +3//0",
    "Nb": "+5; +4//0",
    "Mo": "+6; +5//0",
    "Tc": "+7; +6//0",
    "Ru": "+4/+3; +2/+1/0",
    "Rh": "+3; +2/+1/0",
    "Pd": "+4; +3/+2/+1/0",
    "Ag": "+1; +2/0",
    "Cd": "+2; +1/0",
    "In": "+3; +2/+1/0",
    "Sn": "+4; +3//0",
    "Sb": "+5; +4//0",
    "Te": "+6; +5//0",
    "I":  "-1; 0",
    "Xe": "0",
    "Cs": "+1; 0",
    "Ba": "+2; +1/0",
    "La": "+3; +2//0",
    "Ce": "+3/+4; +4//0",
    "Pr": "+3/+4; +4//0",
    "Nd": "+3; +2//0",
    "Pm": "+3; +2//0",
    "Sm": "+3/+2; +1/0",
    "Eu": "+3/+2; +1/0",
    "Gd": "+3; +2/+1/0",
    "Tb": "+3/+4; +2/+1/0",
    "Dy": "+3; +2/+1/0",
    "Ho": "+3; +2/+1/0",
    "Er": "+3; +2/+1/0",
    "Tm": "+3; +2/+1/0",
    "Yb": "+3/+2; +1/0",
    "Lu": "+3; +2/+1/0",
    "Hf": "+4; +3/+2/+1/0",
    "Ta": "+5; +4/+3/+2/+1/0",
    "W":  "+6; +5/+4/+3/+2/+1/0",
    "Re": "+7/+6; +5/+4/+3/+2/+1/0",
    "Os": "+4; +3/+2/+1/0",
    "Ir": "+3; +2/+1/0",
    "Pt": "+2/+4; +3/+1/0",
    "Au": "+1; 0",
    "Hg": "+1; 0",
    "Tl": "+1; 0",
    "Pb": "+2/+4; +3/+1/0",
    "Bi": "+3; +2/+1/0",
    "Po": "+4; +3/+2/+1/0",
    "At": "-1; 0",
    "Rn": "0",
}

def parse_valence(val_in: str):
    v1 = val_in.split(";")
    v1main = []
    v2 = v1[0]
    if "//" in v2:
        v3 = [ int(t1.strip()) for t1 in v2.split("//")]
        if v3[0]>v3[1]:
            step3 = -1
        else:
            step3 = +1
        v4 = list(range(v3[0],v3[1]+step3,step3))
    else:
        v4 = [ int(t1.strip()) for t1 in v2.split("/")]
    for v5 in v4:
        if v5 not in v1main:
            v1main.append(v5)
    v1sub = []
    if len(v1)==2:
        v2 = v1[1]
        if "//" in v2:
            v3 = [ int(t1.strip()) for t1 in v2.split("//")]
            if v3[0]>v3[1]:
                step3 = -1
            else:
                step3 = +1
            v4 = list(range(v3[0],v3[1]+step3,step3))
        else:
            v4 = [ int(t1.strip()) for t1 in v2.split("/")]
        for v5 in v4:
            if v5 not in v1sub and v5 not in v1main:
                v1sub.append(v5)
    return {"main":v1main, "sub":v1sub}

# def setup_folders_vasp(toml_path="inpydecs_setup.toml"):
def setup_folders_vasp():
    parser = argparse.ArgumentParser(
        prog='pydecs-run-setupFolders',
        description='Generating folders for VASP run'
    )
    parser.add_argument(
        'input_toml', 
        nargs="?",
        type=str, 
        default="inpydecs_setup.toml",
        help='Path to input toml file')
    parser.add_argument(
        "-p", "--print_template",
        action="store_true",
        help='Printout template input file (inpydecs_genDefs.toml)')
    args = parser.parse_args()
    toml_path = args.input_toml
    if args.print_template:
        str_input_template = """
input_paths_strs = ["",""]

valence.Ga = "+3; +2//0"
valence.O = "-2; -1//0"

# set_nupdown = true

"""
        if not os.path.exists(toml_path):
            fout1 = open("inpydecs_setup.toml","w")
            fout1.write(str_input_template)
        else:
            print(str_input_template)
            print("### Input-file name is \"inpydecs_setup.toml\", wihch already exists in this folder.")
        sys.exit()

    print(f"  Starting setup_folders_vasp")
    run_list = open("run_list.txt", "w")
    if not os.path.exists(toml_path):
        print(f"  Error: '{toml_path}' not found.")
        print(f"    Template file is output by option \"-p\" ")
        sys.exit()
    params_in = toml.load(toml_path)

    input_paths = params_in.get("input_paths_strs")
    if input_paths is None:
        sys.exit("  Error: Key 'input_paths_strs' not found in the input file.")

    set_nupdown = False
    input_nupdown = params_in.get("set_nupdown")
    if input_paths != None:
        set_nupdown = input_nupdown
    print(f"  set_nupdown = {set_nupdown}")

    valences_dict1 = copy.deepcopy(elems_valences)
    input_vals = params_in.get("valence")
    if input_paths != None:
        for k1,v1 in input_vals.items():
            if k1 not in valences_dict1:
                print(f"  {k1} for the valence setting from the input file, not exist in the default element list, but continued.")
            valences_dict1[k1] = v1

    vasp_files = []
    print(f"  Searching vasp files:")
    for p in input_paths:
        pattern = os.path.join(p, "defModel_*.vasp")
        matched = glob.glob(pattern)
        print(f"    Folder-name: '{p}'")
        print(f"      Found {len(matched)} files.")
        vasp_files.extend(matched)
    vasp_files.sort()

    if not vasp_files:
        print("Warning: No files matching 'defModel_*.vasp' were found in the specified directories.")
    elems_set = set()
    for f1 in vasp_files:
        f2 = os.path.basename(f1)
        if "supercell" in f2:
            continue
        f3 = f2.split("_")
        e1 = f3[2].strip()
        e2 = f3[3].strip()
        e3 = e2.split("[")[0]
        if "vac" != e1.lower():
            elems_set.add(e1)
        if "int" != e3.lower():
            elems_set.add(e3)
    str1 = "  Elements:"
    for e1 in elems_set:
        str1 += f" {e1},"
    print(f"{str1[:-1]}")
    
    valences_dict2 = {}
    for e1 in elems_set:
        v1 = valences_dict1[e1]
        valences_dict2[e1] = parse_valence(v1)
    print(f"  Valence list:")
    for k2,v2 in valences_dict2.items():
        str1 = f"    {k2}-main:"
        for v3 in v2["main"]:
            str1 += f" {v3},"
        print(f"{str1[:-1]}")
        str1 = f"    {k2}-sub:"
        for v3 in v2["sub"]:
            str1 += f" {v3},"
        print(f"{str1[:-1]}")
    
    cwd = os.getcwd()
    path_INCAR_temp = os.path.join(cwd, "INCAR_temp")
    path_kpoints = os.path.join(cwd, "KPOINTS")
    if not os.path.exists(path_INCAR_temp):
        sys.exit(f"  Error: INCAR_temp not found: '{path_INCAR_temp}'")
    if not os.path.exists(path_kpoints):
        path_kpoints = None
    for f1 in vasp_files:
        f2 = os.path.basename(f1)
        fol3 = f2[f2.find("_")+1:f2.find(".vasp")]
        os.makedirs(fol3, exist_ok=True)
        print(f"  Making der: {fol3} ")
        shutil.copy(f1, fol3)
        with open(f1) as fin1:
            fin2 = fin1.readlines()
            elems = [ t1.strip() for t1 in fin2[5].split()]
            natoms =  [ int(t1) for t1 in fin2[6].split()]
        path_POTCAR = os.path.join(fol3, "POTCAR")
        NELECT = 0
        with open(path_POTCAR, "w") as f_pot:
            for e1,n1 in zip(elems,natoms):
                pot_src = os.path.join(cwd, f"POTCAR_{e1}")
                if not os.path.exists(pot_src):
                    sys.exit(f"  Error: POTCAR_<elem> not found: '{pot_src}'")
                zval1 = None
                with open(pot_src) as f_in:
                    l1 = f_in.readline()
                    while l1:
                        f_pot.write(l1)
                        if "ZVAL" in l1:
                            zval1 = int(float(l1.split()[5]))
                        l1 = f_in.readline()
                NELECT += zval1*n1
        print(f"    {NELECT = }")
        qmain_list =[]
        qsub_list =[]
        def3 = fol3[fol3.find("_")+1:]
        if "supercell" in def3:
            qmain_list.append(0)
        else:
            def4 = def3.split("_")
            e4 = def4[0]
            s4 = def4[1]
            es4 = s4.split("[")[0]
            qe4_main = [0]
            qe4_sub = [0]
            if e4 in valences_dict2:
                qe4_main = valences_dict2[e4]["main"]
                qe4_sub = valences_dict2[e4]["sub"]
            qes4_main = [0]
            qes4_sub = [0]
            if es4 in valences_dict2:
                qes4_main = valences_dict2[es4]["main"]
                qes4_sub = valences_dict2[es4]["sub"]
            for q4 in qe4_main:
                for qs4 in qes4_main:
                    dq4 = q4-qs4
                    if dq4 not in qmain_list:
                        qmain_list.append(dq4)
            qsub_list =[]
            for q4 in qe4_main+qe4_sub:
                for qs4 in qes4_main+qes4_sub:
                    dq4 = q4-qs4
                    if dq4 not in qmain_list and dq4 not in qsub_list:
                        qsub_list.append(dq4)
            qmain_list.sort(reverse=True)
            qsub_list.sort(reverse=True)
        for iq1,q1 in enumerate(qmain_list+qsub_list):
            folder2 = os.path.join(fol3,f"{iq1+1:03}_q{q1}")
            os.makedirs(folder2, exist_ok=True)
            print(f"    Making der: {folder2} ")
            NUDlist = ["None"]
            if set_nupdown:
                for q2 in qmain_list:
                    dq12 = abs(q2-q1)
                    NUDlist_tmp = list(range(dq12,-1,-2))
                    for nud1 in NUDlist_tmp:
                        if nud1 not in NUDlist:
                            NUDlist.append(nud1)
            print(f"      {NUDlist = }")
            for inud1,nud1 in enumerate(NUDlist):
                # folder3 = f"{folder2}/{inud1+1:03}_nud{nud1}"
                folder3 = os.path.join(folder2,f"{inud1+1:03}_nud{nud1}")
                os.makedirs(folder3, exist_ok=True)
                print(f"      Making der: {folder3} ")
                shutil.copy(f1, os.path.join(folder3, "POSCAR"))
                if path_kpoints != None:
                    shutil.copy(path_kpoints, os.path.join(folder3, "KPOINTS"))
                shutil.copy(path_POTCAR, os.path.join(folder3, "POTCAR"))

                nelect3 = NELECT - q1
                out_path = os.path.join(folder3, "INCAR_temp2")
                with open(out_path, "w") as fout:
                    fout.write(f"\nNELECT = {nelect3}\n")
                    if nud1 != "None":
                        fout.write(f"NUPDOWN = {nud1}\n")
                    with open(path_INCAR_temp) as fin:
                        fout.write(fin.read())
                run_list.write(os.path.abspath(folder3) + "\n")


    return 


if __name__ == "__main__":
    setup_folders_vasp()


