
import sys
import os
import re
import glob
import json
import numpy as np
import math
import shutil


class UNIT:
    d = '°'
    du = '°'
    degree = '°'


def safe_remove(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
            print(f"文件 {path} 已删除")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            print(f"目录 {path} 已删除")
        else:
            print(f"{path} 不存在")
    except Exception as e:
        print(f"删除 {path} 时出错: {e}")


def runs(cmds, num):
    from multiprocessing import Pool
    pool = Pool(processes = num)
    for cmd in cmds:
        pool.apply_async(os.system, (cmd,))
    pool.close()
    pool.join()


def llr2xyz(lon, lat, R=6371):
    pi = 3.141592654
    r = R*np.cos(lat/180*math.pi)
    z = R*np.sin(lat/180*math.pi)
    x = r*np.cos(lon/180*math.pi)
    y = r*np.sin(lon/180*math.pi)
    return x,y,z


def Rotate(a, theta, x, y, z):
    # {{{
    '''对坐标进行旋转操作'''

    theta = theta/180*math.pi

    if a == 1:
        rotate = np.array([[1, 0, 0], [0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]])
    elif a == 2:
        rotate = np.array([[np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]])
    elif a == 3:
        rotate = np.array([[np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]])

    temp = np.dot(rotate,np.vstack((x.flatten(), y.flatten(), z.flatten())))
    xn = temp[0,:].reshape(x.shape)
    yn = temp[1,:].reshape(x.shape)
    zn = temp[2,:].reshape(x.shape)
    return xn, yn, zn
    # }}}


def local_xyz2lonlat(xj_1, yj_1, zj_1, lon0, lat0, alt0=0):
    # {{{
    xj = xj_1.flatten()
    yj = yj_1.flatten()
    zj = zj_1.flatten()

    x0, y0, z0 = llr2xyz(0, 0, R=6371)
    x = zj+x0+alt0
    y = xj
    z = yj

    x, y, z = Rotate(2, 0-lat0, x, y, z)
    x, y, z = Rotate(3, lon0, x, y, z)
    alt = np.sqrt(x**2+y**2+z**2) - 6371

    lon = np.arctan2(y,x)
    lat = np.arctan2(z,np.sqrt(x**2 + y**2))
    lon = lon / np.pi * 180
    lat = lat / np.pi * 180
    return lon.reshape(xj_1.shape),\
            lat.reshape(xj_1.shape),\
            alt.reshape(xj_1.shape),\
    # }}}


def get_range_id(lon, lat, z, i, j, k, xlim, ylim, zlim):
    # {{{
    id =\
         (lon.flatten()[i] >= xlim[0]) &\
         (lon.flatten()[j] >= xlim[0]) &\
         (lon.flatten()[k] >= xlim[0]) &\
         (lon.flatten()[i] <= xlim[1]) &\
         (lon.flatten()[j] <= xlim[1]) &\
         (lon.flatten()[k] <= xlim[1]) &\
         (lat.flatten()[i] >= ylim[0]) &\
         (lat.flatten()[j] >= ylim[0]) &\
         (lat.flatten()[k] >= ylim[0]) &\
         (lat.flatten()[i] <= ylim[1]) &\
         (lat.flatten()[j] <= ylim[1]) &\
         (lat.flatten()[k] <= ylim[1]) &\
         (z.flatten()[i] >= zlim[0]) &\
         (z.flatten()[j] >= zlim[0]) &\
         (z.flatten()[k] >= zlim[0]) &\
         (z.flatten()[i] <= zlim[1]) &\
         (z.flatten()[j] <= zlim[1]) &\
         (z.flatten()[k] <= zlim[1])
    return id
    # }}}


def triangle_area_3d(x1, x2, x3, y1, y2, y3, z1, z2, z3):
    # {{{
    
    # 计算每个三角形的顶点坐标
    A = np.column_stack((x1, y1, z1))
    B = np.column_stack((x2, y2, z2))
    C = np.column_stack((x3, y3, z3))

    # 计算向量 AB 和 AC
    AB = B - A
    AC = C - A

    # 计算叉积
    cross_product = np.cross(AB, AC)

    # 计算每个三角形的面积
    areas = 0.5 * np.linalg.norm(cross_product, axis=1)
    return areas
    # }}}


def area_by_xyz(x1, y1, x2, y2, x3, y3):
    return 0.5 * np.abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))


def geotiff2cogtiff(input_path, output_path):
    # {{{
    """
    将输入 TIFF 转换为 Cloud Optimized GeoTIFF (COG)

    参数：
    input_path (str): 输入 TIFF 文件路径
    output_path (str): 输出 COG 文件路径
    """
    from osgeo import gdal
    try:
        # 注册所有 GDAL 驱动
        gdal.AllRegister()

        # 打开原始文件
        src_ds = gdal.Open(input_path, gdal.GA_ReadOnly)
        if src_ds is None:
            raise RuntimeError(f"无法打开输入文件: {input_path}")

        # 获取原始波段信息
        band = src_ds.GetRasterBand(1)
        nodata = band.GetNoDataValue()
        dtype = gdal.GetDataTypeName(band.DataType)

        # 检查 NoData 值兼容性（针对 Byte 类型）
        if dtype == 'Byte' and nodata is not None:
            if nodata > 255 or nodata < 0:
                print(f"警告: NoData 值 {nodata} 超出 Byte 范围(0-255)，自动重置为 255")
                nodata = 255

        # COG 转换选项
        options = [
            'TILED=YES',               # 启用分块
            'BLOCKXSIZE=512',          # 分块宽度
            'BLOCKYSIZE=512',          # 分块高度
            'COMPRESS=LZW',            # 压缩算法
            'OVERVIEWS=AUTO',          # 自动生成金字塔
            'OVERVIEW_RESAMPLING=AVERAGE',  # 重采样方法
            'BIGTIFF=IF_NEEDED',       # 处理大文件
            'COPY_SRC_OVERVIEWS=YES',  # 复制现有金字塔（如果有）
            'NUM_THREADS=ALL_CPUS'     # 多线程加速
        ]

        # 执行转换
        print(f"开始转换: {input_path} -> {output_path}")
        cog_ds = gdal.Translate(
            output_path,
            src_ds,
            format='COG',
            creationOptions=options,
            noData=nodata
        )

        if cog_ds is None:
            raise RuntimeError("COG 转换失败")

        # 显式关闭数据集（重要！确保数据写入磁盘）
        cog_ds = None
        src_ds = None

        print("转换成功！")
        print(f"输出文件: {output_path}")

    except Exception as e:
        print(f"错误发生: {str(e)}")
        sys.exit(1)
    # }}}


def array2cogtiff(data_array, lats, lons, output_path, epsg=4326):
    # {{{
    """
    将二维数组 + 经纬度坐标存储为 COG
    
    参数：
    data_array : numpy.ndarray  二维数据矩阵（行对应纬度，列对应经度）
    lats       : numpy.ndarray  纬度数组（从北到南递减）
    lons       : numpy.ndarray  经度数组（从西到东递增）
    output_path: str            输出文件路径
    epsg       : int            坐标系 EPSG 代码（默认 WGS84）
    """
    from osgeo import gdal, osr
    try:
        # 验证输入数据
        assert data_array.ndim == 2, "数据必须是二维数组"
        assert len(lats) == data_array.shape[0], "纬度维度不匹配"
        assert len(lons) == data_array.shape[1], "经度维度不匹配"

        # 获取栅格尺寸
        rows, cols = data_array.shape
        
        # 计算地理变换参数 (GeoTransform)
        # 格式: (左上角经度, 经度分辨率, 旋转, 左上角纬度, 旋转, 纬度分辨率)
        lon_res = (lons[-1] - lons[0]) / (len(lons) - 1)
        lat_res = (lats[-1] - lats[0]) / (len(lats) - 1)
        geotransform = (
            lons[0] - lon_res/2,  # 左上角经度 (像元中心对齐)
            lon_res,              # 经度方向分辨率
            0,                    # 旋转参数（通常为0）
            lats[0] - lat_res/2,  # 左上角纬度
            0,                    # 旋转参数（通常为0）
            lat_res               # 纬度方向分辨率（通常为负）
        )

        # 创建内存数据集
        driver = gdal.GetDriverByName('MEM')  # 先在内存中创建
        ds = driver.Create('', cols, rows, 1, gdal.GDT_Float32)

        # 设置地理参考
        ds.SetGeoTransform(geotransform)
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(epsg)
        ds.SetProjection(srs.ExportToWkt())

        # 写入数据
        band = ds.GetRasterBand(1)
        band.WriteArray(data_array)
        band.FlushCache()

        # COG 转换选项
        cog_options = [
            'TILED=YES',
            'BLOCKXSIZE=512', 
            'BLOCKYSIZE=512',
            'COMPRESS=LZW',
            'OVERVIEWS=AUTO',
            'OVERVIEW_RESAMPLING=AVERAGE',
            'BIGTIFF=IF_NEEDED'
        ]

        # 转换为 COG
        driver = gdal.GetDriverByName('COG')
        cog_ds = driver.CreateCopy(output_path, ds, options=cog_options)
        
        # 显式释放资源
        cog_ds = None
        ds = None
        
        print(f"成功生成 COG: {output_path}")

    except Exception as e:
        print(f"生成 COG 失败: {str(e)}")
        raise
    # }}}
