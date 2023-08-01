
# I think source of most problems on main.py was the system exit code I didn't know what it did
from histogram_coloring import histogram_equalize_detector_image
from matplotlib_dummy_grid import plot_images_on_grid


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
#raise SystemExit(9)

#print(np.shape(data_arrays))

#np.save('iuvs_test_array', data_arrays)

###### end ######



# histogram fxn next
# attempt import of matplotlib_dummy_grid.py function that working on too

# fxn (image: np.ndarray, mask: np.ndarray = None) -> np.ndarray:
histogram_equalize_detector_image(data_arrays)


# fxn (image_dir, image_files, output_file)
image_dir = "/Users/jmzator/Desktop/LASP_Maven_job/globe_sample_images/dummy_images_from_kyle/"
image_files = [
        "orbit03453-Ls1820-angle0410-binning0133x0019-heq-globe.png",
        "orbit03475-Ls1843-angle0345-binning0133x0019-heq-globe.png",

        # above is just two dummy images over and over again
        # add more then, for final project will need code to add all as created
    ]

output_file = "sample_grid_on_main.png"
plot_images_on_grid(image_dir, image_files, output_file)

# before, couldn't get the fxn to fun in main, now when running main, always runs fxn even when not calling it??????

#matplotlib_dummy_grid.plot_images_on_grid("/Users/jmzator/Desktop/LASP_Maven_job/globe_sample_images/dummy_images_from_kyle/", "orbit03453-Ls1820-angle0410-binning0133x0019-heq-globe.png", "sample_grid.png")
#plot_images_on_grid("/Users/jmzator/Desktop/LASP_Maven_job/globe_sample_images/dummy_images_from_kyle/", "orbit03453-Ls1820-angle0410-binning0133x0019-heq-globe.png", "sample_grid.png")


# main.py seems to be having issues running code - is there a stop point somewhere above??
# I couldn't get cartopy code to work and output a figure in main, but when copied
# over to new python file 'cartopy_work.py' then it ran with no issue immediately
# did I change a setting in main? or put stop point above that's preventing code from fully running?
# I've spent at least 6 hours over today and yesterday working in main and not realizing same code
# works in different py file in this project; what's going on??????
##### BASED ON RESEARCH, THINK IT WAS THE RAISE SYSTEM EXIT CODE THAT STOPS PROGRAM AND GIVES 'ERROR' MESSAGE 9


