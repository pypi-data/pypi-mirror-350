#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from osgeo import gdal
from qgis.core import *
from qgis.PyQt.QtGui import QFont, QColor
import shutil
from common import safe_remove

def createQGISMap(tiffile, pngfile, qgs_template, items_dict, colorbarfile, level=3, et='', mapid='Map1', removetiff=True):
    print(tiffile, pngfile, qgs_template, items_dict, colorbarfile)
    # {{{
    # 解决ERROR 6: The PNG driver does not support update access to existing datasets.
    gdal.PushErrorHandler('CPLQuietErrorHandler')
    gdal.SetConfigOption("GDAL_PAM_ENABLED", "NO")

    # create a reference to the QgsApplication, setting the # second argument to False disables the GUI
    qgs = QgsApplication([], False)
    # load providers
    qgs.initQgis()

    # p1：读取qgs模板文件
    project = QgsProject.instance()
    project.read(qgs_template)

    # 加载栅格图层
    rlayer = QgsRasterLayer(tiffile, "rlayer")
    project.addMapLayer(rlayer)

    # 修改图层顺序
    root = project.layerTreeRoot()

    myrlayer = root.findLayer(rlayer.id())
    rlayclone = myrlayer.clone()
    parent = myrlayer.parent()
    parent.insertChildNode(level, rlayclone)
    parent.removeChildNode(myrlayer)

    # rlayer.renderer().setRedBand(3)
    # rlayer.renderer().setGreenBand(2)
    # rlayer.renderer().setBlueBand(1)
    ContrastEnhancement = QgsContrastEnhancement.StretchToMinimumMaximum

    myRedBand = rlayer.renderer().redBand()
    myRedType = rlayer.renderer().dataType(myRedBand)
    myRedEnhancement = QgsContrastEnhancement(myRedType)
    myRedEnhancement.setContrastEnhancementAlgorithm(ContrastEnhancement, True)
    myRedEnhancement.setMinimumValue(0)
    myRedEnhancement.setMaximumValue(255)
    rlayer.renderer().setRedContrastEnhancement(myRedEnhancement)

    myGreenBand = rlayer.renderer().greenBand()
    myGreenType = rlayer.renderer().dataType(myGreenBand)
    myGreenEnhancement = QgsContrastEnhancement(myGreenType)
    myGreenEnhancement.setContrastEnhancementAlgorithm(ContrastEnhancement, True)
    myGreenEnhancement.setMinimumValue(0)
    myGreenEnhancement.setMaximumValue(255)
    rlayer.renderer().setGreenContrastEnhancement(myGreenEnhancement)

    myBlueBand = rlayer.renderer().blueBand()
    myBlueType = rlayer.renderer().dataType(myBlueBand)
    myBlueEnhancement = QgsContrastEnhancement(myBlueType)
    myBlueEnhancement.setContrastEnhancementAlgorithm(ContrastEnhancement, True)
    myBlueEnhancement.setMinimumValue(0)
    myBlueEnhancement.setMaximumValue(255)
    rlayer.renderer().setBlueContrastEnhancement(myBlueEnhancement)
    rlayer.triggerRepaint()

    # 获取qgs模板文件中的制图模板
    layout = project.layoutManager().layoutByName("layout")
    if str(type(et)) ==  str(type('')):
        pass
    else:
        mapitem = layout.itemById(mapid)
        extent = QgsRectangle(et[0], et[1], et[2], et[3])
        extent.scale(1.0)
        mapitem.zoomToExtent(extent)

    if colorbarfile == '':
        pass
    else:
        try:
            rec = layout.itemById("colorbar")
            rec.setPicturePath(colorbarfile)    
        except Exception as e:
            print(e)

    for k, v in items_dict.items():
        print(k, v)
        try:
            if re.search('colorbar', k):
                rec = layout.itemById(k)
                rec.setPicturePath(v)    
            else:
                layout.itemById(k).setText(v)
        except Exception as e:
            print(e)

    layout.refresh()

    # 输出图片
    exporter = QgsLayoutExporter(layout)
    exporter.exportToImage(pngfile+'.tmp.qgs.png', QgsLayoutExporter.ImageExportSettings())
    print(tiffile, pngfile, qgs_template, items_dict, colorbarfile)
    print(removetiff)
    if removetiff:
        safe_remove(tiffile)

    if re.search(r'\.cliptiff\.', tiffile):
        safe_remove(tiffile)

    os.replace(pngfile+'.tmp.qgs.png', pngfile)
    return
    # }}}


def createQGISMaps(tiffiles, pngfile, qgs_template, items_dict, colorbarfile, levels='3,5', et='', mapid='Map1', removetiff=True):
    # {{{
    # 解决ERROR 6: The PNG driver does not support update access to existing datasets.
    gdal.PushErrorHandler('CPLQuietErrorHandler')
    gdal.SetConfigOption("GDAL_PAM_ENABLED", "NO")

    # create a reference to the QgsApplication, setting the # second argument to False disables the GUI
    qgs = QgsApplication([], False)
    # load providers
    qgs.initQgis()

    # p1：读取qgs模板文件
    project = QgsProject.instance()
    project.read(qgs_template)

    itiff = -1
    levels = re.findall(r'\d+', str(levels))
    for tiffile in tiffiles:
        itiff += 1
        level = int(levels[itiff])
        # 加载栅格图层
        rlayer = QgsRasterLayer(tiffile, "rlayer")
        project.addMapLayer(rlayer)

        # 修改图层顺序
        root = project.layerTreeRoot()

        myrlayer = root.findLayer(rlayer.id())
        rlayclone = myrlayer.clone()
        parent = myrlayer.parent()
        parent.insertChildNode(level, rlayclone)
        parent.removeChildNode(myrlayer)

        # rlayer.renderer().setRedBand(3)
        # rlayer.renderer().setGreenBand(2)
        # rlayer.renderer().setBlueBand(1)
        ContrastEnhancement = QgsContrastEnhancement.StretchToMinimumMaximum

        myRedBand = rlayer.renderer().redBand()
        myRedType = rlayer.renderer().dataType(myRedBand)
        myRedEnhancement = QgsContrastEnhancement(myRedType)
        myRedEnhancement.setContrastEnhancementAlgorithm(ContrastEnhancement, True)
        myRedEnhancement.setMinimumValue(0)
        myRedEnhancement.setMaximumValue(255)
        rlayer.renderer().setRedContrastEnhancement(myRedEnhancement)

        myGreenBand = rlayer.renderer().greenBand()
        myGreenType = rlayer.renderer().dataType(myGreenBand)
        myGreenEnhancement = QgsContrastEnhancement(myGreenType)
        myGreenEnhancement.setContrastEnhancementAlgorithm(ContrastEnhancement, True)
        myGreenEnhancement.setMinimumValue(0)
        myGreenEnhancement.setMaximumValue(255)
        rlayer.renderer().setGreenContrastEnhancement(myGreenEnhancement)

        myBlueBand = rlayer.renderer().blueBand()
        myBlueType = rlayer.renderer().dataType(myBlueBand)
        myBlueEnhancement = QgsContrastEnhancement(myBlueType)
        myBlueEnhancement.setContrastEnhancementAlgorithm(ContrastEnhancement, True)
        myBlueEnhancement.setMinimumValue(0)
        myBlueEnhancement.setMaximumValue(255)
        rlayer.renderer().setBlueContrastEnhancement(myBlueEnhancement)
        rlayer.triggerRepaint()

    # 获取qgs模板文件中的制图模板
    layout = project.layoutManager().layoutByName("layout")
    if str(type(et)) ==  str(type('')):
        pass
    else:
        mapitem = layout.itemById(mapid)
        extent = QgsRectangle(et[0], et[1], et[2], et[3])
        extent.scale(1.0)
        mapitem.zoomToExtent(extent)

    if colorbarfile == '':
        pass
    else:
        rec = layout.itemById("colorbar")
        rec.setPicturePath(colorbarfile)    

    for k, v in items_dict.items():
        if re.search('colorbar', k):
            rec = layout.itemById(k)
            rec.setPicturePath(v)    
        else:
            layout.itemById(k).setText(v)
    layout.refresh()

    # 输出图片
    exporter = QgsLayoutExporter(layout)
    exporter.exportToImage(pngfile+'.tmp.png', QgsLayoutExporter.ImageExportSettings())
    if removetiff:
        pass
    os.replace(pngfile + '.tmp.png', pngfile)
    # }}}


if __name__ == '__main__':
    tiffile = r"D:\bin\peng\amv.test.tiff"
    pngfile = r"D:\bin\peng\amv1.png"
    qgs_template = r"D:\bin\peng\china\template.qgs"

    chndict = {"title": "卫星云导风产品空间分布图",
               "date": "2021-01-11 10:10:00(北京时)",
               "satellite": "卫星/传感器:FY-4A/AGRI",
               "resolution": "分辨率:4000M"}

    createQGISMap(tiffile, pngfile, qgs_template, chndict, pngfile)
