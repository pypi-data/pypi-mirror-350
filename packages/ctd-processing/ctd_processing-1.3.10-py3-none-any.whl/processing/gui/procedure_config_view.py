from pathlib import Path
from tkinter import ttk
import tkinter as tk
from processing.gui.toml_editor import TomlEditor

import customtkinter as ctk

from processing.modules.available_modules import (
    get_list_of_available_processing_modules,
)


class ProcedureConfigView(TomlEditor):
    """
    A frame that contains the configuration for a procedure.
    """

    def __init__(
        self,
        master: ctk.CTkFrame,
        title: str = "Processing Procedure Config Editor",
        possible_parameters: list[str] = [
            "psa_directory",
            "output_dir",
            "output_name",
        ],
        config_file: Path | str = "",
        title_size: int = 20,
        custom_processing_modules: Path | str = Path("custom_processing_modules"),
    ):
        super().__init__(
            master,
            title,
            possible_parameters,
            config_file,
            title_size,
        )
        self.module_frames = {}
        self.new_module_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.new_module_frame.grid(row=3, column=0)
        self.new_module_selector = ctk.CTkComboBox(
            self.new_module_frame,
            values=get_list_of_available_processing_modules(custom_processing_modules),
        )
        self.new_module_selector.grid(row=0, column=0)
        self.add_module_button = ctk.CTkButton(
            self.new_module_frame, text="Add Module", command=self.new_module
        )
        self.add_module_button.grid(row=0, column=1, padx=5, pady=10)

    def new_module(self):
        self.add_module(self.new_module_selector.get())

    def remove_module(self, module_name, frame):
        frame.destroy()
        self.config_data["modules"].pop(module_name, None)
        self.module_frames.pop(module_name, None)

    def remove_module_param(
        self, module_name, frame, key_entry, value_entry, param_entries
    ):
        self.update_module_params(module_name, param_entries)
        parent_frame = frame.master
        key_entry.destroy()
        value_entry.destroy()
        frame.grid_forget()
        frame.destroy()
        parent_frame.grid()
        param_entries.pop(key_entry, None)

    def load_config_specific_data(self, row=0):
        if "modules" in self.config_data:
            for module_name, params in self.config_data["modules"].items():
                self.add_module(module_name, params, row=row)
                row += 1

    def add_module(self, module_name=None, params=None, row=None):
        frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        frame.grid(row=row, column=0, sticky="ew", padx=5, pady=5)
        frame.grid_columnconfigure(0, weight=1)
        ttk.Separator(frame, orient="horizontal").grid(
            row=0, column=0, columnspan=3, sticky="ew"
        )
        header = ctk.CTkLabel(
            frame,
            text=f"Module: {module_name or 'New Module'}",
            font=("Arial", 14, "bold"),
        )
        header.grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        if module_name is None:
            module_name = f"module_{len(self.module_frames) + 1}"

        self.module_frames[module_name] = frame

        param_entries = {}
        if params:
            for index, (key, value) in enumerate(params.items()):
                self.create_module_param_field(
                    module_name, frame, key, value, param_entries, index
                )
        add_param_button = ctk.CTkButton(
            frame,
            text="+",
            command=lambda: self.create_module_param_field(
                module_name, frame, "", "", param_entries
            ),
        )
        add_param_button.grid(row=1, column=2, sticky="e", padx=5, pady=5)

        remove_module_button = ctk.CTkButton(
            frame,
            text="Remove Module",
            command=lambda: self.remove_module(module_name, frame),
        )
        remove_module_button.grid(row=1, column=1, sticky="e", padx=5, pady=5)
        self.config_data.setdefault("modules", {})[module_name] = {}
        self.update_module_params(module_name, param_entries)
        frame.bind(
            "<FocusOut>",
            lambda e: self.update_module_params(module_name, param_entries),
        )

    def update_module_params(self, module_name, param_entries):
        self.config_data["modules"][module_name] = {
            k.get(): v.get() for k, v in param_entries.items()
        }

    def create_module_param_field(
        self,
        module_name: str,
        parent_frame: ctk.CTkFrame,
        key: str,
        value: str,
        param_entries: dict,
        index=None,
    ):
        if not index:
            index = len(parent_frame.winfo_children())
        frame = ctk.CTkFrame(parent_frame, fg_color="transparent")

        def reload_frame(e):
            frame.destroy()
            try:
                param_entries.pop(key_entry)
            except KeyError:
                pass
            self.create_module_param_field(
                module_name, parent_frame, e, value, param_entries, index
            )

        key_entry = ctk.CTkComboBox(
            frame, values=["psa", "file_suffix"], command=reload_frame
        )

        key_entry.grid(row=0, column=0, padx=20, pady=5)
        key_entry.set(key)

        value_entry = ctk.CTkEntry(frame)

        def update_param(event=None):
            param_entries[key_entry] = value_entry
            self.update_module_params(module_name, param_entries)

        if key == "psa":
            file_picker = self.create_picker_element(
                frame=frame,
                entry=value_entry,
                directory=False,
                callback=update_param,
                initial_dir=self.config_data["psa_directory"],
            )
            file_picker.grid(row=0, column=1)
            width = 340
        else:
            width = 400

        value_entry.grid(row=0, column=2, padx=5, pady=5)
        value_entry.configure(require_redraw=True, width=width)
        value_entry.insert(0, value)
        value_entry.xview(tk.END)

        remove_button = ctk.CTkButton(
            frame,
            text="-",
            command=lambda: self.remove_module_param(
                module_name, frame, key_entry, value_entry, param_entries
            ),
        )
        remove_button.grid(row=0, column=3, padx=5, pady=5)
        param_entries[key_entry] = value_entry

        key_entry.bind("<FocusOut>", update_param)
        value_entry.bind("<FocusOut>", update_param)
        frame.grid(row=index + 1, column=0, columnspan=3, sticky="ew")

    def check_input(self) -> bool:
        # TODO: think about sophisticated check here
        return True


# Example usage
if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.geometry("800x600")

    editor = ProcedureConfigView(
        app,
        config_file="proc_test.toml",
        title_size=35,
    )

    editor.grid(row=0, column=0, sticky="nsew")

    # Configure the grid to make the editor expand with the window
    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=1)
    app.mainloop()
