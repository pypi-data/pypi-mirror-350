# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)


class EEX_Mixin:
    """A mixin class for handling the energy expression (eex)."""

    def eex_atomic_charge(self, eex, configuration):
        """Handle charges."""
        self.eex_bond_charge_increment(eex, configuration)

    def eex_charge(self, eex, configuration):
        """Do nothing routine since charges are handled by the increments."""
        pass

    def eex_bond_charge_increment(self, eex, configuration):
        """Get the charges for the structure

        If they do not exist on the structure, they are created
        using the bond increments and saved on the structure"""

        logger.debug("entering eex_increment")

        # terms = self.terms
        # ff_name = self.current_forcefield
        # atoms = configuration.atoms
        # if "atomic charge" in terms and "shell model" in terms:
        #     logger.debug("Getting the charges for the system")

        #     # Atom types
        #     key = f"atom_types_{ff_name}"
        #     atom_types = atoms.get_column(key)

        #     total_charge = configuration.charge
        #     n_atoms = configuration.n_atoms
        #     eex["charges"] = charges = [None] * n_atoms
        #     total_q = 0.0
        #     if "shell model" in terms:
        #         # Use charges from shell model by preference.
        #         shell_q = []
        #         for i, itype in enumerate(atom_types):
        #             tmp = self.shell_model(itype)
        #             if tmp is None:
        #                 # Fall back to charges
        #                 parameters = self.charges(itype)[3]
        #                 q = float(parameters["Q"])
        #                 charges[i] = q
        #                 total_q += q
        #             else:
        #                 parameters = tmp[3]
        #                 q = float(parameters["Q"])
        #                 y = float(parameters["Y"])
        #                 charges[i] = q - y
        #                 shell_q.append(y)
        #                 total_q += q
        #         charges.extend(shell_q)
        #     else:
        #         # First see if there are any templates
        #         molecule = configuration.to_RDKMol()
        #         fragments = self.get_fragments()
        #         for smiles, data in fragments.items():
        #             if "charges" not in data:
        #                 continue

        #             smarts = data["SMARTS"]
        #             pattern = rdkit.Chem.MolFromSmarts(smarts)
        #             matches = molecule.GetSubstructMatches(
        #                 pattern, maxMatches=6 * n_atoms
        #             )
        #             for match in matches:
        #                 for charge, atom in zip(data["charges"], match):
        #                     # Check if this has been assigned by another fragment
        #                     if charges[atom] is not None:
        #                         if charge != charges[atom]:
        #                             msg = (
        #                                 f"Error in fragment charges for atom {atom} "
        #                                 f"already has charge:\n{charges[atom]}\n"
        #                                 f"New assignment: {charge}"
        #                             )
        #                             logger.error(msg)
        #                             raise ForcefieldChargeError(msg)
        #                     charges[atom] = charge
        #         # Use the increments and charges for any left
        #         for i, itype in enumerate(atom_types):
        #             if charges[i] is None:
        #                 parameters = self.charges(itype)[3]
        #                 charges[i] = float(parameters["Q"])
        #             total_q += charges[i]
        #     if abs(total_q - total_charge) > 0.001:
        #         delta = (total_q - total_charge) / len(charges)
        #         charges = [q - delta for q in charges]
        #         logger.warning(
        #             f"The total charge from the forcefield, {total_q:3f}, does not "
        #             f"match the formal charge, {total_charge}."
        #             f"\nAdjusted each atom's charge by {-delta:.3f} to compensate."
        #         )
        #     logger.debug("Charges from charges:\n" + pprint.pformat(charges))
        # else:
        #     key = f"charges_{ff_name}"
        #     if key in atoms:
        #         eex["charges"] = [*atoms[key]]
        #     else:
        #         raise RuntimeError("No charges on system!")

        logger.debug("leaving eex_increment")

    def eex_atoms(self, eex, configuration):
        """List the atoms into the energy expression.

        Note that if using the shell model, an extra "atom" is added for the shell.
        At the moment the mass is split 90:10 between core and shell.
        The shells are appended at the end of the atoms so bonds, etc. work using
        the atom indices.
        """
        atoms = configuration.atoms
        n_atoms = configuration.n_atoms
        coordinates = atoms.get_coordinates(fractionals=False)
        if self.ff_form == "reaxff":
            types = atoms.symbols
        else:
            key = f"atom_types_{self.current_forcefield}"
            types = atoms.get_column(key)

        result = eex["atoms"] = []
        atom_types = eex["atom types"] = []
        masses = eex["masses"] = []

        shells = []
        eex["shell_of_atom"] = shell_of_atom = []

        for itype, xyz in zip(types, coordinates):
            x, y, z = xyz
            if self.shell_model(itype) is None:
                if itype in atom_types:
                    index = atom_types.index(itype) + 1
                else:
                    atom_types.append(itype)
                    index = len(atom_types)
                    masses.append((self.mass(itype), itype))
                result.append((x, y, z, index))
                shell_of_atom.append(None)
            else:
                if itype in atom_types:
                    # core
                    index = atom_types.index("core_" + itype) + 1
                    result.append((x, y, z, index))
                    # shell
                    index = atom_types.index(itype) + 1
                    shell_of_atom.append(len(shells) + n_atoms)
                    shells.append((x, y, z, index))
                else:
                    # core
                    atom_types.append("core_" + itype)
                    index = len(atom_types)
                    masses.append((0.9 * float(self.mass(itype)), "core_" + itype))
                    result.append((x, y, z, index))
                    # shell
                    atom_types.append(itype)
                    index = len(atom_types)
                    masses.append((0.1 * float(self.mass(itype)), "shell_" + itype))
                    shell_of_atom.append(len(shells) + n_atoms)
                    shells.append((x, y, z, index))

        if len(shells) > 0:
            result.extend(shells)

        eex["n_atoms"] = n_atoms = len(result)
        eex["n_atom_types"] = len(atom_types)

        # molecule for each atom and shell (if any)
        molecule = eex["molecule"] = [1] * n_atoms
        molecules = configuration.find_molecules(as_indices=True)
        for molecule_id, atoms in enumerate(molecules):
            for atom in atoms:
                molecule[atom] = molecule_id
                if shell_of_atom[atom] is not None:
                    molecule[shell_of_atom[atom]] = molecule_id

    def eex_pair(self, eex, configuration):
        """Create the pair (non-bond) portion of the energy expression"""
        logger.debug("In eex_pair")
        types = self.topology["types"]

        found = False
        for pair_type in ("nonbond(12-6)", "nonbond(9-6)", "buckingham"):
            if pair_type in self.ff["functional_forms"]:
                found = True
                break
        if not found:
            raise RuntimeError("Error finding pair_type in eex_pair")

        result = eex["nonbonds"] = []
        parameters = eex["nonbond parameters"] = []
        if pair_type == "buckingham":
            types = eex["atom types"]
            for i, itype in enumerate(types):
                if itype[0:5] == "core_":
                    itype = "core"
                for j, jtype in enumerate(types[0 : i + 1]):
                    if jtype[0:5] == "core_":
                        jtype = "core"
                    # print(f"{i}-{j} {itype} - {jtype} ##")
                    (
                        parameters_type,
                        real_types,
                        form,
                        parameter_values,
                    ) = self.nonbond_parameters(itype, jtype, form=pair_type)
                    new_value = (
                        form,
                        parameter_values,
                        (itype, jtype),
                        parameters_type,
                        real_types,
                    )
                    index = None
                    # print(f"{itype}-{jtype} --> {new_value}")
                    for value, count in zip(parameters, range(1, len(parameters) + 1)):
                        # print(f"\t{value}")
                        if self.eex_compare_values(value, new_value):
                            index = count
                            break
                    # if index is None:
                    parameters.append(new_value)
                    index = len(parameters)
                    # print(f"Added {new_value} as {index}")
                    result.append(index)
        else:
            for itype in types[1:]:
                if itype[0:5] == "core_":
                    itype = "core"
                (
                    parameters_type,
                    real_types,
                    form,
                    parameter_values,
                ) = self.nonbond_parameters(itype, form=pair_type)
                new_value = (
                    form,
                    parameter_values,
                    (itype,),
                    parameters_type,
                    real_types,
                )
                index = None
                for value, count in zip(parameters, range(1, len(parameters) + 1)):
                    if self.eex_compare_values(value, new_value):
                        index = count
                        break
                if index is None:
                    parameters.append(new_value)
                    index = len(parameters)
                result.append(index)
        eex["n_nonbonds"] = len(result)
        eex["n_nonbond_types"] = len(parameters)

    def eex_shell_model(self, eex, configuration):
        """Create the shell model portion of the energy expression"""
        types = self.topology["types"]

        if "bonds" not in eex:
            eex["bonds"] = []
            eex["bond parameters"] = []
        result = eex["bonds"]
        parameters = eex["bond parameters"]

        key = f"atom_types_{self.current_forcefield}"
        types = configuration.atoms.get_column(key)
        shell_of_atom = eex["shell_of_atom"]
        n_atoms = configuration.n_atoms

        for atom_no, shell_no, itype in zip(range(n_atoms), shell_of_atom, types):
            if shell_no is not None:
                parameters_type, real_types, form, parameter_values = self.shell_model(
                    itype
                )
                real_type = real_types[0]
                new_value = (
                    form,
                    {"R0": 0.0, "K2": parameter_values["k"]},
                    ("core_" + itype, itype),
                    parameters_type,
                    ("core_" + real_type, real_type),
                )
                index = None
                for value, count in zip(parameters, range(1, len(parameters) + 1)):
                    if self.eex_compare_values(value, new_value):
                        index = count
                        break
                if index is None:
                    parameters.append(new_value)
                    index = len(parameters)
                result.append((atom_no + 1, shell_no + 1, index))

        eex["n_bonds"] = len(result)
        eex["n_bond_types"] = len(parameters)

    def eex_bond(self, eex, configuration):
        """Create the bond portion of the energy expression"""
        types = self.topology["types"]
        bonds = self.topology["bonds"]

        if "bonds" not in eex:
            eex["bonds"] = []
            eex["bond parameters"] = []
        result = eex["bonds"]
        parameters = eex["bond parameters"]
        for i, j in bonds:
            parameters_type, real_types, form, parameter_values = self.bond_parameters(
                types[i], types[j]
            )
            new_value = (
                form,
                parameter_values,
                (types[i], types[j]),
                parameters_type,
                real_types,
            )
            index = None
            for value, count in zip(parameters, range(1, len(parameters) + 1)):
                if self.eex_compare_values(value, new_value):
                    index = count
                    break
            if index is None:
                parameters.append(new_value)
                index = len(parameters)
            result.append((i, j, index))
        eex["n_bonds"] = len(result)
        eex["n_bond_types"] = len(parameters)

    def eex_angle(self, eex, configuration):
        """Create the angle portion of the energy expression"""
        types = self.topology["types"]
        angles = self.topology["angles"]

        result = eex["angles"] = []
        parameters = eex["angle parameters"] = []
        for i, j, k in angles:
            parameters_type, real_types, form, parameter_values = self.angle_parameters(
                types[i], types[j], types[k]
            )
            new_value = (
                form,
                parameter_values,
                (types[i], types[j], types[k]),
                parameters_type,
                real_types,
            )
            index = None
            for count, value in enumerate(parameters, start=1):
                if self.eex_compare_values(value, new_value):
                    index = count
                    break
            if index is None:
                parameters.append(new_value)
                index = len(parameters)
            result.append((i, j, k, index))
        eex["n_angles"] = len(result)
        eex["n_angle_types"] = len(parameters)

    def eex_torsion(self, eex, configuration):
        """Create the torsion portion of the energy expression"""
        types = self.topology["types"]
        torsions = self.topology["torsions"]

        result = eex["torsions"] = []
        parameters = eex["torsion parameters"] = []
        for i, j, k, l in torsions:
            (
                parameters_type,
                real_types,
                form,
                parameter_values,
            ) = self.torsion_parameters(types[i], types[j], types[k], types[l])
            new_value = (
                form,
                parameter_values,
                (types[i], types[j], types[k], types[l]),
                parameters_type,
                real_types,
            )
            index = None
            for value, count in zip(parameters, range(1, len(parameters) + 1)):
                if self.eex_compare_values(value, new_value):
                    index = count
                    break
            if index is None:
                parameters.append(new_value)
                index = len(parameters)
            result.append((i, j, k, l, index))
        eex["n_torsions"] = len(result)
        eex["n_torsion_types"] = len(parameters)

    def eex_out_of_plane(self, eex, configuration):
        """Create the out-of-plane portion of the energy expression"""
        types = self.topology["types"]
        oops = self.topology["oops"]

        result = eex["oops"] = []
        parameters = eex["oop parameters"] = []
        for i, j, k, l in oops:
            parameters_type, real_types, form, parameter_values = self.oop_parameters(
                types[i], types[j], types[k], types[l], zero=True
            )

            if form == "dreiding_out_of_plane" and parameters_type == "zeroed":
                continue

            new_value = (
                form,
                parameter_values,
                (types[i], types[j], types[k], types[l]),
                parameters_type,
                real_types,
            )
            index = None
            for value, count in zip(parameters, range(1, len(parameters) + 1)):
                if self.eex_compare_values(value, new_value):
                    index = count
                    break
            if index is None:
                parameters.append(new_value)
                index = len(parameters)
            result.append((i, j, k, l, index))
        eex["n_oops"] = len(result)
        eex["n_oop_types"] = len(parameters)

    def eex_bond_bond(self, eex, configuration):
        """Create the bond-bond portion of the energy expression"""
        types = self.topology["types"]
        angles = self.topology["angles"]

        result = eex["bond-bond"] = []
        parameters = eex["bond-bond parameters"] = []
        for i, j, k in angles:
            (
                parameters_type,
                real_types,
                form,
                parameter_values,
            ) = self.bond_bond_parameters(types[i], types[j], types[k], zero=True)
            new_value = (
                form,
                parameter_values,
                (types[i], types[j], types[k]),
                parameters_type,
                real_types,
            )
            index = None
            for value, count in zip(parameters, range(1, len(parameters) + 1)):
                if self.eex_compare_values(value, new_value):
                    index = count
                    break
            if index is None:
                parameters.append(new_value)
                index = len(parameters)
            result.append((i, j, k, index))
        eex["n_bond-bond"] = len(result)
        eex["n_bond-bond_types"] = len(parameters)

    def eex_bond_angle(self, eex, configuration):
        """Create the bond-angle portion of the energy expression"""
        types = self.topology["types"]
        angles = self.topology["angles"]

        result = eex["bond-angle"] = []
        parameters = eex["bond-angle parameters"] = []
        for i, j, k in angles:
            (
                parameters_type,
                real_types,
                form,
                parameter_values,
            ) = self.bond_angle_parameters(types[i], types[j], types[k], zero=True)
            new_value = (
                form,
                parameter_values,
                (types[i], types[j], types[k]),
                parameters_type,
                real_types,
            )
            index = None
            for value, count in zip(parameters, range(1, len(parameters) + 1)):
                if self.eex_compare_values(value, new_value):
                    index = count
                    break
            if index is None:
                parameters.append(new_value)
                index = len(parameters)
            result.append((i, j, k, index))
        eex["n_bond-angle"] = len(result)
        eex["n_bond-angle_types"] = len(parameters)

    def eex_torsion_middle_bond(self, eex, configuration):
        """Create the middle_bond-torsion portion of the energy expression"""
        types = self.topology["types"]
        torsions = self.topology["torsions"]

        result = eex["middle_bond-torsion_3"] = []
        parameters = eex["middle_bond-torsion_3 parameters"] = []
        for i, j, k, l in torsions:
            (
                parameters_type,
                real_types,
                form,
                parameter_values,
            ) = self.middle_bond_torsion_3_parameters(
                types[i], types[j], types[k], types[l], zero=True
            )
            new_value = (
                form,
                parameter_values,
                (types[i], types[j], types[k], types[l]),
                parameters_type,
                real_types,
            )
            index = None
            for value, count in zip(parameters, range(1, len(parameters) + 1)):
                if self.eex_compare_values(value, new_value):
                    index = count
                    break
            if index is None:
                parameters.append(new_value)
                index = len(parameters)
            result.append((i, j, k, l, index))
        eex["n_middle_bond-torsion_3"] = len(result)
        eex["n_middle_bond-torsion_3_types"] = len(parameters)

    def eex_torsion_end_bond(self, eex, configuration):
        """Create the end_bond-torsion portion of the energy expression"""
        types = self.topology["types"]
        torsions = self.topology["torsions"]

        result = eex["end_bond-torsion_3"] = []
        parameters = eex["end_bond-torsion_3 parameters"] = []
        for i, j, k, l in torsions:
            (
                parameters_type,
                real_types,
                form,
                parameter_values,
            ) = self.end_bond_torsion_3_parameters(
                types[i], types[j], types[k], types[l], zero=True
            )
            new_value = (
                form,
                parameter_values,
                (types[i], types[j], types[k], types[l]),
                parameters_type,
                real_types,
            )
            index = None
            for value, count in zip(parameters, range(1, len(parameters) + 1)):
                if self.eex_compare_values(value, new_value):
                    index = count
                    break
            if index is None:
                parameters.append(new_value)
                index = len(parameters)
            result.append((i, j, k, l, index))
        eex["n_end_bond-torsion_3"] = len(result)
        eex["n_end_bond-torsion_3_types"] = len(parameters)

    def eex_torsion_angle(self, eex, configuration):
        """Create the angle-torsion portion of the energy expression"""
        types = self.topology["types"]
        torsions = self.topology["torsions"]

        result = eex["angle-torsion_3"] = []
        parameters = eex["angle-torsion_3 parameters"] = []
        for i, j, k, l in torsions:
            (
                parameters_type,
                real_types,
                form,
                parameter_values,
            ) = self.angle_torsion_3_parameters(
                types[i], types[j], types[k], types[l], zero=True
            )
            new_value = (
                form,
                parameter_values,
                (types[i], types[j], types[k], types[l]),
                parameters_type,
                real_types,
            )
            index = None
            for value, count in zip(parameters, range(1, len(parameters) + 1)):
                if self.eex_compare_values(value, new_value):
                    index = count
                    break
            if index is None:
                parameters.append(new_value)
                index = len(parameters)
            result.append((i, j, k, l, index))
        eex["n_angle-torsion_3"] = len(result)
        eex["n_angle-torsion_3_types"] = len(parameters)

    def eex_angle_torsion_angle(self, eex, configuration):
        """Create the angle-angle-torsion portion of the energy expression"""
        types = self.topology["types"]
        torsions = self.topology["torsions"]

        result = eex["angle-angle-torsion_1"] = []
        parameters = eex["angle-angle-torsion_1 parameters"] = []
        for i, j, k, l in torsions:
            (
                parameters_type,
                real_types,
                form,
                parameter_values,
            ) = self.angle_angle_torsion_1_parameters(
                types[i], types[j], types[k], types[l], zero=True
            )
            new_value = (
                form,
                parameter_values,
                (types[i], types[j], types[k], types[l]),
                parameters_type,
                real_types,
            )
            index = None
            for value, count in zip(parameters, range(1, len(parameters) + 1)):
                if self.eex_compare_values(value, new_value):
                    index = count
                    break
            if index is None:
                parameters.append(new_value)
                index = len(parameters)
            result.append((i, j, k, l, index))
        eex["n_angle-angle-torsion_1"] = len(result)
        eex["n_angle-angle-torsion_1_types"] = len(parameters)

    def eex_1_3_bond_bond(self, eex, configuration):
        """Create the 1,3 bond-bond portion of the energy expression"""
        types = self.topology["types"]
        torsions = self.topology["torsions"]

        result = eex["bond-bond_1_3"] = []
        parameters = eex["bond-bond_1_3 parameters"] = []
        for i, j, k, l in torsions:
            (
                parameters_type,
                real_types,
                form,
                parameter_values,
            ) = self.bond_bond_1_3_parameters(
                types[i], types[j], types[k], types[l], zero=True
            )
            new_value = (
                form,
                parameter_values,
                (types[i], types[j], types[k], types[l]),
                parameters_type,
                real_types,
            )
            index = None
            for value, count in zip(parameters, range(1, len(parameters) + 1)):
                if self.eex_compare_values(value, new_value):
                    index = count
                    break
            if index is None:
                parameters.append(new_value)
                index = len(parameters)
            result.append((i, j, k, l, index))
        eex["n_bond-bond_1_3"] = len(result)
        eex["n_bond-bond_1_3_types"] = len(parameters)

    def eex_angle_angle(self, eex, configuration):
        """Create the angle-angle portion of the energy expression

        j is the vertex atom of the angles. For the angle-angle parameters
        the bond j-k is the common bond, i.e. the angles are i-j-k and j-k l
        """
        types = self.topology["types"]
        oops = self.topology["oops"]

        result = eex["angle-angle"] = []
        parameters = eex["angle-angle parameters"] = []
        for i, j, k, l in oops:
            (
                parameters_type,
                real_types,
                form,
                parameter_values,
            ) = self.angle_angle_parameters(
                types[i], types[j], types[k], types[l], zero=True
            )
            K1 = parameter_values["K"]
            Theta10 = parameter_values["Theta10"]
            Theta30 = parameter_values["Theta20"]
            tmp = self.angle_angle_parameters(
                types[k], types[j], types[i], types[l], zero=True
            )[3]
            K2 = tmp["K"]
            Theta20 = tmp["Theta20"]
            tmp = self.angle_angle_parameters(
                types[i], types[j], types[l], types[k], zero=True
            )[3]
            K3 = tmp["K"]
            new_value = (
                form,
                {
                    "K1": K1,
                    "K2": K2,
                    "K3": K3,
                    "Theta10": Theta10,
                    "Theta20": Theta20,
                    "Theta30": Theta30,
                },
                (types[i], types[j], types[k], types[l]),
                parameters_type,
                real_types,
            )
            index = None
            for value, count in zip(parameters, range(1, len(parameters) + 1)):
                if self.eex_compare_values(value, new_value):
                    index = count
                    break
            if index is None:
                parameters.append(new_value)
                index = len(parameters)
            result.append((i, j, k, l, index))
        eex["n_angle-angle"] = len(result)
        eex["n_angle-angle_types"] = len(parameters)

    def eex_compare_values(self, old, new):
        """Compare parameters values to see if they are the same."""
        return old[0] == new[0] and old[1] == new[1] and old[4] == new[4]
