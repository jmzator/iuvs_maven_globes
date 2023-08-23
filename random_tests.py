
# dump point for testing random things in project
# keep separate from main or necessary python files
'''
import numpy as np

data = np.load('iuvs_test_array.npy')
print(data)
'''

from astropy.io import fits

filepath = '/Volumes/LASP_MAVEN/orbit18100/'

with fits.open(filepath + 'mvn_iuv_l1b_apoapse-orbit18110-muv_20230130T220601_v13_r01.fits.gz') as hdul:
    hdul.info()

### end ###
