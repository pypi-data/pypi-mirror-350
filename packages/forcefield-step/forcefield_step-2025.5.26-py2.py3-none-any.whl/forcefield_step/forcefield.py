# -*- coding: utf-8 -*-

"""A node or step for the forcefield in a flowchart"""

import logging
import os.path
from pathlib import Path
import pkg_resources
import pprint

import forcefield_step
import seamm_ff_util
import seamm
import seamm_util
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

logger = logging.getLogger(__name__)
# logger.setLevel("DEBUG")
job = printing.getPrinter()
printer = printing.getPrinter("forcefield")


class Forcefield(seamm.Node):
    def __init__(self, flowchart=None, extension=None, logger=logger):
        """Initialize a forcefield step

        Keyword arguments:
        """
        logger.debug("Creating Forcefield {}".format(self))

        super().__init__(
            flowchart=flowchart,
            title="Forcefield",
            extension=extension,
            logger=logger,
        )

        self._files = []
        self.parameters = forcefield_step.ForcefieldParameters()

    @property
    def version(self):
        """The semantic version of this module."""
        return forcefield_step.__version__

    @property
    def git_revision(self):
        """The git version of this module."""
        return forcefield_step.__git_revision__

    @property
    def files(self):
        """The files in the forcefield ... (short name & full path)"""
        return self._files

    def description_text(self, P=None):
        """Return a short description of this step.

        Return a nicely formatted string describing what this step will
        do.

        Keyword arguments:
            P: a dictionary of parameter values, which may be variables
                or final values. If None, then the parameters values will
                be used as is.
        """

        if not P:
            P = self.parameters.values_to_dict()

        if P["task"] == "setup forcefield":
            if P["forcefield_file"][0] == "$":
                text = (
                    "Read the forcefield file given in the variable"
                    " '{forcefield_file}' and use the {forcefield} "
                    "forcefield."
                )
            elif P["forcefield_file"] == "OpenKIM":
                text = "Use the OpenKIM potential '{potentials}'"
            else:
                text = (
                    "Read the forcefield file '{forcefield_file}' "
                    "and use the {forcefield} forcefield."
                )
        elif P["task"] == "assign forcefield to structure":
            text = "Assign the atom types to the structure."

        return (
            self.header
            + "\n"
            + __(
                text,
                indent=4 * " ",
                **P,
            ).__str__()
        )

    def run(self):
        """Setup the forcefield"""

        next_node = super().run(printer=printer)

        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        printer.important(__(self.header, indent=self.indent))

        if P["task"] == "setup forcefield":
            self.setup_forcefield(P)
        elif P["task"] == "assign forcefield to structure":
            ff = self.get_variable("_forcefield")
            if ff.ff_form in ("reaxff",):
                printer.important(
                    __(
                        "There is no atom-type assignment needed for ReaxFF",
                        indent=self.indent + 4 * " ",
                    )
                )
            else:
                system_db = self.get_variable("_system_db")
                configuration = system_db.system.configuration
                try:
                    ff.assign_forcefield(configuration)
                except seamm_ff_util.ForcefieldAssignmentError as e:
                    printer.important(__(f"\n\nError: {e}", self.indent + 4 * " "))
                    raise
                printer.important(
                    __(
                        "Successfully assigned the atom types for "
                        f"{ff.current_forcefield}.",
                        indent=self.indent + 4 * " ",
                    )
                )
        printer.important("")

        return next_node

    def assign_forcefield(self, P=None, configuration=None):
        """Assign the forcefield to the structure, i.e. find the atom types
        and charges.

        Parameters
        ----------
        P : {str: Any}
            The final values of the parameters.

        Returns
        -------
        None
        """
        # if P is None:
        #     P = self.parameters.current_values_to_dict(
        #         context=seamm.flowchart_variables._data
        #     )

        ff = self.get_variable("_forcefield")
        if configuration is None:
            system_db = self.get_variable("_system_db")
            configuration = system_db.system.configuration

        ffname = ff.current_forcefield
        printer.important(
            __(
                "Assigning the atom types and charges for forcefield "
                f"'{ffname}' to the system",
                indent=self.indent + "    ",
            )
        )

        # Atom types
        self.logger.debug("Atom typing, getting the SMILES for the system")
        smiles = configuration.to_smiles(hydrogens=True)
        self.logger.debug("Atom typing -- smiles = " + smiles)
        ff_assigner = seamm_ff_util.FFAssigner(ff)
        atom_types = ff_assigner.assign(configuration)
        self.logger.info("Atom types: " + ", ".join(atom_types))
        key = f"atom_types_{ffname}"
        if key not in configuration.atoms:
            configuration.atoms.add_attribute(key, coltype="str")
        configuration.atoms[key] = atom_types

        # Now get the charges if forcefield has them.
        terms = ff.data["forcefield"][ffname]["parameters"]
        if "bond_increments" in terms:
            self.logger.debug("Getting the charges for the system")
            neighbors = configuration.bonded_neighbors(as_indices=True)

            self.logger.debug(f"{atom_types=}")
            self.logger.debug(f"{neighbors=}")

            charges = []
            total_q = 0.0
            for i in range(configuration.n_atoms):
                itype = atom_types[i]
                parameters = ff.charges(itype)[3]
                q = float(parameters["Q"])
                for j in neighbors[i]:
                    jtype = atom_types[j]
                    parameters = ff.bond_increments(itype, jtype)[3]
                    q += float(parameters["deltaij"])
                charges.append(q)
                total_q += q
            if abs(total_q) > 0.0001:
                self.logger.warning("Total charge is not zero: {}".format(total_q))
                self.logger.info(
                    "Charges from increments and charges:\n" + pprint.pformat(charges)
                )
            else:
                self.logger.debug(
                    "Charges from increments:\n" + pprint.pformat(charges)
                )

            key = f"charges_{ffname}"
            if key not in configuration.atoms:
                configuration.atoms.add_attribute(key, coltype="float")
            charge_column = configuration.atoms.get_column(key)
            charge_column[0:] = charges
            self.logger.debug(f"Set column '{key}' to the charges")

            printer.important(
                __(
                    "Assigned atom types and charges to "
                    f"{configuration.n_atoms} atoms.",
                    indent=self.indent + "    ",
                )
            )
        elif "charges" in terms:
            self.logger.debug("Getting the charges for the system")

            charges = []
            total_q = 0.0
            for i in range(configuration.n_atoms):
                itype = atom_types[i]
                parameters = ff.charges(itype)[3]
                q = float(parameters["Q"])
                charges.append(q)
                total_q += q
            if abs(total_q) > 0.0001:
                self.logger.warning("Total charge is not zero: {}".format(total_q))
                self.logger.info("Charges from charges:\n" + pprint.pformat(charges))
            else:
                self.logger.debug("Charges from charges:\n" + pprint.pformat(charges))

            key = f"charges_{ffname}"
            if key not in configuration.atoms:
                configuration.atoms.add_attribute(key, coltype="float")
            charge_column = configuration.atoms.get_column(key)
            charge_column[0:] = charges
            self.logger.debug(f"Set column '{key}' to the charges")

            printer.important(
                __(
                    "Assigned atom types and charges to "
                    f"{configuration.n_atoms} atoms.",
                    indent=self.indent + "    ",
                )
            )
        else:
            printer.important(
                __(
                    f"Assigned atom types to {configuration.n_atoms} " "atoms.",
                    indent=self.indent + "    ",
                )
            )

    def list_data_files(self, local_only=True):
        """Returns the forcefield files needed by this step."""
        result = []

        P = self.parameters.values_to_dict()

        if P["task"] != "setup forcefield":
            return result

        if self.is_expr(P["forcefield_file"]):
            return result

        if P["forcefield_file"] == "OpenKIM":
            return result

        ff_file = P["forcefield_file"]
        if ff_file.startswith("personal:"):
            ff_file = "Forcefields/" + ff_file[9:]
            uri = f"data:{ff_file}"
            path = self.find_data_file(ff_file)
            result.append((uri, path))
        elif ff_file.startswith("local:"):
            ff_file = "Forcefields/" + ff_file[6:]
            uri = f"data:{ff_file}"
            path = self.find_data_file(ff_file)
            result.append((uri, path))
        else:
            uri = ff_file
            path = Path(pkg_resources.resource_filename(__name__, "data/"))
            path = path / ff_file
            if not local_only:
                result.append((uri, path))

        ff_file = str(path)

        # Now read through the forcefield file to pick up any included files
        with seamm_util.Open(
            path, "r", include="#include", uri_handler=self.uri_handler
        ) as fd:
            for line in fd:
                pass
            files = fd.visited

        for uri, path in files:
            if uri.startswith("local:"):
                uri = "data:Forcefields/" + uri[6:]
                result.append((uri, path))
            elif not local_only:
                result.append((uri, path))

        return result

    def setup_forcefield(self, P=None):
        """Setup the forcefield for later use.

        Parameters
        ---------
        P : {str: Any}
            The final values of the parameters.

        Returns
        -------
        None
        """
        if P is None:
            P = self.parameters.current_values_to_dict(
                context=seamm.flowchart_variables._data
            )

        if P["forcefield_file"] == "OpenKIM":
            printer.important(
                __(
                    "Using the OpenKIM potential '{potentials}'",
                    **P,
                    indent=self.indent + "    ",
                )
            )
            self.set_variable("_forcefield", "OpenKIM")
            self.set_variable("_OpenKIM_Potential", P["potentials"])
        else:
            # Find the forcefield file
            ff_file = P["forcefield_file"]
            printer.important(
                self.indent + 4 * " " + f"Reading the forcefield file {ff_file}"
            )
            if ff_file.startswith("local:"):
                ff_file = "Forcefields/" + ff_file[6:]
                path = self.find_data_file(ff_file)
                ff_file = str(path)
            else:
                path = pkg_resources.resource_filename(__name__, "data/")
                ff_file = os.path.join(path, P["forcefield_file"])

            printer.important("")
            printer.important(self.indent + 8 * " " + str(ff_file))
            printer.important("")

            ff = seamm_ff_util.Forcefield(
                ff_file, uri_handler=self.uri_handler, references=self.references
            )
            self.set_variable("_forcefield", ff)

            # Print any included files
            self._files = [(P["forcefield_file"], ff_file)]
            files = ff.files_visited
            if len(files) > 1:
                printer.important(self.indent + 4 * " " + "which included:")
                for file_ in files[1:]:
                    self._files.append(file_)
                    short = file_[0]
                    filename = str(file_[1])
                    printer.important(self.indent + 8 * " " + f"{short:}\t{filename}")
                printer.important("")

            if P["forcefield"] == "default":
                printer.important(
                    __(
                        "   Using the default forcefield '{ff}'.",
                        ff=ff.forcefields[0],
                        indent=self.indent + 4 * " ",
                    )
                )

                ff.initialize_biosym_forcefield()
            else:
                printer.important(
                    __(
                        "   Using the forcefield '{forcefield}'",
                        **P,
                        indent=self.indent + 4 * " ",
                    )
                )

                ff.initialize_biosym_forcefield(P["forcefield"])

    def uri_handler(self, path):
        """Return the actual file given a path that may have a uri.

        Parameters
        ----------
        path : str or pathlib.Path
            The filename or uri for the file.

        Returns
        -------
        path : pathlib.Path
            The full path to the file

        Note
        ----
        Forcefields can be in one of 3 locations:

            1. In the data directory of this Python package. This is where the standard
               forcefields are stored.

            2. In the local installation, under ~/SEAMM/data/Forcefields. This allows a
               site to add or customize forcefields for all users. The user for the
               SEAMM installation may not be the same as the user running the code! So
               '~/' may reference a different directory than the next item.

            3. In the users directory at ~/seamm.d/data/Forcefields. This allows the
               user to add or override any existing forcefield.

        When a forcefield is referenced, if it has no URI it is assumed to be in (1),
        the default location for forcefields shipped with the release.

        If it has a URI, i.e. the path starts with 'local:', the code searches for it
        first in the users local data (3). If it is not found, the search continues in
        site location (2).

        Jobs executed by the JobServer are handled a bit differently, because the site
        and home directories may not exist or may be different on the machine that the
        JobServer is running on. When a job is submitted to the Dashboard, the code
        locates the forcefields on the local machine, as outlined above. It then sends
        copies to the data/Forcefields directory of the job. The path for the job's
        data/ directory is changed to its local data/ directory, so the copies sent with
        the job are used.
        """
        filename = str(path)
        if filename.startswith("local:"):
            filename = "Forcefields/" + filename[6:]
            return self.find_data_file(filename)
        else:
            return Path(path).expanduser().resolve()
