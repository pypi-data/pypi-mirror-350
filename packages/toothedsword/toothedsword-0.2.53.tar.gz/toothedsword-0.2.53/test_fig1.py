
from toothedsword import figure, htt, project
import time
import numpy as np
import sys
from matplotlib.font_manager import FontProperties
yh_font = FontProperties(fname='/usr/share/fonts/msyh.ttc')


say, p = project(sys.argv[-1], '初始化|绘图|输出')
stime = htt.time2str(time.time(), 'yyyy/mm/dd HH:MM:SS')

fig = figure(dpi=200, figsize=[10,5])
ax = fig.add_axes([0.1, 0.1, 0.5, 0.8])
im = ax.imshow(np.random.random(400).reshape([20,20]), 
               aspect='auto', vmin=0, vmax=1, 
               extent=[60, 150, 10, 60])

fig.addcolorbar(im, orientation='vertical')
say('绘图完成')

outfile = 'test_sat_toothedsword_v.PNG'
fig.save2qgis(outfile,
              '/home/leon/src/qgis/new/achn/template_testv.qgs',
              info={'varname':'反射率', 'varunit':'度',
                    'title':'测试图片', 'date':stime, 
                    'satellite':'卫星/载荷:FY4B/AGRI',
                    'resolution':'分辨率:4公里',
                    'removeout':'yes', 'debug':'yes',
                    })
say(':'+outfile)
say('输出完成')
say()
