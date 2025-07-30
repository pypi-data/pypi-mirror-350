import sys
import json
import os
import re
import glob
# from mayavi import mlab
# import time_htht as htt
from toothedsword import time_htht as htt
import numpy as np
# import pandas as pd
import copy

class figorg():
    pass

try:
    import matplotlib.pyplot as plt
    from matplotlib.font_manager import FontProperties
    figorg = plt.Figure
except Exception as e:
    print(e)
# from osgeo import gdal
# from skimage import morphology
import time
import xml.etree.ElementTree as ET
from .common import safe_remove

prodir = os.path.dirname(os.path.abspath(__file__))

font_path = os.path.join(prodir, 'msyh.ttc')

try:
    yh_font = FontProperties(fname=os.path.join(prodir, 'font', 'msyh.ttc'))
    kai_font = FontProperties(fname=os.path.join(prodir, 'font', 'simkai.ttf'))
    hei_font = FontProperties(fname=os.path.join(prodir, 'font', 'simhei.ttf'))
except Exception as e:
    print(e)

def get_layout_extent(project_file):
    from pyproj import Transformer
    # 读取 QGIS 项目文件
    # project_file = "./template.qgs"
    tree = ET.parse(project_file)
    root = tree.getroot()

    # 查找地图项（LayoutItemMap）
    for item in root.findall(".//LayoutItem[@type='65639']"):
        extent = item.find("Extent")
        if extent is not None:
            # 提取投影坐标
            xmin = float(extent.get("xmin"))
            xmax = float(extent.get("xmax"))
            ymin = float(extent.get("ymin"))
            ymax = float(extent.get("ymax"))

            # 查找 CRS 信息
            crs = item.find(".//crs/spatialrefsys/authid")
            if crs is not None:
                source_crs = crs.text  # 例如 "EPSG:4499"
                target_crs = "EPSG:4326"  # 目标坐标系（WGS84 经纬度）

                # 创建坐标转换器
                transformer = Transformer.from_crs(source_crs, target_crs, always_xy=True)

                # 将投影坐标转换为经纬度坐标
                lon_min, lat_min = transformer.transform(xmin, ymin)
                lon_max, lat_max = transformer.transform(xmax, ymax)

                # 打印结果
                print(f"地图项范围 (投影坐标):")
                print(f"  xmin: {xmin}, ymin: {ymin}")
                print(f"  xmax: {xmax}, ymax: {ymax}")
                print(f"地图项范围 (经纬度坐标):")
                print(f"  经度范围: {lon_min} 到 {lon_max}")
                print(f"  纬度范围: {lat_min} 到 {lat_max}")
                return float(lon_min), float(lon_max), \
                        float(lat_min), float(lat_max)
            else:
                print("未找到 CRS 信息。")
        else:
            print("未找到 <Extent> 元素。")

def get_lim_from_qgs(template_file):
    xmin, xmax, ymin, ymax = get_layout_extent(template_file)
    return [xmin, xmax], [ymin, ymax]


def set_lim_from_qgs(ax, template_file):
    xlim, ylim = get_lim_from_qgs(template_file)
    dx = xlim[1] - xlim[0]
    dy = ylim[1] - ylim[0]

    if dx > dy:
        ylim = [np.mean(ylim)-dx/2, np.mean(ylim)+dx/2]
    if dx < dy:
        xlim = [np.mean(xlim)-dy/2, np.mean(xlim)+dy/2]
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)


def get_qgis_extent(template_file):
# 读取 QGIS 模板文件
# template_file = "template.qgs"
    tree = ET.parse(template_file)
    root = tree.getroot()

# 查找 DefaultViewExtent 元素
    default_view_extent = root.find(".//DefaultViewExtent")

# 提取 xmax, xmin, ymin, ymax
    if default_view_extent is not None:
        xmax = default_view_extent.get("xmax")
        xmin = default_view_extent.get("xmin")
        ymin = default_view_extent.get("ymin")
        ymax = default_view_extent.get("ymax")

        # 打印结果
        print(f"xmax: {xmax}")
        print(f"xmin: {xmin}")
        print(f"ymin: {ymin}")
        print(f"ymax: {ymax}")
        return float(xmin), float(xmax),\
                float(ymin), float(ymax)
    else:
        print("DefaultViewExtent not found in the template file.")

def remove_white(figname, maxw=0.05, axis=0, outfile='', idy=''):
    im = plt.imread(figname).astype(np.float32)
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


def figure(*args, add_axes=False, **kw):
    fig = plt.figure(*args, **kw, FigureClass=FIG)
    fig.plt = plt
    fig.yh_font = yh_font
    fig.kai_font = kai_font
    fig.hei_font = hei_font
    if add_axes:
        ax = fig.add_axes_auto()
        fig.ax = ax
    return fig


class FIG(figorg):
    """Docstring for . """
    def init(self):
        try:
            dpi = self.dpi
        except Exception as e:
            self.dpi = 400

        try:
            t = self.fig_varunit
        except Exception as e:
            self.fig_varunit = ''

        try:
            t = self.fig_varname
        except Exception as e:
            self.fig_varname = ''

        if os.path.exists('/usr/bin'):
            self.python = 'python3'
        else:
            self.python = 'python'

        self.qgs_template = '/home/leon/src/qgisfig/new/achn/template.qgs'
        self.qgs_template = '/home/leon/src/qgisfig/glob/template.qgs'
        self.qgs_template = '/home/leon/src/qgis-050/dynamic-range/template.qgs'
        self.fontproperties = kai_font
        self.fontcolor = '#000000'
        self.pngfile = str(time.time())+'.png'
        self.png_json_file = self.pngfile + '.json'
        self.outfile = self.pngfile+'.png'
        self.time = time.time()
        self.ttl = 'xxxxx'
        self.sat = 'xxx'
        self.axpos = self.ax.get_position().bounds
        try:
            t = self.cb_axpos_out
        except Exception as e:
            self.cb_axpos_out = [0,0,1,0.2]
        self.res = 'xxx'
        self.prodir = os.path.dirname(os.path.abspath(__file__))
        self.qgs_template_json = self.qgs_template + '.json'
        self.update_png_json = {}
        self.say = print

    def fontzoom(self, scale):
        for text_obj in self.findobj(match=type(plt.Text)):
            try:
                text_obj.set_fontsize(text_obj.get_fontsize() * scale)
            except Exception as e:
                pass

    def remove_close_text(self, mindis, text_objs, rt='CC'):
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        def dis(x1,y1,x0,y0,xlim,ylim):
            x1 = (x1 - xlim[0])/(xlim[1]-xlim[0])
            y1 = (y1 - ylim[0])/(ylim[1]-ylim[0])
            x0 = (x0 - xlim[0])/(xlim[1]-xlim[0])
            y0 = (y0 - ylim[0])/(ylim[1]-ylim[0])
            return np.sqrt((x1-x0)**2+(y1-y0)**2)

        for text_obj in text_objs:
            try:
                s0 = text_obj.get_text()
                x0, y0 = text_obj.get_position()
                if s0 == ' ':
                    continue
                
                for text_obj1 in text_objs:
                    try:
                        s1 = text_obj1.get_text()
                        x1, y1 = text_obj1.get_position()
                        d = dis(x1,y1,x0,y0,xlim,ylim)
                        if d > 0 and d < mindis and not(s1 == ' '):
                            text_obj1.set_text(' ')
                        
                    except Exception as e1:
                        print('---------------')
                        print(e1)
            except Exception as e:
                print('---------------')
                print(e)

    def add_axes_auto(self, type='main'):
        if type == 'main':
            ax = self.add_axes([0.15, 0.15, 0.7, 0.7])
            self.ax = ax
        if re.search('cb', type):
            if re.search('h', type):
                ax = self.add_axes([0.15, 0.15, 0.7, 0.02])
            else:
                ax = self.add_axes([0.87, 0.15, 0.02, 0.7])
            self.cax = ax
        return ax

    def set_timetick(self, xy='x', ss='yyyymmddHHMMSS'):
        ax = self.ax
        xticks = ax.get_xticks()
        xticklabels = []
        for x in xticks:
            xticklabels.append(htt.time2str(x, ss))
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels)

    def add_space(self, dr, wd):
        ax = self.ax
        current_position = ax.get_position()
        current_position_list = [current_position.x0, current_position.y0, current_position.width, current_position.height]
        
        try:
            cax = self.cax
            cposition = cax.get_position()
            cposition_list = [cposition.x0, cposition.y0, cposition.width, cposition.height]
        except Exception as e:
            print(e)

        if dr == 'top':
            current_position_list[3] -= wd
            cposition_list[3] -= wd

        if dr == 'right':
            current_position_list[2] -= wd
            cposition_list[0] -= wd

        if dr == 'bottom':
            current_position_list[3] -= wd
            current_position_list[1] += wd
            cposition_list[3] -= wd
            cposition_list[1] += wd

        if dr == 'left':
            current_position_list[2] -= wd
            current_position_list[0] += wd

        ax.set_position(current_position_list)
        try:
            cax.set_position(cposition_list)
        except Exception as e:
            print(e)

    def save(self, *args, maxw=[1,1], **kw):
        self.savefig(*args, **kw)
        fname = args[0]
        remove_white(fname, maxw=maxw[0], axis=0)
        remove_white(fname, maxw=maxw[1], axis=1)

    def set_axes_thick(self, thick):
        # for ax in self.axes:
        for ax in self.get_axes():
            # 获取当前Axes对象的边框
            spines = ax.spines

            # 设置边框线宽度为3
            for spine in spines.values():
                spine.set_linewidth(thick)

    def add_colorbar(self):
        self.ax_cb = self.fig.add_axes(self.cb_axpos_in)
        cb = plt.colorbar(self.it, cax=self.ax_cb, 
                orientation='horizontal')

    def addcolorbar(self, im, cax='', 
                 orientation='horizontal', 
                 var='xxx', unit='xxx'):
        
        if str(type(cax)) == str(type('')):
            if orientation=='horizontal':
                cax = self.add_axes([0.2, 0.1, 0.6, 0.02])
                self.cb_axpos_out = [0,0,1,0.2]
            if orientation=='vertical':
                cax = self.add_axes([0.8, 0.1, 0.02, 0.8])
                self.cb_axpos_out = [0.7,0,0.3,1]
            self.ax_cb = cax
        

        plt.colorbar(im, cax=cax, orientation=orientation)
        if var == 'xxx':
            pass
        else:
            self.fig_varname = var

        if unit == 'xxx':
            pass
        else:
            self.fig_varunit = unit

    def copy_attr_from_parent(self):
        pass

    def add_ll_unit_ax_y2(self):
        # {{{
        ax = self.ax
        ts = []
        it = 1
        for t in ax.get_xticklabels():
            it += 1
            t1 = t.get_text()+''
            if float(t.get_text()) == 0:
                pass
            elif re.search(r'-', t.get_text()):
                t1 = re.sub(r'-','',t.get_text())+'W'
            else:
                t1 = t.get_text()+'E'
            ts.append(t1)
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(ts)

        ts = []
        it = 0
        for t in ax.get_yticklabels():
            it += 1
            t1 = t.get_text()+''
            if float(t.get_text()) == 0:
                pass
            elif re.search(r'-', t.get_text()):
                t1 = re.sub(r'-','',t.get_text())+'S'
            else:
                t1 = t.get_text()+'N'
            if it % 2 == 0:
                t1 = ' '
            ts.append(t1)
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels(ts)
        # }}}

    def add_ll_unit_ax(self):
        # {{{
        ax = self.ax
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        ts = []
        for t in ax.get_xticklabels():
            t1 = t.get_text()+''
            if float(t.get_text()) == 0:
                pass
            elif re.search(r'-', t.get_text()):
                t1 = re.sub(r'-','',t.get_text())+'$^{o}$W'
            else:
                t1 = t.get_text()+'$^{o}$E'
            ts.append(t1)
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(ts)

        ts = []
        for t in ax.get_yticklabels():
            t1 = t.get_text()+''
            if float(t.get_text()) == 0:
                pass
            elif re.search(r'-', t.get_text()):
                t1 = re.sub(r'-','',t.get_text())+'$^{o}$S'
            else:
                t1 = t.get_text()+'$^{o}$N'
            ts.append(t1)
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels(ts)
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        # }}}

    def add_tick_space(self, xy):
        # {{{
        ax = self.ax
        ts = []
        it = 1
        for t in ax.get_xticklabels():
            it += 1
            t1 = t.get_text()+''
            if xy[0] > 0:
                if it % xy[0] == 1:
                    pass
                else:
                    t1 = ' '
            ts.append(t1)
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(ts)

        ts = []
        it = 0
        for t in ax.get_yticklabels():
            it += 1
            t1 = t.get_text()+''
            if xy[1] > 0:
                if it % xy[1] == 1:
                    t1 = ' '
            ts.append(t1)
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels(ts)
        # }}}

    def add_ll_unit_ax1(self):
        # {{{
        ax = self.ax
        ts = []
        it = 1
        for t in ax.get_xticklabels():
            it += 1
            t1 = t.get_text()+''
            if float(t.get_text()) == 0:
                pass
            elif re.search(r'-', t.get_text()):
                t1 = re.sub(r'-','',t.get_text())+'W'
            else:
                t1 = t.get_text()+'E'
            if it % 3 == 1:
                pass
            else:
                t1 = ' '
            ts.append(t1)
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(ts)

        ts = []
        it = 0
        for t in ax.get_yticklabels():
            it += 1
            t1 = t.get_text()+''
            if float(t.get_text()) == 0:
                pass
            elif re.search(r'-', t.get_text()):
                t1 = re.sub(r'-','',t.get_text())+'S'
            else:
                t1 = t.get_text()+'N'
            if it % 2 == 1:
                t1 = ' '
            ts.append(t1)
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels(ts)
        # }}}

    def add_ll_unit_ax2(self):
        # {{{
        ax = self.ax
        ts = []
        it = 1
        for t in ax.get_xticklabels():
            it += 1
            t1 = t.get_text()+''
            if float(t.get_text()) == 0:
                pass
            elif re.search(r'-', t.get_text()):
                t1 = re.sub(r'-','',t.get_text())+'W'
            else:
                t1 = t.get_text()+'E'
            if it % 2 == 1:
                pass
            else:
                t1 = ' '
            ts.append(t1)
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(ts)

        ts = []
        it = 0
        for t in ax.get_yticklabels():
            it += 1
            t1 = t.get_text()+''
            if float(t.get_text()) == 0:
                pass
            elif re.search(r'-', t.get_text()):
                t1 = re.sub(r'-','',t.get_text())+'S'
            else:
                t1 = t.get_text()+'N'
            if it % 2 == 1:
                t1 = ' '
            ts.append(t1)
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels(ts)
        # }}}

    def add_ll_unit_ax0(self):
        # {{{
        ax = self.ax
        ts = []
        it = 1
        for t in ax.get_xticklabels():
            it += 1
            t1 = t.get_text()+''
            if it % 2 == 1:
                pass
            else:
                t1 = ' '
            ts.append(t1)
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(ts)

        ts = []
        it = 0
        for t in ax.get_yticklabels():
            it += 1
            t1 = t.get_text()+''
            if it % 2 == 1:
                t1 = ' '
            ts.append(t1)
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels(ts)
        # }}}

    def set_fmt_ax(self):
        # {{{ 
        ax = self.ax
        ts = []
        i = 0
        for t in ax.get_xticklabels():
            i += 1
            t1 = t.get_text()+''
            if float(t.get_text()) == 0:
                pass
            elif re.search(r'-', t.get_text()):
                t1 = re.sub(r'-','',t.get_text())+'$^{o}$S'
            else:
                t1 = t.get_text()+'$^{o}$N'
            t1 = re.sub(r'(\d.\d)\d*', r'\1', t1)
            if i % 2 == 1:
                t1 = ' '
            ts.append(t1)
        ax.set_xticks(ax.get_xticks())
        ax.set_xticklabels(ts)
        # }}}

    def add_sub_axes(self, nr, nc, xjg, yjg, xmargin, ymargin, cw=[0,0], add=True):
        # {{{
        axes = []
        width_sub = (1 - xmargin[0] - xmargin[1] - (nc-1)*xjg)/nc
        height_sub = (1 - ymargin[0] - ymargin[1] - (nr-1)*yjg)/nr

        width_sub0 = width_sub + xjg
        height_sub0 = height_sub + yjg

        if cw[0] == 0:
            pass
        else:
            axes_cb = []
            width_sub -= cw[1]+cw[0]

        for ir_1 in range(0, nr):
            ir = nr - ir_1 - 1
            tmp = []
            tmp_cb = []
            for ic in range(0, nc):
                axpos = [xmargin[0]+width_sub0*ic, 
                         ymargin[0]+height_sub0*ir,
                         width_sub, height_sub]
                if not(add):
                    tmp.append(axpos)
                else:
                    ax = self.add_axes(axpos)
                    tmp.append(ax)
                if cw[1] > 0:
                    axpos = [xmargin[0]+width_sub0*ic+width_sub+cw[0], 
                             ymargin[0]+height_sub0*ir,
                             cw[1], height_sub]
                    if not(add):
                        tmp_cb.append(axpos) 
                    else:
                        ax_cb = self.add_axes(axpos)
                        tmp_cb.append(ax_cb) 
            axes.append(tmp)
            if cw[1] > 0:
                axes_cb.append(tmp_cb)

        self.axes_all = axes
        if cw[1] > 0:
            self.axes_cb_all = axes_cb
        return # }}}

    def save_png(self):
        # {{{
        pngfile = self.pngfile
        fig = self
        ax = self.ax
        ax_cb = self.ax_cb
        ym = ax_cb.get_ylim()
        xm = ax_cb.get_xlim()
        dy = ym[1]-ym[0]
        dx = xm[1]-xm[0]
        pos = ax_cb.get_position()
      
        if pos.width > pos.height:
            if not(self.fig_varname == ''):
                ax_cb.text(xm[0], ym[0]+dy/2, 
                           self.fig_varname+'  ', 
                           fontproperties=self.fontproperties,
                           horizontalalignment='right', 
                           verticalalignment='center')
            if not(self.fig_varunit == ''):
                ax_cb.text(xm[1], ym[0]+dy/2, 
                           '  '+self.fig_varunit, 
                           fontproperties=yh_font,
                           horizontalalignment='left', 
                           verticalalignment='center')
        else:
            if not(self.fig_varname == ''):
                ax_cb.text(xm[0]+dx/2, ym[0]-dy/100, 
                           self.fig_varname, 
                           fontproperties=self.fontproperties,
                           horizontalalignment='center', 
                           verticalalignment='top')
            if not(self.fig_varunit == ''):
                ax_cb.text(xm[0]+dx/2, ym[1]+dy/100,
                           self.fig_varunit, 
                           fontproperties=self.fontproperties,
                           horizontalalignment='center', 
                           verticalalignment='bottom')

        if self.fontcolor == '#ffffff':
            import matplotlib.patheffects as path_effects
            fe = [path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()]
            for tax in [ax, ax_cb]: 
                # {{{
                ts = tax.get_children()
                ts.extend(tax.get_xticklabels())
                for t in ts:
                    try:
                        if re.search(r'Text', str(type(t))):
                            t.set_path_effects(fe)
                            t.set_color('w')
                    except Exception as e:
                        print(e)
                        # }}}

        outdir = re.sub(r'[^\/]+$', '', self.outfile)
        try:
            os.makedirs(outdir, exist_ok=True)
        except Exception as e:
            print(e)
        fig.savefig(pngfile, transparent=True, dpi=self.dpi)
        # }}}

    def gen_png_dict(self):
        # {{{
        fig = self
        ax = self.ax
        ax_cb = self.ax_cb
        self.textspan0 = ''
        self.textspan1 = ''

        if self.fontcolor == '#ffffff':
            self.textspan0 = '<p style="color:'+self.fontcolor+\
                    ';-webkit-text-stroke: 4px black">'
            self.textspan1 = '</p>'

        stime = htt.time2str(self.time, 'yyyymmddHHMMSS')
        outfile = self.outfile

        outdir = re.sub(r'[^\/]+$', '', outfile)
        try:
            os.makedirs(outdir, exist_ok=True)
        except Exception as e:
            print(e)

        lonlim = ax.get_xlim()
        latlim = ax.get_ylim()

        pngdict = {'title': self.textspan0+self.ttl+self.textspan1, 
                   'date': self.textspan0+htt.time2str(self.time+8*3600, 'yyyy-mm-dd HH:MM')+'(北京时间)'+self.textspan1,
                   'lonlim': [lonlim[0], lonlim[1]], 
                   'latlim': [latlim[0], latlim[1]], 
                   'qgsfile': outfile,
                   'satellite': self.textspan0+'卫星: '+self.sat+self.textspan1,
                   'axpos': self.axpos,
                   'cbpos': self.cb_axpos_out,
                   "tuli": self.textspan0+"图 例"+self.textspan1,
                   "guojie": self.textspan0+"国界"+self.textspan1,
                   "shengjie": self.textspan0+"省界"+self.textspan1,
                   "haiyang": self.textspan0+"海洋"+self.textspan1,
                   "ludi": self.textspan0+"陆地"+self.textspan1,
                   'resolution': self.textspan0+'分辨率: '+self.res+self.textspan1}
        try:
            pngdict['date'] = self.textspan0+self.rttl+self.textspan1
        except Exception as e:
            print(e)
        try:
            for k in self.pngdict_add.keys():
                pngdict[k] = self.pngdict_add[k]
        except Exception as e:
            pass
        for k in pngdict.keys():
            try:
                if re.search(r'^###', pngdict[k]):
                    pngdict[k] = self.textspan0+\
                            re.sub(r'^###', self.textspan0, 
                                    pngdict[k])+self.textspan1
            except Exception as e:
                print(e)
        self.pngdict = pngdict
        # }}}

    def save_png_json(self):
        # {{{
        pngfile = self.pngfile
        png_json_file = pngfile+'.tmp.json'

        with open(png_json_file, "w", encoding='utf-8') as f:
            json.dump(self.pngdict, f)
        self.png_json_file = png_json_file
        # }}}

    def gen_qgis(self, run=True):
        # {{{
        pngfile = self.pngfile
        cmd = self.python+' '+os.path.join(self.prodir, 'exe_png2qgis.py')+' --png='+pngfile+' --qgs='+self.qgs_template+' --png_json='+self.png_json_file
        if self.qgs_template_json == '':
            pass
        else:
            cmd += ' --qgs_json='+self.qgs_template_json
        print(cmd)
        if run:
            os.system(cmd)
        return cmd
        pass
        # }}}

    def save2qgis(self, outfile='', qgs_template='', 
                  qgs_template_json='',info={}, run=True):
        """
        fig.save2qgis('1.png', 
              '/home/leon/src/qgis/new/achn/template_test.qgs',
              info={'varname':'亮温', 'varunit':'K',
                    'title':'测试图片', 'date':a.stime, 
                    'satellite':'卫星/载荷:FY4B/AGRI',
                    'removeout':'yes', 'qgslevel':12,
                    'resolution':'分辨率:4公里'})
        """
        self.info = info
        try:
            t = self.ax
        except Exception as e:
            self.ax = self.axes[0]

        if 'gextent' in info:
            if info['gextent'] == 'qgs':
                # xmin, xmax, ymin, ymax =\
                #         get_qgis_extent(qgs_template)
                xmin, xmax, ymin, ymax =\
                        get_layout_extent(qgs_template)
                if xmin > -180 and xmin < 180 and\
                   xmax > -180 and xmax < 180 and\
                   ymin > -90 and ymin < 90 and\
                   ymax > -90 and ymax < 90:
                    self.ax.set_xlim([xmin, xmax])
                    self.ax.set_ylim([ymin, ymax])
        
        try:
            for i in range(0, len(self.clabel)):
                try:
                    self.clabel[i].remove()
                except Exception as e:
                    pass
        except Exception as e:
            print(e)

        try:
            self.clabel =\
                    self.plt.clabel(
                            self.ct, inline=False,
                            inline_spacing=1, fontsize=7)
        except Exception as e:
            print(e)

        try:
            self.ct.set_linewidths(self.ct_lw)
        except Exception as e:
            print(e)

        if 'varname' in info:
            self.fig_varname = info['varname']

        if 'varunit' in info:
            self.fig_varunit = info['varunit']

        try:
            t = self.ax_cb
        except Exception as e:
            try:
                self.ax_cb = self.axes[1]
            except Exception as e:
                pass

        self.init()
        if outfile=='':
            pass
        else:
            self.outfile = outfile
            self.pngfile = self.outfile + '.tmp.png'
       
        if not(qgs_template==''):
            self.qgs_template = qgs_template
 
        if qgs_template_json=='':
            self.qgs_template_json = self.qgs_template+'.json'
        else:
            self.qgs_template_json = qgs_template_json

        if not(os.path.exists(self.qgs_template_json)):
            tmp = {"label": 
                        {"title": "",
                         "date": "",
                         "satellite": "",
                         "resolution": ""
                        },
                   "level": 12,
                   "mapid": "Map 1"
                  }
            with open(self.qgs_template_json, "w", 
                      encoding='utf-8') as f:
                json.dump(tmp, f)

        self.save_png()
        self.gen_png_dict()

        try:
            if self.removeout:
                self.pngdict.update({'removeout':'yes'})
        except Exception as e:
            print(e)
        try:
            if self.maxw0 > 0:
                self.pngdict.update({'maxw0':self.maxw0})
        except Exception as e:
            print(e)
        try:
            if self.maxw1 > 0:
                self.pngdict.update({'maxw1':self.maxw1})
        except Exception as e:
            print(e)
        self.pngdict.update(self.update_png_json)
        self.pngdict.update(info)
        self.save_png_json()
        cmd = self.gen_qgis(run=run)
        if run:
            pass
        else:
            return cmd

        if 'debug' in self.pngdict:
            if self.pngdict['debug'] == 'yes':
                return
        for infile in glob.glob(self.pngfile+'*'):
            print(infile)
            if re.search(r'\.png\.tmp\.png\.', infile):
                safe_remove(infile)
            if re.search(r'\.png\.tmp\.png$', infile):
                safe_remove(infile)
            if re.search(r'\.PNG\.tmp\.png.*', infile):
                safe_remove(infile)
        return cmd


def fontzoom(obj, scale):
    for text_obj in obj.findobj(match=type(plt.Text)):
        try:
            text_obj.set_fontsize(text_obj.get_fontsize() * 2)
        except Exception as e:
            print(e)


def main():
    fig = figure()
    ax = fig.add_axes([0.1,0.3,0.8,0.7])
    it = ax.imshow([[0,1],[3,4]], extent=[70, 150, 0, 70])

    cax = fig.add_axes([0.3,0.1,0.6,0.02])
    fig.plt.colorbar(it, cax=cax)

    fig.ax, fig.it, fig.ax_cb = ax, it, cax
    fig.init()
    fig.update_png_json['extent'] = [100, 150, 0, 50]
    fig.save2qgis()

def main1():
    fig = figure()
    ax = fig.add_axes([0.1,0.3,0.8,0.7])
    import numpy as np

    t = np.arange(10000).reshape(100, 100)
    it = ax.imshow(t, extent=[70, 150, 0, 70])

    cax = fig.add_axes([0.3,0.1,0.6,0.02])
    fig.update_png_json['extent'] = [100, 150, 0, 50]
    fig.plt.colorbar(it, cax=cax)

    fig.ax, fig.it, fig.ax_cb = ax, it, cax
    fig.init()
    fig.update_png_json['extent'] = [100, 150, 0, 50]
    fig.update_png_json['extent'] = [100, 150, 0, 50]
    fig.save2qgis()


def test():
    fig = figure()
    ax = fig.add_axes([0.1, 0.3, 0.8, 0.7])

    it = ax.imshow([[0,1],[3,4]], extent=[70, 150, 0, 70])

    cax = fig.add_axes([0.3,0.1,0.6,0.02])
    fig.plt.colorbar(it, cax=cax, orientation='horizontal')

    fig.ax, fig.it, fig.ax_cb = ax, it, cax
    fig.init()
    fig.update_png_json['qgslevel'] = 3
    fig.qgs_template = './achn/template.qgs'
    fig.qgs_template_json = './achn/template.qgs.json'
    fig.save2qgis()


def test0():
    fig = figure()
    ax = fig.add_axes([0.1, 0.3, 0.8, 0.7])

    it = ax.imshow([[0,1],[3,4]], extent=[70, 150, 0, 70])

    cax = fig.add_axes([0.3,0.1,0.6,0.02])
    fig.plt.colorbar(it, cax=cax, orientation='horizontal')

    fig.ax, fig.it, fig.ax_cb = ax, it, cax
    fig.init()
    fig.qgsfile = '/tmp/1.png'
    fig.update_png_json = {'qgslevel':12}
    fig.qgs_template = './achn/template.qgs'
    fig.qgs_template_json = './achn/template.qgs.json'
    fig.save2qgis()


def test1():
    fig = figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax = imshow([[1,2],[3,4]])
    ax.plot([1,2,3])

    fig.int()
    fig.update_png_json()
    fig.save2qgis()

if __name__ == "__main__":
    test()

