# COI Table Generator

Utility script for generating conflict of interest tables for grants. 

This directory contains a Python script that will read a specially-formated Excel file and write out a list of collaborators in the format needed by different types of grants.

## Installation

No installation is required, but there are Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The Excel document associated with this repository, `collaborators.xlsx`, which contains lists of different types of collaborators.
For now, the types are limited to "co-author" and "mentorship" relationships.
In the case of co-authors

Once you update the lists of authors in these lists, the `print-to-latex.py` script will allow you to render the data in different formats.

To run the script with default settings, simply call `python print-to-latex.py` from the command line.

`print-to-latex` takes several different keyword arguments.
For example, `--date` sets the submission date for the grant, which changes which authors are included in the COI list.
Call `python print-to-latex.py --help` for a full list of options.

\[PS. At present `--date` is the only keyword argument\]

### Supported Formats

The script currently only supports the DOE format, which separates "Co-authors," "Co-editors" and "Advisees/Mentors" and writes them in three separate sections in a table format.

The code currently use [`longtable`](https://ctan.org/pkg/longtable?lang=en) to generate multi-page tables.
