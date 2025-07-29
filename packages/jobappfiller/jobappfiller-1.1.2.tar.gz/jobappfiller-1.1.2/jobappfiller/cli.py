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
"""Collects the CLI tools from each module and adds them to the main package."""

import importlib.metadata

import click

from jobappfiller.tools.cli import (
        cli_print_resume_json,
        cli_print_companies,
        cli_run_gui
)

JAF_VERSION: str = importlib.metadata.version("jobappfiller")


@click.group()
@click.version_option(version=JAF_VERSION, package_name="jobappfiller")
@click.pass_context
def cli(ctx):  # pylint: disable=W0613
    pass


cli.add_command(cli_print_resume_json, name="print-resume")
cli.add_command(cli_print_companies, name="print-companies")
cli.add_command(cli_run_gui, name="gui")

if __name__ == "__main__":
    cli()  # pylint: disable=E1120
