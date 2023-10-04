# Import necessary libraries
from psychopy import visual, core, event, gui, data
import numpy as np
import random
import os


# grid size
n_rows = 3
n_cols = 3

# Create a window
win = visual.Window([800, 800], units='pix', fullscr=False, color=[1,1,1], colorSpace='rgb')

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2020.2.8'
expName = 'visual-search'  # from the Builder filename that created this script
expInfo = {'participant': '', 'session': '001'}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion
# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)


# Define a list of shape stimuli
shapes = ['square', 'diamond', 'circle', 'triangle', 'hexagon', 'heart']
trial_number = 5

for n in range(trial_number-1):
    # Create a grid of shape stimuli
    grid = [[None for _ in range(n_rows)] for _ in range(n_cols)]

    # choose a target shape
    target = random.choice(shapes)
    pos_y  = random.randrange(n_rows)
    pos_x  = random.randrange(n_cols)

    # a new list without the target
    available_shapes = shapes.copy()
    available_shapes.remove(target)

    # shapes color parameters 
    space='rgb'
    colorRGB=[0,0,0]
    
    # Heart shape componet:
    # Create an array of parameter values from 0 to 2π
    t = np.linspace(0, 2 * np.pi, 1000)
    
    # Parametric equations for x(t) and y(t) for the heart shape
    x = 16 * np.sin(t)**3
    y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
    
    # Scale and shift the x and y coordinates to fit the window
    x = (x - np.min(x)) / (np.max(x) - np.min(x))  # Scale to [0, 1]
    x = (x - 0.5)
    
    y = (y - np.min(y)) / (np.max(y) - np.min(y))  # Scale to [0, 1]
    y = (y - 0.5)
    
    # Create a list of vertices for the heart shape
    vertices = list(zip(x, y))

    def drawer(shape):
        if shape == 'square':
            figure = visual.Rect(win, width=100, height=100, 
                                fillColor=colorRGB,
                                colorSpace=space,
                                name='square')
        elif shape == 'diamond':
            figure = visual.ShapeStim(win, 
                                    vertices=[[-50, 0], [0, 50], [50, 0], [0, -50]],
                                    fillColor=colorRGB,
                                    colorSpace=space,
                                    name='diamond')
        elif shape == 'hexagon':
            figure = visual.ShapeStim(win, 
                                    vertices=[(0, 58), (-50, 29), (-50, -29), (0, -58), (50, -29), (50, 29)], 
                                    fillColor=colorRGB,
                                    colorSpace=space,
                                    name='hexagon')
        elif shape == 'heart':
            figure = visual.ShapeStim(win, 
                                    vertices = vertices,
                                    fillColor=colorRGB,
                                    colorSpace=space,
                                    size=100,
                                    name='heart')
        elif shape == 'circle':
            figure = visual.Circle(win, radius = 50,
                                    fillColor=colorRGB,
                                    colorSpace=space,
                                    name='circle')
        elif shape == 'triangle':
            figure = visual.Polygon(win, size=100, 
                                    fillColor=colorRGB,
                                    colorSpace=space,
                                    name='triangle')
        return figure

    # Display the visual que in the middle of grid (fixed size)
    target = drawer(target)
    target.draw()
    win.flip()
    core.wait(3.0)

    # Display the task
    message = visual.TextStim(win, text=f"Find the {target.name}", color='black')
    message.draw()
    win.flip()
    core.wait(3.0)

    # Create shape stimuli and randomly fill the grid
    for row in range(n_rows):
        for col in range(n_cols):
            if row == pos_y and col == pos_x:
                grid[row][col] = target
            else:
                rnd = random.choice(available_shapes)
                grid[row][col] = drawer(rnd)

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
    while True:
        mouse = event.Mouse()
        if mouse.isPressedIn(target):
            break

    # Record the time when the user clicked on the target
    response_time = clock.getTime()

    # Display the recorded time
    time_message = visual.TextStim(win, 
                                text=f"Response Time: {response_time:.2f} seconds",
                                pos=(0, -100), height=20, color='black')
    time_message.draw()
    thisExp.addData('response_time', response_time)
    thisExp.nextEntry()
    win.flip()
    core.wait(2.0)


end_message = visual.TextStim(win, 
                              text="Press any key to end experiment",
                              color='black')
end_message.draw()
win.flip()
event.waitKeys()
# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
# Close the window
win.close()

# Quit PsychoPy
core.quit()

