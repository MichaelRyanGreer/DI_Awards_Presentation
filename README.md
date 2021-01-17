# DI_Awards_Presentation #

## Created for Mid-Cities DI by Michael Greer ##

## Code for generating awards ceremony presentations based on score CSV input. ##

### Installation: ###
1. Install python3, pip3, and git
2. Clone this repository using git
3. Install dependencies using "pip3 install -r requirements.txt"

### Usage ###
1. Run the software locally using "python3 main.py"
2. Navigate to "localhost:8080" in your browser
3. Upload the score csv file you wish to use (an example file is included in test_input)
4. Follow prompts

Right now, the program shows results in the order they are displayed. The teams that did not move on are shown first, then the high IC scores, then the teams that did advance.

### Planned changes: ###
1. Allow user to select each competition group seperately to change order in which awards are shown
2. Better file checking (right now there is no file checking)
3. Improve usability so the program could be hosted on an external server
4. Add command line options to change things like templates to use, port number, etc.

 If you have other ideas for how this could be improved or otherwise want to help develop this tool, feel free to reach out and I would be happy to add you to the repo with branch permissions.
