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

    row_val = results.iloc[section_start - team]

    section_name = row_val[' Challenge'] + ": " + row_val[' Level'] 

    team_name = row_val[' TeamName']

    award = row_val[' Rank']

    if (row_val[' Tie'] == 'T'):
        award = 'Tie: ' + row_val[' Rank']

    school = row_val[' MembName']

    next_link = '/next_award_section={}_team={}'.format(section, team + 1)

    return template('award_disp', section=section_name, award=award, team=team_name, school=school, link=next_link)


@route("/next_award_section=<section>_team=<team>")
def next_award(section, team):

    global mode

    section = int(section)
    team = int(team)

    # If we've gone through all sections, move on to the next mode
    if (section >= len(sections)):

        if (mode == 'nogoing'):
            mode = 'ic'
            section = 0
            team = 0

        elif (mode == 'ic'):
            mode = 'going'
            section = 0
            team = 0

        elif (mode == 'going'):
            bottle.redirect('/')

    section_start = sections[section][3]
    section_end = sections[section][2]

    # If we're done with this section, move on to next
    if (section_start - team < section_end):

        return next_award(section + 1, 0)

    print(section_start - team)
    row_val = results.iloc[section_start - team]

    # If the team did not compete, skip
    if (row_val['Competitive'] == 'NO'):

        return next_award(section, team+1)

    # Display teams that did not advance
    if (mode == 'nogoing'):

        if (row_val[' Rank'] == 'HighIC'):

            return next_award(section, team + 1)

        if (row_val[' GoingOn'] == 'G'):

            return next_award(section + 1, 0)

        bottle.redirect('/show_award_section={}_team={}'.format(section, team))
        return
    
    # Display teams that earned high IC scores
    elif (mode == 'ic'):

        if (row_val[' Rank'] != 'HighIC'):
            
            return next_award(section, team + 1)

        bottle.redirect('/show_award_section={}_team={}'.format(section, team))
        return

    # Display the teams that are advancing
    elif (mode == 'going'):

        if (row_val[' GoingOn'] != 'G'):

            return next_award(section, team + 1)

        if (row_val[' Rank'] == 'HighIC'):

            return next_award(section, team + 1)

        bottle.redirect('/show_award_section={}_team={}'.format(section, team))
        return

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

    sections[-1][3] = num_rows - 1

    return sections

mode = 'nogoing'

results = pd.read_csv('../test_input/MidCities_all_scores_export.csv')

print()

sections = sections_parser(results)

print(sections)

print(len(sections))

run(host='localhost', port=8080, debug=True)
