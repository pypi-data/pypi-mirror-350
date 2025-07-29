# -*- coding: utf-8 -*-

"""Main class for handling forcefields"""

import logging

import rdkit
import rdkit.Chem
import rdkit.Chem.Draw
import rdkit.Chem.AllChem

logger = logging.getLogger(__name__)
# logger.setLevel("DEBUG")


class ForcefieldAssignmentError(Exception):
    """The forcefield could not be assigned successfully."""

    def __init__(self, message="The atom-types could not be assigned."):
        super().__init__(message)


class FFAssigner(object):
    def __init__(self, forcefield):
        """Handle the assignment of the forcefield to the structure

        This class is closely related to the Forcefield class, but
        separated from it due to the dependencies it carries along,
        coupled with the fact that it is not needed in some
        computations where the forcefield itself is.
        """

        self.forcefield = forcefield

    def assign(self, configuration, picture=False):
        """Assign the atom types to the structure using SMARTS templates"""
        if self.forcefield.ff_form in ("reaxff",):
            # Nothing to do.
            return

        molecule = configuration.to_RDKMol()

        n_atoms = configuration.n_atoms

        atom_types = ["?"] * n_atoms

        # First try the fragments, if any
        fragments = self.forcefield.get_fragments()
        for smiles, data in fragments.items():
            smarts = data["SMARTS"]

            pattern = rdkit.Chem.MolFromSmarts(smarts)

            matches = molecule.GetSubstructMatches(pattern, maxMatches=6 * n_atoms)
            logger.debug(smiles + ": ")
            if len(matches) > 0:
                for match in matches:
                    for _type, atom in zip(data["atom types"], match):
                        # Check if this has already been assigned to another fragment
                        if atom_types[atom] != "?":
                            key1 = atom_types[atom].split("_")[0]
                            key2 = _type.split("_")[0]
                            if key2 != key1:
                                self.draw_atom_types(
                                    molecule,
                                    atom_types,
                                    filename="duplicate_atom_types.png",
                                )
                                msg = (
                                    f"Error in fragment atom typing: atom {atom} "
                                    f"already typed:\n{atom_types[atom]}\n"
                                    f"New assignment: {_type}"
                                )
                                logger.error(msg)
                                raise ForcefieldAssignmentError(msg)
                        atom_types[atom] = _type

        # Fragments have priority, so don't change their assignments
        assigned = [type_ != "?" for type_ in atom_types]

        # And now the templates for the atom_types
        templates = self.forcefield.get_templates()
        for atom_type in templates:
            template = templates[atom_type]
            for smarts in template["smarts"]:
                pattern = rdkit.Chem.MolFromSmarts(smarts)

                ind_map = {}
                for atom in pattern.GetAtoms():
                    map_num = atom.GetAtomMapNum()
                    if map_num:
                        ind_map[map_num - 1] = atom.GetIdx()
                map_list = [ind_map[x] for x in sorted(ind_map)]

                matches = molecule.GetSubstructMatches(pattern, maxMatches=6 * n_atoms)
                logger.debug(atom_type + ": ")
                if len(matches) > 0:
                    for match in matches:
                        atom_ids = [match[x] for x in map_list]
                        for x in atom_ids:
                            if not assigned[x]:
                                atom_types[x] = atom_type
                        tmp = [str(x) for x in atom_ids]
                        logger.debug("\t" + ", ".join(tmp))

        # Create a picture with the atom types if requested
        if picture:
            self.draw_atom_types(molecule, atom_types)

        i = 0
        untyped = []
        for atom, atom_type in zip(molecule.GetAtoms(), atom_types):
            if atom_type == "?":
                untyped.append(i)
            logger.debug("{}: {}".format(atom.GetSymbol(), atom_type))
            i += 1

        if len(untyped) > 0:
            msg = (
                "The forcefield does not have atom types for"
                " the molecule!. See missing_atom_types.png"
                " for more detail."
            )
            logger.error(msg)
            self.draw_atom_types(
                molecule,
                atom_types,
                filename="missing_atom_types.png",
                highlight_atoms=untyped,
            )
            raise ForcefieldAssignmentError(msg)
        else:
            logger.info("The molecule was successfully atom-typed")

        return atom_types

    def draw_atom_types(
        self,
        molecule,
        atom_types,
        legend=None,
        filename="atom_types.png",
        highlight_atoms=None,
    ):
        """Create a picture of the molecule labeled by atom types.

        Parameters
        ----------
        molecule : rdkit.molecule
            The molecule as an RDKit molecule.
        atom_types : [str]
            The labels for the atom types
        legend : str
            The legend for the picture. Defaults to "Atom types for ff_file:ffname"
        filename : str or pathlib.Path
            The file to write the picture to.
        highlight_atoms : [int]
            The atoms to highlight
        """
        if legend is None:
            legend = (
                f"Atom Types for {self.forcefield.filename}:"
                f"{self.forcefield.current_forcefield}"
            )

        for atom, atom_type in zip(molecule.GetAtoms(), atom_types):
            atom.SetProp("atomNote", atom_type)
        rdkit.Chem.AllChem.Compute2DCoords(molecule)
        rdkit.Chem.rdDepictor.StraightenDepiction(molecule)

        d2d = rdkit.Chem.Draw.MolDraw2DCairo(1000, 1000)
        dopts = d2d.drawOptions()
        dopts.addAtomIndices = True
        dopts.legendFontSize = 30

        d2d.DrawMolecule(molecule, legend=legend, highlightAtoms=highlight_atoms)
        d2d.FinishDrawing()
        d2d.WriteDrawingText(filename)
