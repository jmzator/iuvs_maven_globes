
# work with cartopy now to get handle on it before use IUVS data

import cartopy
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

# example says need 2d data array (like 180 lat and 360 lon for globe)
lat = np.linspace(-90, 90, 180)
lon = np.linspace(-180, 180, 360)
data = np.random.rand(180, 360)

# need meshgrid for lat and lon then
lon2d, lat2d = np.meshgrid(lon, lat)

fig = plt.figure(figsize=(10, 10))

# orthographic projection seems to be one I want for globe visual want to reproduce
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Orthographic(central_longitude=0, central_latitude=0))
ax.set_global()

# plot the 2d data array
img = ax.pcolormesh(lon2d, lat2d, data, transform=ccrs.PlateCarree(), cmap='viridis')

# plt.show()

plt.savefig("globe_try.png")

# this code block works to produce viridis colored pixels globe as test/sample


### end ###
