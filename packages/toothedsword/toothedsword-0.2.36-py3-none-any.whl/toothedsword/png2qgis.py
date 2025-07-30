
import glob
import re
import os
import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal
import json
from tiff2png import createQGISMap
from tiff2png import createQGISMaps
import time
import cv2
import matplotlib.patheffects as path_effects
import time_htht as htt
from common import safe_remove
import shutil


def say(*args, **kw):
    print(*args, **kw, flush=True)
    return time.time()


def remove_white(figname, maxw=0.05, 
                 axis=0, outfile='', idy=''):
    im = plt.imread(figname).astype(np.float32)
    while im.shape[axis] <= 100:
        im = cv2.resize(im, [im.shape[1]*2, im.shape[0]*2])

    if str(type(idy)) == str(type('')):
        height, width = im.shape[0], im.shape[1]
        rgb = im[:,:,0]+im[:,:,1]+im[:,:,2]
        rgb[im[:,:,3] == 0] = 255 
        rgb = np.sum(rgb, 1-axis)
       
        w = im.shape[1-axis]*3*255
        w = np.max(rgb)
        rgb[0] = 0
        rgb[-1] = 0
        id = np.where(rgb < w)
        id = id[0]
        idb = id[1:] - id[0:-1]

        maxw = maxw * im.shape[axis]
        idb_gt_maxw = np.where(idb >  maxw)
        idb_gt_maxw = idb_gt_maxw[0]
        idy = rgb >= 0
        for i in idb_gt_maxw.tolist():
            idy[id[i]:id[i+1]] = False
            idy[id[i]:int(id[i]+maxw)] = True

    if axis == 0:
        im = im[idy, :, :]
    else:
        im = im[:, idy, :]
    
    if outfile == '':
        outfile = figname

    plt.imsave(outfile, np.ascontiguousarray(im))
    return idy


def clip_data(filepath, clipedpath, shpfile, filevalue=255):
    import rioxarray as rxr
    import geopandas as gpd
    from shapely.geometry import mapping
    ds1 = rxr.open_rasterio(filepath).squeeze()
    ds1 = ds1.rename({'x': 'longitude', 'y': 'latitude'})
    ds1.attrs["_FillValue"] = filevalue
    geodf = gpd.read_file(shpfile)
    try:
        ds1_new = ds1.rio.clip(
                geodf.geometry.apply(mapping),
                geodf.crs, drop=True)
        ds1_new.rio.to_raster(clipedpath)
    except Exception as e:
        print(e)


def writeTif_GLL(outputpath, data, lon, lat, 
                 miss=9999, datatype=gdal.GDT_Int16):
    # {{{
    wkt = 'GEOGCS["WGS 84",' \
                      'DATUM["WGS_1984",' \
                              'SPHEROID["WGS 84",6378137,298.257223563,' 'AUTHORITY["EPSG","7030"]],' \
                              'AUTHORITY["EPSG","6326"]],' \
                      'PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],' \
                      'UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],' \
                      'AXIS["Latitude",NORTH],' \
                      'AXIS["Longitude",EAST],' \
                      'AUTHORITY["EPSG","4326"]]'

    if len(data.shape) == 3:
        bands, height, width = data.shape
    else:
        bands, (height, width) = 1, data.shape
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(outputpath, width, height, bands, datatype)
    if (dataset != None):
        dataset.SetProjection(wkt)  # 写入投影
        dataset.SetGeoTransform([lon[0], lon[1]-lon[0], 0.0, lat[0], 0.0, lat[1]-lat[0]])  # 写入仿射变换参数
    if bands == 1:
        dataset.GetRasterBand(1).WriteArray(data)
        dataset.GetRasterBand(1).SetNoDataValue(miss)
    else:
        for i in range(bands):
            dataset.GetRasterBand(i + 1).WriteArray(data[i])
            dataset.GetRasterBand(i + 1).SetNoDataValue(miss)
    dataset.FlushCache()
    del dataset
    driver = None
    # }}}


class fig(object):

    """Docstring for fig. """

    def __init__(self):
        """TODO: to be defined. """
        self.prodir = os.path.dirname(os.path.abspath(__file__))
        

    def png2qgs(self):
        # generate geotifffile
        # {{{
        # figname = '/home/leon/src/fy/amv.test.png'
        figname = self.pngname
        t = plt.imread(figname)
        lonlim = self.lonlim
        latlim = self.latlim
        a = t[:,:,3]
        longd = np.linspace(lonlim[0], lonlim[1], t.shape[1])
        latgd = np.linspace(latlim[0], latlim[1], t.shape[0])
        t = t * 255
        r = t[:,:,0]
        g = t[:,:,1]
        b = t[:,:,2]
        r[a == 0] = 999
        t[:,:,0] = r
        # t[2000:2100,2000:2100,:] = 1
        # t[2100:2200,2100:2200,:] = 255
        t = np.transpose(t[-1::-1,:,0:3], [2, 0, 1])
        tiffile = figname+'.tiff'
        writeTif_GLL(tiffile, t, longd, latgd, miss=999)
        # }}}

        # genrate qgs file
        # {{{
        try:
            pngfile = self.qgsfile
        except Exception as e:
            pngfile = self.pngname
            self.qgsfile = pngfile

        qgs_template = self.qgs_template
        chndict = {"title": self.ttl,
                   "date": self.rttl,
                   "satellite": self.instrument,
                   "resolution": self.resolution}

        if self.mpro:
            import multiprocessing
            ctx = multiprocessing.get_context('spawn')
            p = ctx.Process(target=tiff2png.createQGISMap, args=(tiffile, pngfile, qgs_template, chndict, self.colorbarfile, self.qgslevel))
            p.start()
            p.join()
        else:
            schndict = dict2str(chndict)
            cmd = 'python3 '+self.prodir+'/qgisfig/tiff2png_exe.py '+tiffile+' '+pngfile+' '+\
                    qgs_template+' "'+schndict+'" '+self.colorbarfile+' '+str(self.qgslevel)
            try:
                cmd = cmd + ' ' + self.et
            except Exception as e:
                print(e)
            say(cmd)
            os.system(cmd)

        self.qgsfile = pngfile
        # }}}


    def png2qgs_json(self):
        # generate geotifffile
        # {{{
        # figname = '/home/leon/src/fy/amv.test.png'
        print(htt.time2str(time.time(), 'yyyy:mm:dd HH:MM:SS'))
        tiffile = ''

        with open(self.qgs_json_file) as json_file:
            self.qgs_json = json.load(json_file)

        with open(self.png_json_file) as json_file:
            self.png_json = json.load(json_file)

        self.qgsfile = self.png_json['qgsfile']

        if 'tiff' in self.png_json:
            if os.path.exists(self.png_json['tiff']):
                tiffile = self.png_json['tiff']

        if tiffile == '':
            time0 = say('gen tiff')
            print(htt.time2str(time.time(), 'yyyy:mm:dd HH:MM:SS'))
            figname = self.pngfile
            t = plt.imread(figname)

            if 'cbpos' in self.png_json:
                cbpos = self.png_json['cbpos']
                xsize = t.shape[1]
                ysize = t.shape[0]
                ynd = int((1-cbpos[1])*ysize)
                yst = int((1-cbpos[1]-cbpos[3])*ysize)
                xst = int(cbpos[0]*xsize)
                xnd = int((cbpos[0]+cbpos[2])*xsize)
                cb = t[yst:ynd,xst:xnd,:]
                cbfile = self.pngfile+'.cb.tmp.png'
                plt.imsave(cbfile, cb)
                maxw0 = 0.01
                maxw1 = 0.01
                try:
                    maxw0 = float(self.png_json['maxw0'])
                except Exception as e:
                    pass
                try:
                    maxw1 = float(self.png_json['maxw1'])
                except Exception as e:
                    pass
                remove_white(cbfile, maxw=maxw0, axis=0)
                remove_white(cbfile, maxw=maxw1, axis=1)

                if 'cb_alpha' in self.png_json:
                    t1 = plt.imread(cbfile)
                    a1 = t1[:,:,3]

                    r1 = t1[:,:,0]
                    g1 = t1[:,:,1]
                    b1 = t1[:,:,2]
                    if 'cb_bg' in self.png_json:
                        r1[a1 == 0] = self.png_json['cb_bg'][0]
                        g1[a1 == 0] = self.png_json['cb_bg'][1]
                        b1[a1 == 0] = self.png_json['cb_bg'][2]
                    else:
                        r1[a1 == 0] = 0
                        g1[a1 == 0] = 0
                        b1[a1 == 0] = 0
                    a1[a1 == 0] = self.png_json['cb_alpha']

                    plt.imsave(cbfile, t1)

                if 'colorbar' in self.png_json:
                    pass
                else:
                    self.png_json['colorbar'] = cbfile
                    self.colorbarfile = cbfile
                    say('cmd:rm -rf '+cbfile)
                    with open(self.png_json_file, "w", encoding='utf-8') as f:
                        json.dump(self.png_json, f)
                    pass

            if 'axpos' in self.png_json:
                axpos = self.png_json['axpos']
                xsize = t.shape[1]
                ysize = t.shape[0]
                ynd = int((1-axpos[1])*ysize)
                yst = int((1-axpos[1]-axpos[3])*ysize)
                xst = int(axpos[0]*xsize)
                xnd = int((axpos[0]+axpos[2])*xsize)
                t = t[yst:ynd,xst:xnd,:]

            print(htt.time2str(time.time(), 'yyyy:mm:dd HH:MM:SS'))
            lonlim = self.png_json['lonlim']
            latlim = self.png_json['latlim']
            longd = np.linspace(lonlim[0], lonlim[1], t.shape[1])
            latgd = np.linspace(latlim[0], latlim[1], t.shape[0])
            t = t * 255
            r = t[:,:,0]
            g = t[:,:,1]
            b = t[:,:,2]
            try:
                a = t[:,:,3]
                r[a == 0] = 999
            except Exception as e:
                print(e)
            t[:,:,0] = r
            # t[2000:2100,2000:2100,:] = 1
            # t[2100:2200,2100:2200,:] = 255
            t = np.transpose(t[-1::-1,:,0:3], [2, 0, 1])
            try:
                tiffile = self.png_json['tiff']
            except Exception as e:
                tiffile = figname+'.'+str(time.time())+'.tiff'
            if 'tiffdatatype' in self.png_json:
                if self.png_json['tiffdatatype'] == 'uint8':
                    t1 = np.ones([t.shape[0]+1, t.shape[1], t.shape[2]])
                    t1[0:3, :, :] = t
                    t1[3, :, :] = 255
                    r = t1[0, :, :]
                    g = t1[1, :, :]
                    b = t1[2, :, :]
                    a = t1[3, :, :]
                    a[(r > 255) | (g > 255) | (g > 255)] = 0
                    t1[t1 > 255] = 255
                    t1[t1 < 0] = 0
                    writeTif_GLL(tiffile, t1, longd, latgd, 
                                 miss=999, datatype=gdal.GDT_Byte)
            else:
                writeTif_GLL(tiffile, t, longd, latgd, miss=999)
            say('gen tiff finished', time.time()-time0)
            print(htt.time2str(time.time(), 'yyyy:mm:dd HH:MM:SS'))

            if 'outpng' in self.png_json:
                t1 = np.ones([t.shape[1], t.shape[2], 4])
                t1[:, :, 0:3] = t.transpose(1,2,0)/255
                r = t1[:, :, 0] 
                g = t1[:, :, 1]
                b = t1[:, :, 2]
                a = t1[:, :, 3]
                id = (r > 1) | (g > 1) | (b > 1)
                r[id] = 1
                g[id] = 1
                b[id] = 1
                a[id] = 0
                plt.imsave(self.png_json['outpng'], t1)

        tiffile1 = tiffile
        try:
            if self.png_json['removeout'] == 'yes':
                t0 = say('clip tiff')
                print(htt.time2str(time.time(), 'yyyy:mm:dd HH:MM:SS'))
                try:
                    shpfile = self.png_json['bounds']
                except Exception as e:
                    shpfile = re.sub(r'[^\/\\]+$', 'bounds.shp', 
                            self.qgs_template)
                tiffile1 = tiffile + '.cliptiff.'+str(time.time())+'.tiff'
                try:
                    clip_data(tiffile, tiffile1, shpfile, filevalue=999)
                except Exception as e:
                    print(e)
                    shutil.copy2(tiffile, tiffile1)
                try:
                    if 'keeptiff' in self.png_json:
                        pass
                    else:
                        safe_remove(tiffile)
                except Exception as e:
                    print(e)
                say('clip tiff finished', time.time()-t0)
                print(htt.time2str(time.time(), 'yyyy:mm:dd HH:MM:SS'))
        except Exception as e:
            print(e)
            pass
        # }}}

        # genrate qgs file
        # {{{
        print(htt.time2str(time.time(), 'yyyy:mm:dd HH:MM:SS'))
        chndict = self.qgs_json['label']
        for k in chndict.keys():
            try:
                chndict[k] = self.png_json[k]
            except Exception as e:
                pass
        self.qgslevel = int(self.qgs_json['level'])
        try:
            self.qgslevel = self.png_json['qgslevel']
        except Exception as e:
            pass

        deletepng = True
        try:
            if self.png_json['deletepng'] == 'no':
                deletepng = True
        except Exception as e:
            pass

        et = ''
        try:
            et = self.png_json['extent']
        except Exception as e:
            pass

        self.colorbarfile = ''
        try:
            self.colorbarfile = self.png_json['colorbar']
        except Exception as e:
            pass

        mapid='Map1'
        try:
            mapid = self.qgs_json['mapid']
        except Exception as e:
            pass

        t0 = say('start convert qgis')
        removetiff = True
        if 'keeptiff' in self.png_json:
            removetiff = False
        else:
            pass

        try:
            for k in chndict.keys():
                chndict[k] = re.sub(r'号台风热带低压', '号热带低压', chndict[k])
                chndict[k] = re.sub(r'号台风"热带低压"', '号热带低压', chndict[k])
        except Exception as e:
            print(e)
        print(self.colorbarfile)

        if 'outcolorbar' in self.png_json:
            shutil.copy2(self.colorbarfile, self.png_json['outcolorbar'])

        if 'noqgs' in self.png_json:
            say('end convert tiff', time.time()-t0)
            return

        try:
            createQGISMap(tiffile1, self.qgsfile, self.qgs_template, 
                    chndict, self.colorbarfile, level=self.qgslevel, 
                    et=et, mapid=mapid, removetiff=removetiff)
        except Exception as e:
            print(e)
        
        say('end convert qgis', time.time()-t0)
        print(htt.time2str(time.time(), 'yyyy:mm:dd HH:MM:SS'))
        # }}}

    def pngs2qgs_json(self):
        # generate geotifffile
        # {{{
        # figname = '/home/leon/src/fy/amv.test.png'

        with open(self.qgs_json_file) as json_file:
            self.qgs_json = json.load(json_file)

        with open(self.png_json_file) as json_file:
            self.png_json = json.load(json_file)

        fignames = self.pngfile
        tiffs = []
        for figname in re.findall(r'[^\,]+', fignames):
            self.qgsfile = self.png_json['qgsfile']

            time0 = say('gen tiff')
            t = plt.imread(figname)
            lonlim = self.png_json['lonlim']
            latlim = self.png_json['latlim']
            a = t[:,:,3]
            longd = np.linspace(lonlim[0], lonlim[1], t.shape[1])
            latgd = np.linspace(latlim[0], latlim[1], t.shape[0])
            t = t * 255
            r = t[:,:,0]
            g = t[:,:,1]
            b = t[:,:,2]
            r[a == 0] = 999
            t[:,:,0] = r
            # t[2000:2100,2000:2100,:] = 1
            # t[2100:2200,2100:2200,:] = 255
            t = np.transpose(t[-1::-1,:,0:3], [2, 0, 1])
            tiffile = figname+'.tiff'
            writeTif_GLL(tiffile, t, longd, latgd, miss=999)
            say('gen tiff finished', time.time()-time0)

            tiffile1 = tiffile
            try:
                if self.png_json['removeout'] == 'yes':
                    t0 = say('clip tiff')
                    try:
                        shpfile = self.png_json['bounds']
                    except Exception as e:
                        shpfile = re.sub('[^\/]+$', 'bounds.shp', 
                                self.qgs_template)
                    tiffile1 = tiffile + '.'+str(time.time())+'.tiff'
                    clip_data(tiffile, tiffile1, shpfile, filevalue=999)
                    try:
                        if 'keeptiff' in self.png_json:
                            pass
                        else:
                            safe_remove(tiffile)
                    except Exception as e:
                        pass
                    say('clip tiff finished', time.time()-t0)
            except Exception as e:
                pass
            tiffs.append(tiffile1)
            # }}}

        # genrate qgs file
        # {{{
        chndict = self.qgs_json['label']
        for k in chndict.keys():
            try:
                chndict[k] = self.png_json[k]
            except Exception as e:
                pass
        self.qgslevel = int(self.qgs_json['level'])
        try:
            self.qgslevel = self.png_json['qgslevel']
        except Exception as e:
            self.qgslevel = str(self.qgslevel-2)+','+str(self.qgslevel)

        deletepng = True
        try:
            if self.png_json['deletepng'] == 'no':
                deletepng = True
        except Exception as e:
            pass

        et = ''
        try:
            et = self.png_json['extent']
        except Exception as e:
            pass

        self.colorbarfile = ''
        try:
            self.colorbarfile = self.png_json['colorbar']
        except Exception as e:
            pass
        mapid='Map1'
        try:
            mapid = self.qgs_json['mapid']
        except Exception as e:
            pass

        t0 = say('start convert qgis')
        removetiff = True
        if 'keeptiff' in self.png_json:
            removetiff = False
        else:
            pass

        for k in chndict.keys():
            chndict[k] = re.sub(r'号台风热带低压', '号热带低压', chndict[k])
            chndict[k] = re.sub(r'号台风"热带低压"', '号热带低压', chndict[k])
        createQGISMaps(tiffs, self.qgsfile, self.qgs_template, 
                chndict, self.colorbarfile, levels=self.qgslevel, 
                et=et, mapid=mapid, removetiff=removetiff)
        say('end convert qgis', time.time()-t0)
        # }}}


def convert_png2qgs(infile, instrument, resolution, qgs_template,
                    colorbarfile, ttl, rttl, lonlim, latlim, et,
                    figname, qgslevel, qgsfile):
    sinfile = re.sub('.*\/', '', infile)
    a = fig()
    a.instrument = instrument
    a.resolution = resolution
    a.qgs_template = qgs_template
    a.pngname = infile
    a.qgsfile = qgsfile
    a.colorbarfile = colorbarfile
    a.ttl = ttl
    a.rttl = rttl
    a.lonlim = lonlim
    a.latlim = latlim
    a.et = et
    a.mpro = False
    a.qgslevel = qgslevel
    a.png2qgs()


def t1_convert_png2qgs():
    for infile in glob.glob('/home/leon/Documents/台风大风/*png'):
        sinfile = re.sub('.*\/', '', infile)
        tmp = re.search('^([^_]+)_(.*)\.png$', sinfile) 
        instrument = 'FY3D/MWRI'
        resolution = '15km'
        qgs_template = '/home/leon/src/qgisfig/glob/template.qgs'
        qgsfile = '/home/leon/src/fy/tmp/wind_'+sinfile+'.q.png'
        colorbarfile = './bai1.png'
        colorbarfile1 = '/home/leon/Documents/台风大风/colorbar/'+\
                tmp.group(1)+'.png'
        if os.path.exists(colorbarfile1):
            colorbarfile = colorbarfile1
        ttl = '台风'+tmp.group(1)
        rttl = '2021-07-21 11:00:00(北京时)'
        t2 = re.findall('[^_]+', tmp.group(2))
        lonlim = [float(t2[0]), float(t2[2])]
        latlim = [float(t2[1]), float(t2[3])]
        dlon = (lonlim[1]-lonlim[0])/10
        dlat = (latlim[1]-latlim[0])/10
        print(dlon)
        print(dlat)
        et = str(lonlim[0]+dlon)+'_'+str(latlim[0]+dlat)+'_'\
                +str(lonlim[1]-dlon)+'_'+str(latlim[1]-dlat)
        figname = tmp.group(1)
        qgslevel = 2
        convert_png2qgs(infile, instrument, resolution, qgs_template,
                        colorbarfile, ttl, rttl, lonlim, latlim, et, 
                        figname, qgslevel, qgsfile)


def test_convert_png2qgs():
    for infile in glob.glob('/home/leon/Documents/台风大风/*png'):
        sinfile = re.sub('.*\/', '', infile)
        tmp = re.search('^([^_]+)_(.*)\.png$', sinfile) 
        a = fig()
        a.instrument = 'FY3D/MWRI'
        a.resolution = '15km'
        a.qgs_template = '/home/leon/src/qgisfig/glob/template.qgs'
        a.pngname = infile
        a.qgsfile = '/home/leon/src/fy/tmp/wind_'+sinfile+'.q.png'
        a.colorbarfile = './bai1.png'
        colorbarfile = '/home/leon/Documents/台风大风/colorbar/'+\
                tmp.group(1)+'.png'
        if os.path.exists(colorbarfile):
            a.colorbarfile = colorbarfile
        a.ttl = '台风'+tmp.group(1)
        a.rttl = '2021-07-21 11:00:00(北京时)'
        t2 = re.findall('[^_]+', tmp.group(2))
        a.lonlim = [float(t2[0]), float(t2[2])]
        a.latlim = [float(t2[1]), float(t2[3])]
        dlon = (a.lonlim[1]-a.lonlim[0])/10
        dlat = (a.latlim[1]-a.latlim[0])/10
        print(dlon)
        print(dlat)
        a.et = str(a.lonlim[0]+dlon)+'_'+str(a.latlim[0]+dlat)+'_'\
                +str(a.lonlim[1]-dlon)+'_'+str(a.latlim[1]-dlat)
        a.figname = tmp.group(1)
        print(a.et)
        print(a.lonlim)
        print(a.latlim)
        print(a.lonlim)
        a.mpro = False
        a.qgslevel = 2
        a.png2qgs()


def test_exe():
    fig = plt.figure(figsize=(9,10))
    axpos = (0.1,0.4,0.8,0.5)
    ax = fig.add_axes(axpos)
    it = ax.imshow(np.array([[1,2],[3,4]]), aspect='auto')
    ax1 = fig.add_axes([0.15,0.1,0.6,0.02])
    cb = plt.colorbar(it, cax=ax1, orientation='horizontal')
    ym = ax1.get_ylim()
    xm = ax1.get_xlim()
    dy = ym[1]-ym[0]
    ax1.text(xm[0], ym[0]+dy/2, 'xxxx  ',
            horizontalalignment='right', verticalalignment='center')
    ax1.text(xm[1], ym[0]+dy/2, '  xxxx',
            horizontalalignment='left', verticalalignment='center')
    ax1.set_xticklabels(ax1.get_xticks())
    fe = [path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()]
    for tax in plt.gcf().axes:  
        # {{{
        ts = tax.get_children()
        ts.extend(tax.get_xticklabels())
        for t in ts:
            try:
                if re.search('Text', str(type(t))):
                    t.set_path_effects(fe)
                    t.set_color('w')
            except Exception as e:
                pass  # }}}

    fig.savefig('5.png', transparent=True, dpi=200)
    pngdict = {'title': 'xxxxxxxxxxx', 
               'date': '0000-00-00',
               'lonlim': [0,180], 
               'latlim': [-20, 80], 
               'qgsfile': '5.qgs.png',
               'satellite': 'xxx/xx',
               'axpos': axpos,
               'cbpos': [0,0,1,0.2],
               'qgslevel': 12,
               'qgsfile': '5.qgsc.png',
               'removeout': 'yes',
               'resolution': '??km'}

    with open('5.png.json', "w", encoding='utf-8') as f:
        json.dump(pngdict, f)

    cmd = 'python3 exe_png2qgis.py --png=5.png --qgs=/.out/home/leon/src/qgis/new/weather-ll/template-regc.qgs'
    print(cmd)
    os.system(cmd)
    

if __name__ == "__main__":
    # t1_convert_png2qgs()
    test_exe()
    
    exit()
    clip_data('', clipedpath, shpfile, filevalue=255)

