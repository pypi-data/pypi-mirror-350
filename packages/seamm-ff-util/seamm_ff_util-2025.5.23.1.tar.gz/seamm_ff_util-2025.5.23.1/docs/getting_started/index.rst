***************
Getting Started
***************

Installation
============
The SEAMM Forcefield Utilities (seamm_ff_util) are probably already installed in your
SEAMM environment, but if not or if you wish to check, follow the directions for the
`SEAMM Installer`_. The graphical installer is the easiest to use. In the SEAMM conda
environment, simply type::

  seamm-installer

or use the shortcut if you installed one. Switch to the second tab, `Components`, and
check for `seamm-ff-util`. If it is not installed, or can be updated, check the box
next to it and click `Install selected` or `Update selected` as appropriate.

The non-graphical installer is also straightforward::

  seamm-installer install --update seamm-ff-util

will ensure both that it is installed and up-to-date.

.. _SEAMM Installer: https://molssi-seamm.github.io/installation/index.html

Ther are no user-accessible functions in this library. See the :ref:`Developer Guide
<developer-guide>` for more information about using the library in codes.
