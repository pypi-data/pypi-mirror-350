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
"""Collects the functions of the `jobappfiller.tools` module to make usable
by the click library for CLI use.
"""

import json

import click
from rich import print_json

from jobappfiller.tools.app import run_gui
from jobappfiller.tools.parse_job_config import parse_resume, list_companies


@click.command()
@click.option("-f", "--file", type=str)
def cli_print_resume_json(file: str):
    parsed_dictionary: dict = parse_resume(resume_config_file=file)
    parsed_dictionary_json: str = json.dumps(parsed_dictionary)
    print_json(parsed_dictionary_json)


@click.command()
@click.option("-f", "--file", type=str)
def cli_print_companies(file: str):
    parsed_dictionary: dict = parse_resume(resume_config_file=file)
    list_of_companies: list[str] = list_companies(parsed_dictionary)

    for company in list_of_companies:
        print(company)


@click.command()
@click.option("-f", "--file", type=str, help="Path to resume config file.")
@click.option(
        "--datefmt",
        is_flag=False,
        flag_value="",
        type=str,
        help="Date format. Must be "
        "[\"yyyy/MM\" | \"yyyy-MM\"], [\"MM/yyyy\" | \"MM-yyyy\"], "
        "[\"yyyy/MM/dd\" | \"yyyy-MM-dd\"], or "
        "[\"MM/dd/yyyy\" | \"MM-dd-yyyy\"]. "
        "Defaults to \"MM/dd/yyyy\"."
)
def cli_run_gui(file: str, datefmt: str):
    run_gui(resume_config_file=file, date_format=datefmt)
