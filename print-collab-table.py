from datetime import datetime, timedelta
import pandas as pd
import argparse

# My home instition(s)
_home_insts = ['Argonne National Laboratory', 'University of Chicago']

# Read in the command-line options
parser = argparse.ArgumentParser()
parser.add_argument('--date', help='Date of proposal submission in MM-DD-YYYY', type=str, default=None)
parser.add_argument('--format', help='Format of the output', type=str, default='latex',
                    choices=['latex', 'bes', 'bes-plus-advisors', 'paragraph', 'nsf'])
parser.add_argument('--years', help='Years of collaborators to print', default=4, type=int)
parser.add_argument('--remove-home', action='store_true', help='Whether to remove people from home institution.')
args = parser.parse_args()

# Get the date of the proposal
if args.date is None:
    # Assume the next 14 days
    date = datetime.now() + timedelta(days=14)
else:
    date = datetime.strptime(args.date, '%m-%d-%Y')
print(f'Getting collaborators {args.years} years before {date.date()}')

# Read in collaborator list
collabs = pd.read_excel('collaborators.xlsx', sheet_name='Coauthors')
print('{} total collaborators'.format(len(collabs)))

# Get the advisors and advisees
advis = pd.read_excel('collaborators.xlsx', sheet_name='Mentorship')

# Remove people from home institions, if requested
if args.remove_home:
    collabs = collabs[collabs['Present Institution'].apply(lambda x: x not in _home_insts)]
    print(f'Removed collaborators from: {", ".join(_home_insts)}')

# Filter out the names
weeks = args.years * 52
collabs = collabs[collabs['Last Collaboration'] > date - timedelta(weeks=weeks)]
print('{} relevant collaborators'.format(len(collabs)))

# Compute first and last names
def get_first_and_surname(name):
    x = name.split()
    return x[-1], ' '.join(x[:-1])
collabs['surname'], collabs['first_name'] = zip(*collabs['Name'].apply(get_first_and_surname))
advis['surname'], advis['first_name'] = zip(*advis['Name'].apply(get_first_and_surname))

# Sort by surname
collabs.sort_values('surname', ascending=True, inplace=True)


# Write in desired formats
if args.format == 'latex':
    with open('collabs.tex', 'w') as fp:
        print('\\subsection*{Co-authors}\n\n', file=fp)
        collabs[['Name', 'Present Institution']].to_latex(fp, index=False, longtable=True)
        
        print('\\subsection*{Co-editors}\n\nNone.\n', file=fp)
        
        print('\\subsection*{Advisors and Advisees}\n', file=fp)
        advis[['Name', 'Present Institution', 'Relationship']].to_latex(fp, index=False, longtable=True)
elif args.format == 'bes':
    collabs[['surname', 'first_name', 'Present Institution']].to_csv('bes_table.csv', index=False)
elif args.format == 'bes-plus-advisors':
    # Add relationship to each table
    collabs['Role'] = 'Collaborator'
    advis['Role'] = 'Advisor'

    # Print both, removing duplicates
    output = pd.concat([collabs, advis])[['surname', 'first_name', 'Present Institution', 'Role']]
    output = output.sort_values(['surname', 'Role']).drop_duplicates(['surname', 'first_name'], keep='first')
    output.to_csv('bes_table.csv', index=False)
elif args.format == 'paragraph':
    with open('paragraph.txt', 'w') as fp:
        text = ', '.join(collabs.apply(lambda x: f'{x["first_name"]} {x["surname"]} ({x["Present Institution"]})', axis=1))
        print(text, file=fp)
elif args.format == "nsf":
    collabs["name"] = [f"{s}, {f}" for s, f in zip(collabs["surname"], collabs["first_name"])]
    collabs[["name", "Present Institution", "Last Collaboration"]].to_csv("nsf_table.csv", index=False)
else:
    raise NotImplementedError(f'{args.format} not a recognized format')
