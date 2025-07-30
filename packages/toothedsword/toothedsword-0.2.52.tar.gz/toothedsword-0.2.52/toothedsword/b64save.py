import re
import os
import json
import base64
import numpy as np
import netCDF4 as nc
from io import BytesIO
from weakref import finalize
from collections.abc import Mapping
import h5py


def dict2b64(data):
    if str(type(data)) == str(type({0:1})):
        ks = list(data.keys())
        for k in ks:
            if str(type(data[k])) == str(type(np.array([0,1]))):
                b = base64.b64encode(data[k])
                sb = str(b)[2:-1]+'|numpy'
                data[k+'_type'] = str(data[k].dtype)
                data[k+'_shape'] = data[k].shape
                data[k] = sb
            else:
                dict2b64(data[k])
    elif str(type(data)) == str(type([0,1])):
        for k in range(0, len(data)):
            dict2b64(data[k])
    else:
        return


def dict2numpy(data, file, name):
    if str(type(data)) == str(type({0:1})):
        ks = list(data.keys())
        for k in ks:
            if str(type(data[k])) == str(type(np.array([0,1]))):
                outdir = file+'.data/'
                if ~os.path.exists(outdir):
                    os.system('mkdir -p '+outdir)
                b = name+'.'+k+'.npy'
                np.save(outdir+b, data[k])
                data[k] = b
            else:
                dict2numpy(data[k],file,name+'.'+str(k))
    elif str(type(data)) == str(type([0,1])):
        for k in range(0, len(data)):
            dict2numpy(data[k],file,name+'.'+str(k))
    else:
        return


def b642dict(data):
    if str(type(data)) == str(type({0:1})):
        for k in data.keys():
            if str(type(data[k])) == str(type('s')):
                if re.search(r'\|numpy$', data[k]):
                    b = base64.decodebytes(bytes(re.sub(r'\|.*','',data[k]), "utf8"))
                    data[k] = np.frombuffer(b, dtype=data[k+'_type']).reshape(data[k+'_shape'])
            else:
                b642dict(data[k])
    elif str(type(data)) == str(type([0,1])):
        for k in range(0, len(data)):
            b642dict(data[k])
    else:
        return


def numpy2dict(data,file,name=''):
    if str(type(data)) == str(type({0:1})):
        for k in data.keys():
            if str(type(data[k])) == str(type('s')):
                if re.search(r'\.npy$', data[k]):
                    if re.search(r'ALLDATA', name):
                        print(file+'.data/'+data[k])
                        data[k] = np.load(file+'.data/'+data[k])
                    else:
                        if re.search(r'0\.'+name+r'\.npy$', data[k]):
                            data[k] = np.load(file+'.data/'+data[k])
            else:
                numpy2dict(data[k],file,name)
    elif str(type(data)) == str(type([0,1])):
        for k in range(0, len(data)):
            numpy2dict(data[k],file,name)
    else:
        return


def dict2json(data, file):
    dict2b64(data)
    with open(file, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def dict2jsons(data, file):
    dict2numpy(data, file, '0')
    with open(file, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def json2dict(file):
    with open(file) as json_file:
        data = json.load(json_file)
    pass
    b642dict(data)
    return data 


def jsons2dict(file,name='ALLDATA'):
    with open(file) as json_file:
        data = json.load(json_file)
    pass
    if name == 'None':
        pass
    else:
        numpy2dict(data,file,name)
    return data 


class LazyNetCDFArray:
    # {{{
    """惰性加载的NetCDF数组包装类，支持文件自动管理"""
    def __init__(self, filepath, variable_path):
        self.filepath = filepath
        self.variable_path = variable_path
        self._dataset = None
        self._variable = None
        self._data = None

        # 注册终结器确保资源释放
        self._finalizer = finalize(self, self._close)

    def _ensure_open(self):
        """确保文件已打开"""
        if self._dataset is None:
            self._dataset = nc.Dataset(self.filepath, 'r')
            parts = self.variable_path.split('/')
            obj = self._dataset
            for part in parts:
                if part in obj.groups:
                    obj = obj.groups[part]
                else:
                    obj = obj.variables[part]
            self._variable = obj

    def _close(self):
        """关闭文件"""
        if self._dataset is not None:
            self._dataset.close()
            self._dataset = None
            self._variable = None

    def __getitem__(self, key):
        self._ensure_open()
        if self._data is None:
            self._data = self._variable[:]
        return self._data[key]

    @property
    def shape(self):
        self._ensure_open()
        return self._variable.shape

    @property
    def dtype(self):
        self._ensure_open()
        return self._variable.dtype

    def __array__(self):
        return self[:]

    def __repr__(self):
        try:
            self._ensure_open()
            return f"LazyNetCDFArray(shape={self.shape}, dtype={self.dtype})"
        except:
            return "LazyNetCDFArray(<closed>)"
    # }}}


def netcdf2lazydict(nc_file_path):
    # {{{
    """
    惰性加载的NetCDF到字典转换函数

    参数:
        nc_file_path (str): NetCDF文件路径

    返回:
        dict: 包含所有数据和结构的字典，数组变量为惰性加载对象
    """
    def process_group(group, current_path=""):
        """递归处理NetCDF组"""
        result = {}

        # 特别处理根组的全局属性
        if current_path=="":
            result['global_attrs'] = {}
            for attr_name in group.ncattrs():
                attr_value = group.getncattr(attr_name)
                # 转换NumPy类型为Python原生类型
                if isinstance(attr_value, np.generic):
                    attr_value = attr_value.item()
                result['global_attrs'][attr_name] = attr_value

        # 处理变量
        for var_name, var in group.variables.items():
            var_path = f"{current_path}/{var_name}" if current_path else var_name
            result[var_name] = LazyNetCDFArray(nc_file_path, var_path)

        # 处理子组
        for group_name, subgroup in group.groups.items():
            group_path = f"{current_path}/{group_name}" if current_path else group_name
            result[group_name] = process_group(subgroup, group_path)

        return result

    # 打开NetCDF文件并处理根组
    with nc.Dataset(nc_file_path, 'r') as dataset:
        return process_group(dataset)
    # }}}


def netcdf2dict(nc_file_path, convert_numeric_arrays=False):
    # {{{
    """
    将 NetCDF 文件转换为多层字典，可选择保留数值型 NumPy 数组
    
    参数:
        nc_file_path (str): NetCDF 文件路径
        convert_numeric_arrays (bool): 是否将数值数组转换为列表，默认为False(保留为NumPy数组)
    
    返回:
        dict: 包含所有数据和结构的字典
    """
    def process_group(group):
        """递归处理 NetCDF 组"""
        result = {}
        
        # 处理变量
        for var_name, var in group.variables.items():
            # 获取变量数据
            data = np.array(var[:])  # 确保是NumPy数组
            dtype = var.dtype
            
            # 处理标量变量
            if not var.shape:
                # 处理字符串标量
                if hasattr(dtype, 'kind') and dtype.kind == 'S':
                    data = data.item().decode('utf-8') if isinstance(data.item(), bytes) else str(data.item())
                # 处理布尔值（存储为int8的）
                elif str(dtype) == 'int8' and data.item() in (0, 1):
                    data = bool(data.item())
                result[var_name] = data
                continue
            
            # 处理数组变量
            if hasattr(dtype, 'kind'):
                if dtype.kind == 'S':
                    # 处理字符串数组
                    data = np.char.decode(data, 'utf-8') if data.dtype.kind == 'S' else data
                    data = data.tolist()  # 字符串数组总是转为列表
                elif str(dtype) == 'int8' and np.all(np.isin(data, [0, 1])):
                    # 处理布尔数组（存储为int8的）
                    data = data.astype(bool)
                    if convert_numeric_arrays:
                        data = data.tolist()
                elif dtype.kind in ['i', 'u', 'f']:  # 整数、无符号整数、浮点数
                    if convert_numeric_arrays:
                        data = data.tolist()
                else:
                    # 其他数值类型数组
                    if convert_numeric_arrays:
                        data = data.tolist()
            else:
                # 未知类型，根据convert_numeric_arrays决定
                data = data.tolist() if convert_numeric_arrays else data
            
            # 简化单元素数组为标量（只有当转换为列表时才应用）
            if convert_numeric_arrays and len(data) == 1 and not isinstance(data[0], (list, np.ndarray)):
                data = data[0]
            
            result[var_name] = data
        
        # 处理子组
        for group_name, subgroup in group.groups.items():
            result[group_name] = process_group(subgroup)
        
        return result
    
    # 打开 NetCDF 文件并处理根组
    with nc.Dataset(nc_file_path, 'r') as dataset:
        return process_group(dataset)
    # }}}


def dict2netcdf(data_dict, output_path, group=None, parent_group=None, compress=True):
    # {{{
    """
    将多层字典转换为 NetCDF 文件
    
    参数:
        data_dict (dict): 要转换的字典，可以包含多层嵌套
        output_path (str): 输出的 NetCDF 文件路径
        group (str): 当前处理的组名（用于递归调用）
        parent_group: 父组对象（用于递归调用）
    
    返回:
        None
    """
    # 第一次调用时创建根组
    if parent_group is None:
        with nc.Dataset(output_path, 'w', format='NETCDF4') as rootgrp:
            if 'global_attrs' in data_dict:
                for attr_name, attr_value in data_dict['global_attrs'].items():
                    setattr(rootgrp, attr_name, attr_value)
                data_dict.pop('global_attrs')

            dict2netcdf(data_dict, output_path, group=None, parent_group=rootgrp, compress=compress)
        return
    
    # 获取当前组
    current_group = parent_group if group is None else parent_group.createGroup(group)
    j = -1
    gdim_dict = {}
    gdim_dddd = {}
    gdim_list = []
 
    for key, value in data_dict.items():
        # 处理嵌套字典（创建子组）
        if isinstance(value, Mapping):
            dict2netcdf(value, output_path, group=key, parent_group=current_group, compress=compress)
            continue
         
        # 处理字符串类型
        if isinstance(value, str):
            # 创建字符串变量
            max_len = len(value)
            str_type = f'S{max_len}'  # 固定长度字符串类型
            current_group.createVariable(key, str_type, ())
            current_group.variables[key][:] = np.array(value, dtype=str_type)
            continue
        
        # 处理列表或数组类型
        if isinstance(value, (list, np.ndarray)):
            # 转换为 numpy 数组
            arr = np.array(value)
            
            # 处理布尔数组 - 转换为int8
            if arr.dtype == bool:
                arr = arr.astype('i1')
            
            # 创建维度（如果不存在）
            for i, dim_size in enumerate(arr.shape):
                dim_name_key = f'{key}_dim_{i}'
                if dim_size in gdim_list:
                    gdim_dict[dim_name_key] = gdim_dddd[dim_size]
                else:
                    j += 1
                    dim_name = f'd{dim_size}'
                    current_group.createDimension(dim_name, dim_size)
                    gdim_list.append(dim_size)
                    gdim_dict[dim_name_key] = dim_name
                    gdim_dddd[dim_size] = dim_name
            
            # 创建变量
            if arr.dtype.kind == 'U':
                # 处理Unicode字符串数组
                max_len = max(len(s) for s in arr.ravel())
                str_type = f'S{max_len}'
                var = current_group.createVariable(key, str_type, tuple(gdim_dict[f'{key}_dim_{i}'] for i in range(arr.ndim)))
                var[:] = np.char.encode(arr, 'utf-8')
            else:
                # 处理数值数组
                if compress:
                    var = current_group.createVariable(key, arr.dtype, tuple(gdim_dict[f'{key}_dim_{i}'] for i in range(arr.ndim)), zlib=True)
                else:
                    var = current_group.createVariable(key, arr.dtype, tuple(gdim_dict[f'{key}_dim_{i}'] for i in range(arr.ndim)))
                var[:] = arr
            continue
        
        # 处理布尔标量
        if isinstance(value, bool):
            current_group.createVariable(key, 'i1', ())
            current_group.variables[key][:] = int(value)
            continue
        
        # 处理标量数值
        if isinstance(value, (int, float, np.number)):
            current_group.createVariable(key, type(value), ())
            current_group.variables[key][:] = value
            continue
        
        # 如果是不支持的类型，跳过并打印警告
        print(f"警告: 跳过键 '{key}' - 不支持的类型: {type(value)}")
    # }}}


def dict2hdf(data_dict, hdf5_file, group=None, mode='w'):
# {{{
    """
    将Python字典写入HDF5文件（递归处理嵌套结构）
    
    参数:
        data_dict: 要写入的字典
        hdf5_file: HDF5文件路径或已打开的h5py.File对象
        group: 目标组路径（默认为根组）
        mode: 文件模式 ('w'写入, 'a'追加)
    """
    def write_item(parent, key, value):
        if isinstance(value, dict):
            # 创建子组并递归处理
            subgroup = parent.create_group(key)
            for k, v in value.items():
                write_item(subgroup, k, v)
        else:
            # 处理数据
            if isinstance(value, (list, tuple)):
                value = np.array(value)
            
            # 特殊处理字符串类型
            if isinstance(value, str):
                value = np.string_(value.encode('utf-8'))
            elif isinstance(value, np.ndarray) and value.dtype.kind == 'U':
                value = np.char.encode(value, 'utf-8')
            
            # 写入数据集
            if isinstance(value, (np.ndarray, np.generic)):
                parent.create_dataset(key, data=value)
            else:
                # 处理其他Python原生类型
                parent.create_dataset(key, data=np.array(value))

    if isinstance(hdf5_file, str):
        with h5py.File(hdf5_file, mode) as f:
            target = f.create_group(group) if group else f
            for k, v in data_dict.items():
                write_item(target, k, v)
    else:
        target = hdf5_file.create_group(group) if group else hdf5_file
        for k, v in data_dict.items():
            write_item(target, k, v)
# }}}


def hdf2dict(hdf5_file, group=None):
# {{{
    """
    将HDF5文件/组转换为Python字典（递归处理嵌套结构）
    
    参数:
        hdf5_file: HDF5文件路径或已打开的h5py.File对象
        group: 要转换的组路径（默认为根组）
    
    返回:
        dict: 包含所有数据和子结构的字典
    """
    def process_item(item):
        if isinstance(item, h5py.Dataset):
            # 处理数据集
            data = item[()]
            if isinstance(data, np.ndarray):
                # 处理字符串数组
                if data.dtype.kind == 'S':
                    data = np.char.decode(data, 'utf-8')
                # 转换为Python原生类型
                if data.size == 1:
                    data = data.item()
                else:
                    data = data.tolist()
            elif isinstance(data, np.generic):
                data = data.item()
            return data
        elif isinstance(item, h5py.Group):
            # 递归处理组
            return {name: process_item(item[name]) for name in item}
        return None

    if isinstance(hdf5_file, str):
        with h5py.File(hdf5_file, 'r') as f:
            target = f[group] if group else f
            return process_item(target)
    else:
        target = hdf5_file[group] if group else hdf5_file
        return process_item(target)
# }}}


class LazyHDF5Array:
    # {{{
    """惰性加载的HDF5数据集包装类"""
    def __init__(self, filepath, dataset_path):
        self.filepath = filepath
        self.dataset_path = dataset_path
        self._file = None
        self._dataset = None
        self._data = None
        self._finalizer = finalize(self, self._close)
    
    def _ensure_open(self):
        """确保文件和数据集已打开"""
        if self._file is None:
            self._file = h5py.File(self.filepath, 'r')
            self._dataset = self._file[self.dataset_path]
    
    def _close(self):
        """关闭文件"""
        if self._file is not None:
            self._file.close()
            self._file = None
            self._dataset = None
    
    def __getitem__(self, key):
        self._ensure_open()
        if self._data is None:
            self._data = self._dataset[:]
        return self._data[key]
    
    @property
    def shape(self):
        self._ensure_open()
        return self._dataset.shape
    
    @property
    def dtype(self):
        self._ensure_open()
        return self._dataset.dtype
    
    def __array__(self):
        return self[:]
    
    def __repr__(self):
        try:
            self._ensure_open()
            return f"LazyHDF5Array(shape={self.shape}, dtype={self.dtype})"
        except:
            return "LazyHDF5Array(<closed>)"
    # }}}


def hdf2lazydict(hdf5_filepath):
    # {{{
    """
    将HDF5文件转换为惰性加载的字典结构
    
    参数:
        hdf5_filepath (str): HDF5文件路径
    
    返回:
        dict: 惰性加载的字典，数据集只在访问时读取
    """
    def process_group(group, current_path=""):
        """递归处理HDF5组"""
        result = {}
        
        # 处理数据集
        for name, item in group.items():
            if isinstance(item, h5py.Dataset):
                # 数据集路径
                dataset_path = f"{current_path}/{name}" if current_path else name
                result[name] = LazyHDF5Array(hdf5_filepath, dataset_path)
            elif isinstance(item, h5py.Group):
                # 递归处理子组
                group_path = f"{current_path}/{name}" if current_path else name
                result[name] = process_group(item, group_path)
        
        return result
    
    # 打开HDF5文件并处理根组
    with h5py.File(hdf5_filepath, 'r') as f:
        return process_group(f)
    # }}}


def t1():
    dt = {}
    t = np.array([1,2,3], dtype=np.float32)
    t = np.arange(24).reshape(4, 3, 2).astype(np.float32)
    dt['t'] = t
    print(dt)
    dict2b64(dt) 
    print(dt)
    b642dict(dt)
    print(dt)


def test():
    t = {}
    t[1] = 1
    t[2] = np.array([0,1], dtype=np.float32)
    t[2] = np.arange(24).reshape(3, 4, 2).astype(np.float32)
    b = base64.b64encode(t[2])
    sb = str(b)
    data = base64.decodebytes(bytes(sb[2:-1], "utf8"))
    t1 = np.frombuffer(data, dtype=np.float32)
    print(t1)
    breakpoint()
    b64 = 'data:application/octet-stream;base64,'+str(b)[2:-1]
    t[2] = b64
    with open('t.json', "w", encoding='utf-8') as f:
        json.dump(t, f)
    exit()

# numpy数组转base64编码
    arr = np.arange(12).reshape(3, 4)
    bytesio = BytesIO()
    np.savetxt(bytesio, arr) # 只支持1维或者2维数组，numpy数组转化成字节流
    content = bytesio.getvalue()  # 获取string字符串表示
    print(content)
    b64_code = base64.b64encode(content)
     
# 从base64编码恢复numpy数组
    b64_decode = base64.b64decode(b64_code)
    arr = np.loadtxt(BytesIO(b64_decode))
    print(arr)
    breakpoint()


def main():
    # 数据
    dt = {}
    t = np.array([2,3], dtype=np.float32)
    t = np.arange(32).reshape(2, 2, 8).astype(np.int16)
    np.save('t.npy', t)
    dt['n'] = t
    dt['d'] = {1:4, 'a':'b'}
    dt['l'] = [1,2,3,'o']
    dt['n1'] = t+1
    import copy
    dt1 = copy.deepcopy(dt)

    # 将数据存为json
    dict2json(dt, 'dt.json')

    # 读取json数据
    dto = json2dict('dt.json')

    # 将数据存为json
    dict2jsons(dt1, 'dt1.json')

    # 读取json数据
    dto1 = jsons2dict('dt1.json', 'None')
    print(dto1)


if __name__ == "__main__":
    main()
