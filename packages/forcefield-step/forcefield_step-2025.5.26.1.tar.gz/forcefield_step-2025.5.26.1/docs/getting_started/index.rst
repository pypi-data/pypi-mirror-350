***************
Getting Started
***************

Installation
============
The Forcefield step is probably already installed in your SEAMM environment, but
if not or if you wish to check, follow the directions for the `SEAMM Installer`_. The
graphical installer is the easiest to use. In the SEAMM conda environment, simply type::

  seamm-installer

or use the shortcut if you installed one. Switch to the second tab, `Components`, and
check for `forcefield-step`. If it is not installed, or can be updated, check the box
next to it and click `Install selected` or `Update selected` as appropriate.

The non-graphical installer is also straightforward::

  seamm-installer install --update forcefield-step

will ensure both that it is installed and up-to-date.

.. _SEAMM Installer: https://molssi-seamm.github.io/installation/index.html

Intoduction to the Forcefield Step
==================================
The Forcefield Step is used to read a forcefield into SEAMM and set it as the default
forcefield until another Forcefield Step changes the default. You can also use the
Forcefield Step to assign the forcefield to your system, though the assignment will also
be done automatically when needed so you do not need to explicitly ask the Forcefield
Step to do the assignment.

The Forcefield Step resides in the Simulation section of the Flowchart. Typically it is
one of the firt couple steps in a Flowchart, defining the forcefield to be used by
subsequent steps:

.. figure:: images/initial.png
   :align: center
   :alt: A flowchart with a Forcefield Step
   
   A flowchart with a single Forcefield Step

Opening the Forcefield Step gives this dialog:

.. figure:: images/dialog.png
   :align: center
   :alt: The initial forcefield dialog
   
   The initial forcefield dialog

The first field, "What to do:", allows you to setup a forcefield or to assign it to the
current system, as mentioned above. The second, "Forcefield Repository", is used to
select the type of forcefield to setup:

.. figure:: images/ff_choices.png
   :align: center
   :alt: The forcefield choices
   
   The choice of forcefield to set up.

There are currently four main possibilities:

   #. OpenKIM_ is an online repository that contains many of the "interatomic potentials"
      used for materials simulations. These are potentials such as the Stillinger-Webber
      potential for silicon, the potentials for the embedded atom method (EAM), and
      those for the modified embedded atom method (MEAM).

   #. OPLS-AA_, the Optimized Potentials for Liquid Simulations -- All Atoms forcefield
      of William Jorgensen and et al. [#]_, has wide coverage of organic and
      biomolecular systems.

   #. PCFF2018_, the Polymer Consistent Force Field [#]_,also covers organic molecules
      with an emphasis on (synthetic) polymers.

   #. local:OPLS_AA/ligpargen.frc contains parameters that the user has downloaded from
      the LigParGen server. See the :ref:`LigParGen` section in the :ref:`User Guide
      <user-guide>` for more information.

Your installation may have a different set of forcefields than shown above. Once you
have setup a forcefield you can proceed to e.g. LAMMPS to run the simulation using the
forcefield.

That should be enough to get started. For more detail about the functionality in this
plug-in, see the :ref:`User Guide <user-guide>`.


.. [#] W.L. Jorgensen, J. Tirado-Rives,
       Potential energy functions for atomic-level simulations of water and organic and
       biomolecular systems,
       Proc. Natl. Acad. Sci. 102 (2005) 6665–6670.
       https://doi.org/10.1073/pnas.0408037102.
       
.. [#] Huai Sun, Stephen J. Mumby, Jon R. Maple, and Arnold T. Hagler,
       An ab Initio CFF93 All-Atom Force Field for Polycarbonates
       Journal of the American Chemical Society 1994 116 (7), 2978-2987
       DOI: 10.1021/ja00086a030

.. _OPLS-AA: https://doi.org/10.1073/pnas.0408037102
.. _OpenKIM: https://www.openkim.org
.. _PCFF2018: https://pubs.acs.org/doi/10.1021/ja00086a030
