#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Давид'

import arcpy

infc = arcpy.GetParameterAsText(0)
blnFile = arcpy.GetParameterAsText(1)
name = arcpy.GetParameterAsText(2)
desr = arcpy.GetParameterAsText(3)

filds = ["OID@", "SHAPE@"]
names = []
descriptions = []
points = []

# Enter for loop for each feature
#
for row in arcpy.da.SearchCursor(infc, filds):
    # Print the current multipoint's ID
    #
    print("Feature {0}:".format(row[0]))
    partnum = 0

    # Step through each part of the feature
    #
    for part in row[1]:
        # Print the part number
        #
        print("Part {0}:".format(partnum))

        # Step through each vertex in the feature
        #
        pp = []
        for pnt in part:
            if pnt:
                # Print x,y coordinates of current point
                #
                print("{0}, {1}".format(pnt.X, pnt.Y))
                pp.append((pnt.X, pnt.Y))
            else:
                # If pnt is None, this represents an interior ring
                #
                points.append(pp)
                print("Interior Ring:")
                pp = []
        partnum += 1
        points.append(pp)

print points