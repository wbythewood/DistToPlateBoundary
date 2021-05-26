#!/bin/csh

#meant to be used with DistanceToPlateBoundaries.py

gmt gmtset FORMAT_FLOAT_OUT %2.0f

# variables
set Rm = "-Rg"
set Jm = "-JKf0/23"
set Jm = "-JKf180/23"

set ofn = "PB_Map.ps"
set pdfn = "PB_Map.pdf"

# coast
gmt pscoast -A1000/0/4 -W1/0.25 -W2/0.1 -Y5 $Rm $Jm -Dl -K -Ba90f30/a30f15wEsN > $ofn

#plate boundaries

if ($#argv > 0) then
    gmt psxy $1 $Rm $Jm -W1.0,red -O -K >> $ofn
    echo $1 | gmt pstext $Rm $Jm -F+cBC+f14p,red -Ya-1.0 -N -O -K >> $ofn
endif

if ($#argv > 1) then
    gmt psxy $2 $Rm $Jm -W1.0,black -O -K >> $ofn
    echo $2 | gmt pstext $Rm $Jm -F+cBC+f14p,black -Ya-1.5 -N -O -K >> $ofn
endif

if ($#argv > 2) then
    gmt psxy $3 $Rm $Jm -W1.0,blue -O -K >> $ofn
    echo $3 | gmt pstext $Rm $Jm -F+cBC+f14p,blue -Ya-2.0 -N -O -K >> $ofn
endif

if ($#argv > 3) then
    echo "Too many plate boundary models... modify PBMap.csh to add more models!"
    exit
endif

# stations
gmt psxy -Sc0.08 -Gblack $Jm $Rm -O StaLocs.tmp >> $ofn

ps2pdf $ofn $pdfn
rm $ofn
open $pdfn
