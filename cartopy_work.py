
# work with cartopy now to get handle on it before use full IUVS data

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

# example says need 2d data array (like 180 lat and 360 lon for globe)
lat = np.linspace(-90, 90, 180)
lon = np.linspace(-180, 180, 360)
#data = np.random.rand(180, 360)  this was just for random trial
data = np.load('iuvs_test_array.npy')
data_bin = np.reshape(data, (data.shape[0] * data.shape[1], data.shape[2]))
#data_bin = data[:, :, 0]  this was for leaving off last array shape since cartopy wants 2 not 3
lats = np.linspace(-90, 90, data.shape[0])
lons = np.linspace(0, 360, data.shape[1])

# need meshgrid for lat and lon then
lon2d, lat2d = np.meshgrid(lons, lats)

fig = plt.figure(figsize=(10, 10))

# orthographic projection seems to be one I want for globe visual want to reproduce
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Orthographic(central_longitude=0, central_latitude=0))
ax.set_global()

# plot the 2d data array (still need to make sure can add 3rd as the RGB
img = ax.pcolormesh(lon2d, lat2d, data_bin, transform=ccrs.PlateCarree()) #, cmap='viridis')

# plt.show()

plt.savefig("globe_try.png")

# this code block works to produce viridis colored pixels globe as test/sample
# changed now to use test array of iuvs data, produces globe but looks terrible hahaha
# getting there bit by bit!


### end ###

