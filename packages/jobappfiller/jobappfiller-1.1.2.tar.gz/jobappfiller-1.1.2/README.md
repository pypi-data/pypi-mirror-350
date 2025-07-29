<!--
 Copyright (C) 2025 Ash Hellwig <ahellwig.dev@gmail.com>

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as
 published by the Free Software Foundation, either version 3 of the
 License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->

# jobappfiller

This is a CLI and GUI application designed to make it easier to apply to jobs
in which the online application requires one to add **all of their experience**
again in their own text boxes (*even when you already submit a resume*).

Simply fill out the `TOML` configuration and run the application GUI and
you can simply click each button to copy that field to your clipboard and
paste into the website.

Future plans are to utilize `selenium` to auto-fill these fields, but I am
trying to work around the differences in these fields company-to-company.

## Usage

### Downloading

First, download the repository.

```bash
git clone https://github.com/ashellwig/jobappfiller.git
cd jobappfiller
```

Next, customize the `resume.toml` file.

```bash
mv resume.example.toml resume.toml
```

### Configuration

Use the following format:

```toml
[[default]]
name = "Default"

[[default.experience]]
name = ""
location = ""
startdate = "" # Use MM/DD/YYYY format.
enddate = ""  # Use MM/DD/YYYY format.
jobtitle = ""
description = """\
    Begin job description here.\
    """
```

Make sure you use the `\` character to break long lines in the string. Make sure
all of the fields are of a string type.

This way, you can make **many** of these configuration files to adjust your
experience descriptions on a per-application basis by specifying the resume
configuration file.

#### Configuration Example

Just to illustrate how to use the configuration file format, here is the top
two experience entries I personally have in my default resume TOML
configuration at `resume.toml`:

```toml
[[default]]

[[default.experience]]
name = "TAKKION (TP&L Management Solutions)"
location = "Broomfield, CO"
startdate = "09/01/2023"
enddate = "03/01/2025"
jobtitle = "IT Cloud Developer"
description = """\
    Migrate C#/.NET and Python Applications to the GCP/Azure \
    cloud environment. Implement automated account provisioning on Microsoft \
    Azure Entra ID through Paylocity's API with serverless \
    functions and webhooks.\
    """

[[default.experience]]
name = "American Express"
location = "Phoenix, AZ"
startdate = "07/01/2022"
enddate = "09/01/2023"
jobtitle = "Python & SQL Developer"
description = """\
    Migrate massive dataset from Teradata to Hive and ensure 1:1 mapping \
    of rules and regulatory reports through TSQL to Hive SQL. Utilize GCP, \
    AWS, JFrog, and Jira for CI/CD. Written a Python package to pull HiveQL \
    Query results and format them using a personally written Python package \
    for CornerStone to convert the data into XML format for reporting \
    requirements as requested by FR, MX, IT, and NL. Utilize Azure cloud \
    functions and Spring Boot for microservices. ETL pipelines. SQLAlchemy \
    library for interaction with Python and C#/.NET.\
    """
```

### Installing

This application has only been tested with `Python 3.13.2` on
`Arch Linux (v6.14.6-arch1-1)`. If you are using other platforms and experience
issues, please open a request.

Assuming you are already in the source directory of the repository and
have completed your configuration, simply build the package with `pip`
or `pyinstaller` depending on if you wish to build the development Python
package (`pip`) or a distributable executable file of the CLI (`pyinstaller`).

#### Installing with Local Repo

```bash
# Installing with `pip install --editable .`.
python -m venv .venv
source ./.venv/bin/activate
python -m pip install -r requirements.txt  # Probably unnecessary.
python -m pip install --editable .

# Installing by building the executable locally.
# Run the above commands, then run:
pyinstaller \
    --onefile \
    --icon=./jobappfiller/resources/favicon.ico \
    --name jobappfiller-cli \
    --collect-all jobappfiller \
    ./jobappfiller/cli.py
```

#### Installing by downloading the latest release

Either visit the [latest release] page on github or use the following script
(also found at
[scripts/download_latest_release.sh](scripts/download_latest_release.sh))

```bash
latest_release="releases/latest/download/jobappfiller-cli"

if type "wget" >/dev/null; then
    wget "https://github.com/ashellwig/jobappfiller/${latest_release}"
    chmod +x ./jobappfiller-cli
    echo -e "\033[1,32mSuccessfully downloaded ${latest_release}\033[0m"
elif type "curl" >/dev/null; then
    echo -e "\033[1,33mUsing curl to download ${latest_release}\033[0m"
    curl \
        -L "https://github.com/ashellwig/jobappfiller/${latest_release}" \
        >jobappfiller-cli
    chmod +x ./jobappfiller
    echo -e "\033[1,32mSuccessfully downloaded ${latest_release}\033[0m"
else
    echo -e "\033[1,31mPlease install either wget or curl.\033[0m"
    exit 1
fi
```

Then you are ready to run!

#### Running

To run the GUI, after installing or downloading the [latest release] simply:

```bash
# Installed with `pip install --editable .`.
jobappfiller gui -f resume.toml --datefmt "MM/dd/yyyy"

# Installed by locally building the execuatable.
./dist/jobappfiller-cli gui -f resume.toml -datefmt "MM/dd/yyyy"

# Installed with downloaded release.
${DOWNLOAD_PATH}/jobappfiller gui -f resume.toml --datefmt "MM/dd/yyyy"
```

This will open the GUI for your specified configuration. If you have many
experience listings, remove the line `app.geometry("900x450")` in the
[app.py](jobappfiller/tools/app.py) in the `run_gui()` function, or adjust
it to your liking.

[latest release]: https://github.com/ashellwig/jobappfiller/releases/latest
