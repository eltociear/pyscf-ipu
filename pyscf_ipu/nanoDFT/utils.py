# Copyright (c) 2023 Graphcore Ltd. All rights reserved.

import sys
import h5py
import pubchempy
import numpy as np
from itertools import combinations
from operator import itemgetter


spice_amino_acids = [
    "TRP", "LYN", "TYR", "PHE", "LEU", 
    "ILE", "HIE", "MET", "GLN", "HID", 
    "GLH", "VAL", "GLU", "THR", "PRO", 
    "ASN", "ASH", "ASP", "SER", "CYS", 
    "CYX", "ALA", "GLY"
]

def open_spice_amino_acids_hdf5():
    """Returns a h5py File object for the solvated amino acids data set in SPICE.
    Downloads the data set from github (1.4MB) if the file does not exist in the current directory."""
    import os.path

    spice_aa_fn = "solvated-amino-acids.hdf5"
    spice_aa_permalink = "https://github.com/openmm/spice-dataset/raw/e4e4ca731a8094b9a448d9831dd05de29124bfd9/solvated-amino-acids/solvated-amino-acids.hdf5"

    if not os.path.exists(spice_aa_fn):
        from urllib import request

        request.urlretrieve(spice_aa_permalink, spice_aa_fn)
    
    f_aa = h5py.File(spice_aa_fn)

    return f_aa
        

def get_mol_str_spice_aa(entry: str = "TRP", conformation: int = 0):
    """Returns the geometry for the amino acid in the 'entry' parameter.
    The data is extracted from the solvated amino acid data set in SPICE
    If the data set is not already available in the current dir, it is downloaded"""

    print(f"Getting geometry from the SPICE 'Solvated Amino Acids Dataset v1.1' for '{entry}'")
    f_aa = open_spice_amino_acids_hdf5()

    mol = f_aa[entry]
    nm_to_angstrom = 10.0
    return list(
        zip(
                [n for n in filter(str.isalpha, mol['smiles'][0].decode().upper())],
                mol['conformations'][conformation]*nm_to_angstrom
        )
    )

def get_mol_str_pubchem(entry: str):
    """Returns the geometry for the compound specified as 'entry' from the
    PubChem database.
    'entry' is interpreted as Compound ID if it is a string of digits or as
    name of a compound otherwise"""

    if entry.isdigit():                    # If all digits, we assume it is a CID
        print(f"Searching in PubChem for CID '{entry}'")
        compound = pubchempy.get_compounds(entry, "cid", record_type='3d')
    else:  
        print(f"Searching in PubChem for compound with name '{entry}'")                              # if not, we assume it is a name
        compound = pubchempy.get_compounds(entry, 'name', record_type='3d')
    mol_str = []
    if len(compound) > 1:
        print("INFO: PubChem returned more than one compound; using the first...", file=sys.stderr)
    elif len(compound) == 0:
        print(f"No compound found with the name '{entry}' in PubChem")
        return None
    print(f"Found compound: {compound[0].synonyms[0]}") 
    for a in compound[0].atoms:
        mol_str.append((a.element,np.array([a.x, a.y, a.z])))   
    return mol_str


def process_mol_str(mol_str: str):
    if mol_str == "benzene":
        mol_str = [
            ["C", ( 0.0000,  0.0000, 0.0000)],
            ["C", ( 1.4000,  0.0000, 0.0000)],
            ["C", ( 2.1000,  1.2124, 0.0000)],
            ["C", ( 1.4000,  2.4249, 0.0000)],
            ["C", ( 0.0000,  2.4249, 0.0000)],
            ["C", (-0.7000,  1.2124, 0.0000)],
            ["H", (-0.5500, -0.9526, 0.0000)],
            ["H", (-0.5500,  3.3775, 0.0000)],
            ["H", ( 1.9500, -0.9526, 0.0000)], 
            ["H", (-1.8000,  1.2124, 0.0000)],
            ["H", ( 3.2000,  1.2124, 0.0000)],
            ["H", ( 1.9500,  3.3775, 0.0000)]
        ]

    elif mol_str == "c20":
        mol_str = [["C", ( 1.56910, -0.65660, -0.93640)],
                   ["C", ( 1.76690,  0.64310, -0.47200)],
                   ["C", ( 0.47050, -0.66520, -1.79270)],
                   ["C", ( 0.01160,  0.64780, -1.82550)],
                   ["C", ( 0.79300,  1.46730, -1.02840)],
                   ["C", (-0.48740, -1.48180, -1.21570)],
                   ["C", (-1.56350, -0.65720, -0.89520)],
                   ["C", (-1.26940,  0.64900, -1.27670)],
                   ["C", (-0.00230, -1.96180, -0.00720)],
                   ["C", (-0.76980, -1.45320,  1.03590)],
                   ["C", (-1.75760, -0.63800,  0.47420)],
                   ["C", ( 1.28780, -1.45030,  0.16290)],
                   ["C", ( 1.28960, -0.65950,  1.30470)],
                   ["C", ( 0.01150, -0.64600,  1.85330)],
                   ["C", ( 1.58300,  0.64540,  0.89840)],
                   ["C", ( 0.48480,  1.43830,  1.19370)],
                   ["C", (-0.50320,  0.64690,  1.77530)],
                   ["C", (-1.60620,  0.67150,  0.92310)],
                   ["C", (-1.29590,  1.48910, -0.16550)],
                   ["C", (-0.01020,  1.97270, -0.00630)]]

    elif mol_str == "c100":
        mol_str = [["C", (-1.59600, 4.04060, 1.32260)],["C", (-2.78560, 3.62030, 0.86750)],["C", (1.12220, 4.19180, 1.58100)],["C", (0.55610, 4.64280, 0.46450)],["C", (-0.77450, 4.57120, 0.33060)],["C", (2.38160, 3.69870, 1.54910)],["C", (-1.02360, 4.37320, -1.01930)],["C", (-2.15360, 3.78860, -1.47040)],["C", (-3.11650, 3.57250, -0.49370)],["C", (-4.07380, 2.65850, -0.62040)],["C", (-4.08550, 1.85070, -1.70820)],["C", (0.17640, 4.21330, -1.63780)],["C", (1.57810, 2.79300, -2.77190)],["C", (0.31370, 3.29660, -2.67280)],["C", (-0.78760, 2.51750, -3.11720)],["C", (-2.05650, 2.85680, -2.55400)],["C", (-3.04480, 1.90090, -2.60350)],["C", (2.45400, 3.92590, -0.79790)],["C", (1.19210, 4.46580, -0.72750)],["C", (4.72530, 0.48500, -0.82090)],["C", (4.33740, 1.81210, -0.85310)],["C", (3.52930, 2.11560, -1.94060)],["C", (2.62760, 3.12360, -1.90640)],["C", (3.15780, 3.56490, 0.37740)],["C", (4.17050, 1.69290, 1.50600)],["C", (4.09670, 2.50770, 0.35700)],["C", (-4.78460, 0.88520, 0.69790)],["C", (-4.94170, 0.10250, -0.42550)],["C", (-4.35220, 2.13210, 0.60270)],["C", (-4.50980, 0.58230, -1.61180)],["C", (-3.75240, -0.20620, -2.43260)],["C", (-4.72170, -1.17630, -0.10650)],["C", (-4.10050, -2.08990, -0.97260)],["C", (-3.52710, -1.54660, -2.19040)],["C", (1.81720, 1.54840, -3.29360)],["C", (0.80120, 0.66170, -3.69130)],["C", (-0.54510, 1.15100, -3.61770)],["C", (-1.59230, 0.16810, -3.53580)],["C", (-2.82410, 0.61220, -3.06230)],["C", (0.04120, -1.69860, -3.50530)],["C", (-1.33460, -1.24450, -3.43350)],["C", (-2.33640, -2.08070, -2.75570)],["C", (-1.90190, -3.26080, -2.17080)],["C", (-3.72600, -2.10920, 1.77120)],["C", (-4.36030, 0.10230, 1.72000)],["C", (-4.45960, -1.16570, 1.25030)],["C", (-3.32190, -3.16890, 1.04190)],["C", (-2.44730, -3.79040, -1.00750)],["C", (-3.47160, -3.17320, -0.35860)],["C", (-2.79440, -1.80090, 2.74020)],["C", (-2.51340, -0.49730, 3.17740)],["C", (-3.37210, 0.51980, 2.66280)],["C", (-2.90680, 1.85220, 2.56000)],["C", (-3.47480, 2.63330, 1.52020)],["C", (-0.71820, 1.14100, 3.56130)],["C", (-1.59830, 2.19250, 3.01350)],["C", (-1.00360, 3.37840, 2.43610)],["C", (0.35590, 3.52050, 2.51960)],["C", (-1.88220, -2.80190, 2.68870)],["C", (0.30780, -3.48370, 2.52260)],["C", (-0.59030, -2.60600, 3.11250)],["C", (-0.16700, -1.32420, 3.58230)],["C", (-1.16010, -0.23250, 3.60700)],["C", (1.25530, -1.05910, 3.50810)],["C", (0.69910, 1.36660, 3.58220)],["C", (1.16600, 2.59400, 3.09010)],["C", (-1.43880, -4.46790, -0.35830)],["C", (-1.30850, -4.41700, 1.02040)],["C", (-2.23670, -3.69220, 1.66990)],["C", (-0.03590, -4.36530, 1.50140)],["C", (1.63220, -3.19410, 2.40140)],["C", (2.17870, -2.02470, 2.89450)],["C", (1.65930, 0.29600, 3.55460)],["C", (2.94030, 0.58290, 3.03560)],["C", (3.28150, 1.81110, 2.53170)],["C", (2.41570, 2.78520, 2.55760)],["C", (2.12750, -3.88250, 1.29960)],["C", (3.05340, -3.54940, -0.79220)],["C", (3.20520, -3.42060, 0.60000)],["C", (3.91450, -2.33270, 1.11310)],["C", (3.41180, -1.64450, 2.27850)],["C", (3.75800, -0.31930, 2.40740)],["C", (-0.33620, -4.48080, -1.16030)],["C", (1.91230, -4.03080, -1.37980)],["C", (0.92590, -4.60230, -0.65250)],["C", (1.06310, -4.53250, 0.71870)],["C", (2.46220, -1.11070, -3.21010)],["C", (1.12460, -0.73920, -3.64590)],["C", (2.64170, -2.36200, -2.63770)],["C", (1.63300, -3.24840, -2.50300)],["C", (0.35250, -2.97660, -2.93690)],["C", (-0.61630, -3.69160, -2.27130)],["C", (4.33780, -1.65960, -1.16960)],["C", (4.32530, -0.43960, -1.77130)],["C", (3.40550, -0.14210, -2.78300)],["C", (3.05390, 1.16070, -2.83410)],["C", (3.55050, -2.61110, -1.63070)],["C", (4.51580, 0.38190, 1.48320)],["C", (4.58670, -1.52770, 0.17300)],["C", (4.86400, -0.22290, 0.35100)],]
    elif mol_str == "c180":
        mol_str = [["C", (5.94060, 0.59650, -0.41930)],["C", (5.93570, -0.73530, -0.16200)],["C", (5.66630, -1.38200, -1.32280)],["C", (5.50750, -0.45190, -2.29460)],["C", (5.67810, 0.77110, -1.73860)],["C", (2.83010, 5.12760, 1.23450)],["C", (3.83470, 4.56120, 0.52130)],["C", (3.57290, 4.73550, -0.79620)],["C", (2.39920, 5.40580, -0.89720)],["C", (1.94210, 5.65200, 0.35430)],["C", (3.37000, -0.17130, 4.94290)],["C", (4.38070, 0.08380, 4.07510)],["C", (4.38280, 1.41520, 3.81810)],["C", (3.37330, 1.97720, 4.52830)],["C", (2.75020, 0.99860, 5.22730)],["C", (2.37120, -5.36250, 1.18010)],["C", (3.54640, -4.70310, 1.03000)],["C", (3.81640, -4.05840, 2.19080)],["C", (2.80660, -4.31830, 3.05820)],["C", (1.91470, -5.12670, 2.43360)],["C", (1.21740, -3.27530, -4.86340)],["C", (2.49140, -3.19300, -4.40510)],["C", (2.65450, -4.12300, -3.43440)],["C", (1.47620, -4.77650, -3.28620)],["C", (0.59020, -4.25790, -4.16960)],["C", (1.49520, 3.20730, -4.82930)],["C", (2.66790, 2.53390, -4.72220)],["C", (2.50350, 1.31170, -5.28280)],["C", (1.22700, 1.23160, -5.73180)],["C", (0.60550, 2.40280, -5.45710)],["C", (-5.93570, -0.59440, 0.42270)],["C", (-5.67490, -0.76940, 1.74010)],["C", (-5.50630, 0.45710, 2.29310)],["C", (-5.66940, 1.38700, 1.32150)],["C", (-5.93590, 0.73720, 0.16170)],["C", (-1.94110, -5.64480, -0.34860)],["C", (-2.40080, -5.40690, 0.90320)],["C", (-3.57220, -4.73310, 0.79580)],["C", (-3.83120, -4.55720, -0.52420)],["C", (-2.82610, -5.12390, -1.23370)],["C", (-0.60830, -2.40370, 5.45100)],["C", (-1.22900, -1.22950, 5.72670)],["C", (-2.50360, -1.31650, 5.27460)],["C", (-2.66790, -2.54160, 4.72150)],["C", (-1.49840, -3.21580, 4.83180)],["C", (-0.59120, 4.25700, 4.16640)],["C", (-1.47730, 4.78080, 3.28550)],["C", (-2.65030, 4.11680, 3.43640)],["C", (-2.48640, 3.19020, 4.41060)],["C", (-1.21440, 3.27630, 4.86590)],["C", (-1.91330, 5.12020, -2.42570)],["C", (-2.80240, 4.31240, -3.05500)],["C", (-3.81120, 4.05680, -2.18500)],["C", (-3.54830, 4.70870, -1.02640)],["C", (-2.37370, 5.36730, -1.17590)],["C", (-2.75150, -1.00080, -5.22350)],["C", (-3.37950, -1.97970, -4.52910)],["C", (-4.38810, -1.41580, -3.82380)],["C", (-4.38430, -0.08480, -4.08200)],["C", (-3.37290, 0.17320, -4.94870)],["C", (5.57710, 1.08350, 1.83600)],["C", (4.43850, 3.23390, 2.34680)],["C", (5.28420, 2.79100, 0.04890)],["C", (4.93750, 1.97320, 2.71950)],["C", (5.74720, 1.54940, 0.51980)],["C", (4.65680, 3.60500, 1.00830)],["C", (5.57430, -0.34890, 2.11230)],["C", (4.42640, -2.15060, 3.39110)],["C", (5.26880, -2.59390, 1.09270)],["C", (4.93250, -0.84460, 3.26330)],["C", (5.74000, -1.27030, 1.06310)],["C", (4.64190, -2.99270, 2.28460)],["C", (4.98110, -3.29150, -0.15470)],["C", (3.34730, -4.77230, -1.30340)],["C", (4.49930, -2.97310, -2.57300)],["C", (4.07280, -4.36590, -0.16980)],["C", (5.17630, -2.64090, -1.38770)],["C", (3.61360, -4.06120, -2.48620)],["C", (4.32560, -1.97330, -3.62020)],["C", (2.69660, -1.01610, -5.23840)],["C", (4.33340, 0.46670, -4.09490)],["C", (3.26990, -2.09560, -4.54410)],["C", (4.83730, -0.67480, -3.44870)],["C", (3.27860, 0.24260, -4.99800)],["C", (5.00110, 2.97520, -1.36880)],["C", (3.37090, 3.93170, -2.98480)],["C", (4.51340, 1.78380, -3.49510)],["C", (4.09730, 3.97270, -1.78120)],["C", (5.19190, 1.91430, -2.27160)],["C", (3.63030, 2.82940, -3.81860)],["C", (3.35530, 3.83830, 3.11290)],["C", (1.50250, 3.36900, 4.70820)],["C", (1.20710, 5.07450, 2.91980)],["C", (2.80700, 3.16710, 4.22090)],["C", (2.52450, 4.80090, 2.51020)],["C", (0.75140, 4.35030, 4.03430)],["C", (0.26130, 5.69300, -1.79430)],["C", (-0.22800, 4.50100, -3.92490)],["C", (2.11060, 4.65470, -3.09810)],["C", (-0.61880, 5.24320, -2.79750)],["C", (1.62070, 5.39090, -2.00420)],["C", (1.15220, 4.25230, -4.04230)],["C", (0.25520, 5.63800, 1.96900)],["C", (-2.08430, 5.48330, 1.14000)],["C", (-0.23060, 5.95560, -0.44780)],["C", (-1.12660, 5.45600, 2.16810)],["C", (0.64870, 5.90900, 0.64650)],["C", (-1.59020, 5.76060, -0.14830)],["C", (3.34110, -2.42890, 4.32250)],["C", (1.18430, -3.63500, 4.60310)],["C", (1.49470, -1.38840, 5.62330)],["C", (2.50300, -3.54070, 4.12210)],["C", (2.79910, -1.38800, 5.09960)],["C", (0.73410, -2.54270, 5.36710)],["C", (0.82690, -0.12770, 5.92340)],["C", (-1.32370, 1.10600, 5.72560)],["C", (0.83250, 2.31330, 5.45590)],["C", (-0.57910, -0.06470, 5.95260)],["C", (1.48580, 1.09320, 5.69450)],["C", (-0.57150, 2.27530, 5.50530)],["C", (2.08400, -5.47980, -1.13790)],["C", (-0.25530, -5.63370, -1.96610)],["C", (0.23070, -5.95420, 0.45400)],["C", (1.12480, -5.45150, -2.16760)],["C", (1.58950, -5.75730, 0.14900)],["C", (-0.64750, -5.90410, -0.64310)],["C", (-0.26090, -5.69470, 1.80130)],["C", (-2.11070, -4.65830, 3.10220)],["C", (0.22940, -4.50830, 3.93000)],["C", (-1.62110, -5.39420, 2.00760)],["C", (0.62070, -5.25020, 2.80300)],["C", (-1.14910, -4.25880, 4.04770)],["C", (1.32480, -1.10600, -5.72510)],["C", (-0.82670, 0.12640, -5.92430)],["C", (-0.83270, -2.31670, -5.45360)],["C", (0.57880, 0.06580, -5.95410)],["C", (0.57250, -2.27350, -5.50360)],["C", (-1.48540, -1.09440, -5.69230)],["C", (-1.20610, -5.07110, -2.91790)],["C", (-3.35630, -3.83580, -3.11560)],["C", (-1.50400, -3.37190, -4.70700)],["C", (-2.52500, -4.79620, -2.51020)],["C", (-0.75120, -4.34940, -4.03600)],["C", (-2.80860, -3.16690, -4.22480)],["C", (-1.18410, 3.63010, -4.59950)],["C", (-3.34400, 2.42360, -4.32360)],["C", (-1.49450, 1.38780, -5.62530)],["C", (-2.50400, 3.53340, -4.11940)],["C", (-0.73450, 2.54190, -5.36800)],["C", (-2.79830, 1.38680, -5.10360)],["C", (-5.28210, -2.78640, -0.04890)],["C", (-4.43990, -3.22970, -2.34990)],["C", (-5.58160, -1.08230, -1.83860)],["C", (-4.65460, -3.60040, -1.01090)],["C", (-5.74710, -1.54440, -0.52180)],["C", (-4.94350, -1.96950, -2.72300)],["C", (-4.99750, -2.97540, 1.36780)],["C", (-3.37150, -3.93370, 2.98690)],["C", (-4.51240, -1.78380, 3.49440)],["C", (-4.09640, -3.97220, 1.78180)],["C", (-5.18950, -1.91320, 2.27080)],["C", (-3.63200, -2.83060, 3.81940)],["C", (-4.33190, -0.46660, 4.09240)],["C", (-2.69540, 1.01560, 5.23780)],["C", (-4.32420, 1.97410, 3.62040)],["C", (-3.27600, -0.24160, 4.99570)],["C", (-4.83560, 0.67700, 3.44730)],["C", (-3.27010, 2.09710, 4.54330)],["C", (-4.49720, 2.97340, 2.57230)],["C", (-3.34830, 4.77430, 1.30130)],["C", (-4.98450, 3.29150, 0.15260)],["C", (-3.60960, 4.06190, 2.48420)],["C", (-5.17700, 2.64390, 1.38570)],["C", (-4.07750, 4.36590, 0.16870)],["C", (-5.26910, 2.59410, -1.09490)],["C", (-4.42920, 2.14530, -3.39250)],["C", (-5.57870, 0.34880, -2.11590)],["C", (-4.63860, 2.99100, -2.28840)],["C", (-5.74200, 1.26840, -1.06660)],["C", (-4.93810, 0.84050, -3.26730)],]

    elif mol_str == "methane":
        mol_str = [
            ["C", (0, 0, 0)],
            ["H", (0, 0, 1)],
            ["H", (0, 1, 0)],
            ["H", (1, 0, 0)],
            ["H", (1, 1, 1)]
        ]
    elif mol_str.split('_')[0].lower()  == "c":
        num_c_atoms = int(mol_str.split('_')[1])
        mol_str = [["C", (0, 0, i)] for  i in range(num_c_atoms)]
    elif mol_str in spice_amino_acids:
        mol_str = get_mol_str_spice_aa(mol_str)
    else:
        mol_str = get_mol_str_pubchem(mol_str)

    return mol_str


def min_interatomic_distance(mol_str):
    """This computes the minimum distance between atoms."""
    coords = map(itemgetter(1), mol_str) 
    distances = map(lambda x: np.linalg.norm(np.array(x[0]) - np.array(x[1])), combinations(coords, 2))
    return min(distances)


def save_plot(base_data_dir: str, molecule_name: str, iterations: int, _plot_title: str = "Default Title"):
    import matplotlib.pyplot as plt
    import matplotlib
    import os
    matplotlib.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})

    import seaborn as sns
    sns.set_theme()
    sns.set_style("white")

    data_dir = base_data_dir + molecule_name + '/'

    def prepare(val):
        val = np.abs(val[val == val])
        val[np.logical_and(val<1e-15, val!=0)] = 2e-15 # show the ones that go out of plot
        val[val==0] = 1e-17 # remove zeros.
        return val

    xticks = []
    xticklabels = []

    fig, ax = plt.subplots(1, 1, figsize=(14,8))
    images_subdir = f'{base_data_dir}/tmp_images/num_error/'
    os.makedirs(images_subdir, exist_ok=True)

    for outer_num, i in enumerate(range(iterations)):
        skip = 0
        print(f'figure [{i+1} / {iterations}]\r', end="")
        plt.cla()
        plt.title("[Iterations %i] \n"%(i+1) + _plot_title)
        files = sorted([a for a in os.listdir(data_dir) if "[" not in a and int(a.split("_")[0]) == i and ".jpg" not in a and ".gif" not in a])

        for num, file in enumerate(files):
            val= np.load(data_dir+file, allow_pickle=True)["v"]
            shape = val.shape
            if np.prod(shape) <= 1:
                skip += 1
                continue

            val = prepare(val)
            val = np.sort(val)
            num_max_dots = 500

            if val.size > num_max_dots: val= val[::int(val.size)//num_max_dots]

            ys = -np.ones(val.shape[0])*(num - skip)
            ax.plot([1e-15, 1e18], [ys[0], ys[1]], 'C%i-'%(num%10), lw=10, alpha=0.2)
            ax.plot(val, ys, 'C%io'%(num%10), ms=6, alpha=0.2)

            if i == 0:
                xticks.append(ys[0])
                xticklabels.append(file.replace(".npz", "").replace("%i_"%i, ""))

        plt.plot( [10**(-10), 10**(-10)], [0, xticks[-1]], 'C7--', alpha=0.6)
        plt.plot( [10**(10), 10**10], [0, xticks[-1]], 'C7--', alpha=0.6)
        plt.plot( [10**(0), 10**0], [0, xticks[-1]], 'C7-', alpha=1)

        for x, label in zip(xticks, xticklabels):
            ax.text(1e10, x+0.25, label, horizontalalignment='left', size='small', color='black', weight='normal')

        plt.yticks([], [])
        plt.xscale("log")
        plt.xlim([10**(-15), 10**18])
        if i == 0: plt.tight_layout()

        plt.savefig(f'{images_subdir}num_error{outer_num}.jpg')

    import imageio
    gif_path = f'{base_data_dir}visualize_DFT_num_error_{molecule_name}.gif'
    writer = imageio.get_writer(gif_path, loop=0, duration=7)
    for i in range(iterations):
        writer.append_data(imageio.v2.imread(f'{images_subdir}num_error{i}.jpg'))
    writer.close()
    print("Numerical error visualisation saved in", gif_path)
