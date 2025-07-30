#!/bin/python3

import time as tm
import re
import datetime


def time2str(t, ss, num=1): # {{{
    st = str(datetime.datetime.utcfromtimestamp(t))
    # st = tm.strftime("%Y-%m-%d %H:%M:%S", tm.gmtime(t + tm.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))))
    time = re.search(r'(\d\d\d\d)\-(\d\d)\-(\d\d) (\d\d)\:(\d\d)\:(\d\d)',st)
    year = time.group(1)
    year2 = re.search(r'\d\d(\d\d)',year)
    year2 = year2.group(1)
    month = time.group(2)
    dom = time.group(3)
    doy = vec2time(year, month, dom, 0, 0, 1) - vec2time(year, 1, 1, 0, 0, 0) + 1
    doy = round(doy/24/3600)+1000
    doy = re.sub(r'^1', '', str(doy))
    hour = time.group(4)
    minute = time.group(5)
    sec = time.group(6)
    st = ss
    m3 = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', 
          '05':'May', '06':'Jun', '07':'Jul', '08':'Aug', 
          '09':'Sep', '10':'Oct', '11':'Nov', '12':'Dec'}
    for i in range(0, num):
        st = re.sub('yyyy',year,st);
        st = re.sub('mmm',m3[month],st);
        st = re.sub('mm',month,st);
        st = re.sub('ddd',doy,st);
        st = re.sub('dd',dom,st);
        st = re.sub('HH',hour,st);
        st = re.sub('MM',minute,st);
        st = re.sub('SS',sec,st);
    return st # }}}


def time2vec(t): # {{{
    st = datetime.datetime.utcfromtimestamp(t)
    st = str(st)
    time = re.search(r'(\d\d\d\d)-(\d\d)-(\d\d) (\d\d)\:(\d\d)\:(\d\d)',st)
    year = int(time.group(1))
    month = int(time.group(2))
    dom = int(time.group(3))
    hour = int(time.group(4))
    minute = int(time.group(5))
    sec = int(time.group(6))
    return year,month,dom,hour,minute,sec # }}}


def str2time(s, rs='yyyymmddHHMMSS'):  # {{{
    if rs == 'yyyymmddHHMMSS':
        try:
            s = re.search(r'(\d{14})', s).group(1)
        except Exception as e:
            pass
        rt = re.search(
            r'(\d\d\d\d)[^\d]*(\d\d)[^\d]*(\d\d)[^\d]*' +
            r'(\d\d)[^\d]*(\d\d)[^\d]*(\d\d)', s)
        year = rt.group(1)
        month = rt.group(2)
        dom = rt.group(3)
        hour = rt.group(4)
        minute = rt.group(5)
        sec = rt.group(6)
    else:
        t = re.search(r'yyyy', rs)
        year = s[t.span(0)[0]:t.span(0)[1]]
        t = re.search(r'mm', rs)
        month = s[t.span(0)[0]:t.span(0)[1]]
        t = re.search(r'dd', rs)
        dom = s[t.span(0)[0]:t.span(0)[1]]
        t = re.search(r'HH', rs)
        hour = s[t.span(0)[0]:t.span(0)[1]]
        t = re.search(r'MM', rs)
        minute = s[t.span(0)[0]:t.span(0)[1]]
        t = re.search(r'SS', rs)
        sec = s[t.span(0)[0]:t.span(0)[1]]

    # 创建datetime对象
    dt = datetime.datetime(year=int(year), month=int(month), day=int(dom),
                        hour=int(hour), minute=int(minute), second=int(sec))

    # 计算与1970年1月1日午夜UTC的时间差
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch

    # 将时间差转换为秒数
    ts = delta.total_seconds()
    return ts  # }}}


def vec2time(year, month, dom, hour, minute, sec):  # {{{
    # 创建datetime对象
    dt = datetime.datetime(year=int(year), month=int(month), day=int(dom),
                        hour=int(hour), minute=int(minute), second=int(sec))

    # 计算与1970年1月1日午夜UTC的时间差
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch

    # 将时间差转换为秒数
    ts = delta.total_seconds()

    return ts  # }}}


if __name__ == "__main__":
    infile = '/tmp//FY4/FY4B/GIIRS/L2/AVP/REGC/2024/2024080700/FY4B-_GIIRS-_N_REGC_1050E_L2-_AVP-_MULT_NUL_20240807080000_20240807080000_012KM_V0001.NC'
    # infile = '2024/08/07-08:00:00'
    print(infile)
    dt = str2time(infile)
    print(time2str(dt, 'yyyy/mm/dd HH:MM:SS'))
