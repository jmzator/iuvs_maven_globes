########
# this first block of code is from earlier prep work
# it will be removed after new commit since this
# is only making blank squares grid for sizing but
# I want record of it and to make sure github,
# gitkraken, and pycharm are function correctly
# for this newly formed project folder

###### below here is the copy/paste from old prep project

# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


####### start with copy over of blank sheet code

import matplotlib.pyplot as plt
import numpy as np

square_size_cm = 9
num_rows = 10
num_cols = 10

# convert square size to inches since this will be for 8.5 x 11 inch paper print
square_size_inches = square_size_cm / 2.54

# create array of zeros representing the grid
grid = np.zeros((num_rows, num_cols))

# set figure size based on number of rows and columns
fig, ax = plt.subplots(figsize=(num_cols, num_rows))

# plot grid
ax.imshow(grid, cmap='gray')

# set tick locations and labels so can choose if want later
ax.set_xticks(np.arange(-0.5, num_cols, 1))
ax.set_yticks(np.arange(-0.5, num_rows, 1))
ax.set_xticklabels([])
ax.set_yticklabels([])

# set grid lines so can choose if want later
ax.grid(color='white', linestyle='-', linewidth=1)

# set aspect ratio of plot
ax.set_aspect('equal')

# set the plot limits
ax.set_xlim([-0.5, num_cols - 0.5])
ax.set_ylim([-0.5, num_rows - 0.5])

# set tick length to 0 to remove visible ticks (may need later)
ax.tick_params(axis='both', length=0)

# save plot as pdf
plt.savefig('printable_grid.pdf', format='pdf')

# show plot
plt.show()

###### end that block