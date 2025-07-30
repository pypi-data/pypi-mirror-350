
from toothedsword import figure
import time
import numpy as np
import sys
from matplotlib.font_manager import FontProperties


fig = figure(dpi=200)
ax = fig.add_axes([0.1, 0.4, 0.8, 0.6])
im = ax.imshow(np.random.random(100).reshape([10,10]),
               vmin=0, vmax=1, aspect='auto',
               extent=[60, 150, 10, 60])
fig.addcolorbar(im)

outfile = 'test_sat_toothedsword.PNG'
fig.save2qgis(outfile,
              '/home/leon/src/qgis/new/achn/template_test2.qgs',
              info={'varname':'反射率',
                    'title':'测试图片', 'date':'2022/04/14 12:00', 
                    'satellite':'卫星/载荷:FY4B/AGRI',
                    'resolution':'分辨率:4公里',
                    'removeout':'yes', 'debug':'no',
                    })
