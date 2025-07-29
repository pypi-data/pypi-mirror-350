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
"""Handles data generation from resume configuration file."""

import re
import tomllib


class ResumeDataGen:
    """Portable data generation from resume config file."""

    def __init__(self, resume_config_file: str, date_format: str | None = None):
        if date_format is None:
            self._date_format = "MM/dd/yyyy"
        else:
            self._date_format = date_format

        self.resume_data = self._parse_resume(resume_config_file)

        self._experience_data = \
            self.resume_data.get("default")[0]["experience"]

        self.company_list = self._generate_company_list(self._experience_data)

        self.location_list = self._generate_location_list(self._experience_data)

        self._startdate_list = self._generate_startdate_list(
                self._experience_data
        )
        self.startdate_list = self._format_dates(
                self._startdate_list,
                self._date_format
        )

        self._enddate_list = self._generate_enddate_list(self._experience_data)
        self.enddate_list = self._format_dates(
                self._enddate_list,
                self._date_format
        )

        self.jobtitle_list = self._generate_jobtitle_list(self._experience_data)

        self.description_list = self._generate_description_list(
                self._experience_data
        )

    def _parse_resume(self, resume_config_file: str) -> dict:
        """Reads the resume configuration file into a dictionary.

        Args:
            resume_config_file (str): Path to configuration file as a string.

        Returns:
            dict: Dictionary containing the contents of the resume
                configuration.
        """

        with open(resume_config_file, "rb") as f:
            data: dict = tomllib.load(f)

        return data

    def _generate_company_list(self, experience_data: dict | None) -> list[str]:
        """Gets the company names of the companies in experience_data.

        Args:
            experience_data (dict, optional): Parsed dictionary of
                ONLY experience from the resume data. Defaults to
                `self._experience_data`.

        Returns:
            list[str]: List of company names for each company in experience.
        """
        if experience_data is not None:
            pass
        else:
            experience_data = self._experience_data

        companies: list[str] = []

        for i in range(0, len(experience_data)):
            companies.append(experience_data[i]["name"])

        return companies

    def _generate_location_list(self,
                                experience_data: dict | None) -> list[str]:
        """Gets the locations of the companies in experience_data.

        Args:
            experience_data (dict, optional): Parsed dictionary of
                ONLY experience from the resume data. Defaults to
                `self._experience_data`.

        Returns:
            list[str]: List of company locations for each company in experience.
        """
        if experience_data is not None:
            pass
        else:
            experience_data = self._experience_data

        locations: list[str] = []

        for i in range(0, len(experience_data)):
            locations.append(experience_data[i]["location"])

        return locations

    def _generate_startdate_list(self,
                                    experience_data: dict | None) -> list[str]:
        """Gets the startdates of the companies in experience_data.

        Args:
            experience_data (dict, optional): Parsed dictionary of
                ONLY experience from the resume data. Defaults to
                `self._experience_data`.

        Returns:
            list[str]: List of **UNFORMATTED** startdates for each company
                in experience.
        """

        if experience_data is not None:
            pass
        else:
            experience_data = self._experience_data

        startdates: list[str] = []

        for i in range(0, len(experience_data)):
            startdates.append(experience_data[i]["startdate"])

        return startdates

    def _generate_enddate_list(self, experience_data: dict | None) -> list[str]:
        """Gets the enddates of the companies in experience_data.

        Args:
            experience_data (dict, optional): Parsed dictionary of
                ONLY experience from the resume data. Defaults to
                `self._experience_data`.

        Returns:
            list[str]: List of **UNFORMATTED** enddates for each company
                in experience.
        """

        if experience_data is not None:
            pass
        else:
            experience_data = self._experience_data

        enddates: list[str] = []

        for i in range(0, len(experience_data)):
            enddates.append(experience_data[i]["enddate"])

        return enddates

    def _generate_jobtitle_list(self,
                                experience_data: dict | None) -> list[str]:
        """Gets the jobtitles of the companies in experience_data.

        Args:
            experience_data (dict, optional): Parsed dictionary of
                ONLY experience from the resume data. Defaults to
                `self._experience_data`.

        Returns:
            list[str]: List of jobtitles for each company in experience.
        """

        if experience_data is not None:
            pass
        else:
            experience_data = self._experience_data

        jobtitles: list[str] = []

        for i in range(0, len(experience_data)):
            jobtitles.append(experience_data[i]["jobtitle"])

        return jobtitles

    def _generate_description_list(self,
                                    experience_data: dict | None) -> list[str]:
        """Gets the descriptions of the companies in experience_data.

        Args:
            experience_data (dict, optional): Parsed dictionary of
                ONLY experience from the resume data. Defaults to
                `self._experience_data`.

        Returns:
            list[str]: List of descriptions for each company in experience.
        """

        if experience_data is not None:
            pass
        else:
            experience_data = self._experience_data

        descriptions: list[str] = []

        for i in range(0, len(experience_data)):
            descriptions.append(experience_data[i]["description"])

        return descriptions

    def _format_dates(
            self,
            list_of_dates: list[str],
            date_format: str | None = None
    ) -> list[str]:
        """Format the dates in a list to a new list in the specified format.

        Args:
            list_of_dates (list[str]): The original list of dates in
            "MM/dd/yyyy" format.
            date_format (str | None, optional): Date format to return.
                Defaults to "MM/dd/yyyy".

        Returns:
            list[str]: Formatted list of dates.
        """
        if date_format is not None:
            pass
        else:
            date_format = self._date_format

        dates = list_of_dates

        date_delim = \
            "/" if "/" in date_format else "-" if "-" in date_format else "/"
        modified_dates = []

        for date_str in dates:
            if date_format in ["yyyy/MM", "yyyy-MM"]:
                modified = f"{date_str[-4:]}{date_delim}{date_str[:2]}"
            elif date_format in ["MM/yyyy", "MM-yyyy"]:
                modified = f"{date_str[:2]}{date_delim}{date_str[-4:]}"
            elif date_format in ["yyyy/MM/dd", "yyyy-MM-dd"]:
                day = re.search(r"\/(.*?)\/", date_str).group(1)
                modified = \
                    f"{date_str[-4:]}{date_delim}" \
                    f"{date_str[:2]}{date_delim}{day}"
            else:
                modified = date_str
            modified_dates.append(modified)

        return modified_dates
