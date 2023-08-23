import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np
from pathlib import Path
from histogram_coloring import histogram_equalize_detector_image
import warnings
from h5py import File
from globe_functions import checkerboard
import cartopy.crs as ccrs


def compute_swath_number(mirror_angle: np.ndarray) -> np.ndarray:
    """Make the swath number associated with each mirror angle.

    This function assumes the input is all the mirror angles (or, equivalently,
    the field of view) from an orbital segment. Omitting some mirror angles
    may result in nonsensical results. Adding additional mirror angles from
    multiple segments or orbits will certainly result in nonsensical results.

    Parameters
    ----------
    mirror_angle

    Returns
    -------
    np.ndarray
        The swath number associated with each mirror angle.

    Notes
    -----
    This algorithm assumes the mirror in roughly constant step sizes except
    when making a swath jump. It finds the median step size and then uses
    this number to find swath discontinuities. It interpolates between these
    indices and takes the floor of these values to get the integer swath
    number.

    """
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        mirror_change = np.diff(mirror_angle)
        threshold = np.abs(np.median(mirror_change)) * 4
        mirror_discontinuities = np.where(np.abs(mirror_change) > threshold)[0] + 1
        if any(mirror_discontinuities):
            n_swaths = len(mirror_discontinuities) + 1
            integrations = range(len(mirror_angle))
            interp_swaths = np.interp(integrations, mirror_discontinuities, range(1, n_swaths), left=0)
            swath_number = np.floor(interp_swaths).astype('int')
        else:
            swath_number = np.zeros(mirror_angle.shape)

    return swath_number


# original filepath for first globe tests right below
#files = sorted(Path('/Users/jmzator/Desktop/orbits/18002/').glob('*apoapse*muv*gz'))

# now try rewriting for exHD saved orbits that are bulk saved
files = sorted(Path('/Volumes/LASP_MAVEN/orbit18100/').glob('*apoapse*18154*muv*gz'))
# this works, just need to have exHD plugged in and then just change the wildcard
# after glob to give specific orbit
# note that this leaves some globe portions black for some orbits so
# I need to configure the lat/lon for each globe, pull that from header prob


hduls = [fits.open(f) for f in files]

primary = np.vstack([f['primary'].data for f in hduls])
alts = np.vstack([f['pixelgeometry'].data['pixel_corner_mrh_alt'][..., 4] for f in hduls])
latitudes = np.vstack([f['pixelgeometry'].data['pixel_corner_lat'] for f in hduls])
longitudes = np.vstack([f['pixelgeometry'].data['pixel_corner_lon'] for f in hduls])
solar_zenith_angles = np.vstack([f['pixelgeometry'].data['pixel_solar_zenith_angle'] for f in hduls])

mirror_angle = np.concatenate([f['integration'].data['mirror_deg'] for f in hduls])
swath_number = compute_swath_number(mirror_angle)

flatfield = np.load('/Users/jmzator/Desktop/iuvs_maven_globes/muv_flatfield_133x19.npy')[:,1:16]

primary = primary/flatfield

mask = np.logical_and(alts==0, solar_zenith_angles <= 102)
image = histogram_equalize_detector_image(primary, mask = mask)/255

apsis = File('/Users/jmzator/Desktop/apsis.hdf5')

# here's where can manually change lat/lon (mostly lon) for individual globe creation
subspacecraft_altitude = 5000 # apsis['apoapse/spacecraft_altitude'][5000]
subspacecraft_latitude = 30 #30 # apsis['apoapse/subspacecraft_latitude'][18000]
subspacecraft_longitude = 125 #-55 lon each orbit #45 # apsis['apoapse/subspacecraft_longitude'][18000]

rmars = 3400
fig = plt.figure(figsize=(6, 6), facecolor='w', dpi=200)
globe = ccrs.Globe(semimajor_axis=rmars * 1e3, semiminor_axis=rmars * 1e3)
projection = ccrs.NearsidePerspective(central_latitude=subspacecraft_latitude, central_longitude=subspacecraft_longitude,
                                      satellite_height=subspacecraft_altitude * 10 ** 3, globe=globe)
transform = ccrs.PlateCarree(globe=globe)
globe_ax = plt.axes(projection=projection)

checkerboard_surface = checkerboard()  * 0.1 # (the 0.1 to make checkerboard darker or less visible as checkers
globe_ax.imshow(checkerboard_surface, transform=transform, extent=[-180, 180, -90, 90])


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


for swath in np.unique(swath_number):
    swath_indices = swath_number == swath

    x, y = latlon_meshgrid(latitudes[swath_indices], longitudes[swath_indices], alts[swath_indices])

    rgb = image[swath_indices]
    fill = rgb[..., 0]

    colors = np.reshape(rgb, (rgb.shape[0] * rgb.shape[1], rgb.shape[2]))
    globe_ax.pcolormesh(x, y, fill, color=colors, linewidth=0, edgecolors='none', rasterized=True,
                        transform=transform).set_array(None)

#plt.show()

plt.savefig('globe_orbit_1')
plt.close()
