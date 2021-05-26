'''
DistanceToPlateBoundaries.py

Calculates the distance from a set of points to nearby plate boundaries. 
It does this by calling scripts with gmt commands.

'''
## Modify here
# list of plate boundary files
# filename first, second the label you want to use

# Note that for adding distances to the input file, the code will 
# ONLY use the distances from the first plate boundary model used.

PBFiles = [
    ['Bird2003.txt','Bird03'],
    ['usgs_plates.gmt.txt','usgs']
    ]
# name of input file with station information
ifn = 'InputData.csv'

## No need to edit below here

# set up
import os
import sys
from subprocess import call
import pandas as pd
#import matplotlib.pyplot as plt
#import cartopy.crs as ccrs

# get data from input
StaData = pd.read_csv(ifn, index_col=None)

NWs = StaData.Network
Stnms = StaData.Station
Lats = StaData.Latitude
Lons = StaData.Longitude

if len(Lats) != len(Lons):
    print("Location error... different number of lat/lon elements!")
    sys.exit()

# create temp file with station locations
with open('StaLocs.tmp','w') as tf:
    for i in range(len(Lats)):
        tf.write(str(Lons[i])+' '+str(Lats[i])+'\n') # use gmt notation; lons first
tf.close()

# use station locations to calculate distance to plate boundary
for i in range(len(PBFiles)):
    PBFileName = PBFiles[i][0]
    PBStr = PBFiles[i][1]
    # call shell script with a GMT command inside to calculate distances
    # uses separate script so gmt flags can easily be set
    call(['./PBDist.csh',PBFileName])
    # rename the output temp file with the string
    ofnDist = 'Dists.'+PBStr+'.txt'
    os.rename('dist.tmp',ofnDist)

# Make a map that shows the difference between plate boundary models
callStr = ['./PBMap.csh']
for i in range(len(PBFiles)):
    callStr.extend([PBFiles[i][0]])
call(callStr)

# save new info to the strcuture
DistsData = pd.read_csv('Dists.'+PBFiles[0][1]+'.txt', index_col=None, delimiter='\t')
Dists = DistsData.Dist
Dists_dict = {'Distance to Nearest Plate Boundary ('+PBFiles[0][1]+')' : Dists}
Dists_df = pd.DataFrame(data=Dists_dict)
Dists_df.to_csv('DistToPlateBoundary.csv')

os.remove('dist.tmp')
os.remove('StaLocs.tmp')
