from datetime import datetime, timedelta
import pandas as pd
import argparse

# Read in the command-line options
parser = argparse.ArgumentParser()
parser.add_argument('--date', help='Date of proposal submission in MM-DD-YYYY', type=str, default=None)
parser.add_argument('--format', help='Format of the output', type=str, default='latex',
                    choices=['latex', 'bes', 'paragraph'])
args = parser.parse_args()

# Get the date of the proposal
if args.date is None:
    # Assume the next 14 days
    date = datetime.now() + timedelta(days=14)
else:
    date = datetime.strptime(args.date, '%m-%d-%Y')
print('Getting collaborators 48 months before {}'.format(date.date()))

# Read in collaborator list
collabs = pd.read_excel('collaborators.xlsx', sheet_name='Coauthors')
print('{} total collaborators'.format(len(collabs)))

# Filter out the names
collabs = collabs[collabs['Last Collaboration'] > date - timedelta(weeks=48*4)]
print('{} relevant collaborators'.format(len(collabs)))

# Compute first and last names
def get_first_and_surname(name):
    x = name.split()
    return x[-1], ' '.join(x[:-1])
collabs['surname'], collabs['first_name'] = zip(*collabs['Name'].apply(get_first_and_surname))

# Sort by surname
collabs.sort_values('surname', ascending=True, inplace=True)

# Get the advisors and advisees
advis = pd.read_excel('collaborators.xlsx', sheet_name='Mentorship')

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
elif args.format == 'paragraph':
    with open('paragraph.txt', 'w') as fp:
        text = ', '.join(collabs.apply(lambda x: f'{x["first_name"]} {x["surname"]} ({x["Present Institution"]})', axis=1))
        print(text, file=fp)
else:
    raise NotImplementedError(f'{args.format} not a recognized format')
