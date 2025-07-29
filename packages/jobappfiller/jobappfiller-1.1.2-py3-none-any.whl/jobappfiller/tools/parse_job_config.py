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
"""Parses job resume configuration file."""

import tomllib

from jobappfiller.util.logger import setup_logger

logger = setup_logger(log_file=None)


def parse_resume(resume_config_file: str) -> dict:
    """Reads the resume configuration file into a dictionary.

    Args:
        resume_config_file (str): Path to configuration file as a string.

    Returns:
        dict: Dictionary containing the contents of the resume configuration.
    """
    with open(resume_config_file, "rb") as f:
        data: dict = tomllib.load(f)

    return data


def list_companies(resume_data: dict) -> list[str]:
    """Gets the company names of the companies in `resume_data`

    Args:
        resume_data (dict): Parsed dictionary of resume data.

    Returns:
        list[str]: List of company names for each company in experience.
    """
    companies: list[str] = []
    experience_data = resume_data.get("default")[0]["experience"]
    for i in range(0, len(experience_data)):
        companies.append(experience_data[i]["name"])

    return companies


def list_locations(resume_data: dict) -> list[str]:
    """Gets the locations of the companies in `resume_data`

    Args:
        resume_data (dict): Parsed dictionary of resume data.

    Returns:
        list[str]: List of locations for each company in experience.
    """
    locations: list[str] = []
    experience_data = resume_data.get("default")[0]["experience"]
    for i in range(0, len(experience_data)):
        locations.append(experience_data[i]["location"])

    return locations


def list_startdates(resume_data: dict) -> list[str]:
    """Gets the start date of the companies in `resume_data`

    Args:
        resume_data (dict): Parsed dictionary of resume data.

    Returns:
        list[str]: List of start dates for each company in experience.
    """
    start_dates: list[str] = []
    experience_data = resume_data.get("default")[0]["experience"]
    for i in range(0, len(experience_data)):
        start_dates.append(experience_data[i]["startdate"])

    return start_dates


def list_enddates(resume_data: dict) -> list[str]:
    """Gets the end date of the companies in `resume_data`

    Args:
        resume_data (dict): Parsed dictionary of resume data.

    Returns:
        list[str]: List of end dates for each company in experience.
    """
    end_dates: list[str] = []
    experience_data = resume_data.get("default")[0]["experience"]
    for i in range(0, len(experience_data)):
        end_dates.append(experience_data[i]["enddate"])

    return end_dates


def list_jobtitles(resume_data: dict) -> list[str]:
    """Gets the job title for each company in `resume_data`.

    Args:
        resume_data (dict): Parsed dictionary of resume data.

    Returns:
        list[str]: List of job titles for each company in experience.
    """
    jobtitles: list[str] = []
    experience_data = resume_data.get("default")[0]["experience"]
    for i in range(0, len(experience_data)):
        jobtitles.append(experience_data[i]["jobtitle"])

    return jobtitles


def list_descriptions(resume_data: dict) -> list[str]:
    """Gets the descriptions of each company in `resume_data`.

    Args:
        resume_data (dict): Parsed dictionary of resume data.

    Returns:
        list[str]: List of discriptions for each company in experience.
    """
    descriptions: list[str] = []
    experience_data = resume_data.get("default")[0]["experience"]
    for i in range(0, len(experience_data)):
        descriptions.append(experience_data[i]["description"])

    return descriptions
