# Copyright (C) 2025 Ash Hellwig <ahellwig.dev@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Runs a GUI application to copy the data from each experience entry in
the resume configuration to the clipboard in an easy-to-use menu.
"""

import tkinter as tk
import tkinter.font as tk_font
from tkinter import ttk

import pyperclip

from jobappfiller.tools.resume_data_gen import ResumeDataGen
from jobappfiller.util.logger import setup_logger

LARGEFONT = ("calibri", 36, tk_font.BOLD)
SMALLFONT = ("calibri", 14, tk_font.NORMAL)
logger = setup_logger(log_file=None)


class ClipboardHandler:
    """Handles clipboard operations for button clicks."""

    @staticmethod
    def copy_attribute(event, attribute: str):
        """Copies specified attribute from the event's widget master."""
        value = getattr(event.widget.master, attribute)
        pyperclip.copy(value)
        logger.info(
                "Copying %s for: %s",
                attribute,
                event.widget.master.company_name
        )
        logger.info("%s = %s", attribute, value)


# Generate all the button click handlers for company info.
button_click_company_name = lambda event: ClipboardHandler.copy_attribute(
        event, "company_name"
)
button_click_location = lambda event: ClipboardHandler.copy_attribute(
        event, "location"
)
button_click_startdate = lambda event: ClipboardHandler.copy_attribute(
        event, "startdate"
)
button_click_enddate = lambda event: ClipboardHandler.copy_attribute(
        event, "enddate"
)
button_click_jobtitle = lambda event: ClipboardHandler.copy_attribute(
        event, "jobtitle"
)
button_click_description = lambda event: ClipboardHandler.copy_attribute(
        event, "description"
)


class TkinterApp(tk.Tk):
    """
    Top-level app that serves the purpose of switching frames between each
        company selected.
    """

    def __init__(
            self,
            *args,
            resume_config_file: str = "resume.toml",
            date_format: str | None = None,
            **kwargs
    ):
        tk.Tk.__init__(self, *args, **kwargs)
        resume_data = ResumeDataGen(resume_config_file, date_format=date_format)

        # Generate accessible data from the `resume_config_file`.
        company_list = resume_data.company_list
        location_list = resume_data.location_list
        jobtitle_list = resume_data.jobtitle_list
        description_list = resume_data.description_list
        startdate_list = resume_data.startdate_list
        enddate_list = resume_data.enddate_list

        # Setup containers.
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.company_pages = []

        # Create StartPage frame
        startpage_frame = StartPage(
                parent=container,
                controller=self,
                company_list=company_list
        )
        self.frames[0] = startpage_frame
        startpage_frame.grid(row=0, column=0, sticky="nsew")

        # Create CompanyPage frames
        for idx, company in enumerate(company_list):
            frame = CompanyPage(
                    parent=container,
                    controller=self,
                    company_name=company,
                    location=location_list[idx],
                    startdate=startdate_list[idx],
                    enddate=enddate_list[idx],
                    jobtitle=jobtitle_list[idx],
                    description=description_list[idx]
            )
            self.frames[idx + 1] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(cont=0)

    def show_frame(self, cont: int):
        """Shows the frame of the specified job.

        Args:
            cont (int): Index of the frame under `self.frames` to display.
        """
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    """
    The homepage of the GUI application, listing all the companies found
        in the user's provided configuration file.
    """

    def __init__(self, parent, controller, company_list: list[str]):
        tk.Frame.__init__(self, parent)

        # UI setup
        label = ttk.Label(self, text="Job Application Filler", font=LARGEFONT)
        label.grid(row=0, column=1, padx=5, pady=5)

        separator = ttk.Separator(self, orient="horizontal")
        separator.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5)

        # Configure grid layout
        for col in range(3):
            self.grid_columnconfigure(col, weight=1)
        for row in range(9):
            self.grid_rowconfigure(row, weight=1)

        # Company navigation buttons
        for idx, company in enumerate(company_list):
            ttk.Button(
                    self,
                    text=company,
                    width=60,
                    style="TButton",
                    command=lambda idx=idx + 1: controller.show_frame(idx)
            ).grid(row=idx + 2,
                    column=1,
                    padx=5,
                    pady=5)


class CompanyPage(tk.Frame):
    """Page showing detailed company information and copy buttons."""

    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent)

        # Store company data as instance attributes
        self.company_name = kwargs["company_name"]
        self.location = kwargs["location"]
        self.startdate = kwargs["startdate"]
        self.enddate = kwargs["enddate"]
        self.jobtitle = kwargs["jobtitle"]
        self.description = kwargs["description"]

        # UI elements
        ttk.Label(
                self,
                text=self.company_name,
                font=LARGEFONT
        ).grid(row=0,
                column=1)
        ttk.Separator(self).grid(row=1, column=0, columnspan=3, sticky="ew")

        # Configure grid layout
        for col in range(3):
            self.grid_columnconfigure(col, weight=1)
        for row in range(9):
            self.grid_rowconfigure(row, weight=1)

        # Create the buttons corresponding to the configured company data.
        buttons = [("Company Name",
                    button_click_company_name,
                    2),
                    ("Location",
                        button_click_location,
                        3),
                    ("Start Date",
                        button_click_startdate,
                        4),
                    ("End Date",
                        button_click_enddate,
                        5),
                    ("Job Title",
                        button_click_jobtitle,
                        6),
                    ("Description",
                        button_click_description,
                        7)]

        # Create the button handlers corresponding to the
        # configured company data.
        for text, handler, row in buttons:
            btn = ttk.Button(self, text=text)
            btn.bind("<Button-1>", handler)
            btn.grid(row=row, column=1, padx=5, pady=5)

        # Return to "StartPage" button.
        ttk.Button(
                self,
                text="Start Page",
                command=lambda: controller.show_frame(0)
        ).grid(row=8,
                column=1,
                padx=5,
                pady=5)


def run_gui(
        resume_config_file: str = "resume.toml",
        date_format: str | None = None
):
    """Main function to run the GUI.

    Args:
        resume_config_file (str, optional): Path to resume config file in TOML
            format as a string. Defaults to "resume.toml".
        date_format (str | None, optional): Date format. Must be "yyyy/MM",
            "MM/yyyy", "yyyy/MM/dd", or "MM/dd/yyyy". Defaults to "MM/dd/yyyy".
    """

    app = TkinterApp(
            resume_config_file=resume_config_file,
            date_format=date_format
    )
    app.geometry("900x450")
    app.mainloop()


if __name__ == "__main__":
    run_gui()
