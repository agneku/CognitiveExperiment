from psychopy import visual, core, event
import random 
import numpy as np

def stratify_cues(count_per_type=20):

    cues = sum([['visual_cue']*count_per_type, ['mental_cue']*count_per_type,
                ['no_cue']*count_per_type], [])

    # Shuffle the selected elements to ensure randomness
    # in place method
    random.shuffle(cues)
    return cues


def draw_fixation_piont(win, time):
    # Create a fixation point stimulus at the center
    fixation = visual.ShapeStim(win=win,
                                vertices=((0, -20), (0, 20), (0, 0), (-20, 0), (20, 0)),
                                lineWidth=5,
                                closeShape=False,
                                lineColor='black')

    # Function to display fixation point
    fixation.draw()
    win.flip()
    core.wait(time)  


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
                            name='square',
                            lineColor=colorRGB)
    elif shape == 'diamond':
        figure = visual.ShapeStim(win, 
                                vertices=[[-50, 0], [0, 50], [50, 0], [0, -50]],
                                fillColor=colorRGB,
                                colorSpace=space,
                                size=1.16,
                                name='diamond',
                                lineColor=colorRGB)
    elif shape == 'hexagon':
        figure = visual.ShapeStim(win, 
                                vertices=[(0, 58), (-50, 29), (-50, -29), (0, -58), (50, -29), (50, 29)], 
                                fillColor=colorRGB,
                                colorSpace=space,
                                name='hexagon',
                                lineColor=colorRGB)
    elif shape == 'heart':
        figure = visual.ShapeStim(win, 
                                vertices = vertices,
                                fillColor=colorRGB,
                                colorSpace=space,
                                size=100,
                                name='heart',
                                lineColor=colorRGB)
    elif shape == 'circle':
        figure = visual.Circle(win, radius = 50,
                                fillColor=colorRGB,
                                colorSpace=space,
                                name='circle',
                                lineColor=colorRGB)
    elif shape == 'triangle':
        figure = visual.Polygon(win, size=130, 
                                fillColor=colorRGB,
                                colorSpace=space,
                                name='triangle',
                                lineColor=colorRGB)
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
        display_text(f"Imagine a {target.name}", win, time_of_display=1.5)
        win.flip()
        core.wait(3.0)
    if cue == 'no_cue':
        win.flip()
        core.wait(3.0)
    return cue_order


def present_shapes(shapes, win):
    display_text('Press space to view all shapes', win, time=False)

    for i in shapes:
        display_text(i, win)
        target = drawer(i, win)
        target.draw()
        win.flip()
        core.wait(3.0)

def start_practice_trials(win, n_rows, n_cols, shapes, practice_rounds=5):
    display_text('Press space to start the practice', win, time=False)
    
    for n in range(practice_rounds):
        # Create a grid of shape stimuli
        grid = [[None for _ in range(n_rows)] for _ in range(n_cols)]
        cues_stratified_order=['no_cue' for i in range(practice_rounds)]

        # choose a target shape
        target = random.choice(shapes)
        pos_y  = random.randrange(n_rows)
        pos_x  = random.randrange(n_cols)

        # a new list without the target
        available_shapes = shapes.copy()
        available_shapes.remove(target)

        #Display start the trial Page
        display_text('Press space to start a trial', win, time=False)
        
        target = drawer(target, win)
        
        # select one of the cues (visual, imagery, no_cue) 
        select_cue(cues_stratified_order, win, target)
        cue_type=cues_stratified_order[-1]
        # remove the last element of startified cues list 
        cues_stratified_order.pop()

        # DISPLAY THE TASK
        display_text(f"Find the {target.name}", win, time_of_display=1.5)

        #DISPLAY FIXATION POINT
        draw_fixation_piont(win, random.uniform(1,3))

        # Create shape stimuli and randomly fill the grid
        for row in range(n_rows):
            for col in range(n_cols):
                if row == pos_y and col == pos_x:
                    grid[row][col] = target
                else:
                    rnd = random.choice(available_shapes)
                    grid[row][col] = drawer(rnd, win)

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

        while True:
            mouse = event.Mouse()
            if mouse.isPressedIn(target):
                break
            keys = event.getKeys()
            if keys:
                # q quits the experiment
                if keys[0] == 'q':
                    core.quit()
                    break

