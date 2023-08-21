import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np
from pathlib import Path
from histogram_coloring import histogram_equalize_detector_image

files = sorted(Path('/Users/jmzator/Desktop/orbits/18001/').glob('*apoapse*muv*gz'))

print(files)

hduls = [fits.open(f) for f in files]

primary = np.vstack([f['primary'].data for f in hduls])
alts = np.vstack([f['pixelgeometry'].data['pixel_corner_mrh_alt'][..., 4] for f in hduls])
print(primary.shape)
flatfield = np.load('/Users/jmzator/Desktop/iuvs_maven_globes/muv_flatfield_133x19.npy')[:,1:16]
print(flatfield.shape)
primary = primary/flatfield
print(alts.shape)

mask = alts == 0
rgb = histogram_equalize_detector_image(primary, mask = mask)/255
print(rgb.shape)

fig,ax = plt.subplots()
ax.imshow(rgb)
plt.show()
