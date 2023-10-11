# Import necessary libraries
from psychopy import visual, core, event, gui, data
import numpy as np
import functions
import random
import numpy as np
import os

# grid size
n_rows = 3
n_cols = 3

# Create a window
win = visual.Window([800, 800], units='pix', fullscr=False, color=[1,1,1], 
                    colorSpace='rgb')

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session

expName = 'visual-search'  # from the Builder filename that created this script
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], 
                                                  expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)

# count_per_type = 20 in the final version (20 of each types of cues)
cues_stratified_order = functions.stratify_cues(count_per_type=2)
# count_per_type*3 
trial_number = len(cues_stratified_order)

# Define a list of shape stimuli
shapes = ['square', 'diamond', 'circle', 'triangle', 'hexagon', 'heart']

for n in range(trial_number):
    # Create a pause button
#    pause_button = visual.TextBox2(win, text="Pause", pos=(500, 360),
#                                   size=[None, None], colorSpace='rgb',
#                                   color='grey',
#                                   autoLog=False,
#                                   autoDraw=True)
#    pause_button.draw()
#    is_paused = False
#    paused_duration = 0
    
    # Create a grid of shape stimuli
    grid = [[None for _ in range(n_rows)] for _ in range(n_cols)]

    # choose a target shape
    target = random.choice(shapes)
    pos_y  = random.randrange(n_rows)
    pos_x  = random.randrange(n_cols)

    # a new list without the target
    available_shapes = shapes.copy()
    available_shapes.remove(target)

    #Display start the trial Page
    functions.display_text('Press space to start a trial', win, time=False)
    
    target = functions.drawer(target, win)
    
    # select one of the cues (visual, imagery, no_cue) 
    functions.select_cue(cues_stratified_order, win, target)
    cue_type=cues_stratified_order[-1]
    # remove the last element of startified cues list 
    cues_stratified_order.pop()

    # DISPLAY THE TASK
    functions.display_text(f"Find the {target.name}", win, time_of_display=1.5)

    #DISPLAY FIXATION POINT
    functions.draw_fixation_piont(win, random.uniform(1,3))

    # Create shape stimuli and randomly fill the grid
    for row in range(n_rows):
        for col in range(n_cols):
            if row == pos_y and col == pos_x:
                grid[row][col] = target
            else:
                rnd = random.choice(available_shapes)
                grid[row][col] = functions.drawer(rnd, win)

    # Set positions for the shapes in the grid
    x_positions = [-200, 0, 200]
    y_positions = [200, 0, -200]

    for row in range(3):
        for col in range(3):
            grid[row][col].pos = [x_positions[col], y_positions[row]]

    # Display the grid
    for row in grid:
        for shape in row:
            shape.draw()

    # Update the window to show the grid
    # and start a clock
    win.flip()
    clock = core.Clock()

    # Wait for the user to click on the target shape
    # or click pause
    while True:
        mouse = event.Mouse()
        if mouse.isPressedIn(target):
#        if not is_paused:
            break
#        if mouse.isPressedIn(pause_button):
#            if not is_paused:
#                is_paused = True
#                pause_time = clock.getTime()
#                print("Experiment Paused")
#                paused_msg = visual.TextStim(win, text="Experiment Paused",
#                                             color='black',
#                                             autoLog=False)
#                paused_msg.draw()
#                win.flip()
#            else:
#                is_paused = False
#                paused_duration += clock.getTime() - pause_time
#                pause_time = None
#                # display the grid again
#                for row in grid:
#                    for shape in row:
#                        shape.draw()
#                win.flip()
#                print(f"Experiment Resumes after {paused_duration: .2f} seconds")
        keys = event.getKeys()
        if keys:
            # q quits the experiment
            if keys[0] == 'q':
                core.quit()
                break


    # Record the time when the user clicked on the target
#    response_time = clock.getTime() - paused_duration
    response_time = clock.getTime()
    print(response_time)

    # Display the recorded time
    functions.display_text(f"Response Time: {response_time:.2f} seconds",
                           win, time_of_display=1.5)

    thisExp.addData('response_time', response_time)
    thisExp.addData('cue_type',cue_type )
    thisExp.nextEntry()

#DISPLAY END MESSAGE
functions.display_text("Press any key to end experiment", win, 
                       time_of_display=1.5, time=False)

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
# Close the window
win.close()

# Quit PsychoPy
core.quit()

