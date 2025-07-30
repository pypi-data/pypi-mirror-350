=======
History
=======
2025.5.26 -- Updated the OPLS-AA forcefield file to allow personal versions
   * Updated the OPLS-AA forcefield to support an optional local user file
     'my_oplsaa.frc' to add to or override parameters in the main file.
   * Fixed issues in the ligpargen utility due to changes in the SMILES routines in
     SEAMM.

2025.4.7 -- Added a number of ReaxFF forcefields.
   * Added the ReaxFF forcefields from LAMMPS, plus two from lithium battery work.
   * Added metadata sections to the forcefield to better support the features of
     different forcefields.
   * Improved the listing and display of available forcefields, and made it dynamic so
     that forcefields added locally are immediately found without needing to restart
     SEAMM.
       
2025.4.1 -- Added support for ReaxFF, which does not need atom type assignment.

2025.3.18 -- Added bis(fluorosulfonyl)imide anion (FSI) to the OPLS-AA and CL&P forcefields
  * Added parameters for the bis(fluorosulfonyl)imide anion (FSI) to the OPLS-AA and
    CL&P forcefields.
  * Added a test for FSI in the test suite.
    
2025.3.16 -- Added the Dreiding forcefield

2024.12.14 -- Updated for changes in SMILES handling
  * Changes in the handling of SMILES in MolSystem required small changes in the tests
    to continue using Open Babel for SMILES.
    
2024.10.25 -- Changed the default forcefield to OPLSAA

2024.6.30 -- Bugfix: Error submitting jobs with local forcefield files.

2024.6.29 -- Bugfix: factor of 2 for dihedrals and impropers in ligpargen
  * The ligpargen tool was missing a factor of 2 in the dihedral and improper parameters.
  * Corrected the search paths for forcefields.
  * Improved the documentation.
    
2024.6.28 -- Added customizable local forcefields and LigParGen interface.
  * Added the machinery to handle local forcefield files in either
    ~/.seamm.d/data/Forcefields (personal) or ~/SEAMM/data/Forcefields (site).
  * Added 'ligpargen' command to access custom parameters from the LigParGen service
    at Yale University, ading them to the 'ligpargen.frc' personal forcefield, which
    is automatically included in 'oplsaa.frc' if it exists.

2024.1.10 -- Fixed PF6- issue in CL&P forcefield
  * The angle parameters for PF6- in the CL&P forcefield only work if the 180º F-P-F
    angles are not included in the calculation. Replacing them with an equivalent
    periodic SHAPES-like potential almost works; however, since 0º is a valid angle and
    there are no 1-3 nonbonds, nothing keeps the F atoms apart. This is solved using a
    tabulated potential based on the SHAPES potential but with an added 1-3 repulsion
    large enough that the gradient is always pusing small angles apart, but not large
    enough to affect the minimum at 90º.

2023.9.14 -- Fixed errors! And added C2mim to test.
  * The units of the torsions were incorrect in the last implementation.
  * Added parameters for 1-alkyl-3-methylimidazolium cations from JCP 108, 2038 (2004)
  * Tested much more thoroughly.

2023.9.13 -- Added parameters for TFSI to  CL&P/OPLSAA
  * Parameters for TFSI - bis[(trifluoromethyl)sulfonyl]imide

2023.9.8 -- Added more typing for OPLS-AA
  * cyclopropane -CH2-, -CHR-, and -CR2-
  * hexafluorobenzene
  * difluorobenzene
  * bromobenzene
  * iodobenzene
  * thiophenol
  * alkyl nitriles
  * nitroalkanes
  * nitrobenzene
  * methylene in phenylacetonitrile
  * corrections to methylene nitrile anion

2023.9.7 -- Added typing in OPLS_AA for fluorobenzene

2023.9.6 -- Fixed issue with PF6- geometry
  * The Lennard-Jones repulsive term added to the F-P-F angle was too weak, allowing the
    structure to get trapped in a symmetric state with ~40º angles.

2023.8.27 -- Fixed issue with angle in octahedral systems
  * The SHAPES-type simple fourier potential used for octahedral complexes has a fals
    minimim at 0º. Added a LJ 1/R^12 repulsive term between the two end atoms of the
    angle to prevent small angles. This required using tabulated potentials in LAMMPS.
    
2023.5.1 -- Fixed bug in Lithium battery forcefield
  * Fixed a typo in the angle type unit line which caused a crash
    
2023.4.6 -- Added Lithium battery forcefield
  * An initial set of parameters for cathode materials, specifically LiCoO2.

2023.2.13 -- Added OPLS-AA forcefield
  * Added parameters for OPLS-AA along with some extra parameters for ionic liquids
    * PF6-
    * ethylene carbonate (EC) and fluoronated EC (FEC)
  * Added atom-typing templates for most of OPLS-AA. Still missing a few and amino
    acids and DNA not yet tested.
  * Added extensive, almost-complete testing, for OPLS-AA
    

2021.2.10 (10 February 2021)
----------------------------

* Updated the README file to give a better description.
* Updated the short description in setup.py to work with the new installer.
* Added keywords for better searchability.

2020.8.1 (1 August 2020)
------------------------

* Added support for OpenKIM potentials in LAMMPS

0.9.1 (24 May 2020)
-------------------

* Added the specialized NaCl_water forcefield for testing the MolSSI
  Driver Interface (MDI) metadynamics driver.

0.9 (15 April 2020)
-------------------

* Internal changes for compatibility
  
0.1.0 (24 December 2017)
------------------------

* First release on PyPI.
