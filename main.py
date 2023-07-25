
# ???? why can't get these imports to work??? trying to call functions below...
from histogram_coloring import histogram_equalize_detector_image
from matplotlib_dummy_grid import plot_images_on_grid
import matplotlib_dummy_grid


###########
# now adding the code for reading the fits files into an array
# for histogram equalization prior to mapping onto globe


from pathlib import Path
import numpy as np
from astropy.io import fits


# list of fits files
top_path = Path("/Users/jmzator/Desktop/maven_iuvs_visualization_project/orbit18001/")
# note this 'top_path' pulls from old pycharm project, once working, need to change to main source of orbits data
file_paths = sorted(top_path.glob('*orbit18001*.gz'))


def add_dimension_if_necessary(arr: np.ndarray) -> np.ndarray:
    return arr if np.ndim(arr) == 3 else arr[None, ...]


# note below 790 volts for exluding nightside data (>790 is nightside, <790 is dayside that want to use)
hduls = [fits.open(f) for f in file_paths]
data_arrays = np.vstack([add_dimension_if_necessary(f['primary'].data) for f in hduls if f['observation'].data['mcp_volt'] < 790])
print(data_arrays.shape)
raise SystemExit(9)


print(np.shape(data))


###### end ######



# histogram fxn next, need to troubleshoot the import at top
# try import of matplotlib_dummy_grid.py function that working on too

# fxn (image: np.ndarray, mask: np.ndarray = None) -> np.ndarray:
histogram_equalize_detector_image()


# fxn (image_dir, image_files, output_file)
matplotlib_dummy_grid.plot_images_on_grid()
plot_images_on_grid()


#### start cartopy code - haven't gotten to work in other test project
# add some of that code here and go from there...

import cartopy


