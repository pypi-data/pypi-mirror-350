=======
History
=======
2025.5.23 -- Added charges in templates and tracking original parameters
   * Added charges in templates, which override any assignment from the bond increments
     or charges for the atom types.
   * Track the original parameters before any unit conversions or other transformations,
     so that they can be printed along with the actual parameters used by e.g. LAMMPS.
   * Improved checking for duplicate parameters in the energy expression.

2025.4.7 -- Added ability to handle ReaxFF forcefields
   * Added code to handle ReaxFF forcefield.
   * Added seamm-reaxff utility to import forcefields in the standard Reax/LAMMPS format
     into SEAMM's format.
   * Added handling of a metadata section in the forcefields to be able to support the
     various types of forcefields.

2025.3.16 -- Added handling of Dreiding forcefield.

2025.1.21 -- Bugfix: torsions in 3-membered rings
   * The code allowed the torsion around a 3-membered ring which had the same atom at
     each end of the torsion. This is not a valid torsion, and the code now checks for
     it and removes it.

2024.6.27 -- Support for local forcefield files
   * Added support for local forcefields files which can either be used directly
     or included by existing files.
   * Added URI handler to support local files
   * Added support for BibTex references in forcefield files, and automatically adding
     citations to the Reference Handler.
   * Add 'fragments' section to forcefields for atom-typing via a fragment or entire
     molecule. This supports using LigParGen for OPLS-AA forcefields.

2023.8.27 -- Added support for tabulated angle potentials

2023.4.6 -- Added support for Buckingham potentials
   * Also improved unit handling across all terms in forcefields.

2023.3.5 -- Added molecule numbers for LAMMPS input
   * Added the molecule number for each atom for when using LAMMPS

2023.2.6 -- Added handling of OPLS-AA forcefield
   * Added handling of the OPLS-AA forcefield
   * Moved documentation to new MolSSI theme and diátaxis layout
   * Cleaned up internal dependencies and workflows for GitHub

2022.5.29 -- Fixed bug typing larger systems
   * Fixed bug with atom typing due to limit in matches. by @paulsaxe in #59

2022.2.3 -- Fixed bug due to changing ordering of atoms.
   * Fixed bug with atom type assignment due to changed order of atoms. In the process,
     switch to using RDKit directly, which is both more direct and avoids the ordering
     problem.

0.1.0 -- (2017-12-05)
   * First release on PyPI.
