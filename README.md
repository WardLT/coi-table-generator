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
In the case of co-authors, you list their affiliations and the last date you published a paper with them.

Once you update the lists of authors in these lists, the `print-collab-table.py` script will allow you to render the data in different formats.

To run the script with default settings, simply call `python print-collab-table.py` from the command line.

`print-collab-table` takes several different keyword arguments.
For example, `--date` sets the submission date for the grant, which changes which authors are included in the COI list.
Call `python print-collab-table.py --help` for a full list of options.

### Supported Formats

The script currently only supports a few different formats:

- DOE format, which separates "Co-authors," "Co-editors" and "Advisees/Mentors" and writes them in three separate sections in a table format. The code currently uses [`longtable`](https://ctan.org/pkg/longtable?lang=en) to generate multi-page tables.
- BES format, which saves the collaborators in a single CSV file.
- Paragraph format, which writes out the author names in a long sentence
