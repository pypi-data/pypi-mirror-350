.. _user-guide:

**********
User Guide
**********
The Forcefield plug-in manages one or more forcefields or sets of interatomic potentials
for your simulations. It reads a forcefield file, selects a particular forcefield from
the file, and prepares the forcefield parameters for susbsequent simulation steps. This
step can also be used to assign the forcefield to the molecule or system that you are
working on, though that happens by default when you start the simulation, so you don't
need to handle it explicitly.

If you want to understand more about the theory and definition of forcefields, see the
`Overview of Forcefields`_ in the main SEAMM documentation.

The following sections cover accessing and controlling forcefields.

.. toctree::
   :maxdepth: 2
   :titlesonly:

   ligpargen/index

Index
=====

* :ref:`genindex`


.. _Overview of Forcefields:  https://molssi-seamm.github.io/background/forcefields/overview.html
