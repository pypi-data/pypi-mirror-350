# -*- coding: utf-8 -*-

"""Mixin class and utilities for handling ReaxFF forcefields"""

import argparse
from datetime import date
import logging
import packaging.version
from pathlib import Path
import pprint  # noqa: F401
import sys

from tabulate import tabulate

from .metadata import metadata as ff_metadata
from seamm_util import element_data

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


metadata = {
    "general parameters": [
        {
            "id": 1,
            "description": "Overcoordination parameter 1",
            "parameter": "Pboc,1",
        },
        {
            "id": 2,
            "description": "Overcoordination parameter 2",
            "parameter": "Pboc,2",
        },
        {
            "id": 3,
            "description": "Valency angle conjugation parameter",
            "parameter": "Pcoa,2",
        },
        {
            "id": 4,
            "description": "Triple bond stabilisation parameter",
            "parameter": "Ptrip,4",
        },
        {
            "id": 5,
            "description": "Triple bond stabilisation parameter",
            "parameter": "Ptrip,3",
        },
        {
            "id": 6,
            "description": "C2-correction",
            "parameter": "kc2",
        },
        {
            "id": 7,
            "description": "Over/undercoordination parameter 6",
            "parameter": "Povun,6",
        },
        {
            "id": 8,
            "description": "Triple bond stabilisation parameter 2",
            "parameter": "Ptrip,2",
        },
        {
            "id": 9,
            "description": "Over/undercoordination parameter 7",
            "parameter": "Povun,7",
        },
        {
            "id": 10,
            "description": "Over/undercoordination parameter 8",
            "parameter": "Povun,8",
        },
        {
            "id": 11,
            "description": "Triple bond stabilization parameter 1",
            "parameter": "Ptrip,1",
        },
        {
            "id": 12,
            "description": "Lower Taper-radius",
            "parameter": "Rtaper,lower",
        },
        {
            "id": 13,
            "description": "Upper Taper-radius",
            "parameter": "Rtaper,upper",
        },
        {
            "id": 14,
            "description": "Fe dimer correction?",
            "parameter": "Pfe1",
        },
        {
            "id": 15,
            "description": "Valency undercoordination",
            "parameter": "Pval,7",
        },
        {
            "id": 16,
            "description": "Valency angle/lone pair parameter",
            "parameter": "Plp,1",
        },
        {
            "id": 17,
            "description": "Valency angle",
            "parameter": "Pval,9",
        },
        {
            "id": 18,
            "description": "Valency angle parameter",
            "parameter": "Pval,10",
        },
        {
            "id": 19,
            "description": "Not used",
            "parameter": "not_used_1",
        },
        {
            "id": 20,
            "description": "Double bond/angle parameter",
            "parameter": "Ppen,2",
        },
        {
            "id": 21,
            "description": "Double bond/angle parameter: overcoord",
            "parameter": "Ppen,3",
        },
        {
            "id": 22,
            "description": "Double bond/angle parameter: overcoord",
            "parameter": "Ppen,4",
        },
        {
            "id": 23,
            "description": "Not used",
            "parameter": "not_used_2",
        },
        {
            "id": 24,
            "description": "Torsion/BO parameter",
            "parameter": "Ptor,2",
        },
        {
            "id": 25,
            "description": "Torsion overcoordination",
            "parameter": "Ptor,3",
        },
        {
            "id": 26,
            "description": "Torsion overcoordination",
            "parameter": "Ptor,4",
        },
        {
            "id": 27,
            "description": "Conjugation 0 (not used)",
            "parameter": "not_used_3",
        },
        {
            "id": 28,
            "description": "Conjugation",
            "parameter": "Pcot,2",
        },
        {
            "id": 29,
            "description": "vdWaals shielding",
            "parameter": "PvdW,1",
        },
        {
            "id": 30,
            "description": "Cutoff for bond order (*100)",
            "parameter": "BO_cutoff",
        },
        {
            "id": 31,
            "description": "Valency angle conjugation parameter",
            "parameter": "Pcoa,4",
        },
        {
            "id": 32,
            "description": "Overcoordination parameter",
            "parameter": "Povun,4",
        },
        {
            "id": 33,
            "description": "Overcoordination parameter",
            "parameter": "Povun,3",
        },
        {
            "id": 34,
            "description": "Valency/lone pair parameter",
            "parameter": "Pval,8",
        },
        {
            "id": 35,
            "description": "Not used",
            "parameter": "not_used_4",
        },
        {
            "id": 36,
            "description": "Not used",
            "parameter": "not_used_5",
        },
        {
            "id": 37,
            "description": "Molecular energy (not used)",
            "parameter": "not_used_6",
        },
        {
            "id": 38,
            "description": "Molecular energy (not used)",
            "parameter": "not_used_7",
        },
        {
            "id": 39,
            "description": "Valency angle conjugation parameter",
            "parameter": "Pcoa,3",
        },
    ],
    "atomic parameters": [
        {
            "id": 1,
            "description": "Sigma bond covalent radius",
            "parameter": "R0,alpha",
            "units": "Å",
        },
        {
            "id": 2,
            "description": "Valency",
            "parameter": "Val",
        },
        {
            "id": 3,
            "description": "atomic mass",
            "parameter": "m",
            "units": "Dalton",
        },
        {
            "id": 4,
            "description": "van der Waals radius",
            "parameter": "RvdW",
            "units": "Å",
        },
        {
            "id": 5,
            "description": "van der Waals well depth",
            "parameter": "Dij",
            "units": "kcal/mol",
        },
        {
            "id": 6,
            "description": "gamma for electron equilibration method (EEM)",
            "parameter": "gamma",
            "units": "1/Å",
        },
        {
            "id": 7,
            "description": "Pi bond covalent radius",
            "parameter": "R0,pi",
            "units": "Å",
        },
        {
            "id": 8,
            "description": "number of valence electrons",
            "parameter": "Val,e",
        },
        {
            "id": 9,
            "description": "van der Waals parameter",
            "parameter": "alpha",
        },
        {
            "id": 10,
            "description": "van der Waals shielding",
            "parameter": "gamma,w",
            "units": "1/Å",
        },
        {
            "id": 11,
            "description": "valency for 1-3 bond order correction",
            "parameter": "Val,angle",
        },
        {
            "id": 12,
            "description": "Over/undercoordination parameter 5",
            "parameter": "Povun,5",
            "units": "kcal/mol",
        },
        {
            "id": 13,
            "description": "eReaxff atom type parameter. LAMMPS does not use.",
            "parameter": "not_used_1",
        },
        {
            "id": 14,
            "description": "electronegativity for electron equilibration method (EEM)",
            "parameter": "chi",
            "units": "eV",
        },
        {
            "id": 15,
            "description": "hardness for electron equilibration method (EEM)",
            "parameter": "eta",
            "units": "eV",
        },
        {
            "id": 16,
            "description": "Donor or acceptor switch in h-bonds, integer",
            "parameter": "Phbond",
        },
        {
            "id": 17,
            "description": "bond covalent radius with two pi orbitals",
            "parameter": "R0,pi-pi",
        },
        {
            "id": 18,
            "description": "Energy factor of lone pairs",
            "parameter": "Plp,2",
            "units": "kcal/mol",
        },
        {
            "id": 19,
            "description": "atomic enthalpy of formation. LAMMPS does not use.",
            "parameter": "Hat",
        },
        {
            "id": 20,
            "description": "bond order correction 4",
            "parameter": "Pboc,4",
        },
        {
            "id": 21,
            "description": "bond order correction 3",
            "parameter": "Pboc,3",
        },
        {
            "id": 22,
            "description": "bond order correction 5",
            "parameter": "Pboc,5",
        },
        {
            "id": 23,
            "description": "atomic softness cutoff parameter",
            "parameter": "C_i",
        },
        {
            "id": 24,
            "description": "eReaxFF constant depending on atom. LAMMPS does not use.",
            "parameter": "alpha_e",
        },
        {
            "id": 25,
            "description": "Over/undercoordination parameter 2 for valence angle",
            "parameter": "Povun,2",
        },
        {
            "id": 26,
            "description": "valence angle parameter",
            "parameter": "Pval,3",
        },
        {
            "id": 27,
            "description": "eReaxFF constant depending on atom. LAMMPS does not use.",
            "parameter": "beta",
        },
        {
            "id": 28,
            "description": "number of lone pairs",
            "parameter": "Val,boc",
        },
        {
            "id": 29,
            "description": "valence angle parameter 5",
            "parameter": "Pval,5",
        },
        {
            "id": 30,
            "description": "inner wall vdW repulsion parameter",
            "parameter": "Rcore,2",
        },
        {
            "id": 31,
            "description": "inner wall vdW repulsion parameter",
            "parameter": "Ecore,2",
        },
        {
            "id": 32,
            "description": "inner wall vdW repulsion parameter",
            "parameter": "Acore,2",
        },
    ],
    "bond parameters": [
        {
            "id": 1,
            "description": "Sigma bond dissociation energy",
            "parameter": "De,sigma",
            "units": "kcal/mol",
        },
        {
            "id": 2,
            "description": "Pi bond dissociation energy",
            "parameter": "De,pi",
            "units": "kcal/mol",
        },
        {
            "id": 3,
            "description": "Double pi bond dissociation energy",
            "parameter": "De,pi-pi",
            "units": "kcal/mol",
        },
        {
            "id": 4,
            "description": "bond energy parameter",
            "parameter": "Pbe,1",
        },
        {
            "id": 5,
            "description": "double pi bond parameter",
            "parameter": "Pbo,5",
        },
        {
            "id": 6,
            "description": "1-3 bond order correction",
            "parameter": "13_boc",
        },
        {
            "id": 7,
            "description": "double pi bond order",
            "parameter": "Pbo,6",
        },
        {
            "id": 8,
            "description": "Overcoordination penalty",
            "parameter": "Povun,1",
        },
        {
            "id": 9,
            "description": "bond energy parameter",
            "parameter": "Pbe,2",
        },
        {
            "id": 10,
            "description": "pi bond order parameter",
            "parameter": "Pbo,3",
        },
        {
            "id": 11,
            "description": "pi bond order parameter",
            "parameter": "Pbo,4",
        },
        {
            "id": 12,
            "description": "not used. LAMMPS does not use.",
            "parameter": "not_used_1",
        },
        {
            "id": 13,
            "description": "sigma bond order",
            "parameter": "Pbo_1",
        },
        {
            "id": 14,
            "description": "sigma bond order",
            "parameter": "Pbo,2",
        },
        {
            "id": 15,
            "description": "uncorrected BO overcoordination",
            "parameter": "ovc",
        },
        {
            "id": 16,
            "description": "LAMMPS does not use, nor read",
            "parameter": "not_used_2",
        },
    ],
    "off-diagonal parameters": [
        {
            "id": 1,
            "description": "van der Waals energy",
            "parameter": "Dij",
            "units": "kcal/mol",
        },
        {
            "id": 2,
            "description": "van der Waals radius",
            "parameter": "RvdW",
            "units": "Å",
        },
        {
            "id": 3,
            "description": "van der Waals parameter",
            "parameter": "alpha",
        },
        {
            "id": 4,
            "description": "sigma bond length",
            "parameter": "R0,sigma",
            "units": "Å",
        },
        {
            "id": 5,
            "description": "pi bond length",
            "parameter": "R0,pi",
            "units": "Å",
        },
        {
            "id": 6,
            "description": "pi-pi bond length",
            "parameter": "R0,pi-pi",
            "units": "Å",
        },
    ],
    "angle parameters": [
        {
            "id": 1,
            "description": "180° - equilibrium angle",
            "parameter": "Theta0",
            "units": "degree",
        },
        {
            "id": 2,
            "description": "valence angle parameter 1",
            "parameter": "Pval,1",
            "units": "kcal/mol",
        },
        {
            "id": 3,
            "description": "valence angle parameter 2",
            "parameter": "Pval,2",
        },
        {
            "id": 4,
            "description": "valence conjugation",
            "parameter": "Pcoa,1",
            "units": "kcal/mol",
        },
        {
            "id": 5,
            "description": "Undercoordination penalty",
            "parameter": "Pval,7",
        },
        {
            "id": 6,
            "description": "penalty energy",
            "parameter": "Ppen,1",
        },
        {
            "id": 7,
            "description": "valence angle parameter 4",
            "parameter": "Pval,4",
        },
    ],
    "torsion parameters": [
        {
            "id": 1,
            "description": "V1 torsion barrier",
            "parameter": "V1",
            "units": "kcal/mol",
        },
        {
            "id": 2,
            "description": "V2 torsion barrier",
            "parameter": "V2",
            "units": "kcal/mol",
        },
        {
            "id": 3,
            "description": "V3 torsion barrier",
            "parameter": "V3",
            "units": "kcal/mol",
        },
        {
            "id": 4,
            "description": "Torsion angle parameter",
            "parameter": "Ptor,1",
        },
        {
            "id": 5,
            "description": "Conjugation energy",
            "parameter": "Pcot,1",
            "units": "kcal/mol",
        },
        {
            "id": 6,
            "description": "LAMMPS does not use, nor read",
            "parameter": "not_used_1",
        },
        {
            "id": 7,
            "description": "LAMMPS does not use, nor read",
            "parameter": "not_used_2",
        },
    ],
    "hydrogen bond parameters": [
        {
            "id": 1,
            "description": "hydrogen bond length",
            "parameter": "Rhb",
            "units": "Å",
        },
        {
            "id": 2,
            "description": "hydrogen bond energy",
            "parameter": "Ehb",
            "units": "kcal/mol",
        },
        {
            "id": 3,
            "description": "hydrogen bond angle",
            "parameter": "Thb",
            "units": "degree",
        },
        {
            "id": 4,
            "description": "LAMMPS does read",
            "parameter": "Phb3",
        },
    ],
}

# Add to the main forcefield metadata
ff_metadata["reaxff_general_parameters"] = {
    "equation": [],
    "constants": [
        ("Parameter", ""),
        ("Value", ""),
        ("Description", ""),
    ],
    "topology": {
        "type": "reaxff general parameters",
        "n_atoms": 0,
        "symmetry": "none",
        "fill": 0,
        "flip": 0,
    },
}

# The atomic parameter sections
n_ap = len(metadata["atomic parameters"])
tmp = sorted(metadata["atomic parameters"], key=lambda k: k["parameter"])
for g0 in range(0, n_ap, 8):
    g1 = min(g0 + 8, n_ap)
    ff_metadata[f"reaxff_atomic_parameters_{g0 + 1}-{g1}"] = {
        "equation": [],
        "constants": [
            (d["parameter"], d["units"] if "units" in d else "") for d in tmp[g0:g1]
        ],
        "topology": {
            "type": "reaxff atomic parameters",
            "n_atoms": 1,
            "symmetry": "none",
            "fill": 0,
            "flip": 0,
        },
    }

# The bond parameter sections
n_bp = len(metadata["bond parameters"])
tmp = sorted(metadata["bond parameters"], key=lambda k: k["parameter"])
for g0 in range(0, n_bp, 8):
    g1 = min(g0 + 8, n_ap)
    ff_metadata[f"reaxff_bond_parameters_{g0 + 1}-{g1}"] = {
        "equation": [],
        "constants": [
            (d["parameter"], d["units"] if "units" in d else "") for d in tmp[g0:g1]
        ],
        "topology": {
            "type": "reaxff bond parameters",
            "n_atoms": 2,
            "symmetry": "none",
            "fill": 0,
            "flip": 0,
        },
    }

# The off-diagonal parameter sections
tmp = sorted(metadata["off-diagonal parameters"], key=lambda k: k["parameter"])
ff_metadata["reaxff_off-diagonal_parameters"] = {
    "equation": [],
    "constants": [(d["parameter"], d["units"] if "units" in d else "") for d in tmp],
    "topology": {
        "type": "reaxff off-diagonal parameters",
        "n_atoms": 2,
        "symmetry": "none",
        "fill": 0,
        "flip": 0,
    },
}

# The angle parameter sections
tmp = sorted(metadata["angle parameters"], key=lambda k: k["parameter"])
ff_metadata["reaxff_angle_parameters"] = {
    "equation": [],
    "constants": [(d["parameter"], d["units"] if "units" in d else "") for d in tmp],
    "topology": {
        "type": "reaxff angle parameters",
        "n_atoms": 3,
        "symmetry": "none",
        "fill": 0,
        "flip": 0,
    },
}

# The torsion parameter sections
tmp = sorted(metadata["torsion parameters"], key=lambda k: k["parameter"])
ff_metadata["reaxff_torsion_parameters"] = {
    "equation": [],
    "constants": [(d["parameter"], d["units"] if "units" in d else "") for d in tmp],
    "topology": {
        "type": "reaxff torsion parameters",
        "n_atoms": 4,
        "symmetry": "none",
        "fill": 0,
        "flip": 0,
    },
}

# The hydrogen bond parameter sections
tmp = sorted(metadata["hydrogen bond parameters"], key=lambda k: k["parameter"])
ff_metadata["reaxff_hydrogen-bond_parameters"] = {
    "equation": [],
    "constants": [(d["parameter"], d["units"] if "units" in d else "") for d in tmp],
    "topology": {
        "type": "reaxff hydrogen bond parameters",
        "n_atoms": 3,
        "symmetry": "none",
        "fill": 0,
        "flip": 0,
    },
}


def import_reaxff(options):
    """Import a ReaxFF forcefield in the Reax format"""
    reaxff = Path(options.reaxff).expanduser()
    output = Path(options.output).expanduser()

    if options.personal:
        output = Path("~/.seamm.d/data/Forcefields/").expanduser() / output.name

    if "ffname" not in options:
        ffname = output.stem
    else:
        ffname = options.ffname

    version = options.version if "version" in options else None

    print(f"Importing ReaxFF forcefield from {reaxff} to {output}")

    parameters = read_reaxff_parameters(reaxff)

    write_ff_file(output, parameters, ffname=ffname, version=version)


def parse_reax_data(lines):
    """Parse ReaxFF data from a list of lines

    Note
    ----
    It appears that the codes reading the forcefield files are not very fussy. The file
    contains a header line for each section giving the number of atoms or terms in the
    section. However, the code does not appear to check that the number of atoms or
    terms actually match that given.

    Therefore this code will warn about such mismatches, but not raise an exception. It
    appears that the header line separating sections has a sinlge integer, perhaps
    followed by a comment. We will use that as a marker to separate sections.
    """
    parameters = {}
    it = iter(lines)
    parameters["comment"] = next(it)

    # Handle the general parameters
    header = next(it)
    n_general_parameters = int(header.split()[0])
    mdata = metadata["general parameters"]
    gp = parameters["general parameters"] = {}
    for i, line in enumerate(it):
        line = line.split("!")[0].split()
        if len(line) == 1 and line[0].isdecimal():
            nelements = int(line[0])
            break
        gp[mdata[i]["parameter"]] = line[0]

    if i != n_general_parameters:
        logger.warning(
            f"Expected {n_general_parameters} general parameters, but found {i}"
        )

    # Handle the atomic parameters... the section looks like this:
    #
    #  7    ! Nr of atoms; cov.r; valency;a.m;Rvdw;Evdw;gammaEEM;cov.r2;#
    #            alfa;gammavdW;valency;Eunder;Eover;chiEEM;etaEEM;n.u.
    #            cov r3;Elp;Heat inc.;n.u.;n.u.;n.u.;n.u.
    #            ov/un;val1;n.u.;val3,vval4
    # Li   2.1097   1.0000   6.9410   2.1461   0.3726   0.8651  -0.1000   1.0000
    #      9.0000   1.2063   1.0000   0.0000   0.0000  -6.2351  12.7757   0.0000
    #     -1.0000   0.0000  37.5000   5.4409   6.9107   0.1973   0.8563   0.0000
    #    -17.1659   2.2989   1.0338   1.0000   2.8103   1.3000   0.2000  13.0000
    # Si   2.0057   4.0000  28.0600   1.7098   0.2683   0.3041   1.2635   4.0000
    # ...

    n_atoms = 0
    parameters["atomic parameters"] = {}
    mdata = metadata["atomic parameters"]
    for line in it:
        if line.strip() == "" or line.strip()[0] == "!":
            continue
        line_sv = line
        line = line.split("!")[0].split()
        if len(line) == 1 and line[0].isdecimal():
            nbonds = int(line[0])
            break
        if len(line) > 1 and line[0].isalpha() and len(line[0]) <= 2:
            # Looks like an element!
            symbol = line[0]
            # Except use X as a placeholder...so just skip
            if symbol == "X":
                next(it)
                next(it)
                next(it)
                continue

            if len(line) != 9:
                raise ValueError(
                    f"Expected 8 element parameters, but found {len(line) - 1}"
                    f"\n\t{line_sv}"
                )
            ap = parameters["atomic parameters"][symbol] = {}
            n_atoms += 1
            count = 0
            for val in line[1:]:
                ap[mdata[count]["parameter"]] = val
                count += 1
            for i in range(3):
                line = next(it).split("!")[0].split()
                if len(line) != 8:
                    raise ValueError(
                        f"Expected 8 element parameters, but found {len(line)}"
                        f"\n\t{line_sv}"
                    )
                for val in line:
                    ap[mdata[count]["parameter"]] = val
                    count += 1
    if nelements != n_atoms:
        logger.warning(f"Expected {nelements} atomic parameters, but found {n_atoms}")

    # Handle the bond parameters... the section looks like this:
    #
    # 20      ! Nr of bonds; Edis1;LPpen;n.u.;pbe1;pbo5;13corr;pbo6
    #                         pbe2;pbo3;pbo4;n.u.;pbo1;pbo2;ovcorr
    #  1  1  59.2876   0.0000   0.0000   0.4363   0.3000   0.0000  26.0000   0.4590
    #         0.0485   0.0000  12.0000   1.0000  -0.1990   4.1914   0.0000   0.0000
    #  2  2  71.2687  45.8533  17.1960  -0.4953  -0.3182   1.0000  15.9405   0.0100
    # ...

    n_bonds = 0
    parameters["bond parameters"] = {}
    mdata = metadata["bond parameters"]
    for line in it:
        if line.strip() == "" or line.strip()[0] == "!":
            continue
        line_sv = line
        line = line.split("!")[0].split()
        if len(line) == 1 and line[0].isdecimal():
            noffdiagonals = int(line[0])
            break
        if len(line) > 2 and line[0].isdecimal() and line[1].isdecimal():
            # Looks like a bond!
            if len(line) != 10:
                raise ValueError(
                    f"Expected 8 bond parameters, but found {len(line) - 2}"
                    f"\n\t{line_sv}"
                )
            key = (int(line[0]), int(line[1]))
            n_bonds += 1
            bp = parameters["bond parameters"][key] = {}
            count = 0
            for val in line[2:]:
                bp[mdata[count]["parameter"]] = val
                count += 1
            line = next(it).split("!")[0].split()
            if len(line) != 8:
                raise ValueError(
                    "Expected 8 bond parameters, but found {len(line)}\n\t{line_sv}"
                )
            for val in line:
                bp[mdata[count]["parameter"]] = val
                count += 1
    if nbonds != n_bonds:
        logger.warning(f"Expected {nbonds} bond parameters, but found {n_bonds}")

    # Handle the off-diagonal parameters... the section looks like this:
    #
    # 14    ! Nr of off-diagonal terms; Ediss;Ro;gamma;rsigma;rpi;rpi2
    #  2  1   0.3183   2.4157   9.0000   2.1443   1.0000   1.0000
    #  3  1   0.3984   2.1335   9.6455   1.5037   1.0000   1.0000
    # ...

    n_offdiagonals = 0
    mdata = metadata["off-diagonal parameters"]
    parameters["off-diagonal parameters"] = {}
    for line in it:
        if line.strip() == "" or line.strip()[0] == "!":
            continue
        line_sv = line
        line = line.split("!")[0].split()
        if len(line) == 1 and line[0].isdecimal():
            nangles = int(line[0])
            break
        if len(line) > 2 and line[0].isdecimal() and line[1].isdecimal():
            # Looks like an off-diagonal!
            if len(line) != 8:
                raise ValueError(
                    f"Expected 6 element parameters, but found {len(line) - 2}"
                    f"\n\t{line_sv}"
                )
            key = (int(line[0]), int(line[1]))
            n_offdiagonals += 1
            odp = parameters["off-diagonal parameters"][key] = {}
            count = 0
            for val in line[2:]:
                odp[mdata[count]["parameter"]] = val
                count += 1
    if noffdiagonals != n_offdiagonals:
        logger.warning(
            f"Expected {noffdiagonals} off-diagonal parameters, "
            f"but found {n_offdiagonals}"
        )

    # Handle the angle parameters... the section looks like this:
    #
    # 62    ! Nr of angles;at1;at2;at3;Thetao,o;ka;kb;pv1;pv2;val(bo)
    #  2  2  2  74.0968  15.6349   3.6545   0.0000   0.2525   0.0000   1.2262
    #  3  3  3  62.0574  16.1545   3.0575   0.0000   0.0100   0.3556   1.0000
    #  2  3  3   2.5162  18.6626   4.8139   0.0000   0.0775   0.0000   1.0150
    # ...

    n_angles = 0
    parameters["angle parameters"] = {}
    mdata = metadata["angle parameters"]
    for line in it:
        if line.strip() == "" or line.strip()[0] == "!":
            continue
        line_sv = line
        line = line.split("!")[0].split()
        if len(line) == 1 and line[0].isdecimal():
            ntorsions = int(line[0])
            break
        if (
            len(line) > 3
            and line[0].isdecimal()
            and line[1].isdecimal()
            and line[2].isdecimal()
        ):
            # Looks like an angle!
            if len(line) != 10:
                raise ValueError(
                    f"Expected 10 angle parameters, but found {len(line) - 3}"
                    f"\n\t{line_sv}"
                )
            key = (int(line[0]), int(line[1]), int(line[2]))
            n_angles += 1
            ap = parameters["angle parameters"][key] = {}
            for count, val in enumerate(line[3:]):
                ap[mdata[count]["parameter"]] = val
    if nangles != n_angles:
        logger.warning(f"Expected {nangles} angle parameters, but found {n_angles}")

    # Handle the torsion parameters... the section looks like this:
    #
    # 14    ! Nr of torsions;at1;at2;at3;at4;;V1;V2;V3;V2(BO);vconj;n.u;n
    #  3  3  3  3   2.5000  32.8238   0.2056  -9.0000  -2.2982   0.0000   0.0000
    # ...
    # 0 element indices are wildcards.

    n_torsions = 0
    parameters["torsion parameters"] = {}
    mdata = metadata["torsion parameters"]
    for line in it:
        if line.strip() == "" or line.strip()[0] == "!":
            continue
        line_sv = line
        line = line.split("!")[0].split()
        if len(line) == 1 and line[0].isdecimal():
            nhbonds = int(line[0])
            break
        if (
            len(line) > 4
            and line[0].isdecimal()
            and line[1].isdecimal()
            and line[2].isdecimal()
            and line[3].isdecimal()
        ):
            # Looks like a torsion!
            if len(line) != 11:
                raise ValueError(
                    f"Expected 7 torsion parameters, but found {len(line) - 4}"
                    f"\n\t{line_sv}"
                )
            key = (int(line[0]), int(line[1]), int(line[2]), int(line[3]))
            n_torsions += 1
            tp = parameters["torsion parameters"][key] = {}
            for count, val in enumerate(line[4:]):
                tp[mdata[count]["parameter"]] = val
    if ntorsions != n_torsions:
        logger.warning(
            f"Expected {ntorsions} torsion parameters, but found {n_torsions}"
        )

    # Handle the hydrogen bond parameters... the section looks like this:
    #
    # 1    ! Nr of hydrogen bonds;at1;at2;at3;Rhb;Dehb;vhb1
    # 0  0  0   0.0000  -0.0000   0.0000  00.0000
    # ...

    n_hbonds = 0
    parameters["hydrogen bond parameters"] = {}
    mdata = metadata["hydrogen bond parameters"]
    for line in it:
        if line.strip() == "" or line.strip()[0] == "!":
            continue
        line_sv = line
        line = line.split("!")[0].split()
        if len(line) == 1 and line[0].isdecimal():
            logger.warning(f"Found another section after the hydrogen bonds: {line_sv}")
            break
        if (
            len(line) > 3
            and line[0].isdecimal()
            and line[1].isdecimal()
            and line[2].isdecimal()
        ):
            # Looks like a hydrogen bond!
            if len(line) != 7:
                raise ValueError(
                    f"Expected 4 hydrogen bond parameters, but found {len(line) - 3}"
                    f"\n\t{line_sv}"
                )
            # Zero indices used to indicate no hydrogen bond
            if line[0] == "0" and line[1] == "0" and line[2] == "0":
                nhbonds -= 1
                continue
            key = (int(line[0]), int(line[1]), int(line[2]))
            n_hbonds += 1
            hb = parameters["hydrogen bond parameters"][key] = {}
            for count, val in enumerate(line[3:]):
                hb[mdata[count]["parameter"]] = val
    if nhbonds != n_hbonds:
        logger.warning(
            f"Expected {nhbonds} hydrogen bond parameters, but found {n_hbonds}"
        )

    # See if there is anything else at the end of the file
    for line in it:
        if line.strip() == "" or line.strip()[0] == "!":
            continue
        logger.warning(f"Found another section after the hydrogen bonds: {line_sv}")

    return parameters


def read_reaxff_parameters(filename):
    """Read ReaxFF parameters from a file"""
    with open(filename, "r") as f:
        return parse_reax_data(f.readlines())


def reaxff_to_molssi_format(parameters, ffname="reaxff", version=None):
    """Create the text parameter file for ReaxFF

    Parameters
    ----------
    parameters : dict
        The forcefield parameters to write to the file.
    ffname : str = "reaxff"
        The name of the forcefield
    version : str = None
        The version number, defaults to todays date.

    Returns
    -------
    [str]
    """
    if version is None:
        version = date.isoformat(date.today()).replace("-", ".")

    #
    # The header and definition section
    #

    text = f"!MolSSI forcefield 1\n\n\n#define {ffname}\n\n"

    sections = []
    # The general section
    sections.append("reaxff_general_parameters")

    # The atomic parameter sections
    n_ap = len(metadata["atomic parameters"])
    for g0 in range(0, n_ap, 8):
        g1 = min(g0 + 8, n_ap)
        sections.append(f"reaxff_atomic_parameters_{g0 + 1}-{g1}")

    # The bond parameter sections
    n_bp = len(metadata["bond parameters"])
    for g0 in range(0, n_bp, 8):
        g1 = min(g0 + 8, n_ap)
        sections.append(f"reaxff_bond_parameters_{g0 + 1}-{g1}")

    # The off-diagonal parameter section
    sections.append("reaxff_off-diagonal_parameters")

    # The angle parameter section
    sections.append("reaxff_angle_parameters")

    # The torsion parameter section
    sections.append("reaxff_torsion_parameters")

    # The hydrogen bond parameter sections
    if len(parameters["hydrogen bond parameters"]) > 0:
        sections.append("reaxff_hydrogen-bond_parameters")

    # And tabulate
    table = {
        "Version": [version] * len(sections),
        "Ref": ["1"] * len(sections),
        "Section": sections,
        "Label": [ffname] * len(sections),
    }

    tmp = tabulate(
        table,
        headers="keys",
        tablefmt="simple",
        colalign=("center", "right", "left", "left"),
        disable_numparse=False,
    ).splitlines()
    tmp[0] = "!" + tmp[0][1:]
    tmp[1] = "!" + tmp[1][1:]
    text += "\n".join(tmp)

    #
    # The general parameters
    #

    text += f"\n\n\n#reaxff_general_parameters {ffname}\n\n"

    tmp = [(v["parameter"], v["description"]) for v in metadata["general parameters"]]
    tmp = sorted(tmp, key=lambda k: k[0])

    gp = parameters["general parameters"]
    table = {
        "Version": [version] * len(tmp),
        "Ref": ["1"] * len(tmp),
        "Parameter": [v[0] for v in tmp],
        "Value": [gp[v[0]] for v in tmp],
        "Description": [v[1] for v in tmp],
    }

    tmp = tabulate(
        table,
        headers="keys",
        tablefmt="simple",
        colalign=("center", "right", "center", "decimal", "left"),
        disable_numparse=False,
    ).splitlines()
    tmp[0] = "!" + tmp[0][1:]
    tmp[1] = "!" + tmp[1][1:]
    text += "\n".join(tmp)

    #
    # The atomic parameters, split into groups of 8
    #

    tmp = sorted([v["parameter"] for v in metadata["atomic parameters"]])

    # Get the elements and order by atomic number
    ap = parameters["atomic parameters"]
    atomic_metadata = [
        (element_data[s]["atomic number"], s, index)
        for index, s in enumerate(ap.keys(), start=1)
    ]
    atomic_metadata = sorted(atomic_metadata, key=lambda k: k[0])

    # Create a mapping from old index to new for the bond terms, etc.
    to_new = {data[2]: index for index, data in enumerate(atomic_metadata)}

    # Ordered list of symbols
    symbols = [s[1] for s in atomic_metadata]

    # Groups of 8
    n_a = len(symbols)
    for g0 in range(0, n_ap, 8):
        g1 = min(g0 + 8, n_ap)
        text += f"\n\n\n#reaxff_atomic_parameters_{g0 + 1}-{g1} {ffname}\n\n"
        table = {
            "Version": [version] * n_a,
            "Ref": ["1"] * n_a,
            "Center": symbols,
        }
        for parameter in tmp[g0:g1]:
            table[parameter] = [ap[s][parameter] for s in symbols]
        lines = tabulate(
            table,
            headers="keys",
            tablefmt="simple",
            colalign=["center", "right", "center"] + ["decimal"] * (g1 - g0),
            disable_numparse=False,
        ).splitlines()
        lines[0] = "!" + lines[0][1:]
        lines[1] = "!" + lines[1][1:]
        text += "\n".join(lines)

    #
    # The bond parameters, split into groups of 8
    #

    tmp = sorted([v["parameter"] for v in metadata["bond parameters"]])

    # Get the elements and order by atomic number
    bp = parameters["bond parameters"]

    # The indices, and turn into symbols
    indices = []
    for i, j in bp.keys():
        i1 = to_new[i]
        j1 = to_new[j]
        if i1 < j1:
            i1, j1 = j1, i1
        indices.append((i1, j1, (i, j)))
    indices = sorted(indices, key=lambda k: k[1])
    indices = sorted(indices, key=lambda k: k[0])

    # Groups of 8
    n = len(bp)
    for g0 in range(0, n_bp, 8):
        g1 = min(g0 + 8, n_bp)
        text += f"\n\n\n#reaxff_bond_parameters_{g0 + 1}-{g1} {ffname}\n\n"
        table = {
            "Version": [version] * n,
            "Ref": ["1"] * n,
            "I": [symbols[k[0]] for k in indices],
            "J": [symbols[k[1]] for k in indices],
        }
        for parameter in tmp[g0:g1]:
            table[parameter] = [bp[k[2]][parameter] for k in indices]
        lines = tabulate(
            table,
            headers="keys",
            tablefmt="simple",
            colalign=["center", "right", "center", "center"] + ["decimal"] * (g1 - g0),
            disable_numparse=False,
        ).splitlines()
        lines[0] = "!" + lines[0][1:]
        lines[1] = "!" + lines[1][1:]
        text += "\n".join(lines)

    #
    # The off-diagonal parameters
    #

    tmp = sorted([v["parameter"] for v in metadata["off-diagonal parameters"]])

    # Get the elements and order by atomic number
    odp = parameters["off-diagonal parameters"]
    if len(odp) > 0:
        # The indices, and turn into symbols
        indices = []
        for i, j in odp.keys():
            i1 = to_new[i]
            j1 = to_new[j]
            if i1 < j1:
                i1, j1 = j1, i1
            indices.append((i1, j1, (i, j)))
        indices = sorted(indices, key=lambda k: k[1])
        indices = sorted(indices, key=lambda k: k[0])

        n = len(odp)
        text += f"\n\n\n#reaxff_off-diagonal_parameters {ffname}\n\n"
        table = {
            "Version": [version] * n,
            "Ref": ["1"] * n,
            "I": [symbols[k[0]] for k in indices],
            "J": [symbols[k[1]] for k in indices],
        }
        for parameter in tmp:
            table[parameter] = [odp[k[2]][parameter] for k in indices]
        lines = tabulate(
            table,
            headers="keys",
            tablefmt="simple",
            colalign=["center", "right", "center", "center"] + ["decimal"] * len(tmp),
            disable_numparse=False,
        ).splitlines()
        lines[0] = "!" + lines[0][1:]
        lines[1] = "!" + lines[1][1:]
        text += "\n".join(lines)

    #
    # The angle parameters
    #

    tmp = sorted([v["parameter"] for v in metadata["angle parameters"]])

    # Get the elements and order by atomic number
    ap = parameters["angle parameters"]

    # The indices, and turn into symbols
    indices = []
    for i, j, k in ap.keys():
        i1 = to_new[i]
        j1 = to_new[j]
        k1 = to_new[k]
        if i1 < k1:
            i1, k1 = k1, i1
        indices.append((i1, j1, k1, (i, j, k)))
    indices = sorted(indices, key=lambda k: k[2])
    indices = sorted(indices, key=lambda k: k[0])
    indices = sorted(indices, key=lambda k: k[1])

    n = len(ap)
    text += f"\n\n\n#reaxff_angle_parameters {ffname}\n\n"
    table = {
        "Version": [version] * n,
        "Ref": ["1"] * n,
        "I": [symbols[k[0]] for k in indices],
        "J": [symbols[k[1]] for k in indices],
        "K": [symbols[k[2]] for k in indices],
    }
    for parameter in tmp:
        table[parameter] = [ap[k[3]][parameter] for k in indices]
    lines = tabulate(
        table,
        headers="keys",
        tablefmt="simple",
        colalign=["center", "right", "center", "center"] + ["decimal"] * len(tmp),
        disable_numparse=False,
    ).splitlines()
    lines[0] = "!" + lines[0][1:]
    lines[1] = "!" + lines[1][1:]
    text += "\n".join(lines)

    #
    # The torsion parameters
    #

    tmp = sorted([v["parameter"] for v in metadata["torsion parameters"]])

    # Get the elements and order by atomic number
    tp = parameters["torsion parameters"]

    # The indices, and turn into symbols
    indices = []
    for i, j, k, l in tp.keys():
        i1 = 999 if i == 0 else to_new[i]
        j1 = to_new[j]
        k1 = to_new[k]
        l1 = 999 if i == 0 else to_new[l]
        if j1 < k1 or j1 == k1 and i1 < l1:
            i1, j1, k1, l1 = l1, k1, j1, i1
        indices.append((i1, j1, k1, l1, (i, j, k, l)))
    indices = sorted(indices, key=lambda k: k[3])
    indices = sorted(indices, key=lambda k: k[0])
    indices = sorted(indices, key=lambda k: k[2])
    indices = sorted(indices, key=lambda k: k[1])

    n = len(tp)
    text += f"\n\n\n#reaxff_torsion_parameters {ffname}\n\n"
    table = {
        "Version": [version] * n,
        "Ref": ["1"] * n,
        "I": ["*" if k[0] == 999 else symbols[k[0]] for k in indices],
        "J": [symbols[k[1]] for k in indices],
        "K": [symbols[k[2]] for k in indices],
        "L": ["*" if k[3] == 999 else symbols[k[3]] for k in indices],
    }
    for parameter in tmp:
        table[parameter] = [tp[k[4]][parameter] for k in indices]
    lines = tabulate(
        table,
        headers="keys",
        tablefmt="simple",
        colalign=["center", "right", "center", "center"] + ["decimal"] * len(tmp),
        disable_numparse=False,
    ).splitlines()
    lines[0] = "!" + lines[0][1:]
    lines[1] = "!" + lines[1][1:]
    text += "\n".join(lines)

    #
    # The hydrogen-bond parameters. They are directional, no symmetry.
    #

    tmp = sorted([v["parameter"] for v in metadata["hydrogen bond parameters"]])

    # Get the elements and order by atomic number
    hbp = parameters["hydrogen bond parameters"]

    if len(hbp) > 0:
        # The indices, and turn into symbols
        indices = []
        for i, j, k in hbp.keys():
            i1 = to_new[i]
            j1 = to_new[j]
            k1 = to_new[k]
            indices.append((i1, j1, k1, (i, j, k)))
        indices = sorted(indices, key=lambda k: k[2])
        indices = sorted(indices, key=lambda k: k[0])
        indices = sorted(indices, key=lambda k: k[1])

        n = len(hbp)
        text += f"\n\n\n#reaxff_hydrogen-bond_parameters {ffname}\n\n"
        table = {
            "Version": [version] * n,
            "Ref": ["1"] * n,
            "I": [symbols[k[0]] for k in indices],
            "J": [symbols[k[1]] for k in indices],
            "K": [symbols[k[2]] for k in indices],
        }
        for parameter in tmp:
            table[parameter] = [hbp[k[3]][parameter] for k in indices]
        lines = tabulate(
            table,
            headers="keys",
            tablefmt="simple",
            colalign=["center", "right", "center", "center"] + ["decimal"] * len(tmp),
            disable_numparse=False,
        ).splitlines()
        lines[0] = "!" + lines[0][1:]
        lines[1] = "!" + lines[1][1:]
        text += "\n".join(lines)

    text += f"""

#reference 1
@Author SEAMM
@Date {date.isoformat(date.today())}
ReaxFF forcefield translated from Reax format

{parameters["comment"]}

#end
"""

    return text


def write_ff_file(path, parameters, ffname=None, version=None):
    """Write the MolSSI forcefield to the given path

    Parameters
    ----------
    path : str or pathlib.Path
        The path to write the forcefield to
    parameters : dict
        The forcefield parameters
    ffname : str = None
        The name of the forcefield. The default is to use the stem of the path
    version : str = None
        The version for the forcefield. The default is today's date
    """
    path = Path(path)
    if ffname is None:
        ffname = path.stem

    text = reaxff_to_molssi_format(parameters, ffname, version)
    path.write_text(text)


def run():
    """Run the script from the commandline."""
    # Create the argument parser and set the debug level ASAP
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--log-level",
        default="WARNING",
        type=str.upper,
        choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="The level of informational output, defaults to '%(default)s'",
    )

    # set up the subparsers
    subparser = parser.add_subparsers()

    # The import subparser
    import_parser = subparser.add_parser("import", help="Import a ReaxFF forcefield")

    import_parser.set_defaults(func=import_reaxff)

    import_parser.add_argument(
        "reaxff",
        default=None,
        help="The ReaxFF file to read.",
    )
    import_parser.add_argument(
        "output",
        default=None,
        help="The forcefield file to write.",
    )
    import_parser.add_argument(
        "--personal",
        action="store_true",
        help="Use the personal forcefield database.",
    )
    parser.add_argument(
        "--version",
        default=None,
        help="Forcefield version, defaults to todays date",
    )
    parser.add_argument(
        "--ffname",
        default=None,
        help="Name of the forcefield, defaults to the stem of the file name",
    )

    # Parse the command-line arguments and call the requested function or the GUI
    options = parser.parse_args()

    # Set up the logging
    logging.basicConfig(level=options.log_level)

    # do it!
    if "func" not in options:
        print(f"Missing arguments to the ReaxFF handler: {' '.join(sys.argv[1:])}")
        # Append help so help will be printed
        sys.argv.append("--help")
        # re-run
        run()
    else:
        sys.exit(options.func(options))


class ReaxFFMixin:

    def eex_reaxff_general_parameters(self, eex, configuration):
        """Create the custom forcefield file for the ReaxFF calculation."""
        n_atoms = configuration.n_atoms

        # Need eex["charges"] to write out the correct structure for LAMMPS
        eex["charges"] = [0.0] * n_atoms

        # pprint.pprint(eex)
        # print("\n" * 5)
        # pprint.pprint(self.ff)

        # elements in correct order
        symbols = eex["atom types"]

        # And the forcefield file
        lines = []
        lines.append(
            f"ReaxFF forcefield {self.current_forcefield} for "
            f"{configuration.system.name}/{configuration.name}"
        )

        # General parameters
        P = self.ff["reaxff_general_parameters"]
        lines.append(" 39        ! Number of general parameters")
        for mdata in metadata["general parameters"]:
            parameter = mdata["parameter"]
            D = P[parameter]
            lines.append(
                f" {float(D['value']):9.4f} ! {parameter}: {mdata['description']}"
            )

        # Atomic parameters
        M = metadata["atomic parameters"]
        n = len(M)
        n_types = len(symbols)
        line = f" {n_types:2d}        ! Num atom params; "
        tmp = [d["parameter"] for d in M[0:8]]
        line += "; ".join(tmp)
        lines.append(line)
        for g0 in range(8, n, 8):
            g1 = min(g0 + 8, n)
            tmp = [d["parameter"] for d in M[g0:g1]]
            lines.append("           ! " + "; ".join(tmp))

        # Eat for the atomic energy correction
        Eat = {}
        for S in symbols:
            P = {}
            for section in eex["terms"]["reaxff atomic parameters"]:
                P.update(self.ff[section][(S,)])

            Eat[S] = P["Hat"]
            for g0 in range(0, n, 8):
                g1 = min(g0 + 8, n)
                tmp = [f"{float(P[k['parameter']]):8.4f}" for k in M[g0:g1]]
                if g0 == 0:
                    lines.append(f" {S:2} " + " ".join(tmp))
                else:
                    lines.append("    " + " ".join(tmp))

        # Calculate the atom offset energy
        E = sum([float(Eat[S]) for S in configuration.atoms.symbols])
        eex["Sum of atomic energies"] = E

        # Bond parameters
        M = metadata["bond parameters"]
        n = len(M)

        # How many bonds will we have?
        section = eex["terms"]["reaxff bond parameters"][0]
        indices = []
        for key in self.ff[section]:
            i, j = key
            if i in symbols and j in symbols:
                indices.append(key)

        line = f"{len(indices):3d}        ! Num bonds; "
        tmp = [d["parameter"] for d in M[0:8]]
        line += "; ".join(tmp)
        lines.append(line)
        for g0 in range(8, n, 8):
            g1 = min(g0 + 8, n)
            tmp = [d["parameter"] for d in M[g0:g1]]
            lines.append("           ! " + "; ".join(tmp))

        for key in indices:
            P = {}
            for section in eex["terms"]["reaxff bond parameters"]:
                P.update(self.ff[section][key])

            i, j = key
            i = symbols.index(i) + 1
            j = symbols.index(j) + 1
            for g0 in range(0, n, 8):
                g1 = min(g0 + 8, n)
                tmp = [f"{float(P[k['parameter']]):8.4f}" for k in M[g0:g1]]
                if g0 == 0:
                    lines.append(f"{int(i):3d}{int(j):3d} " + " ".join(tmp))
                else:
                    lines.append("       " + " ".join(tmp))

        # Off-Diagonal parameters
        M = metadata["off-diagonal parameters"]
        n = len(M)

        # How many off-diagonals will we have?
        section = eex["terms"]["reaxff off-diagonal parameters"][0]
        indices = []
        for key in self.ff[section]:
            i, j = key
            if i in symbols and j in symbols:
                indices.append(key)

        line = f"{len(indices):3d}        ! Num off-diagonals; "
        tmp = [d["parameter"] for d in M[0:8]]
        line += "; ".join(tmp)
        lines.append(line)
        for g0 in range(8, n, 8):
            g1 = min(g0 + 8, n)
            tmp = [d["parameter"] for d in M[g0:g1]]
            lines.append("           ! " + "; ".join(tmp))

        for key in indices:
            P = {}
            for section in eex["terms"]["reaxff off-diagonal parameters"]:
                P.update(self.ff[section][key])

            i, j = key
            i = symbols.index(i) + 1
            j = symbols.index(j) + 1
            for g0 in range(0, n, 8):
                g1 = min(g0 + 8, n)
                tmp = [f"{float(P[k['parameter']]):8.4f}" for k in M[g0:g1]]
                if g0 == 0:
                    lines.append(f"{int(i):3d}{int(j):3d} " + " ".join(tmp))
                else:
                    lines.append("       " + " ".join(tmp))

        # Angle parameters
        M = metadata["angle parameters"]
        n = len(M)

        # How many angles will we have?
        section = eex["terms"]["reaxff angle parameters"][0]
        indices = []
        for key in self.ff[section]:
            i, j, k = key
            if i in symbols and j in symbols and k in symbols:
                indices.append(key)

        line = f"{len(indices):3d}        ! Num angles; "
        tmp = [d["parameter"] for d in M[0:8]]
        line += "; ".join(tmp)
        lines.append(line)
        for g0 in range(8, n, 8):
            g1 = min(g0 + 8, n)
            tmp = [d["parameter"] for d in M[g0:g1]]
            lines.append("           ! " + "; ".join(tmp))

        for key in indices:
            P = {}
            for section in eex["terms"]["reaxff angle parameters"]:
                P.update(self.ff[section][key])

            i, j, k = key
            i = symbols.index(i) + 1
            j = symbols.index(j) + 1
            k = symbols.index(k) + 1
            for g0 in range(0, n, 8):
                g1 = min(g0 + 8, n)
                tmp = [f"{float(P[k['parameter']]):8.4f}" for k in M[g0:g1]]
                if g0 == 0:
                    lines.append(f"{int(i):3d}{int(j):3d}{int(k):3d} " + " ".join(tmp))
                else:
                    lines.append("          " + " ".join(tmp))

        # Torsion parameters
        M = metadata["torsion parameters"]
        n = len(M)

        # How many torsions will we have?
        section = eex["terms"]["reaxff torsion parameters"][0]
        indices = []
        for key in self.ff[section]:
            i, j, k, l = key  # noqa:E741
            if i in symbols and j in symbols and k in symbols and l in symbols:
                indices.append(key)

        line = f"{len(indices):3d}        ! Num torsions; "
        tmp = [d["parameter"] for d in M[0:8]]
        line += "; ".join(tmp)
        lines.append(line)
        for g0 in range(8, n, 8):
            g1 = min(g0 + 8, n)
            tmp = [d["parameter"] for d in M[g0:g1]]
            lines.append("           ! " + "; ".join(tmp))

        for key in indices:
            P = {}
            for section in eex["terms"]["reaxff torsion parameters"]:
                P.update(self.ff[section][key])

            i, j, k, l = key  # noqa:E741
            i = 0 if i == "*" else symbols.index(i) + 1
            j = symbols.index(j) + 1
            k = symbols.index(k) + 1
            l = 0 if l == "*" else symbols.index(l) + 1  # noqa:E741
            for g0 in range(0, n, 8):
                g1 = min(g0 + 8, n)
                tmp = [f"{float(P[k['parameter']]):8.4f}" for k in M[g0:g1]]
                if g0 == 0:
                    lines.append(
                        f"{int(i):3d}{int(j):3d}{int(k):3d}{int(l):3d} " + " ".join(tmp)
                    )
                else:
                    lines.append("             " + " ".join(tmp))

        # Hydrogen Bond parameters
        M = metadata["hydrogen bond parameters"]
        n = len(M)

        # How many hydrogen bonds will we have?
        if "reaxff hydrogen bond parameters" not in eex["terms"]:
            indices = []
        else:
            section = eex["terms"]["reaxff hydrogen bond parameters"][0]
            indices = []
            for key in self.ff[section]:
                i, j, k = key
                if i in symbols and j in symbols and k in symbols:
                    indices.append(key)

        line = f"{len(indices):3d}        ! Num hydrogen bonds; "
        tmp = [d["parameter"] for d in M[0:8]]
        line += "; ".join(tmp)
        lines.append(line)
        for g0 in range(8, n, 8):
            g1 = min(g0 + 8, n)
            tmp = [d["parameter"] for d in M[g0:g1]]
            lines.append("           ! " + "; ".join(tmp))

        if "reaxff hydrogen bond parameters" not in eex["terms"]:
            for key in indices:
                P = {}
                for section in eex["terms"]["reaxff hydrogen bond parameters"]:
                    P.update(self.ff[section][key])

                i, j, k = key
                i = symbols.index(i) + 1
                j = symbols.index(j) + 1
                k = symbols.index(k) + 1
                for g0 in range(0, n, 8):
                    g1 = min(g0 + 8, n)
                    tmp = [f"{float(P[k['parameter']]):8.4f}" for k in M[g0:g1]]
                    if g0 == 0:
                        lines.append(
                            f"{int(i):3d}{int(j):3d}{int(k):3d} " + " ".join(tmp)
                        )
                    else:
                        lines.append("          " + " ".join(tmp))

        eex["forcefield"] = "\n".join(lines)

    def eex_reaxff_atomic_parameters(self, eex, configuration):
        """Not used: everything is handled in the general parameters code."""
        pass

    def eex_reaxff_bond_parameters(self, eex, configuration):
        """Not used: everything is handled in the general parameters code."""
        pass

    def eex_reaxff_off_diagonal_parameters(self, eex, configuration):
        """Not used: everything is handled in the general parameters code."""
        pass

    def eex_reaxff_angle_parameters(self, eex, configuration):
        """Not used: everything is handled in the general parameters code."""
        pass

    def eex_reaxff_torsion_parameters(self, eex, configuration):
        """Not used: everything is handled in the general parameters code."""
        pass

    def eex_reaxff_hydrogen_bond_parameters(self, eex, configuration):
        """Not used: everything is handled in the general parameters code."""
        pass

    def _parse_biosym_reaxff_general_parameters(self, data):
        """
        Process general parameters for ReaxFF

        #reaxff_general_parameters ci-reaxff_CH_2018

        !Version      Ref   Parameter       Value  Description
        !---------  -----  ------------  --------  -------------------------------------
        2025.03.21      1   BO_cutoff      0.1     Cutoff for bond order (*100)
        2025.03.21      1     Pboc,1      50       Overcoordination parameter 1
        2025.03.21      1     Pboc,2       9.5469  Overcoordination parameter 2
        2025.03.21      1     Pcoa,2      26.5405  Valency angle conjugation parameter
        ...
        """  # nopep8
        section = data["section"]
        label = data["label"]

        if section not in self.data:
            self.data[section] = {}
        if label in self.data[section]:
            msg = "'{}' already defined in section '{}'".format(label, section)
            logger.error(msg)
            raise RuntimeError(msg)
        self.data[section][label] = data
        gp = self.data[section][label]["parameters"] = {}

        for line in data["lines"]:
            version, reference, parameter, value, description = line.split(maxsplit=4)

            if parameter not in gp:
                gp[parameter] = {}

            V = packaging.version.Version(version)
            if V in gp[parameter]:
                msg = (
                    f"Reax general parameter '{parameter}' defined more than "
                    f"once in section '{section}'!\n\n{line}"
                )
                logger.error(msg)
                raise RuntimeError(msg)
            gp[parameter][V] = {
                "value": value,
                "description": description,
            }

        if not self.keep_lines:
            del data["lines"]


if __name__ == "__main__":
    run()
