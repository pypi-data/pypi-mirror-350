
import re
import os
import glob
from toothedsword import figure, htt, project, runs
import time
import numpy as np
import sys
from matplotlib.font_manager import FontProperties
sys.path.append('/home/leon/src/sat')
from fy4a import agrib


say, p = project(sys.argv[-1], '初始化|绘图|输出')

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
fig.ct = ax.contour(a.longd, a.latgd, a.gd[12], 
           np.arange(150, 350, 20), colors='k',
           linewidths=0.5)
say('绘图完成')

regs = ['agss', 'anwc', 'aswc', 'ysxp', 'yyhp', 'anms', 'achn', 'ajss']
templates = glob.glob('/home/leon/src/qgis/new1/????/template.qgs')
templates.sort()
cmds = []
#for template in templates:
#    reg = re.search(r'\/new1\/(....)\/template',
#                    template).group(1)
for reg in regs:
    template = '/home/leon/src/qgis/new1/'+reg+'/template.qgs'
    outfile = '1.'+reg+'.png'
    if re.search(r'achn', template):
        fig.ct_lw = 0.2
        ge = 'qgs'
        ax.set_xlim([a.longd.min(), a.longd.max()])
        ax.set_ylim([a.latgd.min(), a.latgd.max()])
    else:
        fig.ct_lw = 1
        ge = 'qgs'
    if re.search(r'[pP]$', reg):
        rmo = 'no'
    else:
        rmo = 'yes'
    rmo = 'no'
    cmd = fig.save2qgis(outfile, template, run=False, 
                  info={'varname':'亮温', 'varunit':'K',
                        'gextent': ge,
                        'title':reg, 'date':a.stime, 
                        'satellite':'卫星/载荷:FY4B/AGRI',
                        'removeout':rmo, 'qgslevel':12,
                        'resolution':'分辨率:4公里'})
    cmds.append(cmd)
    say(reg+'结束')

say('绘图完成')
runs(cmds, 10)

say('输出完成')

say()

