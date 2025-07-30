# -*- coding: utf-8 -*-

"""Metadata for describing terms in focefields."""

metadata = {
    "charges": {
        "equation": ["I"],
        "constants": [
            ("Q", "e"),
        ],
        "topology": {
            "type": "atomic charge",
            "n_atoms": 1,
            "symmetry": "none",
            "fill": 0,
            "flip": 0,
        },
    },
    "shell-model": {
        "equation": ["I"],
        "constants": [
            ("Q", "e"),
            ("Y", "e"),
            ("k", "kcal/mol/Å^2"),
        ],
        "topology": {
            "type": "shell model",
            "n_atoms": 1,
            "symmetry": "none",
            "fill": 0,
            "flip": 0,
        },
    },
    "dreiding_atomic_parameters": {
        "equation": [],
        "constants": [
            ("Radius", "Å"),
            ("Theta0", "degree"),
        ],
        "topology": {
            "type": "dreiding atomic parameters",
            "n_atoms": 1,
            "symmetry": "none",
            "fill": 0,
            "flip": 0,
        },
    },
    "bond_increments": {
        "equation": ["delta"],
        "constants": [
            ("deltaij", "e"),
            ("deltaji", "e"),
        ],
        "topology": {
            "type": "bond charge increment",
            "n_atoms": 2,
            "symmetry": "like_bond",
            "fill": 0,
            "flip": 1,
        },
    },
    "quadratic_bond": {
        "equation": ["K2*(R-R0)^2"],
        "constants": [
            ("R0", "Å"),
            ("K2", "kcal/mol/Å^2"),
        ],
        "topology": {
            "type": "bond",
            "n_atoms": 2,
            "symmetry": "like_bond",
            "fill": 0,
            "flip": 0,
        },
    },
    "quartic_bond": {
        "equation": ["K2*(R-R0)^2 + K3*(R-R0)^3 + K4*(R-R0)^4"],
        "constants": [
            ("R0", "Å"),
            ("K2", "kcal/mol/Å^2"),
            ("K3", "kcal/mol/Å^3"),
            ("K4", "kcal/mol/Å^4"),
        ],
        "topology": {
            "type": "bond",
            "n_atoms": 2,
            "symmetry": "like_bond",
            "fill": 0,
            "flip": 0,
        },
    },
    "rigid_bond": {
        "equation": ["R = R0"],
        "constants": [
            ("R0", "Å"),
        ],
        "topology": {
            "type": "bond",
            "n_atoms": 2,
            "symmetry": "like_bond",
            "fill": 0,
            "flip": 0,
        },
    },
    "quadratic_angle": {
        "equation": ["K2*(Theta-Theta0)^2"],
        "constants": [
            ("Theta0", "degree"),
            ("K2", "kcal/mol/radian^2"),
        ],
        "topology": {
            "type": "angle",
            "n_atoms": 3,
            "symmetry": "like_angle",
            "fill": 0,
            "flip": 0,
        },
    },
    "quartic_angle": {
        "equation": [
            "K2*(Theta-Theta0)^2 + K3*(Theta-Theta0)^3" "+ K4*(Theta-Theta0)^4"
        ],
        "constants": [
            ("Theta0", "degree"),
            ("K2", "kcal/mol/radian^2"),
            ("K3", "kcal/mol/radian^3"),
            ("K4", "kcal/mol/radian^4"),
        ],
        "topology": {
            "type": "angle",
            "n_atoms": 3,
            "symmetry": "like_angle",
            "fill": 0,
            "flip": 0,
        },
    },
    "simple_fourier_angle": {
        "equation": ["K*[1-cos(n*Theta)]"],
        "constants": [
            ("K", "kcal/mol"),
            ("n", ""),
        ],
        "topology": {
            "type": "angle",
            "n_atoms": 3,
            "symmetry": "like_angle",
            "fill": 0,
            "flip": 0,
        },
    },
    "tabulated_angle": {
        "constants": [
            ("Eqn", "", str),
            ("K", "kcal/mol", float),
            ("n", "", int),
            ("Rb", "Å", float),
            ("A", "kcal/mol*Å^12", float),
            ("zero-shift", "degree", float),
        ],
        "topology": {
            "type": "angle",
            "n_atoms": 3,
            "symmetry": "like_angle",
            "fill": 0,
            "flip": 0,
        },
    },
    "rigid_angle": {
        "equation": ["Theta = Theta0"],
        "constants": [
            ("Theta0", "degree"),
        ],
        "topology": {
            "type": "angle",
            "n_atoms": 3,
            "symmetry": "like_angle",
            "fill": 0,
            "flip": 0,
        },
    },
    "torsion_1": {
        "equation": ["KPhi * [1 + cos(n*Phi - Phi0)]"],
        "constants": [
            ("KPhi", "kcal/mol"),
            ("n", ""),
            ("Phi0", "degree"),
        ],
        "topology": {
            "type": "torsion",
            "n_atoms": 4,
            "symmetry": "like_torsion",
            "fill": 0,
            "flip": 0,
        },
    },
    "torsion_3": {
        "equation": [
            (
                "V1 * [1 + cos(Phi - Phi0_1)]"
                " + V2 * [1 + cos(2*Phi - Phi0_2)]"
                " + V3 * [1 + cos(3*Phi - Phi0_3)]"
            )
        ],
        "constants": [
            ("V1", "kcal/mol"),
            ("Phi0_1", "degree"),
            ("V2", "kcal/mol"),
            ("Phi0_2", "degree"),
            ("V3", "kcal/mol"),
            ("Phi0_3", "degree"),
        ],
        "topology": {
            "type": "torsion",
            "n_atoms": 4,
            "symmetry": "like_torsion",
            "fill": 0,
            "flip": 0,
        },
    },
    "torsion_opls": {
        "equation": [
            (
                "  1/2 * V1 * [1 + cos(Phi)]"
                "+ 1/2 * V2 * [1 - cos(2*Phi)]"
                "+ 1/2 * V3 * [1 + cos(3*Phi)]"
                "+ 1/2 * V4 * [1 - cos(4*Phi)]"
            )
        ],
        "constants": [
            ("V1", "kcal/mol"),
            ("V2", "kcal/mol"),
            ("V3", "kcal/mol"),
            ("V4", "kcal/mol"),
        ],
        "topology": {
            "type": "torsion",
            "n_atoms": 4,
            "symmetry": "like_torsion",
            "fill": 0,
            "flip": 0,
        },
    },
    "torsion_charmm": {
        "equation": ["K * [1 + cos(n*Phi - d)]"],
        "constants": [
            ("K", "kcal/mol"),
            ("n", ""),
            ("d", "degrees"),
            ("weight", ""),
        ],
        "topology": {
            "type": "torsion",
            "n_atoms": 4,
            "symmetry": "like_torsion",
            "fill": 0,
            "flip": 0,
        },
    },
    "torsion_fourier": {
        "equation": [
            "sum i=1,m {Ki *  [1 + cos(ni*Phi - Phi0i)]}",
        ],
        "constants": [
            ("K", "kcal/mol"),
            ("n", ""),
            ("Phi0", "degree"),
        ],
        "topology": {
            "type": "torsion",
            "n_atoms": 4,
            "symmetry": "like_torsion",
            "fill": 0,
            "flip": 0,
        },
    },
    "wilson_out_of_plane": {
        "equation": ["K*(Chi - Chi0)^2"],
        "constants": [
            ("K", "kcal/mol/radian^2"),
            ("Chi0", "degree"),
        ],
        "topology": {
            "type": "out-of-plane",
            "n_atoms": 4,
            "symmetry": "like_oop",
            "fill": 0,
            "flip": 0,
        },
    },
    "dreiding_out_of_plane": {
        "equation": [
            "1/2*K*[1/sin(Psi0)]**2*[cos(Psi) - cos(Psi0)]**2",
            "K*[1 - cos(Psi)] for Phi0 = 0",
        ],
        "constants": [
            ("K2", "kcal/mol/radian^2"),
            ("Psi0", "degree"),
        ],
        "topology": {
            "type": "out-of-plane",
            "n_atoms": 4,
            "symmetry": "like_oop",
            "fill": 0,
            "flip": 0,
        },
    },
    "improper_opls": {
        "equation": ["1/2 * V2 * [1 - cos(Phi)]"],
        "constants": [
            ("V2", "kcal/mol"),
        ],
        "topology": {
            "type": "out-of-plane",
            "n_atoms": 4,
            "symmetry": "like_improper",
            "fill": 0,
            "flip": 0,
        },
    },
    "improper_harmonic": {
        "equation": ["K2 * (Chi - Chi0)^2"],
        "constants": [
            ("K2", "kcal/mol"),
        ],
        "topology": {
            "type": "out-of-plane",
            "n_atoms": 4,
            "symmetry": "like_improper",
            "fill": 0,
            "flip": 0,
        },
    },
    "nonbond(9-6)": {
        "equation": [
            "eps(ij) [2(r(ij)*/r(ij))**9 - 3(r(ij)*/r(ij))**6]",
            "r(ij) = [(r(i)**6 + r(j)**6))/2]**(1/6)",
            (
                "eps(ij) = 2 * sqrt(eps(i) * eps(j)) * "
                "r(i)^3 * r(j)^3/[r(i)^6 + r(j)^6]"
            ),
        ],
        "constants": [("rmin", "Å"), ("eps", "kcal/mol")],
        "topology": {
            "form": "rmin-eps",
            "type": "pair",
            "subtype": "LJ 6-9",
            "n_atoms": 1,
            "symmetry": "none",
            "fill": 0,
            "flip": 0,
        },
    },
    "nonbond(12-6)": {
        "equation": [
            "E = 4 * eps * [(sigma/r)**12 - (sigma/r)**6]",
            "E = eps * [(rmin/r)**12 - (rmin/r)**6]",
            "E = A/r**12 - B/r**6",
            "rmin = 2**1/6 * sigma ",
            "sigma = rmin / 2**1/6",
            "A = 4 * eps * sigma**12",
            "B = 4 * eps * sigma**6",
            "sigma = (A/B)**1/6",
            "eps = B**2/(4*A)",
        ],
        "constants": [("sigma", "Å"), ("eps", "kcal/mol")],
        "topology": {
            "form": "sigma-eps",
            "type": "pair",
            "subtype": "LJ 12-6",
            "n_atoms": 1,
            "symmetry": "none",
            "fill": 0,
            "flip": 0,
        },
    },
    "buckingham": {
        "equation": ["E = A*exp(r/rho) - C/r**6"],
        "constants": [
            ("A", "kcal/mol"),
            ("rho", "Å"),
            ("C", "kcal/mol*Å**6"),
            ("cutoff", "Å"),
        ],
        "topology": {
            "type": "pair",
            "subtype": "LJ exp-6",
            "n_atoms": 2,
            "symmetry": "like_bond",
            "fill": 0,
            "flip": 0,
        },
    },
    "bond-bond": {
        "equation": ["K*(R-R0)*(R'-R0')"],
        "constants": [("K", "kcal/mol/Å^2")],
        "topology": {
            "type": "bond-bond",
            "n_atoms": 3,
            "symmetry": "like_angle",
            "fill": 0,
            "flip": 0,
        },
    },
    "bond-bond_1_3": {
        "equation": ["K*(R-R0)*(R'-R0')"],
        "constants": [("K", "kcal/mol/Å^2")],
        "topology": {
            "type": "1,3 bond-bond",
            "n_atoms": 4,
            "symmetry": "like_torsion",
            "fill": 0,
            "flip": 0,
        },
    },
    "bond-angle": {
        "equation": ["K*(R-R0)*(Theta-Theta0)"],
        "constants": [
            ("K12", "kcal/mol/Å/radian"),
            ("K23", "kcal/mol/Å/radian"),
        ],
        "topology": {
            "type": "bond-angle",
            "n_atoms": 3,
            "symmetry": "like_angle",
            "fill": 1,
            "flip": 1,
        },
    },
    "angle-angle": {
        "equation": ["K*(Theta-Theta0)*(Theta'-Theta0')"],
        "constants": [("K", "kcal/mol/Å/radian")],
        "topology": {
            "type": "angle-angle",
            "n_atoms": 4,
            "symmetry": "like_angle-angle",
            "fill": 0,
            "flip": 0,
        },
    },
    "end_bond-torsion_3": {
        "equation": [
            (
                "(R_L - R0_L) * (V1_L * [1 + cos(Phi - Phi0_1)]"
                " + V2_L * [1 + cos(2*Phi - Phi0_2)]"
                " + V3_L * [1 + cos(3*Phi - Phi0_3)])"
            ),
            (
                "(R_R - R0_R) * (V1_R * [1 + cos(Phi - Phi0_1)]"
                " + V2_R * [1 + cos(2*Phi - Phi0_2)]"
                " + V3_R * [1 + cos(3*Phi - Phi0_3)])"
            ),
        ],
        "constants": [
            ("V1_L", "kcal/mol"),
            ("V2_L", "kcal/mol"),
            ("V3_L", "kcal/mol"),
            ("V1_R", "kcal/mol"),
            ("V2_R", "kcal/mol"),
            ("V3_R", "kcal/mol"),
        ],
        "topology": {
            "type": "torsion-end bond",
            "n_atoms": 4,
            "symmetry": "like_torsion",
            "fill": 3,
            "flip": 3,
        },
    },
    "middle_bond-torsion_3": {
        "equation": [
            (
                "(R_M - R0_M) * (V1 * [1 + cos(Phi - Phi0_1)]"
                " + V2 * [1 + cos(2*Phi - Phi0_2)]"
                " + V3 * [1 + cos(3*Phi - Phi0_3)])"
            )
        ],
        "constants": [
            ("V1", "kcal/mol"),
            ("V2", "kcal/mol"),
            ("V3", "kcal/mol"),
        ],
        "topology": {
            "type": "torsion-middle bond",
            "n_atoms": 4,
            "symmetry": "like_torsion",
            "fill": 0,
            "flip": 0,
        },
    },
    "angle-torsion_3": {
        "equation": [
            (
                "(Theta_L - Theta0_L)"
                "* (V1_L * [1 + cos(Phi - Phi0_1)]"
                " + V2_L * [1 + cos(2*Phi - Phi0_2)]"
                " + V3_L * [1 + cos(3*Phi - Phi0_3)])"
            ),
            (
                "(Theta_R - Theta0_R)"
                " * (V1_R * [1 + cos(Phi - Phi0_1)]"
                " + V2_R * [1 + cos(2*Phi - Phi0_2)]"
                " + V3_R * [1 + cos(3*Phi - Phi0_3)])"
            ),
        ],
        "constants": [
            ("V1_L", "kcal/mol"),
            ("V2_L", "kcal/mol"),
            ("V3_L", "kcal/mol"),
            ("V1_R", "kcal/mol"),
            ("V2_R", "kcal/mol"),
            ("V3_R", "kcal/mol"),
        ],
        "topology": {
            "type": "torsion-angle",
            "n_atoms": 4,
            "symmetry": "like_torsion",
            "fill": 3,
            "flip": 3,
        },
    },
    "angle-angle-torsion_1": {
        "equation": [
            "K * (Theta_L - Theta0_L) * (Theta_R - Theta0_R) * " "(Phi - Phi0_1)"
        ],
        "constants": [("K", "kcal/mol/degree^2/degree")],
        "topology": {
            "type": "angle-torsion-angle",
            "n_atoms": 4,
            "symmetry": "like_torsion",
            "fill": 0,
            "flip": 0,
        },
    },
    "torsion-torsion_1": {
        "equation": ["K * cos(Phi_L) * cos(Phi_R)"],
        "constants": [("K", "kcal/mol")],
        "topology": {
            "type": "torsion-torsion",
            "n_atoms": 5,
            "symmetry": "like_torsion-torsion",
            "fill": 0,
            "flip": 0,
        },
    },
    "reaxff_general_parameters": {
        "equation": [],
        "constants": [
            ("Radius", "Å"),
            ("Theta0", "degree"),
        ],
        "topology": {
            "type": "reaxff general parameters",
            "n_atoms": 0,
            "symmetry": "none",
            "fill": 0,
            "flip": 0,
        },
    },
}
