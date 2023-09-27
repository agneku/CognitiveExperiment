# Import necessary libraries
from psychopy import visual, core, event
import random

# grid size
n_rows = 3
n_cols = 3

# Create a window
win = visual.Window([800, 800], units='pix', fullscr=False)

# Define a list of shape stimuli
shapes = ['square', 'heart', 'circle', 'polygon', 'pie']

# Create a grid of shape stimuli
grid = [[None for _ in range(n_rows)] for _ in range(n_cols)]

# choose a target shape
target = random.choice(shapes)
pos_y  = random.randrange(n_rows)
pos_x  = random.randrange(n_cols)

# a new list without the target
available_shapes = shapes.copy()
available_shapes.remove(target)

def drawer(shape):
    if shape == 'square':
        figure = visual.Rect(win, width=100, height=100, 
                             lineColor='black', 
                             fillColor='red')
    elif shape == 'heart':
        figure = visual.ShapeStim(win, 
                                  vertices=[[-50, 0], [0, 50], [50, 0], [0, -50]],
                                  fillColor='red')
    elif shape == 'circle':
        figure = visual.Circle(win, radius = 70,
                               lineColor='black', 
                               fillColor='red')
    elif shape == 'polygon':
        figure = visual.Polygon(win, size=100, 
                                lineColor='black', 
                                fillColor='red')
    elif shape == 'pie':
        figure = visual.Pie(win, size = 160,
                            lineColor='black', 
                            fillColor='red')  
    return figure

# Create shape stimuli and randomly fill the grid
for row in range(n_rows):
    for col in range(n_cols):
        if row == pos_y and col == pos_x:
            target = drawer(target)
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
                               pos=(0, -100), height=20)
time_message.draw()
win.flip()

# Wait for a key press to exit the program
event.waitKeys()

# Close the window
win.close()

# Quit PsychoPy
core.quit()
