# -*- coding: utf-8 -*-

# Don't we need some versioning function in the sort? (about line 1200)

"""Main class for handling forcefields"""

from copy import deepcopy
from enum import Enum
import json
import logging
import os.path
import packaging.version
import pprint  # noqa: F401

import rdkit.Chem

import seamm_util
from seamm_util import Q_

from .dreiding import DreidingMixin
from .eex import EEX_Mixin
from .ff_assigner import FFAssigner
from .metadata import metadata
from .reaxff import ReaxFFMixin

logger = logging.getLogger(__name__)
# logger.setLevel("DEBUG")


class NonbondForms(Enum):
    SIGMA_EPS = "sigma-eps"
    RMIN_EPS = "rmin-eps"
    A_B = "A-B"
    AR_BR = "A/r-B/r"


two_raised_to_one_sixth = 2 ** (1 / 6)


class ForcefieldChargeError(Exception):
    """The charges were not assigned successfully."""

    def __init__(self, message="The charges could not be assigned."):
        super().__init__(message)


class Forcefield(EEX_Mixin, DreidingMixin, ReaxFFMixin):
    def __init__(self, filename=None, fftype=None, uri_handler=None, references=None):
        """
        Read, write, and use a forcefield

        The Forcefield object is the main interface for working with
        forcefields. It provides methods to read and write
        forcefields, to assign the forcefield to a molecule, as well
        as to get parameters for bonds, angles, etc.

        Parameters
        ----------
        filename : 'str'
            An optional filename for the forcefield
        fftype : 'str'
            An optional type for the forcefield. If not given and a forcefield
            is read, the code will try to divine the type of forcefield.
        """
        # the extensions and types that can be handled
        self._ff_extensions = {
            ".frc": "Biosym",
        }
        self._ff_readers = {
            "Biosym": self._read_biosym_ff,
        }

        self._fftype = None
        self._filename = None
        self._uri_handler = uri_handler
        self._files_visited = []
        self._references = references
        self._citations = set()
        self.keep_lines = False
        self.data = {}
        self.data["forcefields"] = []
        self.ff = {}

        self.fftype = fftype
        self.filename = filename
        self._current_forcefield = None

    @property
    def charge_method(self):
        """The method for handlign the charges on atoms"""
        if "metadata" in self.ff and "charges" in self.ff["metadata"]:
            return self.ff["metadata"]["charges"]["value"]
        else:
            return "point"

    @property
    def current_forcefield(self):
        """The forcefield currently set up for use."""
        return self._current_forcefield

    @current_forcefield.setter
    def current_forcefield(self, value):
        if value is None:
            self.ff = {}
        elif value != self._current_forcefield:
            self.initialize_biosym_forcefield(forcefield=value)
        self._current_forcefield = value

    @property
    def filename(self):
        """'str' name of file for this forcefield.

        When the filename is set, if the file exists it is read. If it
        does not exist, it is created and initialized as a forcefield
        file. The type of the file may be given by self.fftype; if
        not, the code tries the divine the type of the forcefield. The
        default type for new forcefields is the Biosym .frc format.

        If the filename is changed the object is reset.
        """
        return self._filename

    @filename.setter
    def filename(self, value):
        if value is None:
            self.clear()
            self._filename = None
        else:
            if value == self._filename:
                return

            if os.path.isfile(value):
                self.clear()
                self.data["forcefields"] = []
                self._filename = value
                self._read()
            else:
                self._filename = value
                self._create_file()

    @property
    def files_visited(self):
        """The list of files used in the forcefield"""
        return self._files_visited

    @property
    def ff_form(self):
        """The functional form or type of forcefield, e.g. class2, dreiding, etc."""
        if "metadata" in self.ff and "ff_form" in self.ff["metadata"]:
            return self.ff["metadata"]["ff_form"]["value"]
        else:
            ffname = self.current_forcefield
            if "cff" in ffname:
                return "class2"
            if "dreiding" in ffname:
                return "dreiding"
            if "reaxff" in ffname:
                return "reaxff"

        return "general"

    @property
    def fftype(self):
        """'str' the type of forcefield to handle

        When set, the type is checked to make sure it can be handled. If not
        a RunTimeError is raised.
        """
        return self._fftype

    @fftype.setter
    def fftype(self, value):
        if not value:
            self._fftype = None
        else:
            if value not in self._ff_readers:
                raise RuntimeError("Forcefield type '{}' not supported".format(value))
            self._fftype = value

    @property
    def forcefields(self):
        """The list of current forcefields. The first is the default one"""
        return self.data["forcefields"]

    @property
    def references(self):
        """The reference handler."""
        return self._references

    @property
    def terms(self):
        """The terms in the current forcefield.

        Returns a dictionary whose keys are the terms in the forcefield
        and values are lists of the functional forms for the term.

        Returns
        -------
        dict(str, [str])
        """
        if self.current_forcefield is None:
            raise RuntimeError("The forcefield must be set to access its terms")
        return self.ff["terms"]

    @staticmethod
    def rmin_to_sigma(rmin):
        """Convert rmin to sigma for LJ potential."""
        return rmin / two_raised_to_one_sixth

    @staticmethod
    def sigma_to_rmin(sigma):
        """Convert sigma to rmin for LJ potential."""
        return sigma * two_raised_to_one_sixth

    @staticmethod
    def nonbond_transformation(
        in_form=NonbondForms.SIGMA_EPS,
        in1_units=None,
        in2_units=None,
        out_form=NonbondForms.SIGMA_EPS,
        out1_units="Å",
        out2_units="kcal/mol",
    ):
        """Return the transform method and unit conversions for the nonbonds.

        Parameters
        ----------
        in_form : enum (NonbondForms)
            The form of the parameters input ('sigma-eps', 'rmin-eps', 'A-B' or
            'A/r-B/r')
        in1_units : string
            The units for the first input parameter
        in2_units : string
            The units for the second input parameter
        out_form : enum (NonbondForms)
            The form of the parameters output.
        out1_units : string
            The units for the first output parameter
        out2_units : string
            The units for the second output parameter

        Returns
        -------
        function : function object
            Python function to transform the parameters
        factor1 : float
            Conversion factor to apply to first transformed parameter
        factor2 : float
            Conversion factor to apply to the second transformed parameter
        """
        if out_form == NonbondForms.SIGMA_EPS:
            if in_form == NonbondForms.SIGMA_EPS:
                transform = Forcefield.no_transform
                factor1 = Q_(1.0, in1_units).to(out1_units).magnitude
                factor2 = Q_(1.0, in2_units).to(out2_units).magnitude
            elif in_form == NonbondForms.RMIN_EPS:
                transform = Forcefield.rmin_eps_to_sigma_eps
                factor1 = Q_(1.0, in1_units).to(out1_units).magnitude
                factor2 = Q_(1.0, in2_units).to(out2_units).magnitude
            elif in_form == NonbondForms.A_B:
                transform = Forcefield.a_b_to_sigma_eps
                A = Q_(1.0, in1_units)
                B = Q_(1.0, in2_units)
                factor1 = (A / B) ** (1 / 6).to(out1_units).magnitude
                factor2 = (B**2 / (4 * A)).to(out2_units).magnitude
            elif in_form == NonbondForms.AR_BR:
                transform = Forcefield.ar_br_to_sigma_eps
                A = Q_(1.0, in1_units) ** 12
                B = Q_(1.0, in2_units) ** 6
                sigma = (A / B) ** (1 / 6)
                eps = B**2 / A
                factor1 = sigma.to(out1_units).magnitude
                factor2 = eps.to(out2_units).magnitude
            else:
                raise ValueError(
                    "Cannot handle nonbond input form '" + str(in_form) + "'."
                )
        elif out_form == NonbondForms.RMIN_EPS:
            if in_form == NonbondForms.RMIN_EPS:
                transform = Forcefield.no_transform
                factor1 = Q_(1.0, in1_units).to(out1_units).magnitude
                factor2 = Q_(1.0, in2_units).to(out2_units).magnitude
            else:
                raise ValueError(
                    "Cannot handle nonbond input form '" + str(in_form) + "'."
                )
        elif out_form == NonbondForms.A_B:
            raise NotImplementedError(
                "Nonbond output form '" + str(out_form) + "' not implemented yet."
            )
        elif out_form == NonbondForms.AR_BR:
            raise NotImplementedError(
                "Nonbond output form '" + str(out_form) + "' not implemented yet."
            )
        else:
            raise ValueError(
                "Cannot handle nonbond output form '" + str(out_form) + "'."
            )

        return lambda p1, p2: transform(p1, p2, factor1, factor2)

    @staticmethod
    def no_transform(in1, in2, factor1, factor2):
        """No transformation of nonbond parameters, just units."""
        return in1 * factor1, in2 * factor2

    @staticmethod
    def rmin_eps_to_sigma_eps(rmin, eps, factor1, factor2):
        """Transform nonbond parameters from rmin-eps to sigma-eps
        and apply the unit conversion factors
        """
        return Forcefield.rmin_to_sigma(rmin) * factor1, eps * factor2

    @staticmethod
    def a_b_to_sigma_eps(A, B, factor1, factor2):
        """Transform nonbond parameters from A-B to sigma-eps
        and apply the unit conversion factors
        """
        if A == 0 and B == 0:
            return 0.0, 0.0
        else:
            sigma = (A / B) ** (1 / 6)
            eps = B**2 / (4 * A)
            return sigma * factor1, eps * factor2

    @staticmethod
    def ar_br_to_sigma_eps(A, B, factor1, factor2):
        """Transform nonbond parameters from A/r-B/r to sigma-eps
        and apply the unit conversion factors
        """
        if A == 0 and B == 0:
            return 0.0, 0.0
        else:
            A = A**12
            B = B**6
            sigma = (A / B) ** (1 / 6)
            eps = B**2 / (4 * A)
            return sigma * factor1, eps * factor2

    def clear(self):
        """
        Reset the object to its initial, empty, state
        """
        # self._fftype = None  # leave the type ????
        self._filename = None
        self._files_visited = []
        self.data = {}
        self.data["forcefields"] = []
        self.current_forcefield = None

    def _read(self):
        """Read the forcefield from the file self.filename

        self.fftype gives the type of forcefield file. If it is not set
        the code attempts to divine the type from the extension and the
        first lines.
        """
        if self.fftype:
            if self.fftype in self._ff_readers:
                reader = self._ff_readers[self.fftype]
            else:
                raise RuntimeError(
                    "Forcefield type '{}' not supported".format(self.fftype)
                )
        else:
            ext = seamm_util.splitext(self.filename)
            if ext in self._ff_extensions:
                reader = self._ff_readers[self._ff_extensions[ext]]
            else:
                raise RuntimeError(
                    "Don't recognize forcefield by extension '{}'".format(ext)
                )

        with seamm_util.Open(
            self.filename, "r", include="#include", uri_handler=self._uri_handler
        ) as fd:
            reader(fd)
            self._files_visited = fd.visited

    def _read_biosym_ff(self, fd):
        """
        Read and parse a forcefield in Biosym's format

        Args:
            fd (file object): the file handle
        """
        self.data = {
            "forcefield": {},
            "forcefields": [],
        }

        try:
            # Read and process the first line, which should say
            # what the file is e.g. '!BIOSYM forcefield 1'
            line = next(fd)
            if line[0] == "!" and len(line.split()) == 3:
                file_variant, file_type, version = line[1:].split()
                logger.info(
                    "reading '{}', a {} file from {}, version {}".format(
                        self.filename, file_type, file_variant, version
                    )
                )
            else:
                logger.warning(
                    "reading '{}', expected a header line but got\n\t'{}'".format(
                        self.filename, line
                    )
                )

            # Read the rest of the file, processing the '#'
            # delimited sections
            for line in fd:
                line = line.strip()

                # Empty and comment lines
                if line == "" or line[0] == "!":
                    continue

                if line[0] == "#":
                    # fd.push()
                    words = line[1:].split()
                    section = words[0]

                    # Just ignore #end sections, as they simply close a section
                    if section == "end":
                        continue
                    elif section == "version":
                        self._parse_biosym_version(words)
                        continue

                    if len(words) < 2:
                        logger.warning(
                            section
                            + " section does not have a label!\n\t"
                            + "\n\t".join(fd.stack())
                        )
                        label = "missing"
                        priority = 0
                    else:
                        label = words[1]
                        if len(words) > 2:
                            priority = float(words[2])
                        else:
                            priority = 0

                    logger.debug("reading ff section " + section)

                    result = self._read_biosym_section(fd)

                    result["section"] = section
                    result["label"] = label
                    result["priority"] = priority

                    # Parse the data, looking for specialized implementations
                    if "nonbond" in section:
                        method = "_parse_biosym_nonbonds"
                    else:
                        method = "_parse_biosym_" + section
                    logger.info(
                        f"Parsing forcefield section '{section}' with {method}."
                    )

                    found = False
                    if method in Forcefield.__dict__:
                        Forcefield.__dict__[method](self, result)
                        found = True
                    else:
                        found = False
                        for cls in self.__class__.__mro__:
                            if method in cls.__dict__:
                                cls.__dict__[method](self, result)
                                found = True
                                break
                    if not found and section in metadata:
                        self._parse_biosym_section(result)
                        found = True

                    if not found:
                        logger.warning("Cannot find parser for " + section)

        except IOError:
            logger.exception("Encountered I/O error opening '{}'".format(self.filename))
            raise

    def _read_biosym_section(self, fd):
        """
        Read the body of a section of the forcefield

        Keeps tracks of comments ('!'), annotations ('>'), and modifiers ('@'),
        returning a dictionary with them plus the raw lines of data
        """
        result = {"comments": [], "lines": [], "annotations": [], "modifiers": []}

        for line in fd:
            line = line.strip()

            # Empty and comment lines
            if line == "":
                continue

            if line[0] == "!":
                result["comments"].append(line[1:])
                continue

            if line[0] == "#":
                # At the end of the section, push the line back so the
                # main reader handles it and return the dict with the
                # data
                fd.push()
                return result

            if line[0] == ">":
                # An annotation
                result["annotations"].append(line[1:])
                continue

            if line[0] == "@" and not line.lower().startswith("@bibtex"):
                # A modifier such as units or form
                result["modifiers"].append(line[1:])
                continue

            # Must be a line of data! :-)
            result["lines"].append(line)

    def _parse_biosym_version(self, words):
        """
        Process the 'version' section, which looks like

        #version	pcff.frc	1.0	1-July-91
        """
        pass

    def _parse_biosym_define(self, data):
        """
        Process a forcefield definition section

        #define cff91

        !Ver Ref		Function	     Label
        !--- ---    ------------------------------   ------
         1.0  1     atom_types                       cff91
         1.0  1     equivalence                      cff91
        ...
        """
        section = "forcefield"
        ff_name = data["label"]

        self.data["forcefields"].append(ff_name)

        if section not in self.data:
            self.data[section] = {}
        self.data[section][ff_name] = data
        sections = self.data[section][ff_name]["parameters"] = {}

        for line in data["lines"]:
            words = line.split()
            if len(words) < 4:
                logger.error(
                    "In a define section for {}, the line is too short:".format(ff_name)
                )
                logger.error("    " + line)
            else:
                version, reference, functional_form = words[0:3]
                labels = words[3:]
                if functional_form not in sections:
                    sections[functional_form] = {}
                V = packaging.version.Version(version)
                sections[functional_form][V] = {
                    "version": version,
                    "reference": reference,
                    "sections": labels,
                }

        if not self.keep_lines:
            del data["lines"]

    def _parse_biosym_metadata(self, data):
        """
        Process the metadata describing the forcefield, e.g.

        #metadata CHLiOFSi_Yun_2017

        !Version      Ref   Parameter       Value  Description
        !---------  -----  ------------  --------  -------------------------------------
        2025.04.06      1   ff_form        reaxff  The functional form of the forcefield
        2025.04.06      1   charges        qeq     How charges should be handled
        ...
        """
        section = data["section"]
        label = data["label"]

        if section not in self.data:
            self.data[section] = {}
        if label in self.data[section]:
            msg = "'{}' already defined in section '{}'".format(label, section)
            logger.error(msg)
            raise RuntimeError(msg)
        self.data[section][label] = data
        metadata = self.data[section][label]["parameters"] = {}

        for line in data["lines"]:
            version, reference, parameter, value, description = line.split(maxsplit=4)
            if parameter not in metadata:
                metadata[parameter] = {}
            V = packaging.version.Version(version)
            if V in metadata[parameter]:
                msg = (
                    f"parameter '{parameter}', version {version} defined more than "
                    f"once in section '{section}'!"
                )
                logger.error(msg)
                raise RuntimeError(msg)
            metadata[parameter][V] = {
                "reference": reference,
                "value": value,
                "description": description,
            }

        if not self.keep_lines:
            del data["lines"]

    def _parse_biosym_atom_types(self, data):
        """
        Process the atom types

        #atom_types           cff91

        > Atom type definitions for any variant of cff91
        > Masses from CRC 1973/74 pages B-250.

        !Ver Ref  Type     Mass      Element   connection   Comment
        !--- ---  -----  ----------  -------   ----------   -------------------
        2.1 11   Ag     107.86800     Ag          0        Silver metal
        2.1 11   Al      26.98200     Al          0        Aluminium metal
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
        atom_types = self.data[section][label]["parameters"] = {}

        for line in data["lines"]:
            words = line.split()
            version, reference, atom_type, mass, element, connections = words[0:6]
            comment = " ".join(words[6:])
            if atom_type not in atom_types:
                atom_types[atom_type] = {}
            V = packaging.version.Version(version)
            if V in atom_types[atom_type]:
                msg = "atom type '{}' defined more than ".format(
                    atom_type
                ) + "once in section '{}'!".format(section)
                logger.error(msg)
                raise RuntimeError(msg)
            atom_types[atom_type][V] = {
                "reference": reference,
                "mass": mass,
                "element": element,
                "connections": connections,
                "comment": comment,
            }

        if not self.keep_lines:
            del data["lines"]

    def _parse_biosym_equivalence(self, data):
        """
        Process the atom type equivalences

        #equivalence          cff91

        !                      Equivalences
        !       ------------------------------------------
        !Ver Ref  Type   NonB   Bond   Angle  Torsion  OOP
        !--- ---  -----  -----  -----  -----  -------  -----
        2.1 11   Ag     Ag     Ag     Ag     Ag       Ag
        2.1 11   Al     Al     Al     Al     Al       Al
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
        equivalences = self.data[section][label]["parameters"] = {}

        for line in data["lines"]:
            words = line.split()
            version, reference, atom_type, nonbond, bond, angle, torsion, oop = words
            if atom_type not in equivalences:
                equivalences[atom_type] = {}
            V = packaging.version.Version(version)
            if V in equivalences[atom_type]:
                msg = "atom type '{}' defined more than ".format(
                    atom_type
                ) + "once in section '{}'!".format(section)
                logger.error(msg)
                raise RuntimeError(msg)
            equivalences[atom_type][V] = {
                "reference": reference,
                "nonbond": nonbond,
                "bond": bond,
                "angle": angle,
                "torsion": torsion,
                "oop": oop,
            }

        if not self.keep_lines:
            del data["lines"]

    def _parse_biosym_auto_equivalence(self, data):
        """
        Process the atom type equivalences for automatic types

        #auto_equivalence     cff91_auto

        !                      Equivalences
        !       ------------------------------------------
        !Ver  Ref   Type  NonB Bond   Bond     Angle    Angle     Torsion   Torsion      OOP      OOP
        !                       Inct           End atom Apex atom End Atoms Center Atoms End Atom Center Atom
        !---- ---   ----  ---- ------ ----  ---------- --------- --------- -----------  -------- -----------
        2.0  1     Br    Br   Br     Br_   Br_        Br_       Br_       Br_          Br_      Br_
        2.0  1     Cl    Cl   Cl     Cl_   Cl_        Cl_       Cl_       Cl_          Cl_      Cl_
        ...
        """  # noqa: E501
        section = data["section"]
        label = data["label"]

        if section not in self.data:
            self.data[section] = {}
        if label in self.data[section]:
            msg = "'{}' already defined in section '{}'".format(label, section)
            logger.error(msg)
            raise RuntimeError(msg)
        self.data[section][label] = data
        equivalences = self.data[section][label]["parameters"] = {}

        for line in data["lines"]:
            words = line.split()
            (
                version,
                reference,
                atom_type,
                nonbond,
                bond_increment,
                bond,
                angle_end_atom,
                angle_center_atom,
                torsion_end_atom,
                torsion_center_atom,
                oop_end_atom,
                oop_center_atom,
            ) = words
            if atom_type not in equivalences:
                equivalences[atom_type] = {}
            V = packaging.version.Version(version)
            if V in equivalences[atom_type]:
                msg = "atom type '{}' defined more than ".format(
                    atom_type
                ) + "once in section '{}'!".format(section)
                logger.error(msg)
                raise RuntimeError(msg)
            equivalences[atom_type][V] = {
                "reference": reference,
                "nonbond": nonbond,
                "bond_increment": bond_increment,
                "bond": bond,
                "angle_end_atom": angle_end_atom,
                "angle_center_atom": angle_center_atom,
                "torsion_end_atom": torsion_end_atom,
                "torsion_center_atom": torsion_center_atom,
                "oop_end_atom": oop_end_atom,
                "oop_center_atom": oop_center_atom,
            }

        if not self.keep_lines:
            del data["lines"]

    def _parse_biosym_bond_increments(self, data):
        """
        Process the bond increments

        #bond_increments      cff91_auto

        !Ver Ref    I     J     DeltaIJ   DeltaJI
        !--- ---  ----- -----   -------   -------
        2.1 11   Ag    Ag       0.0000   0.0000
        2.1 11   Al    Al       0.0000   0.0000
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

        parameters = data["parameters"] = {}

        # Copy in the metadata about this functional form
        data.update(metadata[section])

        for line in data["lines"]:
            words = line.split()
            version, reference, i, j, deltaij, deltaji = words
            # order canonically, i<j
            if i > j:
                i, j = j, i
                deltaij, deltaji = deltaji, deltaij
            key = (i, j)
            if key not in parameters:
                parameters[key] = {}
            V = packaging.version.Version(version)
            if V in parameters[key]:
                msg = "bond increment '{}' '{}' defined more ".format(
                    i, j
                ) + "than once in section '{}'!".format(section)
                logger.error(msg)
                raise RuntimeError(msg)
            parameters[key][V] = {
                "reference": reference,
                "deltaij": deltaij,
                "deltaji": deltaji,
            }

        if not self.keep_lines:
            del data["lines"]

    def _parse_biosym_templates(self, data):
        """
        Process the templates, which are simply json

        #templates pcff
        "c": {
            "2017.12.15": {
                "smarts": [
                    "[CX4:1]"
                ],
                "description": "generic SP3 carbon",
                "overrides": []
            }
        },
        "c3": {
            "2017.12.15": {
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

        data["parameters"] = json.loads("\n".join(data["lines"]))

        if not self.keep_lines:
            del data["lines"]

    def _parse_biosym_fragments(self, data):
        """
        Process the templates, which are simply json

        #fragments library

        {
            "FCC#N": {
                "InChIKey": "GNFVFPBRMLIKIM-UHFFFAOYSA-N",
                "SMILES": "FCC#N",
                "SMARTS": "FC(C#N)([H])[H]",
                "atom types": [
                    "GNFVFPBRMLIKIM_800",
                    "GNFVFPBRMLIKIM_801",
                    "GNFVFPBRMLIKIM_802",
                    "GNFVFPBRMLIKIM_803",
                    "GNFVFPBRMLIKIM_804",
                    "GNFVFPBRMLIKIM_805"
                ],
                "name": "2-fluoroacetonitrile"
            },
            "O=[C]1[O][CH][CH][O]1": {
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

        data["parameters"] = json.loads("\n".join(data["lines"]))

        if not self.keep_lines:
            del data["lines"]

    def _parse_biosym_reference(self, data):
        """
        Process a 'reference' section, which looks like::

            #reference 1
            @Author Biosym Technologies inc
            @Date 25-December-91
            cff91 forcefield created
            December 1991
            @bibtex @article{doi:10.1021/jp800281e,
            ...
            }
        """
        section = data["section"]
        label = data["label"]

        if section not in self.data:
            self.data[section] = {}
        if label in self.data[section]:
            msg = "'{}' already defined in section '{}'".format(label, section)
            logger.error(msg)
            raise RuntimeError(msg)
        self.data[section][label] = data
        data["citations"] = {}

        lines = iter(data["lines"])
        text = []
        for line in lines:
            line = line.strip()
            if line.startswith("@"):
                lower = line.lower()
                if lower.startswith("@bibtex"):
                    alias = line.split("{")[1].rstrip(",")
                    citation = [line.split(maxsplit=1)[1]]
                    for line in lines:
                        if line.strip() == "}":
                            citation.append("}")
                            data["citations"][alias] = "\n".join(citation)
                            break
                        else:
                            citation.append(line)
                else:
                    key, rest = line.split(maxsplit=1)
                    key = key[1:].lower()
                    data[key] = rest
            else:
                text.append(line)

        if len(text) > 0:
            data["text"] = "\n".join(text)

        if not self.keep_lines:
            del data["lines"]

    def make_canonical(self, symmetry, atom_types):
        """
        Using the symmetry, order the atom_types canonically
        """

        n = len(atom_types)
        flipped = False
        if n == 1:
            i = atom_types[0]
            return ((i,), flipped)
        elif n == 2:
            i, j = atom_types
            if symmetry == "like_bond":
                # order canonically, i<j
                if i > j:
                    i, j = j, i
                    flipped = True
            return ((i, j), flipped)
        elif n == 3:
            i, j, k = atom_types
            if symmetry == "like_angle":
                # order canonically, i<k
                if i > k:
                    i, k = k, i
                    flipped = True
            return ((i, j, k), flipped)
        elif n == 4:
            i, j, k, l = atom_types  # noqa: E741
            if symmetry == "like_torsion":
                # order canonically, j<k; i<l if j==k
                if j == k and i > l:
                    i, l = l, i  # noqa: E741
                    flipped = True
                elif j > k:
                    i, j, k, l = l, k, j, i  # noqa: E741
                    flipped = True
            elif symmetry == "like_improper":
                # k is central atom
                # order canonically, i<j<l; i=j<l or i<j=l
                i, j, l = sorted((i, j, l))  # noqa: E741
                flipped = [i, j, k, l] != atom_types
            elif symmetry == "like_oop":
                # j is central atom
                # order canonically, i<k<l; i=k<l or i<k=l
                i, k, l = sorted((i, k, l))  # noqa: E741
                flipped = [i, j, k, l] != atom_types
            elif symmetry == "like_angle-angle":
                # order canonically, i<l;
                if i > l:
                    i, l = l, i  # noqa: E741
                    flipped = True
            return ((i, j, k, l), flipped)

    def _parse_biosym_nonbonds(self, data):
        """
        Process the nonbond parameters, accounting for different expressions
        and units.

        For example:
            #nonbond(12-6) spc

            > E = (A/r)^12 - (B/r)^6
            >
            > where    r(ij) is the distance between atoms i and j

            @type A/r-B/r
            @units A (kJ/mol)**(1/12)*nm
            @units B (kJ/mol)**(1/6)*nm
            @combination geometric

            !   Ver    Ref    I            A              B
            !--------- ---  -------   -------------  -----------
            2020.05.13   3  o_spc       0.3428         0.37122
            2020.05.13   3  h_spc       0.0            0.0

            #nonbond(12-6) nacl

            >   E = eps * [(rmin/r)^12 - (rmin/r)^6]
            >
            > where    r is the distance between atoms i and j

            @type eps-rmin
            @units eps kcal/mol
            @units rmin Å
            @combination geometric

            !   Ver    Ref    I           Rmin        Epsilon
            !--------- ---  -------   -------------  -----------
            2020.05.13   4  na+         2.7275         0.0469
            2020.05.13   4  k+          3.5275         0.0870
            2020.05.13   5  cl-         4.5400         0.1500


        """  # nopep8
        logger.debug("Entering _parse_biosym_nonbonds")

        section = data["section"]
        label = data["label"]

        logger.debug("parsing section " + section + " with nonbond parser")
        logger.debug("  data keys: " + str(data.keys()))

        if section not in self.data:
            self.data[section] = {}
        if label in self.data[section]:
            msg = "'{}' already defined in section '{}'".format(label, section)
            logger.error(msg)
            raise RuntimeError(msg)

        self.data[section][label] = data

        # Copy in the metadata about this functional form
        data.update(metadata[section])

        topology = data["topology"]

        out1, out2 = data["constants"]
        out1_units = out1[1]  # Å, nm
        out2_units = out2[1]  # kcal/mol, kJ/mol
        parameter_1 = out1[0]
        parameter_2 = out2[0]

        out_form = NonbondForms(topology["form"])

        # Default for parameters read in
        in_form = out_form
        in1_units = "Å"
        in2_units = "kcal/mol"

        # And see if there are modifiers
        for item in data["modifiers"]:
            modifier = item.split()
            what = modifier[0]
            if what == "type":
                try:
                    in_form = NonbondForms(modifier[1])
                except ValueError:
                    raise ValueError("Unrecognized nonbond form '" + modifier[1] + "'")
            elif what == "units":
                which = modifier[1]
                if which in ["sigma", "rmin", "A"]:
                    in1_units = modifier[2]
                elif which in ["eps", "B"]:
                    in2_units = modifier[2]
                else:
                    raise ValueError("Unrecognized nonbond parameter '" + which + "'")
            elif what == "combination":
                pass
            else:
                raise ValueError(
                    "Unrecognized nonbond modifier '" + what + "' Should be "
                    "one of 'type', 'units' or 'combination'."
                )

        # Now that we know what we are getting as parameters (in1, in2),
        # and what we want (p1, p2), make it so!
        transform = Forcefield.nonbond_transformation(
            in_form, in1_units, in2_units, out_form, out1_units, out2_units
        )

        parameters = data["parameters"] = {}

        for line in data["lines"]:
            version, reference, i, p1, p2 = line.split()

            key = (i,)
            if key not in parameters:
                parameters[key] = {}
            V = packaging.version.Version(version)
            if V in parameters[key]:
                msg = (
                    "value for '"
                    + "' '".join(key)
                    + " defined more "
                    + "than once in section '{}'!".format(section)
                )
                logger.error(msg)
                raise RuntimeError(msg)

            v1, v2 = transform(float(p1), float(p2))

            parameters[key][V] = {
                "reference": reference,
                parameter_1: v1,
                parameter_2: v2,
                "original " + parameter_1: p1,
                "original " + parameter_2: p2,
            }

        if not self.keep_lines:
            del data["lines"]

    def _parse_biosym_section(self, data):
        """
        Process the 1-term torsion parameters

        #torsion_1            cff91_auto

        > E = Kphi * [ 1 + cos(n*Phi - Phi0) ]

        !Ver Ref    I     J     K     L       KPhi     n     Phi0
        !--- ---  ----- ----- ----- -----   --------  ---  ---------
        2.0  2   *     c'_   c'_   *         0.4500    2   180.0000
        2.0  2   *     c'_   c=_   *         0.4500    2   180.0000
        ...
        """  # nopep8
        section = data["section"]
        label = data["label"]

        logger.debug("parsing section " + section + " with generic parser")
        logger.debug("  data keys: " + str(data.keys()))

        if section not in self.data:
            self.data[section] = {}
        if label in self.data[section]:
            msg = "'{}' already defined in section '{}'".format(label, section)
            logger.error(msg)
            raise RuntimeError(msg)

        self.data[section][label] = data

        # Copy in the metadata about this functional form
        data.update(metadata[section])

        logger.debug(f"{data['constants']=}")

        units = {t[0]: {"default": t[1], "input": t[1]} for t in data["constants"]}
        scale = {t[0]: {"default": 1, "input": 1} for t in data["constants"]}

        # Keep track of the equations in the tabulated forms
        eqns = {}

        # And see if there are modifiers
        for item in data["modifiers"]:
            modifier = item.split()
            what = modifier[0]
            if what == "units":
                which = modifier[1]
                if which in units:
                    units[which]["input"] = modifier[2]
                else:
                    raise ValueError(
                        f"Unrecognized parameter '{which}' in section "
                        f"'{section} {label}'"
                    )
            elif what == "equation":
                eqns[modifier[1]] = " ".join(modifier[3:])
            elif what == "scale":
                which = modifier[1]
                if which in scale:
                    scale[which]["input"] = float(modifier[2])
                else:
                    raise ValueError(
                        f"Scale give for unrecognized parameter '{which}' in section "
                        f"'{section} {label}'"
                    )

        factors = []
        for param, tmp in units.items():
            scale_factor = scale[param]["input"]
            if tmp["default"] == tmp["input"]:
                factors.append(1 * scale_factor)
            else:
                factors.append(Q_(tmp["input"]).m_as(tmp["default"]) * scale_factor)

        parameters = data["parameters"] = {}

        for line in data["lines"]:
            words = line.split()
            version, reference = words[0:2]
            symmetry = data["topology"]["symmetry"]
            n_atoms = data["topology"]["n_atoms"]
            try:
                key, flipped = self.make_canonical(symmetry, words[2 : 2 + n_atoms])
            except Exception:
                logger.error(f"{line=}")
                logger.error(f"{symmetry=}")
                logger.error(f"{n_atoms=}")
                raise

            if key not in parameters:
                parameters[key] = {}
            V = packaging.version.Version(version)
            if V in parameters[key]:
                msg = (
                    "value for '"
                    + "' '".join(key)
                    + " defined more "
                    + "than once in section '{}'!".format(section)
                )
                logger.error(msg)
                raise RuntimeError(msg)
            params = parameters[key][V] = {"reference": reference}
            values = words[2 + n_atoms :]
            if "fill" in data["topology"]:
                n = data["topology"]["fill"]
                if n > 0:
                    if len(values) < 2 * n:
                        values.extend(values[0:n])
            if flipped and "flip" in data["topology"]:
                n = data["topology"]["flip"]
                if n > 0:
                    first = values[0:n]
                    values = values[n : 2 * n]
                    values.extend(first)
            for constant, value, factor in zip(data["constants"], values, factors):
                if constant[0] == "Eqn":
                    if value in eqns:
                        params[constant[0]] = eqns[value]
                        params["original " + constant[0]] = eqns[value]
                    else:
                        raise ValueError(f"Equation '{value}' not found in {section}!")
                else:
                    if factor == 1:
                        if len(constant) > 2:
                            params[constant[0]] = constant[2](value)
                            params["original " + constant[0]] = constant[2](value)
                        else:
                            params[constant[0]] = value
                            params["original " + constant[0]] = value
                    else:
                        params[constant[0]] = float(value) * factor
                        params["original " + constant[0]] = value

        if not self.keep_lines:
            del data["lines"]

    def initialize_biosym_forcefield(self, forcefield=None, version=None):
        """
        Initialize the given version of the Biosym-style forcefield

        If not given, the default forcefield is used, and if the version
        is not specified then the default is the latest version.
        """

        if forcefield is None:
            forcefield = self.forcefields[0]
        elif forcefield not in self.forcefields:
            raise ValueError(
                f"The current forcefield file does not contain '{forcefield}'"
            )
        self._current_forcefield = forcefield

        if version is None:
            V = None
        else:
            V = packaging.version.Version(version)

        self.ff = {}

        # definition of the forcefield
        self.ff["modifiers"] = {}
        self.ff["functional_forms"] = {}
        terms = self.ff["terms"] = {}
        fforms = self.data["forcefield"][forcefield]["parameters"]
        for fform in fforms:
            versions = sorted(fforms[fform].keys(), reverse=True)

            if version is None:
                key = versions[0]
            else:
                key = None
                for value in versions:
                    if value <= V:
                        key = value
                        break
                if key is None:
                    raise RuntimeError(
                        "Cannot find version '{}'".format(version)
                        + " for functional form '{}'".format(fform)
                        + " of forcefield '{}'".format(forcefield)
                    )
            self.cite_parameter(fforms[fform][key], level=1)
            self.ff["functional_forms"][fform] = fforms[fform][key]
            if fform in metadata:
                term = metadata[fform]["topology"]["type"]
                if term in terms:
                    terms[term].append(fform)
                else:
                    terms[term] = [fform]

        # Now run through the sections for the functionals forms,
        # processing each
        for fform in self.ff["functional_forms"]:
            self._get_parameters(fform, V)

    def _get_parameters(self, functional_form, Version):
        """Select the correct version parameters from the sections for
        this functional form"""

        logger.debug("_get_parameters, form = " + functional_form)
        sections = self.ff["functional_forms"][functional_form]["sections"]

        logger.debug("  sections = " + str(sections))

        newdata = self.ff[functional_form] = {}
        modifiers = self.ff["modifiers"][functional_form] = {}

        for section in sections:
            if section.endswith(":optional"):
                section = section[:-9]
                if functional_form not in self.data:
                    continue
                if section not in self.data[functional_form]:
                    continue
            data = self.data[functional_form][section]["parameters"]

            modifiers[section] = self.data[functional_form][section]["modifiers"]

            for item in data:
                # Don't we need some versioning function in the sort?
                versions = sorted(data[item].keys(), reverse=True)

                if Version is None:
                    key = versions[0]
                else:
                    key = None
                    for value in versions:
                        if value <= Version:
                            key = value
                            break
                if key is not None:
                    newdata[item] = data[item][key]

    def mass(self, i):
        """Return the atomic mass for an atom type i"""
        if self.ff_form == "reaxff":
            return self.ff["reaxff_atomic_parameters_25-32"][(i,)]["m"]

        if i in self.ff["atom_types"]:
            return self.ff["atom_types"][i]["mass"]

        raise RuntimeError("no atom type data for {}".format(i))

    def charges(self, i):
        """Return the charge given an atom type i

        Handle equivalences.
        """

        if "charges" in self.ff:
            # parameter directly available
            key = (i,)
            if key in self.ff["charges"]:
                parameters = {}
                parameters.update(self.ff["charges"][key])
                return ("explicit", key, "charges", parameters)

            # try equivalences
            if "equivalence" in self.ff:
                ieq = self.ff["equivalence"][i]["nonbond"]
                key = (ieq,)
                if key in self.ff["charges"]:
                    parameters = {}
                    parameters.update(self.ff["charges"][key])
                    return ("equivalent", key, "charges", parameters)

        # return the default of zero
        parameters = {"Q": 0.0}
        return ("default", ("*",), "charges", parameters)

    def shell_model(self, i):
        """Return the shell model parameters given an atom type i

        Handle equivalences.
        """

        if "shell-model" in self.ff:
            # parameter directly available
            key = (i,)
            if key in self.ff["shell-model"]:
                parameters = {}
                parameters.update(self.ff["shell-model"][key])
                return ("explicit", key, "shell-model", parameters)

            # try equivalences
            if "equivalence" in self.ff:
                ieq = self.ff["equivalence"][i]["nonbond"]
                key = (ieq,)
                if key in self.ff["shell-model"]:
                    parameters = {}
                    parameters.update(self.ff["shell-model"][key])
                    return ("equivalent", key, "quadratic_bond", parameters)

        # return the default of None
        return None

    def bond_increments(self, i, j):
        """Return the bond increments given two atoms types i and j

        Handle automatic equivalences.
        """

        # parameter directly available
        key, flipped = self.make_canonical("like_bond", (i, j))
        if key in self.ff["bond_increments"]:
            parameters = {}
            parameters.update(self.ff["bond_increments"][key])
            if flipped:
                parameters["deltaij"], parameters["deltaji"] = (
                    parameters["deltaji"],
                    parameters["deltaij"],
                )
            return ("explicit", key, "bond_increments", parameters)

        # try automatic equivalences
        if "auto_equivalence" in self.ff:
            iauto = self.ff["auto_equivalence"][i]["bond_increment"]
            jauto = self.ff["auto_equivalence"][j]["bond_increment"]
            key, flipped = self.make_canonical("like_bond", (iauto, jauto))
            if key in self.ff["bond_increments"]:
                parameters = {}
                parameters.update(self.ff["bond_increments"][key])
                if flipped:
                    parameters["deltaij"], parameters["deltaji"] = (
                        parameters["deltaji"],
                        parameters["deltaij"],
                    )
                return ("automatic", key, "bond_increments", parameters)

        raise RuntimeError("No bond increments for {}-{}".format(i, j))

    def bond_parameters(self, i, j):
        """Return the bond parameters given two atoms types i and j

        Handle equivalences and automatic equivalences.
        """

        forms = self.ff["terms"]["bond"]

        # parameter directly available
        for form in forms:
            key, flipped = self.make_canonical("like_bond", (i, j))
            if key in self.ff[form]:
                self.cite_parameter(self.ff[form][key])
                return ("explicit", key, form, self.ff[form][key])

        # try equivalences
        if "equivalence" in self.ff:
            ieq = self.ff["equivalence"][i]["bond"]
            jeq = self.ff["equivalence"][j]["bond"]
            key, flipped = self.make_canonical("like_bond", (ieq, jeq))
            for form in forms:
                if key in self.ff[form]:
                    self.cite_parameter(self.ff[form][key])
                    return ("equivalent", key, form, self.ff[form][key])

        # try automatic equivalences
        if "auto_equivalence" in self.ff:
            iauto = self.ff["auto_equivalence"][i]["bond"]
            jauto = self.ff["auto_equivalence"][j]["bond"]
            key, flipped = self.make_canonical("like_bond", (iauto, jauto))
            for form in forms:
                if key in self.ff[form]:
                    self.cite_parameter(self.ff[form][key])
                    return ("automatic", key, form, self.ff[form][key])

        raise RuntimeError("No bond parameters for {}-{}".format(i, j))

    def angle_parameters(self, i, j, k):
        """Return the angle parameters given three atom types

        Handle equivalences and automatic equivalences.
        """

        msg = [f"Looking for angle parameters for {i}-{j}-{k}"]

        forms = self.ff["terms"]["angle"]

        for form in forms:
            # parameters directly available
            result = self._angle_parameters_helper(i, j, k, self.ff[form])
            if result is not None:
                self.cite_parameter(result[2])
                return ("explicit", result[0], form, result[2])

        msg.append("\tNo explicit parameters found")

        # try equivalences
        if "equivalence" in self.ff:
            ieq = self.ff["equivalence"][i]["angle"]
            jeq = self.ff["equivalence"][j]["angle"]
            keq = self.ff["equivalence"][k]["angle"]
            msg.append(f"\tTrying equivalence {ieq}-{jeq}-{keq}")
            for form in forms:
                result = self._angle_parameters_helper(ieq, jeq, keq, self.ff[form])
                if result is not None:
                    self.cite_parameter(result[2])
                    return ("equivalent", result[0], form, result[2])
            msg.append("\t...No equivalent parameters found")
        else:
            msg.append("\tNo equivalences defined")

        # try automatic equivalences
        if "auto_equivalence" in self.ff:
            iauto = self.ff["auto_equivalence"][i]["angle_end_atom"]
            jauto = self.ff["auto_equivalence"][j]["angle_center_atom"]
            kauto = self.ff["auto_equivalence"][k]["angle_end_atom"]
            key, flipped = self.make_canonical("like_angle", (iauto, jauto, kauto))
            msg.append(f"\tTrying automatic equivalence {iauto}-{jauto}-{kauto}")
            for form in forms:
                if key in self.ff[form]:
                    self.cite_parameter(result[2])
                    return ("automatic", key, form, self.ff[form][key])
            msg.append("\t...Not found")

            # try wildcards, which may have numerical precidence
            # Find all the single-sided wildcards, realizing that the
            # triplet might be flipped.
            msg.append("\tTrying wildcards")
            for form in forms:
                left = []
                right = []
                for key in self.ff[form]:
                    if key[0] == "*" or key[2] == "*":
                        continue
                    if jauto == key[1]:
                        if kauto == key[2] and key[0][0] == "*":
                            left.append(key[0])
                        if kauto == key[0] and key[2][0] == "*":
                            left.append(key[2])
                        if iauto == key[0] and key[2][0] == "*":
                            right.append(key[2])
                        if iauto == key[2] and key[0][0] == "*":
                            right.append(key[0])
                if len(left) > 0:
                    if len(right) == 0:
                        key, flipped = self.make_canonical(
                            "like_angle", (left[0], jauto, kauto)
                        )
                        if key in self.ff[form]:
                            self.cite_parameter(self.ff[form][key])
                            return ("automatic", key, form, self.ff[form][key])
                    else:
                        if left[0] < right[0]:
                            key, flipped = self.make_canonical(
                                "like_angle", (left[0], jauto, kauto)
                            )
                            if key in self.ff[form]:
                                self.cite_parameter(self.ff[form][key])
                                return ("automatic", key, form, self.ff[form][key])
                        else:
                            key, flipped = self.make_canonical(
                                "like_angle", (iauto, jauto, right[0])
                            )
                            if key in self.ff[form]:
                                self.cite_parameter(self.ff[form][key])
                                return ("automatic", key, form, self.ff[form][key])
                elif len(right) > 0:
                    key, flipped = self.make_canonical(
                        "like_angle", (iauto, jauto, right[0])
                    )
                    if key in self.ff[form]:
                        self.cite_parameter(self.ff[form][key])
                        return ("automatic", key, form, self.ff[form][key])

                key, flipped = self.make_canonical("like_angle", ("*", jauto, kauto))
                if key in self.ff[form]:
                    self.cite_parameter(self.ff[form][key])
                    return ("automatic", key, form, self.ff[form][key])
                key, flipped = self.make_canonical("like_angle", (iauto, jauto, "*"))
                if key in self.ff[form]:
                    self.cite_parameter(self.ff[form][key])
                    return ("automatic", key, form, self.ff[form][key])
                key, flipped = self.make_canonical("like_angle", ("*", jauto, "*"))
                if key in self.ff[form]:
                    self.cite_parameter(self.ff[form][key])
                    return ("automatic", key, form, self.ff[form][key])
            msg.append("\t...Not found")
        else:
            msg.append("\tNo automatic equivalences defined")

        raise RuntimeError("\n".join(msg))

    def torsion_parameters(self, i, j, k, l):  # noqa: E741
        """Return the torsion parameters given four atoms types

        Handles equivalences and automatic equivalences and wildcards,
        with numerical precedences
        """

        forms = self.ff["terms"]["torsion"]

        # parameter directly available
        for form in forms:
            result = self._torsion_parameters_helper(i, j, k, l, self.ff[form])
            if result is not None:
                self.cite_parameter(result[2])
                return ("explicit", result[0], form, result[2])

        # try equivalences
        if "equivalence" in self.ff:
            ieq = self.ff["equivalence"][i]["torsion"]
            jeq = self.ff["equivalence"][j]["torsion"]
            keq = self.ff["equivalence"][k]["torsion"]
            leq = self.ff["equivalence"][l]["torsion"]
            for form in forms:
                result = self._torsion_parameters_helper(
                    ieq, jeq, keq, leq, self.ff[form]
                )
                if result is not None:
                    self.cite_parameter(result[2])
                    return ("equivalent", result[0], form, result[2])

        # try automatic equivalences
        if "auto_equivalence" in self.ff:
            iauto = self.ff["auto_equivalence"][i]["torsion_end_atom"]
            jauto = self.ff["auto_equivalence"][j]["torsion_center_atom"]
            kauto = self.ff["auto_equivalence"][k]["torsion_center_atom"]
            lauto = self.ff["auto_equivalence"][l]["torsion_end_atom"]
            key, flipped = self.make_canonical(
                "like_torsion", (iauto, jauto, kauto, lauto)
            )
            for form in forms:
                if key in self.ff[form]:
                    self.cite_parameter(self.ff[form][key])
                    return ("automatic", key, form, self.ff[form][key])

                # try wildcards, which may have numerical precidence
                # Find all the single-sided wildcards, realizing that the
                # triplet might be flipped.
                left = []
                right = []
                for key in self.ff[form]:
                    if key[0] == "*" or key[3] == "*":
                        continue
                    if jauto == key[1] and kauto == key[2]:
                        if lauto == key[3] and key[0][0] == "*":
                            left.append(key[0])
                        if lauto == key[0] and key[3][0] == "*":
                            left.append(key[3])
                        if iauto == key[0] and key[3][0] == "*":
                            right.append(key[3])
                        if iauto == key[3] and key[0][0] == "*":
                            right.append(key[0])
                if len(left) > 0:
                    if len(right) == 0:
                        key, flipped = self.make_canonical(
                            "like_torsion", (left[0], jauto, kauto, lauto)
                        )
                        if key in self.ff[form]:
                            self.cite_parameter(self.ff[form][key])
                            return ("automatic", key, form, self.ff[form][key])
                    else:
                        if left[0] < right[0]:
                            key, flipped = self.make_canonical(
                                "like_torsion", (left[0], jauto, kauto, lauto)
                            )
                            if key in self.ff[form]:
                                self.cite_parameter(self.ff[form][key])
                                return ("automatic", key, form, self.ff[form][key])
                        else:
                            key, flipped = self.make_canonical(
                                "like_torsion", (iauto, jauto, kauto, right[0])
                            )
                            if key in self.ff[form]:
                                self.cite_parameter(self.ff[form][key])
                                return ("automatic", key, form, self.ff[form][key])
                elif len(right) > 0:
                    key, flipped = self.make_canonical(
                        "like_torsion", (iauto, jauto, kauto, right[0])
                    )
                    if key in self.ff[form]:
                        self.cite_parameter(self.ff[form][key])
                        return ("automatic", key, form, self.ff[form][key])

                key, flipped = self.make_canonical(
                    "like_torsion", (iauto, jauto, kauto, "*")
                )
                if key in self.ff[form]:
                    self.cite_parameter(self.ff[form][key])
                    return ("automatic", key, form, self.ff[form][key])
                key, flipped = self.make_canonical(
                    "like_torsion", ("*", jauto, kauto, lauto)
                )
                if key in self.ff[form]:
                    self.cite_parameter(self.ff[form][key])
                    return ("automatic", key, form, self.ff[form][key])
                key, flipped = self.make_canonical(
                    "like_torsion", ("*", jauto, kauto, "*")
                )
                if key in self.ff[form]:
                    self.cite_parameter(self.ff[form][key])
                    return ("automatic", key, form, self.ff[form][key])

        raise RuntimeError("No torsion parameters for {}-{}-{}-{}".format(i, j, k, l))

    def _torsion_parameters_helper(self, i, j, k, l, section):  # noqa: E741
        """Return the torsion parameters given four atom types"""

        # parameter directly available
        key, flipped = self.make_canonical("like_torsion", (i, j, k, l))
        if key in section:
            return (key, flipped, section[key])

        # try wildcards
        key, flipped = self.make_canonical("like_torsion", ("*", j, k, l))
        if key in section:
            return (key, flipped, section[key])
        key, flipped = self.make_canonical("like_torsion", (i, j, k, "*"))
        if key in section:
            return (key, flipped, section[key])
        key, flipped = self.make_canonical("like_torsion", ("*", j, k, "*"))
        if key in section:
            return (key, flipped, section[key])

        return None

    def oop_parameters(self, i, j, k, l, zero=False):  # noqa: E741
        """Return the oop parameters given four atoms types

        Handles equivalences and automatic equivalences and wildcards,
        with numerical precedences
        """

        forms = self.ff["terms"]["out-of-plane"]

        for form in forms:
            result = self._oop_parameters_helper(i, j, k, l, form)
            if result is not None:
                return ("explicit", result[0], form, result[1])

        # try equivalences
        if "equivalence" in self.ff:
            ieq = self.ff["equivalence"][i]["oop"]
            jeq = self.ff["equivalence"][j]["oop"]
            keq = self.ff["equivalence"][k]["oop"]
            leq = self.ff["equivalence"][l]["oop"]
            for form in forms:
                result = self._oop_parameters_helper(ieq, jeq, keq, leq, form)
                if result is not None:
                    self.cite_parameter(result[1])
                    return ("equivalent", result[0], form, result[1])

        # try automatic equivalences
        if "auto_equivalence" in self.ff:
            iauto = self.ff["auto_equivalence"][i]["oop_end_atom"]
            jauto = self.ff["auto_equivalence"][j]["oop_center_atom"]
            kauto = self.ff["auto_equivalence"][k]["oop_end_atom"]
            lauto = self.ff["auto_equivalence"][l]["oop_end_atom"]
            for form in forms:
                result = self._oop_parameters_helper(iauto, jauto, kauto, lauto, form)
                if result is not None:
                    self.cite_parameter(result[1])
                    return ("automatic", result[0], form, result[1])

        if zero:
            if form == "wilson_out_of_plane":
                parameters = {"K": 0.0, "Chi0": 0.0}
            elif form == "dreiding_out_of_plane":
                parameters = {"K": 0.0, "Psi0": 0.0}
            elif form == "improper_opls":
                parameters = {"V2": 0.0}
            return ("zeroed", ("*", "*", "*", "*"), form, parameters)
        else:
            raise RuntimeError(
                "No out-of-plane parameters for {}-{}-{}-{}".format(i, j, k, l)
            )

    def _oop_parameters_helper(self, i, j, k, l, form):  # noqa: E741
        """Return the oop parameters given four atoms types

        Handles equivalences and automatic equivalences and wildcards,
        with numerical precedences
        """

        if "improper" in form:
            # for impropers the central atom is 3rd
            # parameter directly available
            key, flipped = self.make_canonical("like_improper", (i, k, j, l))
            if key in self.ff[form]:
                return (key, self.ff[form][key])

            # try wildcards
            key, flipped = self.make_canonical("like_improper", ("*", k, j, l))
            if key in self.ff[form]:
                return (key, self.ff[form][key])
            key, flipped = self.make_canonical("like_improper", (i, "*", j, l))
            if key in self.ff[form]:
                return (key, self.ff[form][key])
            key, flipped = self.make_canonical("like_improper", (i, k, j, "*"))
            if key in self.ff[form]:
                return (key, self.ff[form][key])
            key, flipped = self.make_canonical("like_improper", ("*", "*", k, l))
            if key in self.ff[form]:
                return (key, self.ff[form][key])
            key, flipped = self.make_canonical("like_improper", ("*", k, j, "*"))
            if key in self.ff[form]:
                return (key, self.ff[form][key])
            key, flipped = self.make_canonical("like_improper", (i, "*", j, "*"))
            if key in self.ff[form]:
                return (key, self.ff[form][key])
            key, flipped = self.make_canonical("like_improper", ("*", "*", j, "*"))
            if key in self.ff[form]:
                return (key, self.ff[form][key])
        else:
            # parameter directly available
            key, flipped = self.make_canonical("like_oop", (i, j, k, l))
            if key in self.ff[form]:
                return (key, self.ff[form][key])

            # try wildcards
            key, flipped = self.make_canonical("like_oop", ("*", j, k, l))
            if key in self.ff[form]:
                return (key, self.ff[form][key])
            key, flipped = self.make_canonical("like_oop", (i, j, "*", l))
            if key in self.ff[form]:
                return (key, self.ff[form][key])
            key, flipped = self.make_canonical("like_oop", (i, j, k, "*"))
            if key in self.ff[form]:
                return (key, self.ff[form][key])
            key, flipped = self.make_canonical("like_oop", ("*", j, "*", l))
            if key in self.ff[form]:
                return (key, self.ff[form][key])
            key, flipped = self.make_canonical("like_oop", ("*", j, k, "*"))
            if key in self.ff[form]:
                return (key, self.ff[form][key])
            key, flipped = self.make_canonical("like_oop", (i, j, "*", "*"))
            if key in self.ff[form]:
                return (key, self.ff[form][key])
            key, flipped = self.make_canonical("like_oop", ("*", j, "*", "*"))
            if key in self.ff[form]:
                return (key, self.ff[form][key])

        return None

    def nonbond_parameters(self, i, j=None, form="nonbond(12-6)"):
        """Return the nondbond parameters given one or two atoms types i and j

        Handle equivalences
        """

        # parameter directly available
        if j is None:
            key = (i,)
        else:
            key, flipped = self.make_canonical("like_bond", (i, j))
        if key in self.ff[form]:
            self.cite_parameter(self.ff[form][key])
            return ("explicit", key, form, self.ff[form][key])

        # try equivalences
        if "equivalence" in self.ff:
            ieq = self.ff["equivalence"][i]["nonbond"]
            if j is None:
                key = (ieq,)
            else:
                jeq = self.ff["equivalence"][j]["nonbond"]
                key, flipped = self.make_canonical("like_bond", (ieq, jeq))
            if key in self.ff[form]:
                self.cite_parameter(self.ff[form][key])
                return ("equivalent", key, form, self.ff[form][key])

        # try automatic equivalences
        if "auto_equivalence" in self.ff:
            iauto = self.ff["auto_equivalence"][i]["nonbond"]
            if j is None:
                key = (iauto,)
            else:
                jauto = self.ff["auto_equivalence"][j]["nonbond"]
                key, flipped = self.make_canonical("like_bond", (iauto, jauto))
            if key in self.ff[form]:
                self.cite_parameter(self.ff[form][key])
                return ("automatic", key, form, self.ff[form][key])

        # try wildcards
        if j is None:
            key = ("*",)
            if key in self.ff[form]:
                self.cite_parameter(self.ff[form][key])
                return ("wildcard", key, form, self.ff[form][key])
        else:
            key = (i, "*")
            if key in self.ff[form]:
                self.cite_parameter(self.ff[form][key])
                return ("wildcard", key, form, self.ff[form][key])
            key = ("*", j)
            if key in self.ff[form]:
                self.cite_parameter(self.ff[form][key])
                return ("wildcard", key, form, self.ff[form][key])
            key = ("*", "*")
            if key in self.ff[form]:
                self.cite_parameter(self.ff[form][key])
                return ("wildcard", key, form, self.ff[form][key])

        if j is None:
            raise RuntimeError("No nonbond parameters for {}".format(i))
        else:
            raise RuntimeError("No nonbond parameters for {}-{}".format(i, j))

    def bond_bond_parameters(self, i, j, k, zero=False):
        """Return the bond-bond parameters given three atoms types

        Handle equivalences, and if zero=True, return zero valued
        parameters rather than raise an error
        """

        # Get the reference bond lengths...
        b1_type, b1_types, b1_form, b1_parameters = self.bond_parameters(i, j)
        b2_type, b2_types, b2_form, b2_parameters = self.bond_parameters(j, k)
        values = {"R10": b1_parameters["R0"], "R20": b2_parameters["R0"]}

        # parameters directly available
        result = self._angle_parameters_helper(i, j, k, self.ff["bond-bond"])
        if result is not None:
            if result[1]:
                values = {"R10": b2_parameters["R0"], "R20": b1_parameters["R0"]}
            values.update(result[2])
            self.cite_parameter(result[2])
            return ("explicit", result[0], "bond-bond", values)

        # try equivalences
        if "equivalence" in self.ff:
            ieq = self.ff["equivalence"][i]["angle"]
            jeq = self.ff["equivalence"][j]["angle"]
            keq = self.ff["equivalence"][k]["angle"]
            result = self._angle_parameters_helper(ieq, jeq, keq, self.ff["bond-bond"])
            if result is not None:
                if result[1]:
                    values = {"R10": b2_parameters["R0"], "R20": b1_parameters["R0"]}
                values.update(result[2])
                self.cite_parameter(result[2])
                return ("equivalent", result[0], "bond-bond", values)

        if zero:
            return (
                "zeroed",
                ("*", "*", "*"),
                "bond-bond",
                {"K": "0.0", "R10": "1.5", "R20": "1.5"},
            )
        else:
            raise RuntimeError("No bond-bond parameters for {}-{}-{}".format(i, j, k))

    def _angle_parameters_helper(self, i, j, k, section):
        """Return the angle-like parameters given three atom types"""

        # parameter directly available
        key, flipped = self.make_canonical("like_angle", (i, j, k))
        if key in section:
            return (key, flipped, section[key])

        # try wildcards
        key, flipped = self.make_canonical("like_angle", ("*", j, k))
        if key in section:
            return (key, flipped, section[key])
        key, flipped = self.make_canonical("like_angle", (i, j, "*"))
        if key in section:
            return (key, flipped, section[key])
        key, flipped = self.make_canonical("like_angle", ("*", j, "*"))
        if key in section:
            return (key, flipped, section[key])

        return None

    def bond_bond_1_3_parameters(self, i, j, k, l, zero=False):  # noqa: E741
        """Return the bond-bond_1_3 parameters given four atoms types

        Handles equivalences wildcards
        """
        # Get the reference bond lengths...
        b1_type, b1_types, b1_form, b1_parameters = self.bond_parameters(i, j)
        b3_type, b3_types, b3_form, b3_parameters = self.bond_parameters(k, l)
        values = {"R10": b1_parameters["R0"], "R30": b3_parameters["R0"]}

        # parameter directly available
        result = self._torsion_parameters_helper(i, j, k, l, self.ff["bond-bond_1_3"])
        if result is not None:
            if result[1]:
                values = {"R10": b3_parameters["R0"], "R30": b1_parameters["R0"]}
            values.update(result[2])
            self.cite_parameter(result[2])
            return ("explicit", result[0], "bond-bond_1_3", values)

        # try equivalences
        if "equivalence" in self.ff:
            ieq = self.ff["equivalence"][i]["torsion"]
            jeq = self.ff["equivalence"][j]["torsion"]
            keq = self.ff["equivalence"][k]["torsion"]
            leq = self.ff["equivalence"][l]["torsion"]
            result = self._torsion_parameters_helper(
                ieq, jeq, keq, leq, self.ff["bond-bond_1_3"]
            )
            if result is not None:
                if result[1]:
                    values = {"R10": b3_parameters["R0"], "R30": b1_parameters["R0"]}
                values.update(result[2])
                self.cite_parameter(result[2])
                return ("equivalent", result[0], "bond-bond_1_3", values)

        if zero:
            parameters = {"K": "0.0", "R10": "1.5", "R30": "1.5"}
            return ("equivalent", ("*", "*", "*", "*"), "bond-bond_1_3", parameters)
        else:
            raise RuntimeError(
                "No bond-bond_1_3 parameters for " + "{}-{}-{}-{}".format(i, j, k, l)
            )

    def bond_angle_parameters(self, i, j, k, zero=False):
        """Return the bond-angle parameters given three atoms types

        Handle equivalences, and if zero=True, return zero valued
        parameters rather than raise an error
        """

        # Get the reference bond lengths...
        b1_type, b1_types, b1_form, b1_parameters = self.bond_parameters(i, j)
        b2_type, b2_types, b2_form, b2_parameters = self.bond_parameters(j, k)

        # parameters directly available
        result = self._angle_parameters_helper(i, j, k, self.ff["bond-angle"])
        if result is not None:
            if result[1]:
                parameters = {
                    "reference": result[2]["reference"],
                    "K12": result[2]["K23"],
                    "K23": result[2]["K12"],
                    "R10": b2_parameters["R0"],
                    "R20": b1_parameters["R0"],
                }
                ii, jj, kk = result[0]
                self.cite_parameter(parameters)
                return ("explicit", (kk, jj, ii), "bond-angle", parameters)
            else:
                parameters = dict(**result[2])
                parameters["R10"] = b1_parameters["R0"]
                parameters["R20"] = b2_parameters["R0"]
                self.cite_parameter(parameters)
                return ("explicit", result[0], "bond-angle", parameters)

        # try equivalences
        if "equivalence" in self.ff:
            ieq = self.ff["equivalence"][i]["angle"]
            jeq = self.ff["equivalence"][j]["angle"]
            keq = self.ff["equivalence"][k]["angle"]
            result = self._angle_parameters_helper(ieq, jeq, keq, self.ff["bond-angle"])
            if result is not None:
                if result[1]:
                    parameters = {
                        "reference": result[2]["reference"],
                        "K12": result[2]["K23"],
                        "K23": result[2]["K12"],
                        "R10": b2_parameters["R0"],
                        "R20": b1_parameters["R0"],
                    }
                    ii, jj, kk = result[0]
                    self.cite_parameter(parameters)
                    return ("equivalent", (kk, jj, ii), "bond-angle", parameters)
                else:
                    parameters = dict(**result[2])
                    parameters["R10"] = b1_parameters["R0"]
                    parameters["R20"] = b2_parameters["R0"]
                    self.cite_parameter(parameters)
                    return ("equivalent", result[0], "bond-angle", parameters)

        if zero:
            return (
                "zeroed",
                ("*", "*", "*"),
                "bond-angle",
                {"K12": "0.0", "K23": "0.0", "R10": "1.5", "R20": "1.5"},
            )
        else:
            raise RuntimeError("No bond-angle parameters for {}-{}-{}".format(i, j, k))

    def angle_angle_parameters(self, i, j, k, l, zero=False):  # noqa: E741
        """Return the angle_angle parameters given four atoms types

        Handles equivalences and wildcards
        """
        # Get the reference bond angles...
        a1_type, a1_types, a1_form, a1_parameters = self.angle_parameters(i, j, k)
        a2_type, a2_types, a2_form, a2_parameters = self.angle_parameters(k, j, l)
        Theta10 = a1_parameters["Theta0"]
        Theta20 = a2_parameters["Theta0"]
        values = {"Theta10": Theta10, "Theta20": Theta20}

        # parameter directly available
        result = self._angle_angle_parameters_helper(i, j, k, l, self.ff["angle-angle"])
        if result is not None:
            if result[1]:
                values = {"Theta10": Theta20, "Theta20": Theta10}
                values.update(result[2])
                ii, jj, kk, ll = result[0]
                self.cite_parameter(values)
                return ("explicit", (ll, jj, kk, ii), "angle-angle", values)
            else:
                values.update(result[2])
                self.cite_parameter(values)
                return ("explicit", result[0], "angle-angle", values)

        # try equivalences
        if "equivalence" in self.ff:
            ieq = self.ff["equivalence"][i]["angle"]
            jeq = self.ff["equivalence"][j]["angle"]
            keq = self.ff["equivalence"][k]["angle"]
            leq = self.ff["equivalence"][l]["angle"]
            result = self._angle_angle_parameters_helper(
                ieq, jeq, keq, leq, self.ff["angle-angle"]
            )
            if result is not None:
                if result[1]:
                    values = {"Theta10": Theta20, "Theta20": Theta10}
                    values.update(result[2])
                    ii, jj, kk, ll = result[0]
                    self.cite_parameter(values)
                    return ("equivalent", (ll, jj, kk, ii), "angle-angle", values)
                else:
                    values.update(result[2])
                    self.cite_parameter(values)
                    return ("equivalent", result[0], "angle-angle", values)

        if zero:
            parameters = {"K": 0.0, "Theta10": "109.0", "Theta20": "109.0"}
            return ("zeroed", ("*", "*", "*", "*"), "angle-angle", parameters)
        else:
            raise RuntimeError(
                "No angle-angle parameters for {}-{}-{}-{}".format(i, j, k, l)
            )

    def _angle_angle_parameters_helper(self, i, j, k, l, section):  # noqa: E741
        """Return the torsion parameters given four atom types"""

        # parameter directly available
        key, flipped = self.make_canonical("like_angle-angle", (i, j, k, l))
        if key in section:
            return (key, flipped, section[key])

        # try wildcards
        key, flipped = self.make_canonical("like_angle-angle", ("*", j, k, l))
        if key in section:
            return (key, flipped, section[key])
        key, flipped = self.make_canonical("like_angle-angle", (i, j, k, "*"))
        if key in section:
            return (key, flipped, section[key])
        key, flipped = self.make_canonical("like_angle-angle", ("*", j, k, "*"))
        if key in section:
            return (key, flipped, section[key])
        key, flipped = self.make_canonical("like_angle-angle", ("*", j, "*", "*"))
        if key in section:
            return (key, flipped, section[key])

        return None

    def end_bond_torsion_3_parameters(self, i, j, k, l, zero=False):  # noqa: E741
        """Return the end bond - torsion_3 parameters given four atom types

        Handle equivalences
        """
        # Get the reference bond lengths...
        b1_type, b1_types, b1_form, b1_parameters = self.bond_parameters(i, j)
        b2_type, b2_types, b2_form, b2_parameters = self.bond_parameters(k, l)
        values = {"R0_L": b1_parameters["R0"], "R0_R": b2_parameters["R0"]}

        # parameters directly available
        result = self._torsion_parameters_helper(
            i, j, k, l, self.ff["end_bond-torsion_3"]
        )
        if result is not None:
            if result[1]:
                parameters = {
                    "reference": result[2]["reference"],
                    "V1_L": result[2]["V1_R"],
                    "V2_L": result[2]["V2_R"],
                    "V3_L": result[2]["V3_R"],
                    "V1_R": result[2]["V1_L"],
                    "V2_R": result[2]["V2_L"],
                    "V3_R": result[2]["V3_L"],
                    "R0_L": b2_parameters["R0"],
                    "R0_R": b1_parameters["R0"],
                }
                ii, jj, kk, ll = result[0]
                self.cite_parameter(parameters)
                return ("explicit", (ll, kk, jj, ii), "end_bond-torsion_3", parameters)
            else:
                parameters = dict(**result[2])
                parameters.update(values)
                self.cite_parameter(parameters)
                return ("explicit", result[0], "end_bond-torsion_3", parameters)

        # try equivalences
        if "equivalence" in self.ff:
            ieq = self.ff["equivalence"][i]["torsion"]
            jeq = self.ff["equivalence"][j]["torsion"]
            keq = self.ff["equivalence"][k]["torsion"]
            leq = self.ff["equivalence"][l]["torsion"]
            result = self._torsion_parameters_helper(
                ieq, jeq, keq, leq, self.ff["end_bond-torsion_3"]
            )
            if result is not None:
                if result[1]:
                    parameters = {
                        "reference": result[2]["reference"],
                        "V1_L": result[2]["V1_R"],
                        "V2_L": result[2]["V2_R"],
                        "V3_L": result[2]["V3_R"],
                        "V1_R": result[2]["V1_L"],
                        "V2_R": result[2]["V2_L"],
                        "V3_R": result[2]["V3_L"],
                        "R0_L": b2_parameters["R0"],
                        "R0_R": b1_parameters["R0"],
                    }
                    ii, jj, kk, ll = result[0]
                    self.cite_parameter(parameters)
                    return (
                        "equivalent",
                        (ll, kk, jj, ii),
                        "end_bond-torsion_3",
                        parameters,
                    )
                else:
                    parameters = dict(**result[2])
                    parameters.update(values)
                    self.cite_parameter(parameters)
                    return ("equivalent", result[0], "end_bond-torsion_3", parameters)

        if zero:
            parameters = {
                "V1_L": "0.0",
                "V2_L": "0.0",
                "V3_L": "0.0",
                "V1_R": "0.0",
                "V2_R": "0.0",
                "V3_R": "0.0",
                "R0_L": "1.5",
                "R0_R": "1.5",
            }
            return ("zeroed", ("*", "*", "*", "*"), "end_bond-torsion_3", parameters)
        else:
            raise RuntimeError(
                "No end_bond-torsion_3 parameters for "
                + "{}-{}-{}-{}".format(i, j, k, l)
            )

    def middle_bond_torsion_3_parameters(self, i, j, k, l, zero=False):  # noqa: E741
        """Return the middle bond - torsion_3 parameters given four atom types

        Handle equivalences
        """
        # Get the reference bond lengths...
        b1_type, b1_types, b1_form, b1_parameters = self.bond_parameters(j, k)
        values = {"R0": b1_parameters["R0"]}

        # parameters directly available
        result = self._torsion_parameters_helper(
            i, j, k, l, self.ff["middle_bond-torsion_3"]
        )
        if result is not None:
            values.update(result[2])
            self.cite_parameter(values)
            return ("explicit", result[0], "middle_bond-torsion_3", values)

        # try equivalences
        if "equivalence" in self.ff:
            ieq = self.ff["equivalence"][i]["torsion"]
            jeq = self.ff["equivalence"][j]["torsion"]
            keq = self.ff["equivalence"][k]["torsion"]
            leq = self.ff["equivalence"][l]["torsion"]
            result = self._torsion_parameters_helper(
                ieq, jeq, keq, leq, self.ff["middle_bond-torsion_3"]
            )
            if result is not None:
                values.update(result[2])
                self.cite_parameter(values)
                return ("equivalent", result[0], "middle_bond-torsion_3", values)

        if zero:
            return (
                "zeroed",
                ("*", "*", "*", "*"),
                "middle_bond-torsion_3",
                {"R0": "1.5", "V1": "0.0", "V2": "0.0", "V3": "0.0"},
            )
        else:
            raise RuntimeError(
                "No middle_bond-torsion_3 parameters for "
                + "{}-{}-{}-{}".format(i, j, k, l)
            )

    def angle_torsion_3_parameters(self, i, j, k, l, zero=False):  # noqa: E741
        """Return the angle - torsion_3 parameters given four atom types

        Handle equivalences
        """
        # Get the reference bond angles...
        a1_type, a1_types, a1_form, a1_parameters = self.angle_parameters(i, j, k)
        a2_type, a2_types, a2_form, a2_parameters = self.angle_parameters(j, k, l)
        values = {
            "Theta0_L": a1_parameters["Theta0"],
            "Theta0_R": a2_parameters["Theta0"],
        }

        # parameters directly available
        result = self._torsion_parameters_helper(i, j, k, l, self.ff["angle-torsion_3"])
        if result is not None:
            if result[1]:
                parameters = {
                    "reference": result[2]["reference"],
                    "V1_L": result[2]["V1_R"],
                    "V2_L": result[2]["V2_R"],
                    "V3_L": result[2]["V3_R"],
                    "V1_R": result[2]["V1_L"],
                    "V2_R": result[2]["V2_L"],
                    "V3_R": result[2]["V3_L"],
                    "Theta0_L": a2_parameters["Theta0"],
                    "Theta0_R": a1_parameters["Theta0"],
                }
                ii, jj, kk, ll = result[0]
                self.cite_parameter(parameters)
                return ("explicit", (ll, kk, jj, ii), "angle-torsion_3", parameters)
            else:
                parameters = dict(**result[2])
                parameters.update(values)
                self.cite_parameter(parameters)
                return ("explicit", result[0], "angle-torsion_3", parameters)

        # try equivalences
        if "equivalence" in self.ff:
            ieq = self.ff["equivalence"][i]["torsion"]
            jeq = self.ff["equivalence"][j]["torsion"]
            keq = self.ff["equivalence"][k]["torsion"]
            leq = self.ff["equivalence"][l]["torsion"]
            result = self._torsion_parameters_helper(
                ieq, jeq, keq, leq, self.ff["angle-torsion_3"]
            )
            if result is not None:
                if result[1]:
                    parameters = {
                        "reference": result[2]["reference"],
                        "V1_L": result[2]["V1_R"],
                        "V2_L": result[2]["V2_R"],
                        "V3_L": result[2]["V3_R"],
                        "V1_R": result[2]["V1_L"],
                        "V2_R": result[2]["V2_L"],
                        "V3_R": result[2]["V3_L"],
                        "Theta0_L": a2_parameters["Theta0"],
                        "Theta0_R": a1_parameters["Theta0"],
                    }
                    ii, jj, kk, ll = result[0]
                    self.cite_parameter(parameters)
                    return (
                        "equivalent",
                        (ll, kk, jj, ii),
                        "angle-torsion_3",
                        parameters,
                    )
                else:
                    parameters = dict(**result[2])
                    parameters.update(values)
                    self.cite_parameter(parameters)
                    return ("equivalent", result[0], "angle-torsion_3", parameters)

        if zero:
            parameters = {
                "V1_L": "0.0",
                "V2_L": "0.0",
                "V3_L": "0.0",
                "V1_R": "0.0",
                "V2_R": "0.0",
                "V3_R": "0.0",
                "Theta0_L": "109.0",
                "Theta0_R": "109.0",
            }
            return ("zeroed", ("*", "*", "*", "*"), "angle-torsion_3", parameters)
        else:
            raise RuntimeError(
                "No angle-torsion_3 parameters for " + "{}-{}-{}-{}".format(i, j, k, l)
            )

    def angle_angle_torsion_1_parameters(self, i, j, k, l, zero=False):  # noqa: E741
        """Return the angle - angle - torsion_1 parameters given four atom types

        Handle equivalences
        """
        # Get the reference bond angles...
        a1_type, a1_types, a1_form, a1_parameters = self.angle_parameters(i, j, k)
        a2_type, a2_types, a2_form, a2_parameters = self.angle_parameters(j, k, l)
        values = {
            "Theta0_L": a1_parameters["Theta0"],
            "Theta0_R": a2_parameters["Theta0"],
        }

        # parameters directly available
        result = self._torsion_parameters_helper(
            i, j, k, l, self.ff["angle-angle-torsion_1"]
        )
        if result is not None:
            values.update(result[2])
            self.cite_parameter(values)
            return ("explicit", result[0], "angle-angle-torsion_1", values)

        # try equivalences
        if "equivalence" in self.ff:
            ieq = self.ff["equivalence"][i]["torsion"]
            jeq = self.ff["equivalence"][j]["torsion"]
            keq = self.ff["equivalence"][k]["torsion"]
            leq = self.ff["equivalence"][l]["torsion"]
            result = self._torsion_parameters_helper(
                ieq, jeq, keq, leq, self.ff["angle-angle-torsion_1"]
            )
            if result is not None:
                values.update(result[2])
                self.cite_parameter(values)
                return ("equivalent", result[0], "angle-angle-torsion_1", values)

        if zero:
            parameters = {"Theta0_L": "109.0", "Theta0_R": "109.0", "K": "0.0"}
            return ("zeroed", ("*", "*", "*", "*"), "angle-angle-torsion_1", parameters)
        else:
            raise RuntimeError(
                "No angle-angle-torsion_1 parameters for "
                + "{}-{}-{}-{}".format(i, j, k, l)
            )

    def get_templates(self):
        """Return the templates dict"""
        if "templates" in self.ff:
            return self.ff["templates"]
        else:
            return {}

    def get_fragments(self):
        """Return the fragments dict"""
        if "fragments" in self.ff:
            return self.ff["fragments"]
        else:
            return {}

    def energy_expression(self, configuration, style="LAMMPS", ff_form=None):
        """Create the energy expression for the given structure

        Parameters
        ----------
        configuration : _Configuration
            Which configuration of the system.
        style : str = ''
            The style of energy expression. Currently only 'LAMMPS' is
            supported.
        ff_form : str = None
            The functional form of the forcefield. If None, it is derived from the name
            of the forcefield.

        Returns
        -------
        eex : {str: []}
            The energy expression as a dictionary of terms
        """
        logger.debug("Creating the eex")

        eex = {}

        # The functional form of the forcefield
        if ff_form is None:
            ff_form = self.ff_form

        # The terms in the forcefield
        eex["terms"] = deepcopy(self.ff["terms"])

        sys_atoms = configuration.atoms

        # We will need the elements for fix shake, 1-based.
        eex["elements"] = [""]
        eex["elements"].extend(sys_atoms.symbols)

        # The periodicity & cell parameters
        periodicity = eex["periodicity"] = configuration.periodicity
        if periodicity == 3:
            eex["cell"] = configuration.cell.parameters

        self.setup_topology(configuration, style, ff_form)

        self.eex_atoms(eex, configuration)
        logger.debug(f'    forcefield terms: {self.ff["terms"]}')
        for term in self.ff["terms"]:
            function_name = "eex_" + term.replace("-", "_")
            function_name = function_name.replace(" ", "_")
            function_name = function_name.replace(",", "_")
            function = getattr(self, function_name, None)
            if function is None:
                print("Function {} does not exist yet".format(function_name))
            else:
                function(eex, configuration)

        if ff_form == "dreiding":
            # Handle hbonds for Drieding, which overwrites nonbonds too.
            self.dreiding_hydrogen_bonds(eex, configuration)

        return eex

    def setup_topology(self, configuration, style, ff_form):
        """Create the list of bonds, angle, torsion, etc. for the configuration

        This topology information is held in self.topology.

        Parameters
        ----------
        configuration : int = None
            Which configuration. Defaults to the current_configuration.
        style : str
            The style of energy expression. Currently only 'LAMMPS' is
            supported.
        ff_form : str
            The functional form or type of forcefield.

        Returns
        -------
        None
        """
        self.topology = {}

        sys_atoms = configuration.atoms
        sys_bonds = configuration.bonds

        n_atoms = sys_atoms.n_atoms
        self.topology["n_atoms"] = n_atoms

        # Need the transformation from atom ids to indices
        atom_ids = sys_atoms.ids
        to_index = {j: i + 1 for i, j in enumerate(atom_ids)}

        # extend types with a blank so can use 1-based indexing
        if self.ff_form != "reaxff":
            types = self.topology["types"] = [""]
            key = f"atom_types_{self.current_forcefield}"
            types.extend(sys_atoms.get_column(key))

        # bonds
        bonds = self.topology["bonds"] = [
            (to_index[row["i"]], to_index[row["j"]]) for row in sys_bonds.bonds()
        ]

        # Bond orders
        if ff_form in ("dreiding",):
            bond_orders = self.topology["bond orders"] = {
                (to_index[row["i"]], to_index[row["j"]]): row["bondorder"]
                for row in sys_bonds.bonds()
            }
            bond_orders.update(
                {
                    (to_index[row["j"]], to_index[row["i"]]): row["bondorder"]
                    for row in sys_bonds.bonds()
                }
            )

        # atoms bonded to each atom i
        self.topology["bonds_from_atom"] = configuration.bonded_neighbors(
            as_indices=True, first_index=1
        )
        bonds_from_atom = self.topology["bonds_from_atom"]

        # angles
        angles = self.topology["angles"] = []
        for j in range(1, n_atoms + 1):
            for i in bonds_from_atom[j]:
                for k in bonds_from_atom[j]:
                    if i < k:
                        angles.append((i, j, k))

        # torsions
        torsions = self.topology["torsions"] = []
        for j, k in bonds:
            for i in bonds_from_atom[j]:
                if i == k:
                    continue
                for l in bonds_from_atom[k]:  # noqa: E741
                    if l == j:  # noqa: E741
                        continue
                    if i == l:
                        # 3 membered rings.
                        continue
                    torsions.append((i, j, k, l))

        # Out-of-planes
        oops = self.topology["oops"] = []
        if ff_form == "dreiding":
            for m in range(1, n_atoms + 1):
                if len(bonds_from_atom[m]) == 3:
                    i, j, k = bonds_from_atom[m]
                    oops.append((i, m, j, k))
                    oops.append((j, m, i, k))
                    oops.append((k, m, i, j))
        else:
            for m in range(1, n_atoms + 1):
                if len(bonds_from_atom[m]) == 3:
                    i, j, k = bonds_from_atom[m]
                    oops.append((i, m, j, k))
        if ff_form == "class2":
            for m in range(1, n_atoms + 1):
                if len(bonds_from_atom[m]) == 4:
                    i, j, k, l = bonds_from_atom[m]  # noqa: E741
                    oops.append((i, m, j, k))
                    oops.append((i, m, j, l))
                    oops.append((i, m, k, l))
                    oops.append((j, m, k, l))

    def assign_forcefield(self, configuration):
        """Assign the forcefield to the structure, i.e. find the atom types
        and charges.

        Parameters
        ----------
        configuration : Configuration
            The configuration to assign.

        Returns
        -------
        None
        """
        if self.ff_form in ("reaxff",):
            return

        ffname = self.current_forcefield

        total_charge = configuration.charge

        # Atom types
        logger.debug("Atom typing, getting the SMILES for the system")

        ff_assigner = FFAssigner(self)
        atom_types = ff_assigner.assign(configuration)
        logger.info("Atom types: " + ", ".join(atom_types))
        key = f"atom_types_{ffname}"
        if key not in configuration.atoms:
            configuration.atoms.add_attribute(key, coltype="str")
        configuration.atoms[key] = atom_types

        # Get any charges. First see if there are any templates
        n_atoms = configuration.n_atoms
        charges = [None] * n_atoms
        molecule = configuration.to_RDKMol()
        fragments = self.get_fragments()
        for smiles, data in fragments.items():
            if "charges" not in data:
                continue

            smarts = data["SMARTS"]
            pattern = rdkit.Chem.MolFromSmarts(smarts)
            matches = molecule.GetSubstructMatches(pattern, maxMatches=6 * n_atoms)
            for match in matches:
                for charge, atom in zip(data["charges"], match):
                    # Check if this has been assigned by another fragment
                    if charges[atom] is not None:
                        if charge != charges[atom]:
                            msg = (
                                f"Error in fragment charges for atom {atom} "
                                f"already has charge:\n{charges[atom]}\n"
                                f"New assignment: {charge}"
                            )
                            logger.error(msg)
                            raise ForcefieldChargeError(msg)
                    charges[atom] = charge

        # Now get the charges from increments and charges in the forcefield
        terms = self.terms
        if "bond charge increment" in terms:
            logger.debug("Getting the charges for the system")
            neighbors = configuration.bonded_neighbors(as_indices=True)

            logger.debug(f"{atom_types=}")
            logger.debug(f"{neighbors=}")

            total_q = 0.0
            for i, itype in enumerate(atom_types):
                if charges[i] is None:
                    parameters = self.charges(itype)[3]
                    q = float(parameters["Q"])
                    for j in neighbors[i]:
                        jtype = atom_types[j]
                        parameters = self.bond_increments(itype, jtype)[3]
                        q += float(parameters["deltaij"])
                    charges[i] = q
                total_q += charges[i]
            if abs(total_q - total_charge) > 0.001:
                delta = (total_q - total_charge) / len(charges)
                charges = [q - delta for q in charges]
                logger.warning(
                    f"The total charge from the forcefield, {total_q:3f}, does not "
                    f"match the formal charge, {total_charge}."
                    f"\nAdjusted each atom's charge by {-delta:.3f} to compensate."
                )
            logger.debug("Charges from increments:\n" + pprint.pformat(charges))

            key = f"charges_{ffname}"
            if key not in configuration.atoms:
                configuration.atoms.add_attribute(key, coltype="float")
            charge_column = configuration.atoms.get_column(key)
            charge_column[0:] = charges
            logger.debug(f"Set column '{key}' to the charges")
        elif "atomic charge" in terms:
            logger.debug("Getting the charges for the system")

            total_q = 0.0
            if "shell model" in terms:
                # Use charges from shell model by preference.
                for i, itype in enumerate(atom_types):
                    if charges[i] is None:
                        tmp = self.shell_model(itype)
                        if tmp is None:
                            # Fall back to charges
                            parameters = self.charges(itype)[3]
                            q = float(parameters["Q"])
                            charges[i] = q
                        else:
                            parameters = tmp[3]
                            q = float(parameters["Q"])
                            y = float(parameters["Y"])
                            charges[i] = q - y
                    total_q += charges[i]
            else:
                for i, itype in enumerate(atom_types):
                    if charges[i] is None:
                        parameters = self.charges(itype)[3]
                        q = float(parameters["Q"])
                        charges[i] = q
                    total_q += charges[i]
            if abs(total_q - total_charge) > 0.001:
                delta = (total_q - total_charge) / len(charges)
                charges = [q - delta for q in charges]
                logger.warning(
                    f"The total charge from the forcefield, {total_q:3f}, does not "
                    f"match the formal charge, {total_charge}."
                    f"\nAdjusted each atom's charge by {-delta:.3f} to compensate."
                )
            logger.debug("Charges from charges:\n" + pprint.pformat(charges))

            key = f"charges_{ffname}"
            if key not in configuration.atoms:
                configuration.atoms.add_attribute(key, coltype="float")
            charge_column = configuration.atoms.get_column(key)
            charge_column[0:] = charges
            logger.debug(f"Set column '{key}' to the charges")

    def cite_parameter(self, data, level=2):
        """Add citations from the reference associated with a parameter

        Parameters
        ----------
        data : dict
            The ff data for the parameter
        level : int (optional)
            The citation level, defaults to 2.
        """
        if self.references is not None and "reference" in data:
            ref = data["reference"]
            if ref in self.data["reference"]:
                refdata = self.data["reference"][ref]
                for citation, bibtex in refdata["citations"].items():
                    if citation not in self._citations:
                        forcefield = self.current_forcefield
                        self.references.cite(
                            raw=bibtex,
                            alias=citation,
                            module="forcefield",
                            level=level,
                            note=f"Forcefield '{forcefield}' reference #{ref}",
                        )
                        self._citations.add(citation)
