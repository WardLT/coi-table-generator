from datetime import datetime, timedelta
import pandas as pd
import argparse

# Read in the command-line options
parser = argparse.ArgumentParser()
parser.add_argument('--date', help='Date of proposal submission in MM-DD-YYYY', type=str, default=None)
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

# Sort by surname
collabs['surname'] = collabs['Name'].apply(lambda x: x.split()[-1])
collabs.sort_values('surname', ascending=True, inplace=True)

# Get the advisors and advisees
advis = pd.read_excel('collaborators.xlsx', sheet_name='Mentorship')

# Save to disk
with open('collabs.tex', 'w') as fp:
    print('\\subsection*{Co-authors}\n\n', file=fp)
    collabs[['Name', 'Present Institution']].to_latex(fp, index=False, longtable=True)
    
    print('\\subsection*{Co-editors}\n\nNone.\n', file=fp)
    
    print('\\subsection*{Advisors and Advisees}\n', file=fp)
    advis[['Name', 'Present Institution', 'Relationship']].to_latex(fp, index=False, longtable=True)
    
