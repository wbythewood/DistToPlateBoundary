#!/bin/csh

# Read in plate boundary file name, and calculate distance to plate boundaries
# from a hardwired temporary station file name. 
#
# Meant to be used with python script DistanceToPlateBoundaries.py

set pbfn = $1

gmt gmtset FORMAT_FLOAT_OUT %2.3f
echo "StaLat	StaLon	Dist	NearestLat	NearestLon" > dist.tmp
gmt mapproject StaLocs.tmp -L$pbfn+uk >> dist.tmp 
#+uk makes the output unit in km. Can change, e.g., to meter by appending +ue.
