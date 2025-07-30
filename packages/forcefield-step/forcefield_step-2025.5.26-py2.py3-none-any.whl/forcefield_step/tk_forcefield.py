# -*- coding: utf-8 -*-

"""The graphical part of a Forcefield step"""

import importlib
from importlib.resources import files as data_files
from pathlib import Path

import seamm
import tkinter as tk

try:
    import kim_query
except ModuleNotFoundError:
    pass


class TkForcefield(seamm.TkNode):
    """The graphical part of a forcefield step"""

    def __init__(
        self, tk_flowchart=None, node=None, canvas=None, x=None, y=None, w=200, h=50
    ):
        """Initialize a node

        Keyword arguments:
        """

        self.dialog = None

        super().__init__(
            tk_flowchart=tk_flowchart, node=node, canvas=canvas, x=x, y=y, w=w, h=h
        )

    def right_click(self, event):
        """Probably need to add our dialog..."""

        super().right_click(event)
        self.popup_menu.add_command(label="Edit..", command=self.edit)

        self.popup_menu.tk_popup(event.x_root, event.y_root, 0)

    def edit(self):
        """Present a dialog for editing this step's parameters.
        We need to recreate the PeriodicTable for some reason
        """
        if self.dialog is None:
            self.create_dialog()

        forcefields = self._update_forcefields()
        forcefield = self["forcefield_file"].get()
        self["forcefield_file"].combobox.configure(value=forcefields)
        if forcefields:
            width = max([len(f) for f in forcefields])
        else:
            width = 0
        self["forcefield_file"].combobox.configure(width=width)
        if forcefield not in forcefields:
            if len(forcefields) == 0:
                self["forcefield_file"].set("")
            else:
                self["forcefield_file"].set(forcefields[0])

        # Reset the dialog, which will recreate the PeriodicTable
        # widget
        self.reset_dialog()
        # And resize the dialog to fit...
        self.fit_dialog()

        super().edit()

    def create_dialog(self):
        """Create the dialog for editing the Forcefield flowchart"""

        frame = super().create_dialog("Edit Forcefield Step")

        # Create the widgets
        P = self.node.parameters
        for key in P:
            self[key] = P[key].widget(frame)

        # bindings...
        self["task"].combobox.bind("<<ComboboxSelected>>", self.reset_dialog)
        self["task"].config(state="readonly")

        self["forcefield_file"].combobox.bind("<<ComboboxSelected>>", self.reset_dialog)
        self["forcefield_file"].combobox.bind("<Return>", self.reset_dialog)
        self["forcefield_file"].combobox.bind("<FocusOut>", self.reset_dialog)

        # and set it up the first time
        self.reset_dialog()

    def reset_dialog(self, widget=None):
        """Layout the widgets as needed for the current state"""

        frame = self["frame"]
        for slave in frame.grid_slaves():
            slave.grid_forget()

        task = self["task"].get()
        repository = self["forcefield_file"].get()

        row = 0
        self["task"].grid(row=row, column=0, sticky=tk.W)
        row += 1

        if task == "assign forcefield to structure":
            pass
        elif task == "setup forcefield":
            self["forcefield_file"].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
            row += 1
            if repository == "OpenKIM":
                # For reasons unknown, the PeriodicTable does not redisplay
                # properly, so recreate.
                self["elements"].destroy()
                P = self.node.parameters
                self["elements"] = P["elements"].widget(
                    frame, command=self.update_potentials
                )
                self["elements"].grid(row=row, column=0, columnspan=2)
                frame.rowconfigure(row, weight=1)
                frame.columnconfigure(1, weight=1)
                row += 1
                self["potentials"].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
            else:
                self["forcefield"].grid(row=row, column=0, columnspan=2, sticky=tk.EW)
                frame.rowconfigure(row, weight=0)
                frame.columnconfigure(1, weight=0)
                row += 1

        # And resize the dialog to fit...
        self.fit_dialog()

        return row

    def update_potentials(self, elements):
        """Update the list of possible OpenKIM potentials as the element
        selection changes."""

        potentials = kim_query.get_available_models(elements)

        current_potential = self["potentials"].get()
        self["potentials"].combobox.configure(value=potentials)
        if current_potential not in potentials:
            if len(potentials) == 0:
                self["potentials"].set("")
            else:
                self["potentials"].set(potentials[0])

    def _update_forcefields(self):
        """Update the list of forcefields from scratch."""
        data_path = data_files(__package__).joinpath("data")
        paths = self._traverse(data_path)

        forcefields = sorted([str(p.relative_to(data_path)) for p in paths])

        # Check if we can use OpenKIM
        if importlib.util.find_spec("kim_query") is not None:
            forcefields.append("OpenKIM")

        # and local forcefields in the ~/SEAMM/data/Forcefields
        local = Path.home() / "SEAMM" / "data" / "Forcefields"
        if local.exists():
            tmp = []
            for path in local.glob("**/*.frc"):
                tmp.append("local:" + str(path.relative_to(local)))
            forcefields.extend(sorted(tmp))

        # and local forcefields in the ~/.seamm.d/data/Forcefields
        local = Path.home() / ".seamm.d" / "data" / "Forcefields"
        if local.exists():
            tmp = []
            for path in local.glob("**/*.frc"):
                tmp.append("personal:" + str(path.relative_to(local)))
            forcefields.extend(sorted(tmp))

        return forcefields

    def _traverse(self, path):
        paths = []
        for target in path.iterdir():
            if target.is_file():
                paths.append(target)
            elif target.is_dir():
                paths.extend(self._traverse(target))
        return paths
