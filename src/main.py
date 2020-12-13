import bottle
from bottle import route, run

import pandas as pd

@route('/')
def hello():

    return "Welcome to the DI Awards Ceremony script"


@route('/row=<row>')
def show_award(row):

    global results

    name = results[' TeamName'].iloc[int(row)]

    school = results[' MembName'].iloc[int(row)]

    return "Team: {}\nSchool: {}".format(name, school)


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

print(sections_parser(results))

run(host='localhost', port=8080, debug=True)
