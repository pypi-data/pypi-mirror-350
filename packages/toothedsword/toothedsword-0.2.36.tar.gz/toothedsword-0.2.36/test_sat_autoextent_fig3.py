
from toothedsword import figure, htt, project
import time
import numpy as np
import sys
from matplotlib.font_manager import FontProperties
yh_font = FontProperties(fname='/usr/share/fonts/msyh.ttc')
sys.path.append('/home/leon/src/sat')
from fy4a import agrib

say, p = project(sys.argv[-1], '初始化|绘图|全国图|安徽图|安徽图自动|天津图自动')

a = agrib()
a.fn4km = '/home/leon/src/fy/fy4a_data/FY4B-_AGRI--_N_DISK_1050E_L1-_FDI-_MULT_NOM_20240608060000_20240608061459_4000M_V0001.HDF'

a.get_lon_lat('4km')
a.read_refbt(12)
a.get_time()

a.latgd = np.linspace(10, 65, 2000)
a.longd = np.linspace(70, 135, 2000)
a.gen_grid(12)

fig = figure(dpi=400, figsize=(7,10))
ax = fig.add_axes([0.1, 0.4, 0.8, 0.6])

a.gd[12][a.gd[12] < 0] = np.nan
im = ax.imshow(a.gd[12][-1::-1,:], 
               extent=[a.longd.min(), a.longd.max(),
                       a.latgd.min(), a.latgd.max()])
fig.addcolorbar(im)
a.smooth_more(12, [7,5])
ct = ax.contour(a.longd, a.latgd, a.gd[12], 
           np.arange(150, 350, 20), colors='k',
           linewidths=0.5)
say('绘图完成')

fig.save2qgis('1.png', 
              '/home/leon/src/qgis/new/achn/template.qgs',
              info={'varname':'亮温', 'varunit':'K', 
                    'debug':'yes',
                    'title':'测试图片', 'date':a.stime, 
                    'satellite':'卫星/载荷:FY4B/AGRI',
                    'removeout':'yes', 'qgslevel':12, 
                    'resolution':'分辨率:4公里'})
say('全国图完成')

ct.set_linewidths(1)
fig.save2qgis('2.png', 
              '/home/leon/src/qgis/new1/aahs/template.qgs',
              info={'varname':'亮温', 'varunit':'K',
                    'debug':'yes',
                    'title':'测试图片', 'date':a.stime, 
                    'satellite':'卫星/载荷:FY4B/AGRI',
                    'removeout':'yes', 'qgslevel':12,
                    'resolution':'分辨率:4公里'})
say('安徽图完成')


fig.save2qgis('3.png', 
              '/home/leon/src/qgis/new1/aahs/template.qgs',
              info={'varname':'亮温', 'varunit':'K',
                    'debug':'yes', 'gextent':'qgs',
                    'title':'测试图片', 'date':a.stime, 
                    'satellite':'卫星/载荷:FY4B/AGRI',
                    'removeout':'yes', 'qgslevel':12,
                    'resolution':'分辨率:4公里'})
say('安徽图自动完成')


fig.save2qgis('4.png', 
              '/home/leon/src/qgis/new1/atjs/template.qgs',
              info={'varname':'亮温', 'varunit':'K',
                    'debug':'yes', 'gextent':'qgs',
                    'title':'测试图片', 'date':a.stime, 
                    'satellite':'卫星/载荷:FY4B/AGRI',
                    'removeout':'yes', 'qgslevel':12,
                    'resolution':'分辨率:4公里'})
say('天津图自动完成')

say()

