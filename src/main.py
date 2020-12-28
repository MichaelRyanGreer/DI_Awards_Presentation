import bottle
from bottle import route, run, template

import pandas as pd

@route('/')
def hello():

    return "Welcome to the DI Awards Ceremony script"


@route('/order')
def order():

    global sections

    out = "<h3>List of competiton blocks found</h3>"

    out = out + "<ol>"

    for sec in sections:

        out = out + "<li>"

        out = out + sec[0] + " " + sec[1]

        out = out + "</li>"

    out = out + "</ol>"

    return out


@route("/show_award_section=<section>_team=<team>")
def show_award(section, team):

    section = int(section)
    team = int(team)

    global sections, results

    section_start = sections[section][3]

    row_val = results.iloc[section_start + team]

    team = row_val[' TeamName']

    award = row_val[' Rank']

    school = row_val[' MembName']

    return template('award_disp', award=award, team=team, school=school)

def sections_parser(frame):

    num_rows = frame.shape[0]

    # List to hold section stuff
    sections = [] 

    for row in range(num_rows):

        row_val = frame.iloc[row]

        if (row == 0):

            next_row_val = frame.iloc[row+1]

            sections.append([next_row_val[' Challenge'], next_row_val[' Level'], row + 1, -1])

        elif(row_val['Competitive'] == 'Competitive'):

            next_row_val = frame.iloc[row+1]
            
            sections[-1][3] = row-1

            sections.append([next_row_val[' Challenge'], next_row_val[' Level'], row + 1, -1])

    sections[-1][3] = num_rows

    return sections

results = pd.read_csv('../test_input/MidCities_all_scores_export.csv')

print()

sections = sections_parser(results)

print(sections)

print(results.keys())

run(host='localhost', port=8080, debug=True)
