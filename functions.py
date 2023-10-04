import random 
from psychopy import visual, core, event
import numpy as np

def stratify_cues(count_per_type=20):

    cues = sum([['visual_cue']*count_per_type, ['mental_cue']*count_per_type, ['no_cue']*count_per_type], [])

    # Shuffle the selected elements to ensure randomness
    # in place method
    random.shuffle(cues)
    return cues


def draw_fixation_piont(win):
    # Create a fixation point stimulus at the center
    fixation = visual.ShapeStim(win=win,
                                vertices=((0, -20), (0, 20), (0, 0), (-20, 0), (20, 0)),
                                lineWidth=5,
                                closeShape=False,
                                lineColor='black'
                                )

    # Function to display fixation point
    fixation.draw()
    win.flip()
    core.wait(2)  


def drawer(shape, win, space='rgb', colorRGB=[0,0,0]):
    
    # HEART SHAPE COMPONENTS:
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


def display_text(text, win, time_of_display=1.5, time=True):
    message = visual.TextStim(win, text=text, color='black')
    message.draw()
    win.flip()
    
    if time:
        core.wait(time_of_display)
    else:
        event.waitKeys()


def select_cue(cue_order, win, target):
    cue = cue_order[-1]
    if cue == 'visual_cue':
        target.draw()
        win.flip()
        core.wait(3.0)
    if cue == 'mental_cue':
        display_text(f"Imagine a {target.name}", win, time_of_display=3)
    if cue == 'no_cue':
        win.flip()
        core.wait(3.0)
    return cue_order