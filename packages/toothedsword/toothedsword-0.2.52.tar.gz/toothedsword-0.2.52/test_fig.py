
from toothedsword import figure, htt, project
import time
import numpy as np
import sys
from matplotlib.font_manager import FontProperties

say, p = project(sys.argv[-1], '初始化|绘图|qgis图|输出')
stime = htt.time2str(time.time(), 'yyyy/mm/dd HH:MM:SS')

fig = figure(dpi=800)
ax = fig.add_axes([0.1, 0.4, 0.8, 0.6])
xx, yy = np.meshgrid(np.linspace(-20, 20, 2000),
                     np.linspace(-10, 10, 2000))
ax.set_axis_off()
zz = (np.sin(xx)**2 + np.cos(yy))*10
im = ax.imshow(zz[-1::-1, :],
               aspect='auto',
               extent=[80, 120, 25, 45])
x = np.linspace(80, 120, 2000)
y = np.linspace(25, 45, 2000)
ax.contour(x, y, zz, np.arange(-10, 11, 5), colors='k', linewidths=0.3)

fig.addcolorbar(im)
say('绘图完成')

outfile = '/tmp/test_fig/2025/20250101/test_sat_toothedsword.PNG'
fig.save2qgis(outfile,
              '/home/leon/src/qgis/new/achn/template_test.qgs',
              info={'varname':'亮温', 'varunit':'k',
                    'title':'测试图片', 'date':stime, 
                    'satellite':'卫星/载荷:FY4B/AGRI',
                    'resolution':'分辨率:4公里',
                    'removeout':'yes', 'debug':'no',
                    })
say('qgis图完成')

say(':'+outfile)
say('输出完成')
say()
