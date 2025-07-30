#!/usr/bin/env python
#---------------------------------------------------------------------------
# Copyright 2025 Takafumi Ogawa
# Licensed under the Apache License, Version2.0.
#---------------------------------------------------------------------------
# Auxiliary tool of pydecs library for preparation
#---------------------------------------------------------------------------
import os,sys
import argparse
import warnings
import glob
import math
import random
import copy
import csv
import subprocess
import toml
import shutil
from itertools import product
from collections import Counter
from collections import defaultdict
from pathlib import Path
import numpy as np
import pandas as pd
sys.tracebacklimit = 0

def _ensure_pmg():
    try:
        import pymatgen
        import pymatgen.analysis
        import pandas
    # except ModuleNotFoundError:
    except ImportError:
        raise RuntimeError(
            "  Error!! Additional libraries for this function\n"
            "          pymatgen, pymatgen-analysis-defects, pandas\n"
            "  -> pip install pydecs[prep]\n"
        )

def poscar_to_cif():
    _ensure_pmg()
    import pandas as pd
    from pymatgen.core import Structure,Element
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
    from pymatgen.io.vasp.inputs import Poscar
    from pymatgen.io.vasp.outputs import Chgcar
    from pymatgen.io.cif import CifWriter
    from pymatgen.analysis.structure_matcher import StructureMatcher
    from pymatgen.analysis.defects.utils import get_local_extrema

    warnings.filterwarnings("ignore", category=DeprecationWarning, module="spglib.spglib")
    parser = argparse.ArgumentParser(
        prog='pydecs-prep-poscar2cif',
        description='Convert VASP POSCAR/CONTCAR to symmetry-aware CIF file'
    )
    parser.add_argument(
        'input_POSCAR_file',
        type=Path,
        help='Path to POSCAR/CONTCAR file (e.g., POSCAR.vasp)'
    )
    parser.add_argument(
        '-o', '--output_cif_file',
        type=Path,
        default=None,
        help='Optional output CIF filename (default: input_file with .cif suffix)'
    )
    parser.add_argument(
        '--symprec',
        type=float,
        default=1e-3,
        help='Distance tolerance for symmetry finding (Angs.), default: 1e-3'
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--primitive',
                       action='store_true',
                       help='Output primitive cell CIF')
    group.add_argument('-c', '--conventional',
                       action='store_true',
                       help='Output conventional cell CIF')
    group.add_argument('-k','--keep-cell',
                       action='store_true',
                       help='Output CIF of the original cell without symmetry refinement')
    group.add_argument('-b', '--both',
                       action='store_true',
                       help='Output conventional and primitive cell CIF')

    args = parser.parse_args()
    if not (args.primitive or args.conventional or args.keep_cell or args.both):
        args.both = True
    input_path: Path = args.input_POSCAR_file
    symprec: float = args.symprec
    if args.output_cif_file:
        output_path: Path = args.output_cif_file
        #if output_path.suffix.lower() != '.cif':
        #    output_path = output_path.with_suffix('.cif')
    else:
        output_path = Path(input_path.name)
        # with_suffix('.cif')
    output_path = output_path.stem
    print(f"-"*60)
    print(f"  Starting pydecs-prep-poscar2cif")
    print(f"    Input POSCAR file: {input_path}")
    structure = Poscar.from_file(input_path).structure
    print(f"-"*60)

    if args.primitive or args.both:
        target = SpacegroupAnalyzer(structure, symprec=symprec).get_primitive_standard_structure()
        writer = CifWriter(target, symprec=symprec, write_site_properties=True, refine_struct=False)
        print(f"="*60)
        print("==== Using primitive cell for CIF")
        output_path2 = f"{output_path}_prim.cif"
        writer.write_file(output_path2)
        print(f"==== Generated CIF: {output_path2}")
        sga_orig = SpacegroupAnalyzer(structure, symprec=symprec)
        conv_struct = sga_orig.get_primitive_standard_structure()
        sga = SpacegroupAnalyzer(conv_struct, symprec=symprec)
        symm_struct = sga.get_symmetrized_structure()
        print(symm_struct)
        print(f"="*60)
    if args.conventional or args.both:
        target = SpacegroupAnalyzer(structure, symprec=symprec).get_conventional_standard_structure()
        writer = CifWriter(target, symprec=symprec, write_site_properties=True, refine_struct=False)
        print(f"="*60)
        print("==== Using conventional cell for CIF")
        output_path2 = f"{output_path}_conv.cif"
        writer.write_file(output_path2)
        print(f"==== Generated CIF: {output_path2}")
        sga = SpacegroupAnalyzer(structure, symprec=symprec)
        symm_struct = sga.get_symmetrized_structure()
        print(symm_struct)
        print(f"="*60)
    if args.keep_cell:
        target = structure
        writer = CifWriter(target, write_site_properties=True, refine_struct=False)
        print(f"="*60)
        print("==== Using original input cell for CIF")
        output_path2 = f"{output_path}.cif"
        writer.write_file(output_path2)
        print(f"==== Generated CIF: {output_path2}")
        sga = SpacegroupAnalyzer(structure, symprec=symprec)
        symm_struct = sga.get_symmetrized_structure()
        print(symm_struct)
        print(f"="*60)

def cif_to_poscar():
    _ensure_pmg()
    from pymatgen.core import Structure
    from pymatgen.io.vasp.inputs import Poscar
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="spglib.spglib")
    parser = argparse.ArgumentParser(
        prog='pydecs-prep-cif2poscar',
        description='Convert CIF file to VASP POSCAR/CONTCAR'
    )
    parser.add_argument(
        'input_cif_file',
        type=Path,
        help='Path to CIF file (e.g., Au.cif)'
    )
    parser.add_argument(
        '-o', '--output_poscar_file',
        type=Path,
        default=None,
        help='Optional output POSCAR filename (default: input_file with .vasp suffix)'
    )
    parser.add_argument(
        '--symprec',
        type=float,
        default=1e-3,
        help='Distance tolerance for symmetry finding (Angs.), default: 1e-3'
    )
    parser.add_argument(
        "-s", "--supercell",
        nargs=3,
        type=int,
        default=[1,1,1],
        metavar=("a","b","c"),
        help="Supercell size"
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-p', '--primitive',
                       action='store_true',
                       help='Output primitive cell POSCAR')
    group.add_argument('-c', '--conventional',
                       action='store_true',
                       help='Output conventional cell POSCAR')
    group.add_argument('-k','--keep-cell',
                       action='store_true',
                       help='Output CIF of the original cell without symmetry refinement')

    args = parser.parse_args()
    input_path: Path = args.input_cif_file
    symprec: float = args.symprec
    mult_sc: list = args.supercell
    if args.output_poscar_file:
        output_path: Path = args.output_poscar_file
        if output_path.suffix.lower() != '.vasp':
            output_path = output_path.with_suffix('.vasp')
    else:
        output_path = input_path.with_suffix('.vasp')
    print(f"-"*60)
    print(f"  Starting pydecs-prep-cif2poscar")
    print(f"    Input POSCAR file: {input_path}")
    structure = Structure.from_file(input_path)

    if args.primitive:
        target = SpacegroupAnalyzer(structure, symprec=symprec).get_primitive_standard_structure()
        print("    Using primitive cell for CIF")
    elif args.conventional:
        target = SpacegroupAnalyzer(structure, symprec=symprec).get_conventional_standard_structure()
        print("    Using conventional cell for CIF")
    elif args.keep_cell:
        target = structure
        print("    Using original input cell for CIF")
    else:
        target = SpacegroupAnalyzer(structure, symprec=symprec).get_conventional_standard_structure()
        print("    Using conventional cell for CIF")
    print(f"Making supercell: {mult_sc[0]} x {mult_sc[1]} x {mult_sc[2]}")
    target2 = target.make_supercell(mult_sc)
    Poscar(target).write_file(output_path)
    print(f"    Generated POSCAR: {output_path}")
    print(f"-"*60)

def group_by_symmetry():
    _ensure_pmg()
    import pandas as pd
    from pymatgen.core import Structure,Element
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
    from pymatgen.io.vasp.inputs import Poscar
    from pymatgen.io.vasp.outputs import Chgcar
    from pymatgen.io.cif import CifWriter
    from pymatgen.analysis.structure_matcher import StructureMatcher
    from pymatgen.analysis.defects.utils import get_local_extrema

    warnings.filterwarnings("ignore", category=DeprecationWarning, module="spglib.spglib")
    parser = argparse.ArgumentParser(
        prog='pydecs-prep-groupSymm',
        description="Group POSCAR atoms by crystallographic independent sites"
    )
    parser.add_argument(
        'input_POSCAR_file',
        type=Path,
        help='Path to POSCAR/CONTCAR file (e.g., POSCAR.vasp)'
    )
    parser.add_argument(
        "-o", "--output_POSCAR_file",
        type=Path,
        default=None,
        help='Optional output filename (default: input_file with _grouped.vasp suffix)'
    )
    parser.add_argument(
        "--symprec", 
        type=float, 
        default=1e-3,
        help='Distance tolerance for symmetry finding (Angs.), default: 1e-3'
    )
    args = parser.parse_args()
    input_path: Path = args.input_POSCAR_file
    symprec: float = args.symprec
    if args.output_POSCAR_file:
        output_path: Path = args.output_POSCAR_file
    else:
        output_path = input_path
        output_path = output_path.parent / f"{output_path.stem}_grouped.vasp"
    print(f"-"*60)
    print(f"  Starting pydecs-prep-sepSiteLabels")
    print(f"    Input file: {input_path}")

    struct = Structure.from_file(input_path)
    sga = SpacegroupAnalyzer(struct, symprec=symprec)
    symm_struct = sga.get_symmetrized_structure()
    eq_sites = symm_struct.equivalent_sites  # List[List[PeriodicSite]]
    eq_indices = symm_struct.equivalent_indices # List[List[int]]

    dataset = sga.get_symmetry_dataset()
    wyckoffs = dataset.wyckoffs             # List[str]

    # species_groups1 = defaultdict(list)
    coords_groups1 = []
    indices_groups1 = []
    symbols_list1 = []
    symbols_list2 = []
    wyckoffs_list1 = []
    count_list1 = []
    for sites, idxs in zip(eq_sites, eq_indices):
        symbol = sites[0].specie.symbol
        symbols_list1.append(symbol)
        if symbol not in symbols_list2:
            symbols_list2.append(symbol)
        coords_groups1.append(sites)
        indices_groups1.append(idxs)
        multiplicity = len(idxs)
        count_list1.append(multiplicity)
        w1 = f"{multiplicity}{wyckoffs[idxs[0]]}"
        wyckoffs_list1.append(w1)
    atlabel_list3 = []
    cnt_list1 = Counter(symbols_list1)
    for s1 in symbols_list1:
        icnt1 = cnt_list1[s1]
        for i1 in range(icnt1):
            atlabel = f"{s1}[{i1+1}]"
            if atlabel not in atlabel_list3:
                atlabel_list3.append(atlabel)

    print("    Wyckoff mapping:")
    fnout = output_path.parent / f"{output_path.stem}_Wyckoff_mapping.csv"
    fout = open(fnout,"w")
    fout.write("Group-ID, Wyckoff label\n")
    for iw1, w1 in enumerate(wyckoffs_list1):
        atlabel1 = atlabel_list3[iw1]
        print(f"      {atlabel1} = {w1}")
        fout.write(f"{atlabel1} , {w1}\n")

    with open(output_path, 'w') as f:
        f.write(f"Grouped by site-symmetry (symprec={symprec})\n")
        f.write("1.0\n")
        for vec in struct.lattice.matrix:
            f.write("  ".join(f"{x:.16f}" for x in vec) + "\n")
        f.write("  ".join(atlabel_list3) + "\n")
        str1 = " "
        for c1 in count_list1:
            str1 += f"{c1} "
        f.write(str1+"\n")
        f.write("Direct\n")
        for ic1, c1 in enumerate(coords_groups1):
            for c2 in c1:
                c3 = c2.frac_coords
                f.write(f"  {c3[0]}  {c3[1]}  {c3[2]}\n")
    print(f"    Written grouped POSCAR on output-file: {output_path}")
    print(f"-"*60)

def check_duplication():
    _ensure_pmg()
    import pandas as pd
    from pymatgen.core import Structure,Element
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
    from pymatgen.io.vasp.inputs import Poscar
    from pymatgen.io.vasp.outputs import Chgcar
    from pymatgen.io.cif import CifWriter
    from pymatgen.analysis.structure_matcher import StructureMatcher
    from pymatgen.analysis.defects.utils import get_local_extrema

    parser = argparse.ArgumentParser(
        prog='pydecs-prep-chkDupl',
        description="Group identical structure files by similarity"
    )
    parser.add_argument(
        "input_POSCARs",
        nargs='+',
        help="File paths or glob patterns for input structure files"
    )
    parser.add_argument(
        "-o", "--output",
        default="out_duplication.csv",
        help="Output CSV file name (default: out_duplication.csv)"
    )
    parser.add_argument(
        "-t", "--tolerance",
        type=float,
        default=1e-4,
        help="Tolerance for StructureMatcher (both ltol and stol), default=1e-4"
    )
    args = parser.parse_args()

    # Expand inputs using glob and dedupe
    all_files = []
    for pattern in args.input_POSCARs:
        matched = glob.glob(pattern)
        if not matched and pattern:  # if no glob match, but file may exist literally
            matched = [pattern]
        all_files.extend(matched)
    # Remove duplicates and sort
    files = sorted(set(all_files))
    print(f"-"*60)
    print(f"  Starting pydecs-prep-chkDupl")
    print("  "+f"-"*30)
    print(f"  Input files: ")
    for f1 in files:
        print(f"    {f1}")
    print("  "+f"-"*30)

    if not files:
        print(f"  No files found for inputs: {args.input_POSCARs}")
        return

    # Initialize matcher
    matcher = StructureMatcher(ltol=args.tolerance, stol=args.tolerance)
    groups = []  # each group is a list of filenames

    # Group structures
    for file in files:
        struct = Structure.from_file(file)
        placed = False
        for grp in groups:
            ref_struct = Structure.from_file(grp[0])
            if matcher.fit(struct, ref_struct):
                grp.append(file)
                placed = True
                break
        if not placed:
            groups.append([file])

    # Sort groups by descending size
    groups.sort(key=len, reverse=True)

    # Prepare DataFrame: columns are groups, rows are filenames
    max_len = max(len(grp) for grp in groups)
    data = {}
    for i, grp in enumerate(groups, start=1):
        header = f"group-{i}<{len(grp)}>"
        filenames = grp + [""] * (max_len - len(grp))
        data[header] = filenames

    df = pd.DataFrame(data)
    df.to_csv(args.output, index=False)

    # Print summary
    print(f"  Output of each group")
    for i, grp in enumerate(groups, start=1):
        #print(f"    group-{i}<{len(grp)}>: {', '.join(grp)}")
        print(f"    group-{i}<{len(grp)}>:")
        for g1 in grp:
            print(f"      {g1}")
    print("  "+f"-"*30)
    print(f"  Duplication groups written to {args.output}")
    print(f"-"*60)


def find_interstitial_from_CHGCAR():
    _ensure_pmg()
    import pandas as pd
    from pymatgen.core import Structure,Element
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
    from pymatgen.io.vasp.inputs import Poscar
    from pymatgen.io.vasp.outputs import Chgcar
    from pymatgen.io.cif import CifWriter
    from pymatgen.analysis.structure_matcher import StructureMatcher
    from pymatgen.analysis.defects.utils import get_local_extrema

    parser = argparse.ArgumentParser(
        prog='pydecs-prep-findIntCHGCAR',
        description='Detect and process interstitial sites from CHGCAR and POSCAR'
    )
    parser.add_argument(
        'chgcar', 
        type=Path, 
        help='Path to input CHGCAR file')
    parser.add_argument(
        "-t", "--tolerance",
        type=float, 
        default=1e-4,
        help='Tolerance for local extrema detection')
    parser.add_argument(
        '--symprec',
        type=float, 
        default=1e-4,
        help='Tolerance for symmetry finding')
    parser.add_argument(
        '--prefix', 
        type=str, 
        default="outInt",
        help='Prefix for outputs, default: outInt')
    args = parser.parse_args()
    print(f"-"*60)
    print(f"  Starting pydecs-prep-findInt-CHGCAR")
    print(f"  Input CHGCAR: {args.chgcar}")
    print("  "+f"-"*30)

    # step-1: Extract minima
    chg = Chgcar.from_file(str(args.chgcar))
    minima = get_local_extrema(chg, find_min=True)
    coords_list = []
    info = []
    for i, site in enumerate(minima, start=1):
        # support PeriodicSite, numpy.ndarray, or tuple/list
        if hasattr(site, 'frac_coords'):
            coords = site.frac_coords
        elif isinstance(site, np.ndarray):
            coords = site
        elif isinstance(site, (tuple, list)) and isinstance(site[0], (np.ndarray, list, tuple)):
            coords = np.array(site[0])
        else:
            raise TypeError(f"Unexpected type from get_local_extrema: {type(site)}")
        coords_list.append(coords)
        info.append({'index': i, 'x': float(coords[0]), 'y': float(coords[1]), 'z': float(coords[2])})
    fnout1 = args.prefix+"_01_localMinima.csv"
    pd.DataFrame(info).to_csv(fnout1, index=False)
    print(f"  ###  Step-1  ###")
    print(f"  Interstitial info written to {fnout1}")
    print("  "+f"-"*30)

    # step-2: Individual POSCARs
    print(f"  ###  Step-2  ###")
    orig = chg.structure
    folout1 = args.prefix+"_02_POSCARsWithInt"
    folout1 = Path(folout1)
    folout1.mkdir(exist_ok=True)
    for i, coords in enumerate(coords_list, start=1):
        st = orig.copy()
        st.append('Rn', coords.tolist(), coords_are_cartesian=False)
        out = folout1 / f"POSCAR_{i:04d}.vasp"
        Poscar(st).write_file(out)
    print(f"  Generated {len(coords_list)} single-site POSCARs in {folout1}")
    print("  "+f"-"*30)

    # step-3: Check duplications in the POSCARs with interstitials
    print(f"  ###  Step-3  ###")
    path3 = f"{folout1}/POSCAR_*.vasp"
    fnout3 = args.prefix+"_03_duplication.csv"
    sys.argv = [
        "pydecs-prep-chkDupl",
        "-o", fnout3,
        "-t",str(args.tolerance),
        *glob.glob(path3),
        ]
    print(f"  Running duplication check")
    check_duplication()

    # step-4: Combined POSCARs and CIFs check
    print(f"  ###  Step-4  ###")
    elements = sorted({site.specie.symbol for site in orig},
                      key=lambda x: Element(x).Z, reverse=True)
    header4 = None 
    groups4 = []
    with open(fnout3, newline='', encoding='utf-8') as f:
        f2 = f.readline()
        header4 = f2.split(",")
        for j2 in range(len(header4)):
            groups4.append([])
        f2 = f.readline()
        while f2: 
            g2 = f2.split(",")
            for j2 in range(len(header4)):
                g3 = g2[j2].strip()
                if len(g3)>0:
                    groups4[j2].append(g3)
            f2 = f.readline()
    multiplicities = []
    for h1 in header4:
        h2 = int(h1[h1.find("<")+1:h1.rfind(">")])
        multiplicities.append(h2) 
    coords_list4 = []
    for i1,g1 in enumerate(groups4):
        coords_list4tmp = []
        for d1 in g1:
            j4 = d1[d1.rfind("POSCAR_")+7:d1.rfind(".vasp")]
            c4 = coords_list[int(j4)-1]
            coords_list4tmp.append(c4)
        coords_list4.append(coords_list4tmp)
    folout4 = args.prefix+"_04_POSCARandCIF_forEachIntGroups"
    folout4 = Path(folout4)
    folout4.mkdir(exist_ok=True)

    for gi, coords4 in enumerate(coords_list4, start=1):
        st = orig.copy()
        for c4 in coords4:
            st.append('Rn', c4.tolist(), coords_are_cartesian=False)
        fnout = folout4 / f"POSCARwIntGrouped_{gi:04d}.vasp"
        Poscar(st).write_file(fnout)
        sga = SpacegroupAnalyzer(st, symprec=args.symprec)
        refined = sga.get_refined_structure()
        fnout = folout4 / f"POSCARwIntGrouped_{gi:04d}.cif"
        CifWriter(refined, symprec=args.symprec).write_file(fnout)
    print(f"  Generated {len(coords_list4)} POSCARs with grouped interstitials in {folout4}")
    print("  "+f"-"*30)
    
    # step-5: Append interstitial labels to grouped POSCAR
    print(f"  ###  Step-5  ###")
    fnout5 = args.prefix+"_05_POSCAR_withAllInt.vasp"
    st = orig.copy()
    for gi, coords4 in enumerate(coords_list4, start=1):
        for c4 in coords4:
            st.append('Rn', c4.tolist(), coords_are_cartesian=False)
    Poscar(st).write_file(fnout5)
    print(f"  POSCAR with all interstitials: {fnout5}")
    sys.argv = [
        "pydecs-prep-poscar2cif",
        fnout5,
        ]
    print(f"  Converting to cif from POSCAR")
    poscar_to_cif()

    #sga = SpacegroupAnalyzer(st, symprec=args.symprec)
    #refined = sga.get_refined_structure()
    #fnout5cif = args.prefix+"_05_POSCAR_withAllInt.cif"
    #CifWriter(refined, symprec=args.symprec).write_file(fnout5cif)
    #print(f"  cif-file with all interstitials: {fnout5cif}")
    print("  "+f"-"*30)

    # step-6: POSCAR to grouped POSCAR
    print(f"  ###  Step-6  ###")
    fnout6 = args.prefix+"_06_POSCAR_withAllInt_grouped.vasp"
    sys.argv = [
        "pydecs-prep-chkDupl",
        "-o", fnout6,
        "--symprec", str(args.symprec),
        fnout5,
        ]
    print(f"  Grouping by symmetry")
    group_by_symmetry()
    print("  "+f"-"*30)

def output_defect_poscar(fnout_in,latt_in,sites_in,coords_dict_in,
                         coord_def=None,dev_cutoff=0.0,dev_dict=None):
    elems2 = []
    for s1 in sites_in:
        s2 = s1[:s1.find("[")]
        if s2 not in elems2:
            elems2.append(s2)
    natoms2 = []
    coords2 = {}
    for e2 in elems2:
        nat2 = 0
        coords1 = []
        for is1,s1 in enumerate(sites_in):
            if e2 in s1:
                coords1 += coords_dict_in[s1]
        coords2[e2] = coords1
        natoms2.append(len(coords1))
    if dev_cutoff>0.001:
        inv_latt_in = np.linalg.inv(latt_in)
        coords2rand = {}
        for e2 in elems2:
            dev2 = dev_dict["common"]
            if e2 in dev_dict.keys():
                dev2 = dev_dict[e2]
            coords2rand[e2] = []
            coords3 = coords2[e2]
            for c3 in coords3:
                d4 = [c3[0]-coord_def[0],
                      c3[1]-coord_def[1],
                      c3[2]-coord_def[2]]
                for i4 in range(3):
                    if d4[i4]>1.0:
                        d4[i4]-=1.0
                    elif d4[i4]<-1.0:
                        d4[i4]+=1.0
                d4real = d4 @ latt_in
                d4realabs = np.linalg.norm(d4real)
                if d4realabs < dev_cutoff:
                    c3real = c3 @ latt_in
                    c5real = [c3real[0]+random.random()*dev2,
                              c3real[1]+random.random()*dev2,
                              c3real[2]+random.random()*dev2]
                    c5 = c5real @ inv_latt_in
                    coords2rand[e2].append(c5)
                else:
                    coords2rand[e2].append(c3)
        coords2 = coords2rand

    with open(str(fnout_in), 'w') as f:
        f.write(f"{fnout_in}\n")
        f.write("1.0\n")
        for vec in latt_in:
            f.write("  ".join(f"{x:.16f}" for x in vec) + "\n")
        str1=" "
        for e1 in elems2:
            str1+=f"{e1} "
        f.write(str1+"\n")
        str1 = " "
        for n1 in natoms2:
            str1 += f"{n1} "
        f.write(str1+"\n")
        f.write("Direct\n")
        for e2 in elems2:
            coords3 = coords2[e2]
            for c3 in coords3:
                f.write(f"  {c3[0]}  {c3[1]}  {c3[2]}\n")
        for k1,c1 in coords_dict_in.items():
            if "dummy" in k1:
                k2 = k1[k1.find("-")+1:]
                for c2 in c1:
                    f.write(f"  {c2[0]}  {c2[1]}  {c2[2]} {k2}\n")
    print(f"    Written defect file: {fnout_in}")

def generate_defect_models():
    parser = argparse.ArgumentParser(
        prog='pydecs-prep-genDefModels',
        description='Generating point-detect models from grouped POSCAR'
    )
    parser.add_argument(
        'input_toml', 
        nargs="?",
        type=Path, 
        default="inpydecs_genDefs.toml",
        help='Path to input toml file')
    parser.add_argument(
        "-p", "--print_template",
        action="store_true",
        help='Printout template input file (inpydecs_genDefs.toml)')
    parser.add_argument(
        "-t", "--tolerance",
        type=float, 
        default=1e-4,
        help='Tolerance for local extrema detection')
    args = parser.parse_args()
    # fnin = Path("inpydecs_genDefs.toml")
    fnin = args.input_toml
    ################################################################
    if args.print_template:
        str_input_template = """
input_grouped_POSCAR = "../002_findInt/outInt_06_POSCAR_withAllInt_grouped.vasp"
# clean_before_run = true
# outID_start = 100

supercell_size = [2,2,2]
# allow_self_trapped_defect= true

##### Random deviation in angstrhom
# random_deviation_cutoff_distance  = 4.0
# random_deviation_around_defect.common  = 0.4
# random_deviation_around_defect.H = 0.1
#################################################
##### Foreign (not-intrinsic) elements (FE)
# foreign_elements = ["Sn","Al"]

##### Vacancies: "All", "None", list of element labels, or list of site labels
# vacancies = "All "
# vacancies = "None"
# vacancies = ["Ga","O[3]"]

##### Interstitials: "All", "None", list of defect types
# interstitials = "All"
# interstitials = ["Ga_*","FE_*"]

##### Substitutionals: "All", "None", list of defect types
# substitutionals = "All"
# substitutionals = ["Ga_*","*_Ga[1]","FE_Ga[2]"]

#################################################
##### Protons around anions
# protons.sites = ["O"]
# protons.sites = ["O[3]"]
# protons.distance_to_proton = 1.0

# protons.hyd_bond.enabled = true
# protons.hyd_bond.mindist_to_neighbors = 3.0
# protons.hyd_bond.neighboring_anions = ["O","N"]

# protons.on_sphere.enabled = true
# protons.on_sphere.mindist_to_neighbors = 1.2
# protons.on_sphere.mindist_between_protons = 0.4
#################################################
#################################################
### Defect complexes
# defect_complexes = ["Vac_O+Vac_Ga"]
# defect_complexes = ["3xVac_Ga"]
# cutoffR_complexes = 4.0
# cutoffR_complexes = [3.0, 3.0]
# unsort_complexes = true
        """
        if not fnin.is_file():
            fout1 = open("inpydecs_genDefs.toml","w")
            fout1.write(str_input_template)
        else:
            print(str_input_template)
            print("### Default input-file name is \"inpydecs_genDefs.toml\", wihch already exists in this folder.")
        sys.exit()
    ################################################################
    print(f"-"*60)
    print(f"  Starting pydecs-prep-genDefectModels")
    fnin = args.input_toml
    print(f"  Input toml file: {fnin}")
    if not fnin.is_file():
        print(f"  Error: input tomle file not found: {fnin}")
        print(f"    Template file is output by option \"-p\" ")
        print(f"-"*60)
        sys.exit()
    print("  "+f"-"*30)
    in_params = toml.load(fnin)
    print(f"  Input parameters:")
    fnin_POSCAR = Path(in_params["input_grouped_POSCAR"])
    print(f"    input_grouped_POSCAR = {fnin_POSCAR}")
    if not fnin_POSCAR.is_file():
        print(f"  Error: input_grouped_POSCAR not found: {fnin_POSCAR}")
        print(f"-"*60)
        sys.exit()
    id_def = 1
    if "outID_start" in in_params:
        id_def = in_params["outID_start"]
    if "clean_before_run" in in_params:
        bool_clean = in_params["clean_before_run"]
    else:
        bool_clean = False
    print(f"    clean_before_run = {bool_clean}")
    supercell_size = [1 , 1, 1]
    if "supercell_size" in in_params:
        supercell_size = in_params["supercell_size"]
    print(f"    supercell_size = {supercell_size}")
    allow_selfdefect = False
    if "allow_self_trapped_defect" in in_params:
        allow_selfdefect = in_params["allow_self_trapped_defect"]
    cutoff_deviation  = 0.0
    if "random_deviation_cutoff_distance" in in_params:
        cutoff_deviation = in_params["random_deviation_cutoff_distance"]
    print(f"    random_deviation_cutoff_distance = {cutoff_deviation}")
    dev_rand_dict = {"common":0.2}
    if "random_deviation_around_defect" in in_params:
        dev_rand_list = in_params["random_deviation_around_defect"]
        for k1,dev1 in dev_rand_list.items():
            dev_rand_dict[k1] = dev1
    print(f"    random_deviation_around_defect = {dev_rand_dict}")
    foreign_elements = []
    if "foreign_elements" in in_params:
        foreign_elements = in_params["foreign_elements"]
    print(f"    foreign_elements = {foreign_elements}")
    vacancies = "None"
    if "vacancies" in in_params:
        vacancies = in_params["vacancies"]
    print(f"    vacancies = {vacancies}")
    interstitials = "None"
    if "interstitials" in in_params:
        interstitials = in_params["interstitials"]
    print(f"    interstitials = {interstitials}")
    substitutionals = "None"
    if "substitutionals" in in_params:
        substitutionals = in_params["substitutionals"]
    print(f"    susbtitutionals = {substitutionals}")
    protons_enabled = False
    protons_lattSites = []
    protons_dist = 1.0
    protHB_enabled = False
    protHB_neighbors = []
    protHB_mindist_neighbors = 3.0
    protOnSp_enabled = False
    protOnSp_mindist_Atoms = 1.0
    protOnSp_mindist_HH = 0.3
    if "protons" in in_params:
        protons_enabled = True
        inProt = in_params["protons"]
        if "sites" in inProt:
            protons_lattSites = inProt["sites"]
        if len(protons_lattSites)==0:
            print(f"    Warning: protons.sites not found in the input toml file")
            print(f"           When protons-tool is used, the tag is mandatory.")
            protons_enabled = False
    if protons_enabled:
        if "distance_to_proton" in inProt:
            protons_dist = inProt["distance_to_proton"]
        print(f"    protons-tool enabled")
        print(f"      proton.sites = {protons_lattSites}")
        print(f"      proton.distance_to_proton = {protons_dist}")

        if "hyd_bond" in inProt:
            inProt2 = inProt["hyd_bond"]
            if "enabled" in inProt2:
                protHB_enabled = inProt2["enabled"]
            if "mindist_to_neighbors" in inProt2:
                protHB_mindist_neighbors = inProt2["mindist_to_neighbors"]
            if "neighboring_anions" in inProt2:
                protHB_neighbors = inProt2["neighboring_anions"]
            else:
                for ls1 in protons_lattSites:
                    if "[" in ls1:
                        ls2 = ls1[:ls1.find("[")]
                    else:
                        ls2 = ls1
                if ls2 not in protHB_neighbors:
                    protHB_neighbors.append(ls2)
            print(f"    protons.hyd_bond enabled")
            print(f"      proton.hyd_bond.neighboring_anions = {protHB_neighbors}")
            print(f"      proton.hyd_bond.mindist_to_neighbors = {protHB_mindist_neighbors}")
        if "on_sphere" in inProt:
            inProt2 = inProt["on_sphere"]
            if "enabled" in inProt2:
                protOnSp_enabled = inProt2["enabled"]
            if "mindist_to_neighbors" in inProt2:
                protOnSp_mindist_Atoms = inProt2["mindist_to_neighbors"]
            if "mindist_between_protons" in inProt2:
                protOnSp_mindist_HH = inProt2["mindist_between_protons"]
            print(f"    protons.on_spher enabled")
            print(f"      proton.on_sphere.mindist_to_neighbors = {protOnSp_mindist_Atoms}")
            print(f"      proton.on_sphere.mindist_between_protons = {protOnSp_mindist_HH}")
    complexes = []
    if "defect_complexes" in in_params:
        complexes = in_params["defect_complexes"]
    print(f"    defect_complexes = {complexes}")
    cutoffRcomp = np.ones(len(complexes))*4.0
    if "cutoffR_complexes" in in_params and len(complexes)>0:
        cut1 = in_params["cutoffR_complexes"]
        if isinstance(cut1,float):
            cutoffRcomp = np.ones(len(complexes))*cut1
        elif isinstance(cut1,list):
            if len(cutoffRcomp) == len(cut1):
                cutoffRcomp = np.array(cut1)
            else:
                print(f"    cutoffR_complexes = {cut1}")
                print(f"    Error: cutoffR_complexes: lengths is not same")
                sys.exit()
        else:
            print(f"    cutoffR_complexes = {cut1}")
            print(f"    Error: cutoffR_complexes allowed for float or list of float values")
            sys.exit()
    print(f"    cutoffR_complexes = {cutoffRcomp}")
    unsort_complexes = False
    if "unsort_complexes" in in_params:
        unsort_complexes = in_params["unsort_complexes"]
    print(f"    unsort_complexes = {unsort_complexes}")
    print("  "+f"-"*30)
    ################################################################
    print(f"  Cleaning def*")
    if bool_clean:
        for filepath in glob.glob("def*"):
            if filepath == fnin_POSCAR:
                continue
            try:
                if os.path.isfile(filepath):
                    os.remove(filepath)
                elif os.path.isdir(filepath):
                    shutil.rmtree(filepath)
            except OSError as e:
                print(f"Warning: creaning error")
    print("  "+f"-"*30)
    ################################################################
    max_eachLS = {}
    print(f"  Reading POSCAR")
    with open(fnin_POSCAR, 'r') as f1:
        l1 = f1.readline()
        l1 = f1.readline()
        scale0 = float(l1.strip())
        lattConst0 = []
        for i1 in range(3):
            l1 = f1.readline()
            l2 = [ float(t1)*scale0 for t1 in l1.split()[:3] ]
            lattConst0.append(l2)
        l1 = f1.readline()
        lattSites0 = []
        for e1 in l1.split():
            e2 = e1.replace("Rn","int")
            lattSites0.append(e2)
        l1 = f1.readline()
        natoms_list0 = [int(t1) for t1 in l1.split()]
        natoms_tot0 = sum(natoms_list0)
        l1 = f1.readline()
        coord_type0 = l1.split()[0]
        coords_dict0 = {}
        for ie1,e1 in enumerate(lattSites0):
            n1 = natoms_list0[ie1]
            coords_dict0[e1] = []
            for i2 in range(n1):
                l1 = f1.readline()
                l2 = [ float(t1) for t1 in l1.split()[:3] ]
                coords_dict0[e1].append(l2)
    elems0 = []
    for ie1,ls1 in enumerate(lattSites0):
        ls2 = ls1[:ls1.find("[")]
        if ls2 not in elems0:
            elems0.append(ls2)
        if ls2 not in max_eachLS:
            max_eachLS[ls2] = 1
        else:
            max_eachLS[ls2] += 1
    str1="    Elements: "
    for e1 in elems0:
        str1+=f"{e1} "
    print(str1)
    print("    "+f"_"*15)
    print(f"    LattSite | num")
    for ie1,e1 in enumerate(lattSites0):
        n1 = natoms_list0[ie1]
        print(f"    {e1:<8} | {n1:3d}")
    if coord_type0[0].lower()!="d":
        print(f"  Error: coordination type is not allowed for {coord_type0}")
        sys.exit()
    print("  "+f"-"*30)
    ################################################################
    print(f"  Preparing output")
    print(f"    Defect list output-file: def_list.csv")
    print(f"    Defect list for inpydecs_defects.csv: def_inpydecs_defects.csv")
    foutlist = open("def_list.csv","w")
    foutlist.write("id, file_name, def_type, multiplicity, coordinations\n")
    columns_inpydecs = [
        'commentout','memo','label','defect_type','charge','energy_defect',
        'energy_perfect','energy_correction','multiplicity','',  # 空ヘッダ
        'line_color','line_style','line_width'
        ]
    df_inpydecs = pd.DataFrame(columns=columns_inpydecs)
    def update_df_inpydecs(def_type_in,multiplicity_in):
        nonlocal df_inpydecs
        def_type1 = def_type_in.split("+")
        def_type2 = ""
        def_label2 = ""
        for d1 in def_type1:
            d2 = d1.split("_")
            e1 = d2[0]
            e2 = e1.replace("Vac", "V")
            ls1 = d2[1]
            ls2 = ls1[:ls1.find("[")]
            if max_eachLS[ls2]==1:
                def_type2 += f"{e1}_{ls2}+"
            else:
                def_type2 += d1+"+"
            def_label2 += f"{e2}_"+"{"+f"{ls2}"+"}^{}+"
        def_type2 = def_type2[:-1] 
        def_label2  = def_label2[:-1]
        newRaw1 = [{'label':def_label2,'defect_type':def_type2,'multiplicity':multiplicity_in}]
        newRaw1_df = pd.DataFrame(newRaw1, columns=columns_inpydecs)
        df_inpydecs = pd.concat([df_inpydecs, newRaw1_df], ignore_index=True)
    ################################################################
    print(f"  Making supercell")
    print(f"    The input cell is extended to {supercell_size[0]}x{supercell_size[1]}x{supercell_size[2]} supercell")
    lattConst1 = []
    for i1,lc1 in enumerate(lattConst0):
        lc2 = []
        for i2 in range(3):
            lc2.append(lc1[i2]*supercell_size[i1])
        lattConst1.append(lc2)
    lattConst1 = np.array(lattConst1)
    inv_lattConst1 = np.linalg.inv(lattConst1)
    coords_dict1 = {}
    natoms_list1 = []
    for ie1,e1 in enumerate(lattSites0):
        n1 = natoms_list0[ie1]
        coords0 = coords_dict0[e1]
        coords_dict1[e1] = []
        coords1 = []
        for ic2,c2 in enumerate(coords0):
            c3 = [-1e10,-1e10,-1e10]
            for ic1 in range(supercell_size[0]):
                c3[0] = (c2[0]+float(ic1))/supercell_size[0]
                for ic2 in range(supercell_size[1]):
                    c3[1] = (c2[1]+float(ic2))/float(supercell_size[1])
                    for ic3 in range(supercell_size[2]):
                        c3[2] = (c2[2]+float(ic3))/float(supercell_size[2])
                        coords1.append(copy.copy(c3))
        ref = [0.5,0.5,0.5]
        coords2 = sorted(coords1,key=lambda p: math.dist(p,ref))
        coords_dict1[e1] = coords2
        natoms_list1.append(len(coords_dict1[e1]))
    natoms_tot1 = sum(natoms_list1)
    print(f"    Lattice constants:")
    for i1 in range(3):
        print(f"    {lattConst1[i1][0]:12f},{lattConst1[i1][1]:12f},{lattConst1[i1][2]:12f}")
    print("    "+f"_"*15)
    print(f"    LattSite | num")
    for ie1,e1 in enumerate(lattSites0):
        n1 = natoms_list1[ie1]
        print(f"    {e1:<8} | {n1:3d}")
    output_defect_poscar("def_supercell.vasp",lattConst1,
                         lattSites0,coords_dict1)
    lattSites2 = []
    coords_dict2 = {}
    for j0,ls0 in enumerate(lattSites0):
        if "int" not in ls0:
            lattSites2.append(ls0)
            coords_dict2[ls0]=copy.deepcopy(coords_dict1[ls0])
    output_defect_poscar("defModel_0000_supercell.vasp",lattConst1,
                         lattSites2,coords_dict2)
    print("  "+f"-"*30)
    ################################################################
    print(f"  Generating vacancy models")
    vac_list = []
    if isinstance(vacancies,str):
        if vacancies.strip().lower()=="none":
            print(f"    No vacancies generated")
        elif vacancies.strip().lower()=="all":
            print(f"    All vacancies pattern generated")
            for ie1,ls1 in enumerate(lattSites0):
                if "int" not in ls1:
                    vac_list.append(ls1)
        else:
            print(f"  Error: string-vacancies should be one of None or All:{vacancies}")
            sys.exit()
    elif isinstance(vacancies,list):
        for v1 in vacancies:
            v2 = v1.strip()
            if "[" in v2:
                if v2 not in lattSites0:
                    print(f"  Error: vacancies-tag: {v1} not found")
                    sys.exit()
                if v2 not in vac_list:
                    vac_list.append(v2)
            else:
                bool_none = True
                for ie1,ls1 in enumerate(lattSites0):
                    if v2 in ls1:
                        if ls1 not in vac_list:
                            vac_list.append(ls1)
                        bool_none = False
                if bool_none:
                    print(f"  Error: vacancies-tag: {v2} not found")
                    sys.exit()
    else:
        print(f"  Error: vacancies-tag:{vacancies}")
        sys.exit()
    if len(vac_list)>0:
        str1 = "    Vacancy sites: "
        for v1 in vac_list:
            str1 += f"{v1}, "
        print(str1[:-2])
    for v1 in vac_list:
        lattSites2 = []
        coords_dict2 = {}
        for j0,ls0 in enumerate(lattSites0):
            if "int" not in ls0:
                lattSites2.append(ls0)
                coords_dict2[ls0]=copy.deepcopy(coords_dict1[ls0])
        label_def = f"Vac_{v1}"
        coord_def = coords_dict2[v1].pop(0)
        coords_dict2[f"dummy-{label_def}"]=[coord_def]
        fnout_def = f"defModel_{id_def:04d}_{label_def}.vasp"
        output_defect_poscar(fnout_def,lattConst1,
                             lattSites2,coords_dict2,
                             coord_def,cutoff_deviation,dev_rand_dict)
        foutlist.write(f"{id_def},{fnout_def}, {label_def}, 1,{coord_def}-{label_def}\n")
        update_df_inpydecs(label_def,1)
        id_def += 1 
    print("  "+f"-"*30)
    ################################################################
    print(f"  Generating interstitial defect models")
    int_list = []
    if isinstance(interstitials,str):
        if interstitials.strip().lower()=="none":
            print(f"    No interstitials generated")
        elif interstitials.strip().lower()=="all":
            print(f"    All interstitials pattern generated")
            for e1 in elems0+foreign_elements:
                if "int" in e1:
                    continue
                for ie1,ls1 in enumerate(lattSites0):
                    if "int" in ls1:
                        ls2 = f"{e1}_{ls1}"
                        int_list.append(ls2)
        else:
            print(f"  Error: string-interstitials should be one of None or All:{interstitials}")
            sys.exit()
    elif isinstance(interstitials,list):
        for int1 in interstitials:
            int2 = int1.split("_")
            int2elem = int2[0]
            int2site = int2[1]
            int3_elemlist = []
            int3_sitelist = []
            if int2elem=="*":
                for e1 in elems0+foreign_elements:
                    if "int" in e1:
                        continue
                    int3_elemlist.append(e1)
            elif int2elem=="FE":
                for e1 in foreign_elements:
                    int3_elemlist.append(e1)
            else:
                int3_elemlist.append(int2elem)
            if int2site=="*":
                for ie1,ls1 in enumerate(lattSites0):
                    if "int" in ls1:
                        int3_sitelist.append(ls1)
            else:
                if int2site not in lattSites0:
                    print(f"  Error: interstitials-tag: {int1} can not be defined")
                    sys.exit()
                int3_sitelist.append(int2site)
            for e1 in int3_elemlist:
                for s1 in int3_sitelist:
                    int5 = f"{e1}_{s1}"
                    if int5 not in int_list:
                        int_list.append(int5)
    else:
        print(f"  Error: interstitials-tag:{interstitials}")
        sys.exit()
    if len(int_list)>0:
        str1 = "    Interstitials sites: "
        for int1 in int_list:
            str1 += f"{int1}, "
        print(str1[:-2])
    for int1 in int_list:
        lattSites2 = []
        coords_dict2 = {}
        for j0,ls0 in enumerate(lattSites0):
            if "int" not in ls0:
                lattSites2.append(ls0)
                coords_dict2[ls0]=copy.deepcopy(coords_dict1[ls0])
        label_def = int1
        label_intelem = int1.split("_")[0]
        label_intsite = int1.split("_")[1]
        label_intsite2 = f"{label_intelem}[0]"
        coord_def = coords_dict1[label_intsite][0]
        coords_dict2[label_intsite2] = [coord_def]
        lattSites2.append(label_intsite2)
        fnout_def = f"defModel_{id_def:04d}_{label_def}.vasp"
        output_defect_poscar(fnout_def,lattConst1,
                             lattSites2,coords_dict2,
                             coord_def,cutoff_deviation,dev_rand_dict)
        foutlist.write(f"{id_def},{fnout_def}, {label_def}, 1,{coord_def}-{label_def}\n")
        update_df_inpydecs(label_def,1)
        id_def += 1 
    print("  "+f"-"*30)
    ################################################################
    print(f"  Generating substitutional defect models")
    subs_list = []
    if isinstance(substitutionals,str):
        if substitutionals.strip().lower()=="none":
            print(f"    No substitutionals generated")
        elif substitutionals.strip().lower()=="all":
            print(f"    All substitutionals pattern generated")
            for e1 in elems0+foreign_elements:
                if "int" in e1:
                    continue
                for ie1,ls1 in enumerate(lattSites0):
                    ls2 = ls1[:ls1.find("[")]
                    if "int" not in ls1 and ls2 != e1:
                        ls2 = f"{e1}_{ls1}"
                        subs_list.append(ls2)
        else:
            print(f"  Error: string-interstitials should be one of None or All:{substitutionals}")
            sys.exit()
    elif isinstance(substitutionals,list):
        for subs1 in substitutionals:
            subs2 = subs1.split("_")
            subs2elem = subs2[0]
            subs2site = subs2[1]
            subs3_elemlist = []
            subs3_sitelist = []
            if subs2elem=="*":
                for e1 in elems0+foreign_elements:
                    if "int" in e1:
                        continue
                    subs3_elemlist.append(e1)
            elif subs2elem=="FE":
                for e1 in foreign_elements:
                    subs3_elemlist.append(e1)
            else:
                subs3_elemlist.append(subs2elem)
            if subs2site=="*":
                for ie1,ls1 in enumerate(lattSites0):
                    if "int" not in ls1:
                        subs3_sitelist.append(ls1)
            elif "[" in subs2site:
                if subs2site not in lattSites0:
                    print(f"  Error: substitutionals-tag: {subs1} can not be defined")
                    sys.exit()
                subs3_sitelist.append(subs2site)
            else:
                bool_none = True
                for ie1,ls1 in enumerate(lattSites0):
                    ls2 = ls1[:ls1.find("[")]
                    if ls2==subs2site:
                        subs3_sitelist.append(ls1)
                        bool_none = False
                if bool_none:
                    print(f"  Error: substitutionals-tag: {subs1} can not be defined")
                    sys.exit()
            for e1 in subs3_elemlist:
                for ls1 in subs3_sitelist:
                    subs5 = f"{e1}_{ls1}"
                    ls2 = ls1[:ls1.find("[")]
                    if subs5 not in subs_list:
                        if ls2 != e1:
                            subs_list.append(subs5)
                        elif allow_selfdefect:
                            subs_list.append(subs5)
    else:
        print(f"  Error: substitutionals-tag:{substitutionals}")
        sys.exit()
    if len(subs_list)>0:
        str1 = "    Substitutionals sites: "
        for subs1 in subs_list:
            str1 += f"{subs1}, "
        print(str1[:-2])
    for subs1 in subs_list:
        lattSites2 = []
        coords_dict2 = {}
        for j0,ls0 in enumerate(lattSites0):
            if "int" not in ls0:
                lattSites2.append(ls0)
                coords_dict2[ls0]=copy.deepcopy(coords_dict1[ls0])
        label_def = subs1
        label_subselem = subs1.split("_")[0]
        label_subssite = subs1.split("_")[1]
        label_subssite2 = f"{label_subselem}[0]"
        coord_def = coords_dict2[label_subssite].pop(0)
        coords_dict2[label_subssite2] = [coord_def]
        lattSites2.append(label_subssite2)
        fnout_def = f"defModel_{id_def:04d}_{label_def}.vasp"
        output_defect_poscar(fnout_def,lattConst1,
                             lattSites2,coords_dict2,
                             coord_def,cutoff_deviation,dev_rand_dict)
        foutlist.write(f"{id_def},{fnout_def},{label_def},1,{coord_def}-{label_def}\n")
        update_df_inpydecs(label_def,1)
        id_def += 1 
    print("  "+f"-"*30)
    ################################################################
    ### Proton generation
    def generate_spherical_grid(dtheta_deg, dphi_deg):
        dtheta = np.deg2rad(dtheta_deg)
        dphi   = np.deg2rad(dphi_deg)
        thetas = np.arange(0, np.pi + 1e-8, dtheta)
        phis   = np.arange(0, 2*np.pi, dphi)
        pts = []
        r1 = protons_dist
        for th1 in thetas:
            sinth1 = np.sin(th1)
            costh1 = np.cos(th1)
            for phi1 in phis:
                pts.append([r1*sinth1*np.cos(phi1),r1*sinth1*np.sin(phi1),r1*costh1])
        np.random.shuffle(pts)
        accepted = []
        for p in pts:
            if not accepted:
                accepted.append(p)
                continue
            dists = np.linalg.norm(np.array(accepted)-p, axis=1)
            if np.all(dists >= protOnSp_mindist_HH):
                accepted.append(p)
        return np.array(accepted)
    print(f"  Generating proton-type defect models")
    protons_lattSites2 = []
    if protons_enabled:
        for ls1 in protons_lattSites:
            if "[" in ls1:
                if ls1 not in protons_lattSites2:
                    protons_lattSites2.append(ls1)
            else:
                for j0,ls0 in enumerate(lattSites0):
                    ls2 = ls0[:ls0.find("[")]
                    if ls1 == ls2:
                        if ls0 not in protons_lattSites2:
                            protons_lattSites2.append(ls0)
        str1 = "    Atom sites for hydrogen: "
        for ls2 in protons_lattSites2:
            str1 += f"{ls2}, "
        print(str1[:-2])

        if protHB_enabled:
            print(f"  Searching proton positions with hydrgen bonding to neighboring anions")
            id_HBsearch = 1
            for is1,ls1 in enumerate(protons_lattSites2):
                elem1 = ls1[:ls1.find("[")]
                folout1 = f"def_HSearch_hydBond_{id_HBsearch:04d}"
                id_HBsearch += 1
                folout1 = Path(folout1)
                folout1.mkdir(exist_ok=True)
                os.chdir(folout1)
                print(f"    Creating folder: {folout1}")
                print(f"      Change-dir to: {folout1}")
                lattSites2 = []
                coords_dict2 = {}
                for j0,ls0 in enumerate(lattSites0):
                    if "int" not in ls0:
                        lattSites2.append(ls0)
                        coords_dict2[ls0]=copy.deepcopy(coords_dict1[ls0])
                label_def = f"{elem1}H_{ls1}"
                label_H = f"H[0]"
                lattSites2.append(label_H)
                coord_defH = coords_dict2[ls1][0]
                coord_defHreal = coord_defH @ lattConst1
                id3 = 1
                for ls2 in lattSites2:
                    if label_H == ls2:
                        continue
                    elem2 = ls2[:ls2.find("[")]
                    if elem2 not in protHB_neighbors:
                        continue
                    coords2 = coords_dict2[ls2]
                    for c2 in coords2:
                        coords3 = [c2[0]-coord_defH[0],c2[1]-coord_defH[1],c2[2]-coord_defH[2]]
                        for i1 in range(3):
                            if coords3[i1]>1.0:
                                coords3[i1] -= 1.0
                            elif coords3[i1]<-1.0:
                                coords3[i1] += 1.0
                        coords3real = coords3 @ lattConst1
                        d3 = np.linalg.norm(coords3real)
                        if d3 < 0.001:
                            continue
                        if d3 < protHB_mindist_neighbors:
                            coords4real = [coord_defHreal[0]+coords3real[0]/d3*protons_dist,
                                           coord_defHreal[1]+coords3real[1]/d3*protons_dist,
                                           coord_defHreal[2]+coords3real[2]/d3*protons_dist]
                            coords4 = coords4real @ inv_lattConst1
                            coords_dict2[label_H] = [coords4]
                            fnout_def = f"POSCARwH_{id3:04d}.vasp"
                            id3 += 1
                            output_defect_poscar(fnout_def,lattConst1,
                                lattSites2,coords_dict2)
                if id3==1:
                    print(f"  Warning: No proton site detected in the hydrogen-bond scheme")
                    print(f"    Trye more larger value for protons.hyd_bond.mindist_to_neighbors than {protHB_mindist_neighbors}")
                else:
                    path3 = f"POSCARwH_*.vasp"
                    sys.argv = [
                        "pydecs-prep-chkDupl",
                        "-t",str(args.tolerance),
                        *glob.glob(path3),
                        ]
                    print(f"    Running duplication check")
                    check_duplication()
                    fout3 = open("out_log.txt","w")
                    with open("out_duplication.csv") as fin1:
                        fin2 = fin1.readlines()
                        fnlist2 = [ t1.strip() for t1 in fin2[1].split(",")]
                        multiplicity_H = np.zeros(len(fnlist2),dtype=int)
                        for l2 in fin2[1:]:
                            t2 = l2.split(",")
                            for i3,t3 in enumerate(t2):
                                t4 = t3.strip()
                                if "POSCAR" in t4:
                                    multiplicity_H[i3] += 1
                        for if2,fn2 in enumerate(fnlist2):
                            fnout_def3 = f"../defModel_{id_def:04d}_{label_def}.vasp"
                            with open(fn2) as fin3:
                                l3 = fin3.readlines()[-1]
                                coord_defH = [ float(t1) for t1 in l3.split()]
                            foutlist.write(f"{id_def},{fnout_def3},{label_def},{multiplicity_H[if2]},{coord_defH}-{label_def}\n")
                            update_df_inpydecs(label_def,multiplicity_H[if2])
                            coords_dict2[label_H] = [coord_defH]
                            print(f"    Regenerate {fnout_def3} from {fn2}.")
                            fout3.write(f"Regenerate {fnout_def3} from {fn2}.\n")
                            output_defect_poscar(fnout_def3,lattConst1,
                                            lattSites2,coords_dict2,
                                            coord_defH,cutoff_deviation,dev_rand_dict)
                            id_def += 1 
                    fout3.close()
                print(f"    Change dir to: ../")
                os.chdir("../")
        if protOnSp_enabled:
            print(f"  Searching proton positions on sphere")
            posiHonSph = generate_spherical_grid(2.0,2.0)
            id_Hsp = 1
            for is1,ls1 in enumerate(protons_lattSites2):
                elem1 = ls1[:ls1.find("[")]
                lattSites2 = []
                coords_dict2 = {}
                for j0,ls0 in enumerate(lattSites0):
                    if "int" not in ls0:
                        lattSites2.append(ls0)
                        coords_dict2[ls0]=copy.deepcopy(coords_dict1[ls0])
                label_def = f"{elem1}H_{ls1}"
                label_H = f"H[0]"
                lattSites2.append(label_H)
                coord_defH = coords_dict2[ls1][0]
                coord_defHreal = coord_defH @ lattConst1
                coord_H_list5 = []
                for p1real in posiHonSph:
                    coord_Hreal = [coord_defHreal[0]+p1real[0],
                                   coord_defHreal[1]+p1real[1],
                                   coord_defHreal[2]+p1real[2]]
                    p1 = p1real @ inv_lattConst1
                    coord_H = [coord_defH[0]+p1[0],
                               coord_defH[1]+p1[1],
                               coord_defH[2]+p1[2]]
                    coord_H = coord_Hreal @ inv_lattConst1
                    d3list = []
                    for ls2 in lattSites2:
                        if label_H == ls2:
                            continue
                        elem2 = ls2[:ls2.find("[")]
                        coords2 = coords_dict2[ls2]
                        for c2 in coords2:
                            coords3 = [c2[0]-coord_H[0],
                                       c2[1]-coord_H[1],
                                       c2[2]-coord_H[2]]
                            for i1 in range(3):
                                if coords3[i1]>1.0:
                                    coords3[i1] -= 1.0
                                elif coords3[i1]<-1.0:
                                    coords3[i1] += 1.0
                            coords3real = coords3 @ lattConst1
                            d3 = np.linalg.norm(coords3real)
                            if d3 < 0.01:
                                continue
                            d3list.append(d3)
                    d3list.sort()
                    if d3list[1] > protOnSp_mindist_Atoms:
                        coords_dict2[label_H] = [coord_H]
                        coord_H_list5.append(copy.copy(coord_H))
                        fnout_def = f"defModel_{id_def:04d}_{label_def}.vasp"
                        output_defect_poscar(fnout_def,lattConst1,
                                        lattSites2,coords_dict2,
                                        coord_H,cutoff_deviation,dev_rand_dict)
                        foutlist.write(f"{id_def},{fnout_def},{label_def},1,{coord_H}-{label_def}\n")
                        update_df_inpydecs(label_def,1)
                        id_def += 1 
                fnout_def = f"def_HonSph_{id_Hsp:04d}_{label_def}.vasp"
                coords_dict2[label_H] = coord_H_list5
                output_defect_poscar(fnout_def,lattConst1,
                                    lattSites2,coords_dict2)
                id_Hsp += 1
    else:
        print("    No proton-defects generated")
    print("  "+f"-"*30)
    ################################################################
    ### Defect complexes
    dummy_atomlabels = ["Am","Bh","Cm","Ds","Es","Fm","Hs","Og","Lr","No","Md"]
    def expand_single_def(strdef_in):
        outdef_list = []
        str2 = strdef_in.split("_")
        str2elem = str2[0]
        str2site = str2[1]
        str3_elemlist = []
        str3_sitelist = []
        if str2elem=="*":
            for e1 in elems0+foreign_elements+["Vac"]:
                if "int" in e1:
                    continue
                str3_elemlist.append(e1)
        elif str2elem=="FE":
            for e1 in foreign_elements:
                str3_elemlist.append(e1)
        else:
            str3_elemlist.append(str2elem)
        if str2site=="*":
            for ie1,ls1 in enumerate(lattSites0):
                str3_sitelist.append(ls1)
        elif "[" in str2site:
            if str2site not in lattSites0:
                print(f"  Error: complexes-tag: {sstr2elem} can not be defined")
                sys.exit()
            str3_sitelist.append(str2site)
        else:
            bool_none = True
            for ie1,ls1 in enumerate(lattSites0):
                ls2 = ls1[:ls1.find("[")]
                if ls2==str2site:
                    str3_sitelist.append(ls1)
                    bool_none = False
            if bool_none:
                print(f"  Error: complexes-tag: {str2site} can not be defined")
                sys.exit()
        for e1 in str3_elemlist:
            for ls1 in str3_sitelist:
                ls2 = ls1[:ls1.find("[")]
                if e1=="Vac" and ls2=="int":
                    continue
                str5 = f"{e1}_{ls1}"
                ls2 = ls1[:ls1.find("[")]
                if str5 not in subs_list:
                    if ls2 != e1:
                        outdef_list.append(str5)
                    elif allow_selfdefect:
                        outdef_list.append(str5)
        return outdef_list
    def connect_complexlabel(c_in):
        c1str=""
        for c1tmp in c_in:
            c1str+=c1tmp+"+"
        c1str=c1str[:-1]
        return c1str
    print(f"  Generating defect-complex models")
    if len(complexes)>0:
        id_comp = 1
        complist1 = []
        complist1dummy = []
        complist2sorted = []
        complist3dummy = []
        cutoffRlist = []
        for comp1,rcut1 in zip(complexes,cutoffRcomp):
            comp2 = [ t1.strip() for t1 in comp1.split("+")]
            comp3 = []
            for c2 in comp2:
                if "x" in c2:
                    t2 = [ t1.strip() for t1 in c2.split("x")]
                    try: 
                        mult2 = int(t2[0])
                    except ValueError:
                        print(f"    Error: invalid defect complexes input: {comp1}")
                        print(f"           ex.) 2xV_Al+V_O ")
                        sys.exit()
                    for i2 in range(mult2):
                        comp3.append(t2[1])
                else:
                    comp3.append(c2)
            comp2 = comp3
            if len(comp2)<=1:
                print(f"    Error: invalid defect complexes input: {comp1}")
                print(f"           ex.) V_Al+V_O or Al_*+*_O[1]")
                sys.exit()
            comp3 = []
            for c2 in comp2:
                c3 = expand_single_def(c2)
                comp3.append(c3)
            comp4 = [list(c3) for c3 in product(*comp3)]
            elist4 = elems0+["Vac"]+foreign_elements
            for c4 in comp4:
                for t4 in c4:
                    e1 = t4.split("_")[0]
                    s1 = t4.split("_")[1]
                    if e1 not in elist4:
                        elist4.append(e1)
            comp5sorted = []
            for c4 in comp4:
                clist5 = []
                for ie1,ls1 in enumerate(lattSites0):
                    for e1 in elist4:
                        t1 = f"{e1}_{ls1}"
                        for c5 in c4:
                            if t1==c5:
                                clist5.append(t1)
                comp5sorted.append(clist5)
            comp6dummy  = []
            for c5 in comp5sorted:
                counter5 = Counter(c5)
                icnt6 = 0
                clist6 = []
                for ic6,c6 in enumerate(c5):
                    ls6 = c6.split("_")[1]
                    if ic6!=0 and counter5[c6]==1:
                        icnt6 += 1
                    e6 = dummy_atomlabels[icnt6]
                    t2 = f"{e6}_{ls6}"
                    clist6.append(t2)
                comp6dummy.append(clist6)
            comp7dummy_origSeq  = []
            for c4,c5,c6 in zip(comp4,comp5sorted,comp6dummy):
                mapping5to6 = {}
                for c5t,c6t in zip(c5,c6):
                    if c5t not in mapping5to6:
                        mapping5to6[c5t] = c6t
                    else:
                        if mapping5to6[c5t] != c6t:
                            print("ERROR!!!!!!!!!!!!")
                            print(mapping5to6)
                            sys.exit()
                clist7 = []
                for c4t in c4:
                    clist7.append(mapping5to6[c4t])
                comp7dummy_origSeq.append(clist7)
            #print(comp4)
            #print(comp5sorted)
            #print(comp6dummy)
            # print(comp7dummy_origSeq)
            for c4,c7,c5,c6 in zip(comp4,comp7dummy_origSeq,comp5sorted,comp6dummy):
                if c5 not in complist2sorted:
                    complist1.append(c4)
                    complist1dummy.append(c7)
                    complist2sorted.append(c5)
                    complist3dummy.append(c6)
                    cutoffRlist.append(rcut1)
        #print(complist1)
        #print(complist1dummy)
        #print(complist2sorted)
        #print(complist3dummy)
        unique_groups = []
        group_idlist = []
        for c1d,c3 in zip(complist1dummy,complist3dummy):
            if unsort_complexes:
                if c1d not in unique_groups:
                    unique_groups.append(c1d)
                group_idlist.append(unique_groups.index(c1d)+1)
            else:
                if c3 not in unique_groups:
                    unique_groups.append(c3)
                group_idlist.append(unique_groups.index(c3)+1)
        print("    Defect complex pattens: ")
        with open("defComp_defectLabels.csv","w") as foutC1:
            foutC1.write("def_label_raw,def_label_raw_encoded,def_label_sorted,def_label_encoded,Rcut,id_group\n")
            print("    defLabel | defLabel_encoded | defLabel_sorted | defLabel_sorted_encoded | Rcut | id_group")
            for c1,c1d,c2,c3,r1,ic3 in zip(complist1,complist1dummy,complist2sorted,complist3dummy,cutoffRlist,group_idlist):
                c1str=connect_complexlabel(c1)
                c1dstr=connect_complexlabel(c1d)
                c2str=connect_complexlabel(c2)
                c3str=connect_complexlabel(c3)
                foutC1.write(f"{c1str},{c1dstr},{c2str},{c3str},{r1},{ic3}\n")
                print(f"      {c1str} | {c1dstr} | {c2str} | {c3str} | {r1} | {ic3}")
        with open("defComp_defectGroups.csv","w") as foutC1:
            foutC1.write("id_group,def_label_encoded\n")
            for i1,g1 in enumerate(unique_groups):
                g1str=connect_complexlabel(g1)
                foutC1.write(f"{i1+1},{g1str}\n")
        print("    "+"-"*30)
        for i1,g1 in enumerate(unique_groups):
            idg1 = i1+1
            g1str=connect_complexlabel(g1)
            print(f"  Searching defect complexes for {g1str} ({idg1}/{len(unique_groups)})")
            members1 = []
            rcut1 = 0.0
            for c1,c1d,c2,c3,r1,ic3 in zip(complist1,complist1dummy,complist2sorted,complist3dummy,cutoffRlist,group_idlist):
                if ic3==idg1:
                    members1.append([c1,c1d,c2,c3,r1,ic3])
                    rcut1 = r1
            #print(members1)
            #print(rcut1)

            folout1 = f"defComp_configSearch_{idg1:04d}"
            folout1 = Path(folout1)
            folout1.mkdir(exist_ok=True)
            os.chdir(folout1)
            print(f"    Creating folder: {folout1}")
            print(f"      Change-dir to: {folout1}")

            lattSites2 = []
            coords_dict2 = {}
            for j0,ls0 in enumerate(lattSites0):
                # if "int" not in ls0:
                lattSites2.append(ls0)
                coords_dict2[ls0]=copy.deepcopy(coords_dict1[ls0])
            elem1 = g1[0].split("_")[0]
            ls1 = g1[0].split("_")[1]
            coord_def1 = coords_dict2[ls1].pop(0)
            atlabel_def1 = f"{elem1}[0]"
            lattSites2.append(atlabel_def1)
            coords_dict2[atlabel_def1]=[coord_def1]
            label_defcoord1 = f"{coord_def1}-{g1[0]}"

            near_coordsID_list = {}
            near_coords_list = {}
            g1set = set(g1[1:])
            for g2 in g1set:
                elem2 = g2.split("_")[0]
                ls2 = g2.split("_")[1]
                coords2 = coords_dict2[ls2]
                for ic2,c2 in enumerate(coords2):
                    coords3 = [c2[0]-coord_def1[0],c2[1]-coord_def1[1],c2[2]-coord_def1[2]]
                    for i1 in range(3):
                        if coords3[i1]>1.0:
                            coords3[i1] -= 1.0
                        elif coords3[i1]<-1.0:
                            coords3[i1] += 1.0
                    coords3real = coords3 @ lattConst1
                    d3 = np.linalg.norm(coords3real)
                    bool_check=False
                    if d3 < rcut1:
                        if g2 not in near_coordsID_list:
                            near_coordsID_list[g2] = [(g2,ic2)]
                            near_coords_list[g2] = [[g2,ic2,c2]]
                        else:
                            near_coordsID_list[g2].append((g2,ic2))
                            near_coords_list[g2].append([g2,ic2,c2])
            # print(near_coords_list)
            coords_defs_allcomb3 = []
            coords_defs_allcomb3_set = []
            for g2 in g1[1:]:
                elem2 = g2.split("_")[0]
                ls2 = g2.split("_")[1]
                coords2 = near_coords_list[g2]
                if len(coords_defs_allcomb3)==0:
                    for t2 in coords2:
                        coords_defs_allcomb3.append([t2])
                        set2 = f"{t2[0]}-{t2[1]}"
                        coords_defs_allcomb3_set.append([set2])
                else:
                    coords_defs_allcomb4 = []
                    coords_defs_allcomb4_set = []
                    for t2 in coords2:
                        set2 = f"{t2[0]}-{t2[1]}"
                        # set2 = set([t2[0],t2[1]])
                        for t3,set3 in zip(coords_defs_allcomb3,coords_defs_allcomb3_set):
                            t4 = t3 +[t2]
                            set4 = sorted(set3+[set2])
                            if set2 not in set3:
                                if set4 not in coords_defs_allcomb4_set:
                                    coords_defs_allcomb4.append(t4)
                                    coords_defs_allcomb4_set.append(set4)
                    coords_defs_allcomb3 = coords_defs_allcomb4
                    coords_defs_allcomb3_set = coords_defs_allcomb4_set
            # print(coords_defs_allcomb3)
            coords_defs_allcomb4 = []
            label_defcoord_list4 = []
            id3 = 1
            lattSites4_list = []
            coords_dict4_list = []
            for comb3,set3 in zip(coords_defs_allcomb3,coords_defs_allcomb3_set):
                lattSites4 = []
                coords_dict4 = {}
                for j2,ls2 in enumerate(lattSites2):
                    lattSites4.append(ls2)
                    coords_dict4[ls2]=copy.deepcopy(coords_dict2[ls2])
                # print(comb3)
                remove_list = {}
                label_defcoord_list = [label_defcoord1]
                for c3 in comb3:
                    g3 = c3[0]
                    elem3 = g3.split("_")[0]
                    ls3 = g3.split("_")[1]
                    is3 = c3[1]
                    coords3 = c3[2]
                    # print(coords3)
                    atlabel_def3 =  f"{elem3}[0]"
                    if atlabel_def3 not in coords_dict4:
                        coords_dict4[atlabel_def3]=[coords3]
                        lattSites4.append(atlabel_def3)
                    else:
                        coords_dict4[atlabel_def3].append(coords3)
                    if ls3 not in remove_list:
                        remove_list[ls3] = [is3]
                    else:
                        remove_list[ls3].append(is3)
                    label_defcoord3 = f"{coords3}-{g3}"
                    label_defcoord_list.append(label_defcoord1)
                label_defcoord_list4.append(label_defcoord_list)
                for k1,v1 in remove_list.items():
                    coords5 = [x for j, x in enumerate(coords_dict4[k1]) if j not in v1]
                    coords_dict4[k1] = coords5
                fnout_def = f"POSCARcomplex_{id3:04d}.vasp"
                id3 += 1
                lattSites4 = [t1 for t1 in lattSites4 if "int" not in t1]
                output_defect_poscar(fnout_def,lattConst1,
                                    lattSites4,coords_dict4)
                lattSites4_list.append(lattSites4)
                coords_dict4_list.append(coords_dict4)
            #####== Duplication check
            path3 = f"POSCARcomplex_*.vasp"
            sys.argv = [
                    "pydecs-prep-chkDupl",
                    "-t",str(args.tolerance),
                    *glob.glob(path3),
                    ]
            print(f"    Running duplication check")
            check_duplication()
            fout3 = open("out_log.txt","w")
            #####== Copy to above with multiplicity information
            with open("out_duplication.csv") as fin1:
                fin2 = fin1.readlines()
                fnlist2 = [ t1.strip() for t1 in fin2[1].split(",")]
                multiplicity2 = np.zeros(len(fnlist2),dtype=int)
                for l2 in fin2[1:]:
                    t2 = l2.split(",")
                    for i3,t3 in enumerate(t2):
                        t4 = t3.strip()
                        if "POSCAR" in t4:
                            multiplicity2[i3] += 1
                for if2,fn2 in enumerate(fnlist2):
                    i4 = int(fn2[fn2.find("_")+1:fn2.find(".")])
                    for mem1 in members1:
                        if unsort_complexes:
                            c5dec = mem1[0]
                            c5 = mem1[1]
                        else:
                            c5dec = mem1[2]
                            c5 = mem1[3]
                        label_def5=connect_complexlabel(c5dec)
                        lattSites5 = copy.deepcopy(lattSites4_list[i4-1])
                        coords_dict5 = copy.deepcopy(coords_dict4_list[i4-1])
                        lattSites6 = [t1 for t1 in lattSites0 if "int" not in t1]
                        coord_def5list = []
                        for c6,c6dec in zip(c5,c5dec):
                            elem6 = c6.split("_")[0]
                            ls6 = c6.split("_")[1]
                            elem6dec = c6dec.split("_")[0]
                            ls6dec = c6dec.split("_")[1]
                            atlabel6 = f"{elem6}[0]"
                            atlabel6dec = f"{elem6dec}[0]"
                            coord6 = coords_dict5[atlabel6].pop(0)
                            if atlabel6dec not in coords_dict5:
                                lattSites6.append(atlabel6dec)
                                coords_dict5[atlabel6dec] = [coord6]
                                coord_def5list.append(coord6)
                            else:
                                coords_dict5[atlabel6dec].append(coord6)
                                coord_def5list.append(coord6)
                        lattSites6 = [t1 for t1 in lattSites6 if "Vac" not in t1]
                        fnout_def3 = f"../defModel_{id_def:04d}_{label_def5}.vasp"
                        str1=f"{id_def},{fnout_def3},{label_def5},{multiplicity2[if2]},"
                        for coord6,c6 in zip(coord_def5list,c5dec):
                            str1 += f"{coord6}-{c6},"
                        foutlist.write(str1[:-1]+"\n")
                        update_df_inpydecs(label_def5,multiplicity2[if2])
                        print(f"    Regenerate {fnout_def3} from {fn2}.")
                        fout3.write(f"Regenerate {fnout_def3} from {fn2}.\n")
                        output_defect_poscar(fnout_def3,lattConst1,
                                    lattSites6,coords_dict5,
                                    coord_def1,cutoff_deviation,dev_rand_dict)
                        id_def += 1 
            fout3.close()
            print(f"    Change dir to: ../")
            os.chdir("../")
    else:
        print("    No defect-complexes generated")
    df_inpydecs.to_csv("def_inpydecs_defects.csv",index=False)
    print("  "+f"-"*60)

if __name__ == '__main__':
#    poscar_to_cif()
#    group_by_symmetry()
#    check_duplication()
    findIntCHGCAR()
