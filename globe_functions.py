
##### from Kyle email 2023-08-01 from his quick look globes code
# look through, understand it, ask questions, then work on using it!

# "I have some functions that I use when plotting globes / quicklooks.
# I think you will benefit from these. Please ask questions about their purpose if you have them.
# I started creating globes by plotting a checkerboard pattern on a globe.
# This way it's fairly clear what is and is not data. When you plot data, it'll overplot the checkerboard"


import numpy as np
import matplotlib as plt
import cartopy.crs as ccrs
from histogram_coloring import histogram_equalize_detector_image




def checkerboard():
    """
    Create an 5-degree-size RGB checkerboard array for display with matplotlib.pyplot.imshow().

    Parameters
    ----------
    None

    Returns
    -------
    grid : array
        The checkerboard grid.
    """
    return np.repeat(np.kron([[0.67, 0.33] * 36, [0.33, 0.67] * 36] * 18, np.ones((5, 5)))[:, :, None], 3, axis=2)

# This will create an array for cartopy to plot latitude and longitudes.

def latlon_meshgrid(latitude, longitude, altitude):
    # make meshgrids to hold latitude and longitude grids for pcolormesh display
    X = np.zeros((latitude.shape[0] + 1, latitude.shape[1] + 1))
    Y = np.zeros((longitude.shape[0] + 1, longitude.shape[1] + 1))
    mask = np.ones((latitude.shape[0], latitude.shape[1]))

    # loop through pixel geometry arrays
    for i in range(int(latitude.shape[0])):
        for j in range(int(latitude.shape[1])):

            # there are some pixels where some of the pixel corner longitudes are undefined
            # if we encounter one of those, set the data value to missing so it isn't displayed
            # with pcolormesh
            if np.size(np.where(np.isfinite(longitude[i, j]))) != 5:
                mask[i, j] = np.nan

            # also mask out non-disk pixels
            if altitude[i, j] != 0:
                mask[i, j] = np.nan

            # place the longitude and latitude values in the meshgrids
            X[i, j] = longitude[i, j, 1]
            X[i + 1, j] = longitude[i, j, 0]
            X[i, j + 1] = longitude[i, j, 3]
            X[i + 1, j + 1] = longitude[i, j, 2]
            Y[i, j] = latitude[i, j, 1]
            Y[i + 1, j] = latitude[i, j, 0]
            Y[i, j + 1] = latitude[i, j, 3]
            Y[i + 1, j + 1] = latitude[i, j, 2]

    # set any of the NaN values to zero (otherwise pcolormesh will break even if it isn't displaying the pixel).
    X[np.where(~np.isfinite(X))] = 0
    Y[np.where(~np.isfinite(Y))] = 0

    # set to domain [-180,180)
    X[np.where(X > 180)] -= 360

    # return the coordinate arrays and the mask
    return X, Y

# This is the "main" function that creates globes. I made these using hdf5 files,
# so you'll need to vstack the data every time you see f['some/path']

# add in file and path, etc to clear errors as said in code comments above

def make_apoapse_muv_globe(orbit: int) -> None:
    orbit_block = make_orbit_block(orbit)
    orbit_code = make_orbit_code(orbit)

    f = File(file_path / orbit_block / f'{orbit_code}.hdf5')

    dayside = f['apoapse/muv/integration/dayside_integrations'][:]
    opportunity_swaths = f['apoapse/integration/opportunity_classification'][:]
    dayside_science_integrations = np.logical_and(dayside, ~opportunity_swaths)

    if np.sum(dayside_science_integrations) == 0:
        return

    brightness = f['apoapse/muv/dayside/detector/brightness'][~opportunity_swaths[dayside]]
    swath_number = f['apoapse/integration/swath_number'][dayside]
    tangent_altitude = f['apoapse/muv/dayside/spatial_bin_geometry/tangent_altitude'][:][..., 4]
    solar_zenith_angle = f['apoapse/muv/dayside/spatial_bin_geometry/solar_zenith_angle'][:]
    latitude = f['apoapse/muv/dayside/spatial_bin_geometry/latitude'][~opportunity_swaths[dayside]]
    longitude = f['apoapse/muv/dayside/spatial_bin_geometry/longitude'][~opportunity_swaths[dayside]]
    subspacecraft_latitude = f['apoapse/apsis/subspacecraft_latitude'][0]
    subspacecraft_longitude = f['apoapse/apsis/subspacecraft_longitude'][0]
    subspacecraft_altitude = f['apoapse/apsis/subspacecraft_altitude'][0]

    solar_zenith_angle[tangent_altitude != 0] = np.nan
    #brightness = remove_seam(brightness, swath_number, latitude, longitude, tangent_altitude, subspacecraft_latitude, subspacecraft_longitude, subspacecraft_altitude)

    mask = np.logical_and(tangent_altitude == 0, solar_zenith_angle <= 102)
    try:
        image = histogram_equalize_detector_image(brightness, mask=mask) / 255
    except IndexError:
        return

    # Setup the graphic
    rmars = 3400
    fig = plt.figure(figsize=(6, 6), facecolor='w', dpi=200)
    globe = ccrs.Globe(semimajor_axis=rmars * 1e3, semiminor_axis=rmars * 1e3)
    projection = ccrs.NearsidePerspective(central_latitude=subspacecraft_latitude, central_longitude=subspacecraft_longitude,
                                          satellite_height=subspacecraft_altitude * 10 ** 3, globe=globe)
    transform = ccrs.PlateCarree(globe=globe)
    globe_ax = plt.axes(projection=projection)

    checkerboard_surface = checkerboard() * 0.1
    globe_ax.imshow(checkerboard_surface, transform=transform, extent=[-180, 180, -90, 90])

    for swath in np.unique(swath_number):
        swath_indices = swath_number == swath

        x, y = latlon_meshgrid(latitude[swath_indices], longitude[swath_indices], tangent_altitude[swath_indices])

        rgb = image[swath_indices]
        fill = rgb[..., 0]

        colors = np.reshape(rgb, (rgb.shape[0] * rgb.shape[1], rgb.shape[2]))
        globe_ax.pcolormesh(x, y, fill, color=colors, linewidth=0, edgecolors='none', rasterized=True, transform=transform).set_array(None)

    # Get info I need for the filename (add this in to clear errors)
    solar_longitude = f['apoapse/apsis/solar_longitude'][:][0]
    subsolar_subspacecraft_angle = f['apoapse/apsis/subsolar_subspacecraft_angle'][:][0]
    spatial_bin_width = f['apoapse/muv/dayside/binning/spatial_bin_edges'][:].shape[0] - 1
    spectral_bin_width = f['apoapse/muv/dayside/binning/spectral_bin_edges'][:].shape[0] - 1

    filename = make_filename(orbit_code, solar_longitude, subsolar_subspacecraft_angle, spatial_bin_width, spectral_bin_width, 'heq', 'globe')
    save = save_location / make_orbit_block(orbit) / filename
    save.parent.mkdir(parents=True, exist_ok=True)
    print(save_location / save)
    plt.savefig(save_location / save)
    plt.close(fig)

# These are helper functions for working with the IUVS orbit block conventions

import math


def make_orbit_block(orbit: int) -> str:
    """Make the orbit block corresponding to an input orbit.

    Parameters
    ----------
    orbit
        The orbit number.

    Returns
    -------
    str
        The orbit block.

    See Also
    --------
    make_orbit_code: Make the orbit code corresponding to a given orbit.

    Examples
    --------
    Make the orbit block for orbit 3453

    >>> make_orbit_block(3453)
    'orbit03400'

    """
    block = math.floor(orbit / 100) * 100
    return 'orbit' + f'{block}'.zfill(5)


def make_orbit_code(orbit: int) -> str:
    """Make the orbit code corresponding to an input orbit.

    Parameters
    ----------
    orbit
        The orbit number.

    Returns
    -------
    str
        The orbit code.

    See Also
    --------
    make_orbit_block: Make the orbit block corresponding to a given orbit.

    Examples
    --------
    Make the orbit code for orbit 3453

    >>> make_orbit_code(3453)
    'orbit03453'

    """
    return 'orbit' + f'{orbit}'.zfill(5)


def make_orbit_floor(orbit: int):
    return math.floor(orbit / 100) * 100