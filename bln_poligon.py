#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Давид'

import arcpy
import arcpy.da
import arcpy.mapping
import codecs
import os.path

#inBln = arcpy.GetParameterAsText(0)
#outFC = arcpy.GetParameterAsText(1)
#sr = arcpy.GetParameter(2)

inBln = u"C:/PycharmProjects/BLN/Bln/Mestorogd.bln"
outFC = u"C:/PycharmProjects/BLN/Bln/Mestorogd_BLNImp.shp"
sr = arcpy.SpatialReference(32145)

#arcpy.env.workspace = os.path.dirname(outFC)

#feature_set = arcpy.FeatureSet()
#feature_class = arcpy.CreateFeatureclass_management("in_memory", "tempfc", "POINT")[0]

if arcpy.Exists(inBln):
    if not arcpy.Exists(outFC):
        fc = arcpy.CreateFeatureclass_management(os.path.dirname(outFC),
                                                 os.path.basename(outFC),
                                                 geometry_type="POLYGON",
                                                 spatial_reference=sr)
    ff = codecs.open(inBln, 'r', encoding='cp1251')
    blnLines = ff.readlines()
    ff.close()
    i = 0
    features = []
    names = []
    rows = arcpy.da.InsertCursor(outFC, ["SHAPE@"])
    while i < len(blnLines):
        ll = blnLines[i].split()
        num = ll[0]
        a = ll[1]
        b = ll[2]
        name = u""
        if len(ll) > 3:
            name = " ".join(ll[3:])
        names.append(name)
        i += 1
        feature = []
        for j in range(int(num)):
            x, y = blnLines[i].split()
            feature.append([float(x), float(y)])
            i += 1
        fp = arcpy.Polygon(arcpy.Array([arcpy.Point(*coords) for coords in feature]), sr)
        features.append(fp)
        #row = rows.newRow()
        #row.setValue("SHAPE@", fp)
        #row.setValue("Name", name)
        rows.insertRow([fp])
    del rows,  # row
    dir = os.path.dirname(inBln)
    fn = os.path.basename(inBln)[:-3]+u'shp'
    arcpy.CopyFeatures_management(features, os.path.join(dir,fn))
