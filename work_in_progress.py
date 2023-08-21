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

files = sorted(Path('/Users/jmzator/Desktop/orbits/18001/').glob('*apoapse*muv*gz'))


hduls = [fits.open(f) for f in files]

primary = np.vstack([f['primary'].data for f in hduls])
alts = np.vstack([f['pixelgeometry'].data['pixel_corner_mrh_alt'][..., 4] for f in hduls])
latitudes = np.vstack([f['pixelgeometry'].data['pixel_corner_lat'][..., 4] for f in hduls])
longitudes = np.vstack([f['pixelgeometry'].data['pixel_corner_lon'][..., 4] for f in hduls])
solar_zenith_angles = np.vstack([f['pixelgeometry'].data['pixel_solar_zenith_angle'] for f in hduls])

mirror_angle = np.concatenate([f['integration'].data['mirror_deg'] for f in hduls])
swath_number = compute_swath_number(mirror_angle)

flatfield = np.load('/Users/jmzator/Desktop/iuvs_maven_globes/muv_flatfield_133x19.npy')[:,1:16]

primary = primary/flatfield

mask = np.logical_and(alts==0, solar_zenith_angles <= 102)
rgb = histogram_equalize_detector_image(primary, mask = mask)/255

apsis = File('/Users/jmzator/Desktop/apsis.hdf5')

subspacecraft_altitude = 5000 # apsis['apoapse/spacecraft_altitude'][5000]
subspacecraft_latitude = 30 # apsis['apoapse/subspacecraft_latitude'][18000]
subspacecraft_longitude = 45 # apsis['apoapse/subspacecraft_longitude'][18000]

rmars = 3400
fig = plt.figure(figsize=(6, 6), facecolor='w', dpi=200)
globe = ccrs.Globe(semimajor_axis=rmars * 1e3, semiminor_axis=rmars * 1e3)
projection = ccrs.NearsidePerspective(central_latitude=subspacecraft_latitude, central_longitude=subspacecraft_longitude,
                                      satellite_height=subspacecraft_altitude * 10 ** 3, globe=globe)
transform = ccrs.PlateCarree(globe=globe)
globe_ax = plt.axes(projection=projection)

checkerboard_surface = checkerboard() * 0.1
globe_ax.imshow(checkerboard_surface, transform=transform, extent=[-180, 180, -90, 90])
plt.show()
