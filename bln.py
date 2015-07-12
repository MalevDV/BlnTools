#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Давид'

import arcpy
import codecs
import os.path


#A function to create new Featureclass and return an Insert Cursor, used to store Map Query Extents.
def openCursor(workspace, featureclassName, srid, Ftype):
    if not arcpy.Exists(workspace):
        print "Unable to find Workspace '{0}'...".format(workspace)
        return

    if Ftype == "POLYGON":
        arcpy.CreateFeatureclass_management(workspace, featureclassName, "POLYGON", None, None, None, srid)
    elif Ftype == "POLYLINE":
        arcpy.CreateFeatureclass_management(workspace, featureclassName, "POLYLINE", None, None, None, srid)

    Featureclass = workspace + os.sep + featureclassName

    arcpy.AddField_management(Featureclass, "Name", "TEXT", None, None, 80, None, "NULLABLE", "NON_REQUIRED")
    arcpy.AddField_management(Featureclass, "Descript", "TEXT", None, None, 80, None, "NULLABLE", "NON_REQUIRED")

    # Opening Insert Cursor...
    return arcpy.InsertCursor(Featureclass, ["SHAPE@", "Name", "Descript"])

#inBln = arcpy.GetParameterAsText(0)
#sr = arcpy.GetParameter(1)
#typeF = arcpy.GetParameter(2)
#sepp = arcpy.GetParameter(3)
#numName = arcpy.GetParameter(4)
#numDesc = arcpy.GetParameter(5)

inBln = u"C:/PycharmProjects/BLN/Bln/Produktoprovod.bln"
sr = arcpy.SpatialReference(28414)
typeF = "POLYLINE"
sepp = u"\t"
numName = 3
numDesc = 4

arcpy.env.workspace = os.path.dirname(inBln)
out_folder_path = os.path.dirname(inBln)
#out_name = "myfgdb.gdb"
#dbPath = os.path.normpath(os.path.join(out_folder_path, out_name))
#if not arcpy.Exists(dbPath):
#    arcpy.CreateFileGDB_management(out_folder_path, out_name)
#outputWorkspace = dbPath

# Open Insert Cursor on output
# output = openCursor( outputWorkspace, os.path.basename(inBln)[:-4], sr)
output = openCursor(out_folder_path, os.path.basename(inBln)[:-4]+u'.shp', sr, typeF)

if not output:
    exit()

shapeArray = arcpy.Array()

if arcpy.Exists(inBln):
    ff = codecs.open(inBln, 'r', encoding='cp1251')
    blnLines = ff.readlines()
    ff.close()
    i = 0
    while i < len(blnLines):
        ll = blnLines[i].strip().split(sepp)
        num = ll[0]
        name = u""
        if len(ll) > numName:
            name = "".join(ll[numName])
        descr = u""
        if len(ll) > numDesc:
            descr = "".join(ll[numDesc])
        i += 1
        for j in range(int(num)):
            x, y = blnLines[i].split(sepp)
            shapeArray.add(arcpy.Point(float(x), float(y)))
            i += 1

        # Save if Shape created
        if shapeArray.count > 0:
            # Create new row
            newRow = output.newRow()
            # Add Shape and Event Date
            newRow.setValue("Shape", shapeArray)
            newRow.setValue("Name", name)
            newRow.setValue("Descript", descr)
            output.insertRow(newRow)
            # Clear out Array points
            shapeArray.removeAll()