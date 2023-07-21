########
# this next block replaces the previous commit's block that
# output a blank grid of squares for initial trial on sizing
# this code fills in dummy images into printable grid
# can change the 'square_size' and 'grid_size' parameter below
# to get different number of globes of varying sizes on the sheet
# based upon meeting with Nick & Kyle on 2023-07-17 with different
# size printouts, for now targeting the size that fits 4 columns
# and six rows of globes on the 8.5 x 11 printout (which would be

# square_size = 15 and grid_size = 6, 4

# will need to see how that looks on the 42 inch paper rolls then
# after get approval with some actual globe images

from PIL import Image, ImageDraw

square_size = 15  # cm
grid_size = (6, 4)  # number of squares in the grid (rows, columns)
margin = 0.1  # cm
output_file = "grid.png"

# image size in pixels
image_width = int((grid_size[0] * square_size + (grid_size[0] + 1) * margin) * 37.7952755906)
image_height = int((grid_size[1] * square_size + (grid_size[1] + 1) * margin) * 37.7952755906)

# blank image
image = Image.new("RGB", (image_width, image_height), "white")
draw = ImageDraw.Draw(image)

# add grid lines
for i in range(grid_size[0] + 1):
    x = i * (square_size + margin) * 37.7952755906 + margin * 37.7952755906
    draw.line([(x, margin * 37.7952755906), (x, image_height - margin * 37.7952755906)], fill="black")

for j in range(grid_size[1] + 1):
    y = j * (square_size + margin) * 37.7952755906 + margin * 37.7952755906
    draw.line([(margin * 37.7952755906, y), (image_width - margin * 37.7952755906, y)], fill="black")

# add png dummy file for testing printed size for viewing
for i in range(grid_size[0]):
    for j in range(grid_size[1]):
        # calculate position of square in pixels
        x = (i + 1) * margin * 37.7952755906 + i * square_size * 37.7952755906
        y = (j + 1) * margin * 37.7952755906 + j * square_size * 37.7952755906

        png_file = Image.open("/Users/jmzator/Desktop/LASP_Maven_job/globe_sample_images/dummy_images_from_kyle/orbit03453-Ls1820-angle0410-binning0133x0019-heq-globe.png")

        # resize to fit in the square
        png_file.thumbnail((square_size * 37.7952755906, square_size * 37.7952755906))
        image.paste(png_file, (int(x), int(y)))

# save final image
image.save(output_file)

####end that part####



#### now adding the code I had started building for reading the
# fits files into an array for histogram equalization prior to
# mapping onto globe - this is just copy/paste of code in the state
# it was in after Kyle helped me on 2023-07-17, so it still needs
# clean up since includes my code plus Kyle's more efficient code
# for reading in the files - also note I need to work on getting
# rid of errors from the latter part of that meeting
# copy/paste follows this:

from pathlib import Path
import numpy as np
from astropy.io import fits

# list of fits files
top_path = Path("/Users/jmzator/Desktop/maven_iuvs_visualization_project/orbit18001/")
# note this 'top_path' pulls from old pycharm project, once working, need to change to main source of orbits data
file_paths = sorted(top_path.glob('*orbit18001*.gz'))


def add_dimension_if_necessary(arr: np.ndarray) -> np.ndarray:
    return arr if np.ndim(arr) == 3 else arr[None, ...]


hduls = [fits.open(f) for f in file_paths]
data_arrays = np.vstack([add_dimension_if_necessary(f['primary'].data) for f in hduls])
print(data_arrays.shape)
raise SystemExit(9)


print(np.shape(data))

###### end that part from 2023-07-17 work ######



########################## 2023-07-21 ###########
# now adding copy/paste of histogram equalization code blocks
# from Kyle for once have array of fits files in proper shape
# copy/paste from old pycharm project follows:

# now, here's code from Kyle email today 2023 May 22 regarding
# histogram equalization algorithm in python, a well-known
# data visualization algorithm and something needed for
# producing the globe images from IUVS apoapse data for this project
# several functions follow:

# note from after codes blocks:
# Kyle convo 2023 May 23 lunch break from PSG: really only need to use
# the last function since that one calls the previous functions
# just read in the muv files don't need fuv, etc.
# the .gz on end of .fits is just compression and astropy knows how
# to uncompress when read in those files, so no need to manually unzip

# use numpy vstack, throw away all fuv, use only muv,
# stack those primary ones - prob dimensions like (200, x, 19) first one

# keep the functions commented out until get arrays issue correct

'''
def make_equidistant_spectral_cutoff_indices(n_spectral_bins: int) -> tuple[int, int]:
    """Make indices such that the input spectral bins are in 3 equally spaced color channels.
    Parameters
    ----------
    n_spectral_bins
        The number of spectral bins.
    Returns
    -------
    The blue-green and the green-red cutoff indices.
    Examples
    --------
    Get the wavelength cutoffs for some common apoapse MUV spectral binning schemes.
    >>> make_equidistant_spectral_cutoff_indices(15)
    (5, 10)
    >>> make_equidistant_spectral_cutoff_indices(19)
    (6, 13)
    >>> make_equidistant_spectral_cutoff_indices(20)
    (7, 13)
    """
    blue_green_cutoff = round(n_spectral_bins / 3)
    green_red_cutoff = round(n_spectral_bins * 2 / 3)
    return blue_green_cutoff, green_red_cutoff


def turn_detector_image_to_3_channels(image: np.ndarray) -> np.ndarray:
    """Turn a detector image into 3 channels by coadding over the spectral dimension.
    Parameters
    ----------
    image
        The image to turn into 3 channels. This is assumed to be 3 dimensional and have a shape of (n_integrations,
        n_spatial_bins, n_spectral_bins).
    Returns
    -------
    A co-added image with shape (n_integrations, n_spatial_bins, 3).
    """
    n_spectral_bins = image.shape[2]
    blue_green_cutoff, green_red_cutoff = make_equidistant_spectral_cutoff_indices(n_spectral_bins)

    red = np.sum(image[..., green_red_cutoff:], axis=-1)
    green = np.sum(image[..., blue_green_cutoff:green_red_cutoff], axis=-1)
    blue = np.sum(image[..., :blue_green_cutoff], axis=-1)

    return np.dstack([red, green, blue])


def histogram_equalize_grayscale_image(image: np.ndarray, mask: np.ndarray = None) -> np.ndarray:
    """Histogram equalize a grayscale image.
    Parameters
    ----------
    image
        The image to histogram equalize. This is assumed to be 2-dimensional (2 spatial dimensions) but can have any
        dimensionality.
    mask
        A mask of booleans where :code:`False` values are excluded from the histogram equalization scaling. This must
        have the same shape as :code:`image`.
    Returns
    -------
    A histogram equalized array with the same shape as the inputs with values ranging from 0 to 255.
    See Also
    --------
    histogram_equalize_rgb_image: Histogram equalize a 3-color-channel image.
    Notes
    -----
    I could not get the scikit-learn algorithm to work so I created this.
    The algorithm works like this:
    1. Sort all data used in the coloring.
    2. Use these sorted values to determine the 256 left bin cutoffs.
    3. Linearly interpolate each value in the grid over 256 RGB values and the
       corresponding data values.
    4. Take the floor of the interpolated values since I'm using left cutoffs.
    """
    sorted_values = np.sort(image[mask], axis=None)
    left_cutoffs = np.array([sorted_values[int(i / 256 * len(sorted_values))]
                             for i in range(256)])
    rgb = np.linspace(0, 255, num=256)
    return np.floor(np.interp(image, left_cutoffs, rgb))


def histogram_equalize_rgb_image(image: np.ndarray, mask: np.ndarray = None) -> np.ndarray:
    """Histogram equalize an RGB image.
    Parameters
    ----------
    image
        The image to histogram equalize. This is assumed to be 3-dimensional (the first 2 being spatial and the last
        being spectral). The last dimension as assumed to have a length of 3. Indices 0, 1, and 2 correspond to R, G,
        and B, respectively.
    mask
        A mask of booleans where :code:`False` values are excluded from the histogram equalization scaling. This must
        have the same shape as the first N-1 dimensions of :code:`image`.
    Returns
    -------
    A histogram equalized array with the same shape as the inputs with values ranging from 0 to 255.
    See Also
    --------
    histogram_equalize_grayscale_image: Histogram equalize a single-color-channel image.
    """
    red = histogram_equalize_grayscale_image(image[..., 0], mask=mask)
    green = histogram_equalize_grayscale_image(image[..., 1], mask=mask)
    blue = histogram_equalize_grayscale_image(image[..., 2], mask=mask)
    return np.dstack([red, green, blue])


def histogram_equalize_detector_image(image: np.ndarray, mask: np.ndarray = None) -> np.ndarray:
    """Histogram equalize a detector image.
    Parameters
    ----------
    image
        The image to histogram equalize. This is assumed to be 3-dimensional (the first 2 being spatial and the last
        being spectral).
    mask
        A mask of booleans where :code:`False` values are excluded from the histogram equalization scaling. This must
        have the same shape as the first N-1 dimensions of :code:`image`.
    Returns
    -------
    Histogram equalized IUVS image, where the output array has a shape of (M, N, 3).
    """
    coadded_image = turn_detector_image_to_3_channels(image)
    return histogram_equalize_rgb_image(coadded_image, mask=mask)
'''

######### end Kyle's code from email###########
######### end copy/paste from old pycharm project ##########


