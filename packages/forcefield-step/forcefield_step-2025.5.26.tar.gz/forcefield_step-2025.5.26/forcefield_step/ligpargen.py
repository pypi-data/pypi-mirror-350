import datetime
import getpass
import json
from pathlib import Path

from molsystem.elements import to_symbols
from molsystem.system_db import SystemDB
import pyperclip
import read_structure_step
import rdkit
from tabulate import tabulate

ff_template = """!MolSSI forcefield 1

#define ligpargen

! Version  Ref                Function             Label
!--------- ---    ------------------------------   ------
2024.06.16 101    atom_types                       ligpargen
2024.06.16 101    charges                          ligpargen
2024.06.16 101    nonbond(12-6)                    ligpargen
2024.06.16 101    quadratic_bond                   ligpargen
2024.06.16 101    quadratic_angle                  ligpargen
2024.06.16 101    torsion_opls                     ligpargen
2024.06.16 101    improper_opls                    ligpargen
2024.06.16 101    fragments                        ligpargen

#atom_types           ligpargen

> Atom type definitions for any variant of OPLS-AA

! Version   Ref    Type       Mass  El  # conns           Comment
!---------- ---  --------   ------  --  ------- ---------------------------

#charges ligpargen
! Version   Ref     I      Charge
!---------  ---  -------  --------

#nonbond(12-6)         ligpargen
> E = 4 * eps(ij) * [(sigma(ij)*/r(ij))**12 - (sigma(ij)*/r(ij))**6]
>
> where    sigma(ij) = sqrt(sigma(i) * sigma(j)
>
>            eps(ij) = sqrt(eps(i) * eps(j))

@type sigma-eps
@combination geometric

! Version   Ref     I       sigma     eps
!---------  ---  -------  --------  --------

#quadratic_bond       ligpargen
> E = K2 * (R - R0)^2

! Version   Ref     I         J         R0        K2
!---------  ---  --------  --------  --------  --------

#quadratic_angle       ligpargen
> E = K2 * (Theta - Theta0)^2

! Version   Ref     I         J         K       Theta0     K2
!---------  ---  --------  --------  --------  --------  --------

#torsion_opls       ligpargen
> E = 1/2*V1*[1 + cos(phi1)]
>   + 1/2*V2*[1 - cos(2*phi2)]
>   + 1/2*V3*[1 + cos(3*phi3)]
>   + 1/2*V4*[1 - cos(4*phi4)]

! Version   Ref     I         J         K         L        V1      V2      V3      V4
!---------  ---  --------  --------  --------  --------  ------  ------  ------  ------

#improper_opls       ligpargen
> E = 1/2*V2*[1 - cos(2*phi2)]

> k is the central atom

! Version   Ref     I         J         K         L        V2
!---------  ---  --------  --------  --------  --------  ------

#fragments ligpargen
{
}

#reference 101
@Author Paul Saxe
@Date 2024-06-16
Template for OPLS-AA Library
#end
"""


def reader(path):
    """Reads the .key file and returns the data

    This method reads the .key file output by LigParGen and adds the
    parameters to the local SEAMM forcefield ligpargen.frc file.

    Parameters
    ----------
    path : str or pathlib.Path
        The path to the .key or .xyz files

    Note
    ----
    The .key file is a text file that contains the forcefield parameters for
    Tinker. It looks like this::



              ##############################
              ##                          ##
              ##  Force Field Definition  ##
              ##                          ##
              ##############################


        forcefield              OPLS-AA

        vdwindex                TYPE
        vdwtype                 LENNARD-JONES
        radiusrule              GEOMETRIC
        radiustype              SIGMA
        radiussize              DIAMETER
        epsilonrule             GEOMETRIC
        torsionunit             1.0
        imptorunit              1.0
        vdw-14-scale            2.0
        chg-14-scale            2.0
        electric                332.06
        dielectric              1.0


              #############################
              ##                         ##
              ##  Atom Type Definitions  ##
              ##                         ##
              #############################


        atom        800  800    CT    "C00"          6     12.011     4
        atom        801  801    CZ    "C01"          6     12.011     2
        atom        802  802    NZ    "N02"          7     14.007     1
        atom        803  803     F    "F03"          9     18.998     1
        atom        804  804    HC    "H04"          1      1.008     1
        atom        805  805    HC    "H05"          1      1.008     1



              ################################
              ##                            ##
              ##  Van der Waals Parameters  ##
              ##                            ##
              ################################


        vdw         800           3.5000   0.0660
        vdw         801           3.3000   0.0660
        vdw         802           3.2000   0.1700
        ...

    The interesting keys are:
        - atom: defines the atom types
        - vdw: defines the van der Waals parameters
        - bond: defines the bond parameters
        - angle: defines the angle parameters
        - torsion: defines the torsion parameters
        - imptors: defines the improper torsion parameters
        - charge: defines the charge parameters
    """
    if isinstance(path, str):
        path = Path(path)

    lines = path.read_text().splitlines()

    section = {}
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if line.startswith("#"):
            continue
        tmp = line.split()
        key = tmp[0]
        if key in section:
            section[key].append(tmp[1:])
        else:
            section[key] = [tmp[1:]]

    return section


def add_to_ff(ff, configuration, data):
    """Adds the data to the forcefield file

    This method adds the data from the .key file to the forcefield file.

    Parameters
    ----------
    ff : list
        The list of strings that make up the forcefield file
    configuration : Configuration
        The configuration object
    data : dict
        The data read from the .key file

    Returns
    -------
    str
        The updated forcefield file
    """
    try:
        name = configuration.PC_iupac_name()
    except Exception:
        name = None
    inchikey = configuration.inchikey
    canonical_smiles = configuration.to_smiles(canonical=True)
    smarts = configuration.to_smiles(hydrogens=True)

    # Find the next available reference number
    ref = 0
    for line in ff.splitlines():
        if line.startswith("#reference"):
            tmp = int(line.split()[1])
            if tmp > ref:
                ref = tmp
    ref += 1

    ikey = inchikey.split("-")[0]
    version = datetime.date.today().strftime("%Y.%m.%d")
    result = []
    section = None
    columns = {}
    entry_lines = []
    lines = iter(ff.splitlines())
    for line in lines:
        if line.startswith("#"):
            if section is not None:
                # Add the new data and print to the file
                if section == "atom_types":
                    neighbors = configuration.bonded_neighbors(as_indices=True)
                    nbonds = [str(len(x)) for x in neighbors]
                    atom_types = []
                    for atom, nb in zip(data["atom"], nbonds):
                        symbol = to_symbols([int(atom[4])])[0]
                        columns["Version"].append(version)
                        columns["Ref"].append(ref)
                        columns["Type"].append(ikey + "_" + atom[0])
                        columns["Mass"].append(atom[5])
                        columns["El"].append(symbol)
                        columns["# conns"].append(nb)
                        columns["Comment"].append("?")
                        atom_types.append(ikey + "_" + atom[0])
                    align = (
                        "center",
                        "right",
                        "left",
                        "decimal",
                        "left",
                        "center",
                        "left",
                    )
                elif section == "charges":
                    for charge in data["charge"]:
                        columns["Version"].append(version)
                        columns["Ref"].append(ref)
                        columns["Type"].append(ikey + "_" + charge[0])
                        columns["Charge"].append(charge[1])
                    align = ("center", "right", "left", "decimal")
                elif section == "nonbond(12-6)":
                    for vdw in data["vdw"]:
                        columns["Version"].append(version)
                        columns["Ref"].append(ref)
                        columns["Type"].append(ikey + "_" + vdw[0])
                        columns["Sigma"].append(vdw[1])
                        columns["Epsilon"].append(vdw[2])
                    align = ("center", "right", "left", "decimal", "decimal")
                elif section == "quadratic_bond":
                    for bond in data["bond"]:
                        columns["Version"].append(version)
                        columns["Ref"].append(ref)
                        columns["I"].append(ikey + "_" + bond[0])
                        columns["J"].append(ikey + "_" + bond[1])
                        columns["R0"].append(bond[3])
                        columns["K2"].append(bond[2])
                    align = ("center", "right", "left", "left", "decimal", "decimal")
                elif section == "quadratic_angle":
                    for angle in data["angle"]:
                        columns["Version"].append(version)
                        columns["Ref"].append(ref)
                        columns["I"].append(ikey + "_" + angle[0])
                        columns["J"].append(ikey + "_" + angle[1])
                        columns["K"].append(ikey + "_" + angle[2])
                        columns["Theta0"].append(angle[4])
                        columns["K2"].append(angle[3])
                    align = (
                        "center",
                        "right",
                        "left",
                        "left",
                        "left",
                        "decimal",
                        "decimal",
                    )
                elif section == "torsion_opls":
                    for torsion in data["torsion"]:
                        it, jt, kt, lt, v1, _, _, v2, _, _, v3, _, _ = torsion
                        if it == "0" and jt == "0" and kt == "0" and lt == "0":
                            continue
                        # Tinker has a factor of 2 someplace.
                        v1 = str(round(2 * float(v1), 4))
                        v2 = str(round(2 * float(v2), 4))
                        v3 = str(round(2 * float(v3), 4))
                        columns["Version"].append(version)
                        columns["Ref"].append(ref)
                        columns["I"].append(ikey + "_" + it)
                        columns["J"].append(ikey + "_" + jt)
                        columns["K"].append(ikey + "_" + kt)
                        columns["L"].append(ikey + "_" + lt)
                        columns["V1"].append(v1)
                        columns["V2"].append(v2)
                        columns["V3"].append(v3)
                        columns["V4"].append("0.0")
                    align = (
                        "center",
                        "right",
                        "left",
                        "left",
                        "left",
                        "left",
                        "decimal",
                        "decimal",
                        "decimal",
                        "decimal",
                    )
                elif section == "improper_opls":
                    for imptor in data["imptors"]:
                        it, jt, kt, lt, v2, _, _ = imptor
                        if it == "0" and jt == "0" and kt == "0" and lt == "0":
                            continue
                        # Tinker has a factor of 2 someplace.
                        v2 = str(round(2 * float(v2), 4))
                        columns["Version"].append(version)
                        columns["Ref"].append(ref)
                        columns["I"].append(ikey + "_" + it)
                        columns["J"].append(ikey + "_" + jt)
                        columns["K"].append(ikey + "_" + kt)
                        columns["L"].append(ikey + "_" + lt)
                        columns["V2"].append(v2)
                    align = (
                        "center",
                        "right",
                        "left",
                        "left",
                        "left",
                        "left",
                        "decimal",
                    )
                elif section == "fragments":
                    fragments = json.loads("\n".join(entry_lines))

                    # Need to reorder the atom types to the order of the atoms
                    molecule = configuration.to_RDKMol()
                    pattern = rdkit.Chem.MolFromSmarts(smarts)
                    matches = molecule.GetSubstructMatches(pattern)
                    types = [atom_types[i] for i in matches[0]]

                    fragments[canonical_smiles] = {version: {}}
                    tmp = fragments[canonical_smiles][version]

                    if name is not None:
                        tmp["name"] = name
                    tmp["InChIKey"] = inchikey
                    tmp["SMILES"] = canonical_smiles
                    tmp["SMARTS"] = smarts
                    tmp["atom types"] = types
                    tmp["reference"] = ref

                    text = json.dumps(fragments, indent=4)
                    result.append(text)
                    result.append("")
                    entry_lines = []
                elif section == "reference":
                    pass
                else:
                    raise ValueError(f"Unknown section: {section}")

                if section == "fragments":
                    pass
                elif section == "reference":
                    pass
                else:
                    if len(columns["Version"]) > 0:
                        tlines = tabulate(
                            columns,
                            headers="keys",
                            tablefmt="simple",
                            colalign=align,
                        ).splitlines()
                        result.append("!" + tlines[0])
                        result.append("!" + tlines[1])
                        for tline in tlines[2:]:
                            result.append(" " + tline)
                    else:
                        tline = "!" + " ".join(columns.keys())
                        result.append(tline)
                        tline = "!" + " ".join(["-" * len(k) for k in columns.keys()])
                        result.append(tline)
                columns = {}

            # add a blank line and the new section header
            if section != "reference":
                result.append("")
            result.append(line)
            if section != "reference":
                result.append("")

            # See if this is a section that needs to be updated
            key = line.split()[0][1:]
            if key == "atom_types":
                section = key
                columns = {
                    "Version": [],
                    "Ref": [],
                    "Type": [],
                    "Mass": [],
                    "El": [],
                    "# conns": [],
                    "Comment": [],
                }
                # Reproduce any comment lines, etc, at beginnning
                result.extend(_copy_header(lines))
            elif key == "charges":
                section = key
                columns = {"Version": [], "Ref": [], "Type": [], "Charge": []}
                # Reproduce any comment lines, etc, at beginnning
                result.extend(_copy_header(lines))
            elif key == "nonbond(12-6)":
                section = key
                columns = {
                    "Version": [],
                    "Ref": [],
                    "Type": [],
                    "Sigma": [],
                    "Epsilon": [],
                }
                # Reproduce any comment lines, etc, at beginnning
                result.extend(_copy_header(lines))
            elif key == "quadratic_bond":
                section = key
                columns = {
                    "Version": [],
                    "Ref": [],
                    "I": [],
                    "J": [],
                    "R0": [],
                    "K2": [],
                }
                # Reproduce any comment lines, etc, at beginnning
                result.extend(_copy_header(lines))
            elif key == "quadratic_angle":
                section = key
                columns = {
                    "Version": [],
                    "Ref": [],
                    "I": [],
                    "J": [],
                    "K": [],
                    "Theta0": [],
                    "K2": [],
                }
                # Reproduce any comment lines, etc, at beginnning
                result.extend(_copy_header(lines))
            elif key == "torsion_opls":
                section = key
                columns = {
                    "Version": [],
                    "Ref": [],
                    "I": [],
                    "J": [],
                    "K": [],
                    "L": [],
                    "V1": [],
                    "V2": [],
                    "V3": [],
                    "V4": [],
                }
                # Reproduce any comment lines, etc, at beginnning
                result.extend(_copy_header(lines))
            elif key == "improper_opls":
                section = key
                columns = {
                    "Version": [],
                    "Ref": [],
                    "I": [],
                    "J": [],
                    "K": [],
                    "L": [],
                    "V2": [],
                }
                # Reproduce any comment lines, etc, at beginnning
                result.extend(_copy_header(lines))
            elif key == "fragments":
                section = key
                entry_lines = []
            elif key == "reference":
                section = key
            else:
                section = None
        else:
            if line == "" and section != "reference":
                pass
            else:
                if section == "atom_types":
                    tmp = line.split()
                    columns["Version"].append(tmp[0])
                    columns["Ref"].append(tmp[1])
                    columns["Type"].append(tmp[2])
                    columns["Mass"].append(tmp[3])
                    columns["El"].append(tmp[4])
                    if len(tmp) < 6:
                        columns["# conns"].append("?")
                    else:
                        columns["# conns"].append(tmp[5])
                    if len(tmp) < 7:
                        columns["Comment"].append("?")
                    else:
                        columns["Comment"].append(tmp[6])
                elif section == "charges":
                    tmp = line.split()
                    columns["Version"].append(tmp[0])
                    columns["Ref"].append(tmp[1])
                    columns["Type"].append(tmp[2])
                    columns["Charge"].append(tmp[3])
                elif section == "nonbond(12-6)":
                    tmp = line.split()
                    columns["Version"].append(tmp[0])
                    columns["Ref"].append(tmp[1])
                    columns["Type"].append(tmp[2])
                    columns["Sigma"].append(tmp[3])
                    columns["Epsilon"].append(tmp[4])
                elif section == "quadratic_bond":
                    tmp = line.split()
                    columns["Version"].append(tmp[0])
                    columns["Ref"].append(tmp[1])
                    columns["I"].append(tmp[2])
                    columns["J"].append(tmp[3])
                    columns["R0"].append(tmp[4])
                    columns["K2"].append(tmp[5])
                elif section == "quadratic_angle":
                    tmp = line.split()
                    columns["Version"].append(tmp[0])
                    columns["Ref"].append(tmp[1])
                    columns["I"].append(tmp[2])
                    columns["J"].append(tmp[3])
                    columns["K"].append(tmp[4])
                    columns["Theta0"].append(tmp[5])
                    columns["K2"].append(tmp[6])
                elif section == "torsion_opls":
                    tmp = line.split()
                    columns["Version"].append(tmp[0])
                    columns["Ref"].append(tmp[1])
                    columns["I"].append(tmp[2])
                    columns["J"].append(tmp[3])
                    columns["K"].append(tmp[4])
                    columns["L"].append(tmp[5])
                    columns["V1"].append(tmp[6])
                    columns["V2"].append(tmp[7])
                    columns["V3"].append(tmp[8])
                    columns["V4"].append(tmp[9])
                elif section == "improper_opls":
                    tmp = line.split()
                    columns["Version"].append(tmp[0])
                    columns["Ref"].append(tmp[1])
                    columns["I"].append(tmp[2])
                    columns["J"].append(tmp[3])
                    columns["K"].append(tmp[4])
                    columns["L"].append(tmp[5])
                    columns["V2"].append(tmp[6])
                elif section == "fragments":
                    entry_lines.append(line)
                else:
                    result.append(line)
    # Add the new reference at the end of the file.
    if result[-1] != "#end":
        result[-1] = ""
    result.append(f"#reference {ref}")
    result.append("")
    result.append(f"@Date {datetime.datetime.now().isoformat()}")
    try:
        result.append(f"@User {getpass.getuser()}")
    except Exception:
        pass
    result.append("")
    result.append("Parameters downloaded from LigParGen")
    if name is not None:
        result.append(f"    Name: {name}")
    result.append(f"InChIKey: {inchikey}")
    result.append(f"  SMILES: {canonical_smiles}")
    result.append(f"  SMARTS: {smarts}")
    result.append(
        """
Potential energy functions for atomic-level simulations of water and organic and
biomolecular systems. Jorgensen, W. L.; Tirado-Rives, J. Proc. Nat. Acad. Sci.
USA 2005, 102, 6665-6670

Localized Bond-Charge Corrected CM1A Charges for Condensed-Phase Simulations.
Dodda, L. S.; Vilseck, J. Z.; Tirado-Rives, J.; Jorgensen, W. L.
J. Phys. Chem. B, 2017, 121 (15), 3864-3870

LigParGen web server: An automatic OPLS-AA parameter generator for organic ligands.
Dodda, L. S.;Cabeza de Vaca, I.; Tirado-Rives, J.; Jorgensen, W. L.
Nucleic Acids Research, Volume 45, Issue W1, 3 July 2017, Pages W331-W336

@bibtex @ARTICLE{Jorgensen2005-uh,
  title     = "Potential energy functions for atomic-level simulations of water
               and organic and biomolecular systems",
  author    = "Jorgensen, William L and Tirado-Rives, Julian",
  abstract  = "An overview is provided on the development and status of
               potential energy functions that are used in atomic-level
               statistical mechanics and molecular dynamics simulations of
               water and of organic and biomolecular systems. Some topics that
               are considered are the form of force fields, their
               parameterization and performance, simulations of organic
               liquids, computation of free energies of hydration, universal
               extension for organic molecules, and choice of atomic charges.
               The discussion of water models covers some history, performance
               issues, and special topics such as nuclear quantum effects.",
  journal   = "Proc. Natl. Acad. Sci. U. S. A.",
  publisher = "Proceedings of the National Academy of Sciences",
  volume    =  102,
  number    =  19,
  pages     = "6665--6670",
  month     =  may,
  year      =  2005,
  language  = "en",
  doi       = "10.1073/pnas.0408037102"
}

@bibtex @ARTICLE{Dodda2017-hm,
  title     = "{1.14*CM1A-LBCC}: Localized bond-charge corrected {CM1A} charges
               for condensed-phase simulations",
  author    = "Dodda, Leela S and Vilseck, Jonah Z and Tirado-Rives, Julian and
               Jorgensen, William L",
  abstract  = "The quality of the 1.14*CM1A and 1.20*CM5 charge models was
               evaluated for calculations of free energies of hydration. For a
               set of 426 neutral molecules, 1.14*CM1A and 1.20*CM5 yield MADs
               of 1.26 and 1.21 kcal/mol, respectively. The 1.14*CM1A charges,
               which can be readily obtained for large systems, exhibit large
               deviations only for a subset of functional groups. The results
               for these cases were systematically improved using localized
               bond-charge corrections (LBCC) by which offsetting adjustments
               are made to the partial charges for atoms in specified bond
               types. Only 19 LBCCs were needed to yield 1.14*CM1A-LBCC charges
               that reduce the errors for the 426 $\\Delta$Ghyd values to only
               0.61 kcal/mol. The modified charge method was also tested in
               computation of heats of vaporization and densities for pure
               organic liquids, yielding average errors of 1.40 kcal/mol and
               0.024 g/cm3, similar to those for 1.14*CM1A.",
  journal   = "J. Phys. Chem. B",
  publisher = "American Chemical Society (ACS)",
  volume    =  121,
  number    =  15,
  pages     = "3864--3870",
  month     =  apr,
  year      =  2017,
  language  = "en",
  doi       = "10.1021/acs.jpcb.7b00272"
}

@bibtex @ARTICLE{Dodda2017-in,
  title     = "{LigParGen} web server: an automatic {OPLS-AA} parameter
               generator for organic ligands",
  author    = "Dodda, Leela S and Cabeza de Vaca, Israel and Tirado-Rives,
               Julian and Jorgensen, William L",
  journal   = "Nucleic Acids Res.",
  publisher = "Oxford University Press (OUP)",
  volume    =  45,
  number    = "W1",
  pages     = "W331--W336",
  month     =  jul,
  year      =  2017,
  copyright = "http://creativecommons.org/licenses/by-nc/4.0/",
  doi       = "10.1093/nar/gkx312"
}
"""
    )
    if name is None:
        tmp = ""
    else:
        tmp = " (" + name + ")"
    year, month, day = datetime.datetime.now().isoformat().split("-")
    result.append(
        f"""
@bibtex @Misc{{{inchikey},
  author    = "Dodda, Leela S and Cabeza de Vaca, Israel and Tirado-Rives,
               Julian and Jorgensen, William L",
  title     = "{{LigParGen}} generated parameters for {canonical_smiles}{tmp}",
  month     = "jun",
  year      = "{year}",
  organization = "William L. Jorgensen research group, Yale University",
  url       = "https://traken.chem.yale.edu/ligpargen/",
  address   = "New Haven, CT, USA",
  note      = "Accessed on {year}-{month}-{day}"
}}
"""
    )
    result.append("#end")
    result.append("")

    return "\n".join(result)


def _copy_header(lines):
    result = []
    found = False
    for line in lines:
        if line.strip() == "":
            continue
        if "Version" in line:
            continue
        if "-------" in line:
            break
        found = True
        result.append(line)

    if found:
        result.append("")

    return result


def run():
    ffpath = Path("~/.seamm.d/data/Forcefields/OPLS-AA/ligpargen.frc").expanduser()
    ffpath.parent.mkdir(parents=True, exist_ok=True)
    if ffpath.exists():
        ff = ffpath.read_text()
    else:
        ff = ff_template

    db = SystemDB(filename="file:seamm_db?mode=memory&cache=shared")

    changed = False
    while True:
        smiles = input("Enter a SMILES string (return to exit): ")
        if smiles == "":
            break
        changed = True
        system = db.create_system(name=smiles)
        configuration = system.create_configuration(name="initial")
        configuration.from_smiles(smiles)

        canonical_smiles = configuration.to_smiles(canonical=True)

        # Recreate the system from the canonical SMILES to get the order of atoms
        system.name = canonical_smiles
        configuration.from_smiles(canonical_smiles)

        read_structure_step.write(
            "structure.mol",
            [configuration],
            extension=".mol",
            remove_hydrogens=False,
        )

        url = "https://zarbi.chem.yale.edu/ligpargen/index.html"
        try:
            pyperclip.copy(url)
        except Exception:
            print("You will need to go to the LigParGen website")
            print("    " + url)
            print("and paste the following SMILES string into the SMILES box.")
            print()
            print(canonical_smiles)
            print()
            print("or you can upload the file 'structure.mol' from this directory.")
        else:
            print("You will need to go to the LigParGen website")
            print("    " + url)
            print("The address has been copied to the clipboard.")
            input("Press return for the next step.")
            pyperclip.copy(canonical_smiles)
            print("The following SMILES string has been copied to the clipboard.")
            print("Please paste it into the SMILES box on the LigParGen website.")
            print()
            print(canonical_smiles)
            print()
            print("or you can upload the file 'structure.mol' from this directory.")
        print()
        print("Select the type of charges you want and the molecule's charge")
        print("and click the 'Submit Molecules' button.")
        print()
        print("In the results page that appears after a few seconds, click the KEY")
        print("button under 'TINKER'. This will download a file with a .key extension.")
        input("Press return when you have the file and are ready to continue.")

        # Remove the temporary .mol file
        Path("structure.mol").unlink()

        paths = [*Path("~/Downloads").expanduser().glob("*.key")]
        paths.extend([*Path("~/Downloads").expanduser().glob("download_lpg*.py")])
        time = 0
        path = None
        for tmp_path in paths:
            try:
                t = tmp_path.stat().st_birthtime_ns
            except AttributeError:
                try:
                    t = tmp_path.stat().st_birthtime
                except AttributeError:
                    t = tmp_path.stat().st_mtime
            if t > time:
                time = t
                path = tmp_path
        answer = input(f"Is {path} the file you want to use? [Y/n] ")
        if answer.lower() == "n":
            path = input("Enter the path to the .key file: ")

        data = reader(path)
        path.unlink()

        ff = add_to_ff(ff, configuration, data)

    if changed:
        if ffpath.exists():
            tmp = ffpath.read_text()
            backup = ffpath.with_suffix(".frc-")
            backup.write_text(tmp)
        ffpath.write_text(ff)
        print("The file has been updated and a backup copy made.")


if __name__ == "__main__":
    run()
