********
Overview
********
The heart of the main webpage is this section:

.. figure:: images/ligpargen.png
   :align: center
   :alt: The LigParGen webpage
   
   The LigParGen Webpage

At the top you enter your structure as either SMILES or a Mol or PDB file. After
choosing the charge model and specifying the charge, if any, click on **Submit
Molecule**. For example, if you enter **CC** for ethane as the SMILES, select the **1.14*
CMA1-LBCC** charge model and submit it, you will be sent to a page where you can
download the parameters in formats suitable for various simulation codes. The **KEY**
file for Tinker is easy to read if  bit verbose:

.. include:: images/ethane.key
   :literal:
