
from toothedsword import figure, htt, project, set_lim_from_qgs, runs
import time
import numpy as np
import sys
from matplotlib.font_manager import FontProperties
yh_font = FontProperties(fname='/usr/share/fonts/msyh.ttc')
sys.path.append('/home/leon/src/sat')
from fy4a import agrib
import windpy


def gen_fig(a, reg='achn', template_file=''):
    # {{{
    fig = figure(dpi=400, figsize=(10,10))
    ax = fig.add_axes([0.1, 0.4, 0.6, 0.6])

    im = ax.imshow(a.gd[12][-1::-1,:], aspect='auto',
                   extent=[a.longd.min(), a.longd.max(),
                           a.latgd.min(), a.latgd.max()])
    fig.addcolorbar(im)
    ct = ax.contour(a.longd, a.latgd, a.gd['12s'], 
               np.arange(150, 350, 20), colors='k',
               linewidths=0.5)
    set_lim_from_qgs(ax, template_file)
    xlim = ax.get_xlim()

    if reg == 'achn':
        ix=2
        iy=2
        xs=(xlim[1]-xlim[0])/40
        lw=0.4
    else:
        ct.set_linewidths(1)
        ix=1
        iy=1
        xs=(xlim[1]-xlim[0])/30
        lw=1
    xw, yw, zw, ccc = windpy.wind_flag(
        w.lon, w.lat, w.u, w.v,
        ix=ix, iy=iy, scp=[-60, 60],
        rgb='ww', ns=[10],
        linewidth=lw, xs=xs, 
        lat=w.lat, ax=ax, mi=0, ma=100)
    ax.set_xlim([a.longd.min(), a.longd.max()])
    ax.set_ylim([a.latgd.min(), a.latgd.max()])
    if reg == 'achn':
        pass
    else:
        set_lim_from_qgs(ax, template_file)
    return fig, ax
# }}}


say, p = project(sys.argv[-1], '初始化|预处理|全国图绘图|全国图|安徽图绘图|安徽图|新疆图绘图|新疆图|qgis完成')

a = agrib()
a.fn4km = '/home/leon/src/fy/fy4a_data/FY4B-_AGRI--_N_DISK_1050E_L1-_FDI-_MULT_NOM_20240608060000_20240608061459_4000M_V0001.HDF'

a.get_lon_lat('4km')
a.read_refbt(12)
a.get_time()

a.latgd = np.linspace(0, 65, 4000)
a.longd = np.linspace(70, 135, 4000)
a.gen_grid(12, 'stb')

a.gd[12][a.gd[12] < 0] = np.nan
a.gd['12s'] = a.gd[12] + 0
a.smooth_more('12s', [7,5])

chn = 13
a.amv_file[chn] = '/home/leon/src/fy/fy4a_data/FY4B-_AGRI--_N_DISK_1050E_L2-_AMV-_C013_NUL_20240608060000_20240608061459_048KM_V0001.NC'
a.read_amv(chn)
w = a.amv[chn]
cmds = []
say('预处理完成')


template_file = '/home/leon/src/qgis/new/achn/template.qgs'
fig, ax = gen_fig(a, 'achn', template_file)
say('全国图绘图完成')

cmd = fig.save2qgis('1.png', template_file, run=False,
              info={'varname':'亮温', 'varunit':'K', 
                    'debug':'yes', 
                    'title':'测试图片', 'date':a.stime, 
                    'satellite':'卫星/载荷:FY4B/AGRI',
                    'removeout':'yes', 'qgslevel':12, 
                    'resolution':'分辨率:4公里'})
cmds.append(cmd)
fig.plt.close()
say('全国图完成')


template_file = '/home/leon/src/qgis/new1/aahs/template.qgs'
fig, ax = gen_fig(a, 'anhui', template_file)
say('安徽图绘图完成')
cmd = fig.save2qgis('2.png', template_file, run=False,
              info={'varname':'亮温', 'varunit':'K',
                    'debug':'yes', 'gextent':'qgs',
                    'title':'测试图片', 'date':a.stime, 
                    'satellite':'卫星/载荷:FY4B/AGRI',
                    'removeout':'yes', 'qgslevel':12,
                    'resolution':'分辨率:4公里'})
cmds.append(cmd)
fig.plt.close()
say('安徽图完成')


template_file = '/home/leon/src/qgis/new1/axjs/template.qgs'
fig, ax = gen_fig(a, 'xinjiang', template_file)
say('新疆图绘图完成')

cmd = fig.save2qgis('3.png', template_file, run=False,
              info={'varname':'亮温', 'varunit':'K',
                    'debug':'yes', 'gextent':'qgs',
                    'title':'测试图片', 'date':a.stime, 
                    'satellite':'卫星/载荷:FY4B/AGRI',
                    'removeout':'yes', 'qgslevel':12,
                    'resolution':'分辨率:4公里'})
cmds.append(cmd)
fig.plt.close()
say('新疆图完成')

runs(cmds, 10)
say('qgis完成')
say()

