# -*- coding: utf-8 -*-

"""Mixin class for handling Dreiding forcefields"""

import logging
from math import sqrt, sin, radians  # noqa: F401
import pprint  # noqa: F401

logger = logging.getLogger(__name__)
# logger.setLevel("DEBUG")


class DreidingMixin:

    def eex_dreiding_atomic_parameters(self, eex, configuration):
        """Get the charges for the structure

        If they do not exists on the structure, they are created
        using the bond increments and saved on the structure"""

        logger.debug("entering eex_dreiding_atomic_parameters")

        # Get the bonds, angles, ...
        self.dreiding_bonds(eex, configuration)
        self.dreiding_angles(eex, configuration)
        self.dreiding_dihedrals(eex, configuration)

    def dreiding_bonds(self, eex, configuration):
        """Get the bonds and parameters for the structure."""

        logger.debug("entering dreiding_bonds")

        types = self.topology["types"]
        bonds = self.topology["bonds"]
        bond_orders = self.topology["bond orders"]
        atomic_parameters = self.ff["dreiding_atomic_parameters"]

        # pprint.pp(atomic_parameters)

        # Add the bonds to the eex
        terms = eex["terms"]
        if "bonds" not in terms:
            terms["bonds"] = []
        if "quadratic_bond" not in terms["bonds"]:
            terms["bonds"].append("quadratic_bond")

        if "bonds" not in eex:
            eex["bonds"] = []
            eex["bond parameters"] = []

        result = eex["bonds"]
        parameters = eex["bond parameters"]

        for i, j in bonds:
            itype = types[i]
            jtype = types[j]
            key, flipped = self.make_canonical("like_bond", (itype, jtype))

            parameters_type = "explicit"
            form = "quadratic_bond"
            real_types = (itype, jtype)

            n = bond_orders[(i, j)]
            if n == 5:
                # Aromatic
                n = 1.5

            R_i = float(atomic_parameters[(itype,)]["Radius"])
            R_j = float(atomic_parameters[(jtype,)]["Radius"])
            R0 = R_i + R_j - 0.01
            K2 = n * 700
            # D = n * 70
            # alpha = sqrt(K2/(2*D))

            parameter_values = {"K2": f"{K2 / 2:.4f}", "R0": f"{R0:.4f}"}

            new_value = (
                form,
                parameter_values,
                (types[i], types[j]),
                parameters_type,
                real_types,
            )

            try:
                index = parameters.index(new_value) + 1
            except ValueError:
                parameters.append(new_value)
                index = len(parameters)
            result.append((i, j, index))
        eex["n_bonds"] = len(result)
        eex["n_bond_types"] = len(parameters)

    def dreiding_angles(self, eex, configuration):
        """Get the angles and parameters for the structure."""

        logger.debug("entering dreiding_angles")

        types = self.topology["types"]
        angles = self.topology["angles"]
        atomic_parameters = self.ff["dreiding_atomic_parameters"]

        # Add the angless to the eex
        terms = eex["terms"]
        if "angle" not in terms:
            terms["angle"] = []
        if "cosine/squared" not in terms["angle"]:
            terms["angle"].append("cosine/squared")
        if "cosine" not in terms["angle"]:
            terms["angle"].append("cosine")

        if "angles" not in eex:
            eex["angles"] = []
            eex["angle parameters"] = []

        result = eex["angles"]
        parameters = eex["angle parameters"]

        for i, j, k in angles:
            itype = types[i]
            jtype = types[j]
            ktype = types[k]
            key, flipped = self.make_canonical("like_angle", (itype, jtype, ktype))

            parameters_type = "explicit"
            real_types = (itype, jtype, ktype)

            theta0 = float(atomic_parameters[(jtype,)]["Theta0"])

            if theta0 == 180:
                form = "cosine"
                K2 = 100.0
                parameter_values = {"K2": f"{K2 / 2:.4f}"}
            else:
                form = "cosine/squared"
                K2 = 100.0 / sin(radians(theta0)) ** 2
                parameter_values = {"K2": f"{K2 / 2:.4f}", "Theta0": f"{theta0:.4f}"}

            new_value = (
                form,
                parameter_values,
                (types[i], types[j], types[k]),
                parameters_type,
                real_types,
            )

            try:
                index = parameters.index(new_value) + 1
            except ValueError:
                parameters.append(new_value)
                index = len(parameters)
            result.append((i, j, k, index))
        eex["n_angles"] = len(result)
        eex["n_angle_types"] = len(parameters)

    def dreiding_dihedrals(self, eex, configuration):
        """Get the dihedrals and parameters for the structure."""

        logger.debug("entering dreiding_dihedrals")

        types = self.topology["types"]
        torsions = self.topology["torsions"]
        bond_orders = self.topology["bond orders"]

        # pprint.pp(atomic_parameters)

        # Add the dihedrals to the eex
        terms = eex["terms"]
        if "torsion" not in terms:
            terms["torsion"] = []
        if "torsion_charmm" not in terms["torsion"]:
            terms["torsion"].append("torsion_charmm")

        if "torsions" not in eex:
            eex["torsions"] = []
            eex["torsion parameters"] = []

        result = eex["torsions"]
        parameters = eex["torsion parameters"]

        for i, j, k, l in torsions:
            itype = types[i]
            jtype = types[j]
            ktype = types[k]
            ltype = types[l]
            key, flipped = self.make_canonical(
                "like_torsion", (itype, jtype, ktype, ltype)
            )

            ihyb = itype[2] if len(itype) > 2 else 0
            jhyb = jtype[2] if len(jtype) > 2 else 0
            khyb = ktype[2] if len(ktype) > 2 else 0
            lhyb = ltype[2] if len(ltype) > 2 else 0
            ihyb = 2 if ihyb == "R" else 0 if ihyb == "_" else int(ihyb)
            jhyb = 2 if jhyb == "R" else 0 if jhyb == "_" else int(jhyb)
            khyb = 2 if khyb == "R" else 0 if khyb == "_" else int(khyb)
            lhyb = 2 if lhyb == "R" else 0 if lhyb == "_" else int(lhyb)

            bond_order = bond_orders[(j, k)]
            if bond_order == 5:
                # Aromatic
                bond_order = 1.5

            parameters_type = "explicit"
            form = "torsion_charmm"
            real_types = (itype, jtype, ktype, ltype)

            # An expert system, as written in the paper:
            # (a) A dihedral single bond involving two sp3 atoms (J,K = X_3)
            if jhyb == 3 and khyb == 3:
                V = 2.0
                n = 3
                phi0 = 180

                # (h) A dihedral single bond involving two sp3 atoms of the oxygen
                #     column (J,K = X.3 of column 16)
                if jtype[0:2] in ("O_", "S_", "Se", "Te") and ktype[0:2] in (
                    "O_",
                    "S_",
                    "Se",
                    "Te",
                ):
                    V = 1.0
                    n = 6
                    phi0 = 90

            # (b) A dihedral single bond involving one sp2 center and one sp3center
            #     e.g., the C-C bond in acetic acid [CH3C(0)^0H)]
            #     (J= X.2, X.R; K = X.3)
            elif jhyb == 3 and khyb == 2 and bond_order == 1:
                V = 1.0
                n = 6
                phi0 = 0.0

                # (i) For dihedral bonds involving an sp3 atom of the oxygen column with
                #     an sp2 or resonant atom of another column, the pair and the
                #     oxygen-like prefers to overlap the orbitals of the sp2 atom,
                #     leading to a planar configuration
                #     (J = X.3 of column16, K = X.2,X.R)
                if (jtype[0:2] in ("O_", "S_", "Se", "Te") and khyb == 2) or (
                    ktype[0:2] in ("O_", "S_", "Se", "Te") and jhyb == 2
                ):
                    V = 2.0
                    n = 2
                    phi0 = 180

                # (j) An exception to the above principles is made for the case of a
                #  dihedral single bond involving one sp2 atom (J = X.2, X.R) and one
                #  sp3 atom (K = X.3) (for example, the single bond of propene). The
                #   problem here is that for a system such as propene there is a 3-fold
                #   barrier with the sp3 center eclipsing the double bond, whereas for
                #   the CC bond, say, of acetate anion (CH3-C-00"), the barrier should
                #   have 6-fold character. To accommodate this we use (15) unless I is
                #   not an sp2 center (X.2 or X.R); otherwise we use the following
                #   I ^ X.2, X.R; J = X.2,X.R; K = X.3
                if (jhyb == 2 and ihyb != 2) or (khyb == 2 and lhyb != 2):
                    V = 2.0
                    n = 3
                    phi0 = 180

            # (c) A dihedral double bond involving two sp2 atoms (J,K = X.2)
            elif jhyb == 2 and khyb == 2 and bond_order == 2:
                V = 45.0
                n = 2
                phi0 = 180

            # (d) A dihedral resonance bond (bond order = 1.5) involving
            #     two resonant atoms (J,K = X.R)
            # NB. This is an issue for aromatic rings with single and double bonds.
            elif jhyb == 2 and khyb == 2 and bond_order == 1.5:
                V = 25.0
                n = 2
                phi0 = 180

            # (e) A dihedral single bond involving two sp2 or resonant atoms
            #     [e.g., the middle bond of butadiene] {J,K = X.2, X.R)
            elif jhyb == 2 and khyb == 2 and bond_order == 1:
                V = 5
                n = 2
                phi0 = 180

                # (f) An exception to (e) is that for an exocyclic dihedral single bond
                #     involving two aromatic atoms [e.g., a phenyl ester or the bond
                #     between the two rings of biphenyl] (J,K = X.R)
                # NB. This is an issue for aromatic rings with single and double bonds.
                if (len(jtype) > 2 and jtype[2] == "R") and (
                    len(ktype) > 2 and ktype[2] == "R"
                ):
                    V = 10.0
            else:
                # linear bond, like acetylene, so no torsion
                continue

            # Normalize by the number of dihedrals sharing the central bond
            n_bonds = self.topology["bonds_from_atom"]
            n_j = len(n_bonds[j])
            n_k = len(n_bonds[k])
            V /= n_j * n_k

            # Need to multiply by n and phase of 180 for LAMMPS/charmm
            phi0 = (n * phi0 + 180) % 360
            parameter_values = {
                "n": n,
                "Phi0": int(phi0),
                "K": f"{V / 2:.4f}",
                "weight": 0.0,
            }

            new_value = (
                form,
                parameter_values,
                (types[i], types[j], types[k], types[l]),
                parameters_type,
                real_types,
            )

            try:
                index = parameters.index(new_value) + 1
            except ValueError:
                parameters.append(new_value)
                index = len(parameters)
            result.append((i, j, k, l, index))
        eex["n_torsions"] = len(result)
        eex["n_torsion_types"] = len(parameters)

    def dreiding_hydrogen_bonds(self, eex, configuration):
        """Rework the nonbonds and add the hydrogen bonds, if needed."""

        logger.debug("entering dreiding_bonds")

        types = self.topology["types"]

        # If there are no possible hydrogen bonds, leave the nonbonds as is
        if "H__HB" not in types:
            return

        # Otherwise we need to create the full triangle of non bonds and add the
        # hydrogen bond potentials for pairs that can have hydrogen bonds

        # What atom types are the H__HB bonded to?
        atom_types = self.topology["types"]
        bonds = self.topology["bonds"]
        donors = set()
        for i, j in bonds:
            itype = atom_types[i]
            jtype = atom_types[j]
            if itype == "H__HB":
                donors.add(jtype)
            elif jtype == "H__HB":
                donors.add(itype)
        acceptors = set()
        for itype in ("N_3", "O_3", "F_"):
            if itype in atom_types:
                acceptors.add(itype)

        eex["nonbonds"] = []
        parameters = eex["nonbond parameters"] = []

        types = eex["atom types"]
        h_index = types.index("H__HB") + 1
        for i, itype in enumerate(types, start=1):
            (
                i_parameters_type,
                i_real_types,
                i_form,
                i_parameter_values,
            ) = self.nonbond_parameters(itype, form="nonbond(12-6)")
            i_rmin = i_parameter_values["sigma"]
            i_eps = i_parameter_values["eps"]
            for j, jtype in enumerate(types[0:i], start=1):
                (
                    j_parameters_type,
                    j_real_types,
                    j_form,
                    j_parameter_values,
                ) = self.nonbond_parameters(itype, form="nonbond(12-6)")
                j_rmin = j_parameter_values["sigma"]
                j_eps = j_parameter_values["eps"]
                parameter_values = {
                    "sigma": sqrt(i_rmin * j_rmin),
                    "eps": sqrt(i_eps * j_eps),
                }
                new_value = (
                    i_form,
                    parameter_values,
                    (j, i),
                    (jtype, itype),
                    (j_real_types[0], i_real_types[0]),
                )
                parameters.append(new_value)

                if itype in donors or jtype in donors:
                    # Is there a possible hydrogen bond?
                    if jtype in donors and itype in acceptors:
                        new_value = (
                            "hbond/dreiding/lj",
                            {
                                "h_index": h_index,
                                "donor flag": "i",
                                "eps": 9.0,
                                "sigma": 2.75,
                                "exponent": 4,
                            },
                            (j, i),
                            (jtype, itype),
                            (jtype, itype),
                        )
                    elif jtype in acceptors and itype in donors:
                        new_value = (
                            "hbond/dreiding/lj",
                            {
                                "h_index": h_index,
                                "donor flag": "j",
                                "eps": 9.0,
                                "sigma": 2.75,
                                "exponent": 4,
                            },
                            (j, i),
                            (jtype, itype),
                            (jtype, itype),
                        )
                    parameters.append(new_value)
