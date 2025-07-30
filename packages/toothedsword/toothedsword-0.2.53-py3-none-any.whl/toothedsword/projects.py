import re # {{{
from .b64save import json2dict, dict2json
import os
import sys
from . import time_htht as htt
import time
import shutil


displayed_lines = []
tmp_datas = {}
tmp_datas['term_height'] = 0
tmp_datas['status'] = ''
tmp_datas['simple'] = not(os.isatty(sys.stdout.fileno()))
# }}}


def get_terminal_height():
    # {{{
    _, term_height_new = shutil.get_terminal_size()
    term_height = tmp_datas['term_height']
    t = term_height_new == term_height
    tmp_datas['term_height'] = term_height_new
    if t:
        pass
    else:
        clear_screen()
        # print_status_best(tmp_datas['status'])
        # p = tmp_datas['status']
        # sys.stdout.write(f"\033[{term_height_new};0H{p}\033[K")
        # sys.stdout.flush()
        pass
    return term_height_new
    # }}}


class Colors:
    # {{{
    RESET = "\033[0m"  # 重置颜色
    BLACK = "\033[30m"   # 红色
    RED = "\033[31m"   # 红色
    GREEN = "\033[32m" # 绿色
    YELLOW = "\033[33m" # 黄色
    BLUE = "\033[34m"  # 蓝色
    CYAN = "\033[36m"  # 青色
    WHITE = "\033[37m"  # 青色
    BOLD = "\033[1m"   # 加粗
    UNDERLINE = "\033[4m" # 下划线
    # }}}


def dtime2stime(dtime):
    # {{{
    dtime = str(dtime)
    dtime = re.sub('(^0\.0*\d{3}).*', r'\1', dtime)
    dtime = re.sub(r'(.*[^0].*\.\d{2})\d+', r'\1', dtime)
    dtime = re.sub(r'(\..*[^0])0+$', r'\1', dtime)
    stime = re.sub(r'\.0+$', '.0', dtime)
    return stime
    # }}}


def gen_process_tab(ns, nsl, type='low'):
    # {{{
    fn = int(ns*40/nsl)
    hn = 40 - fn
    if False:
        fn -= 1
        stmp = '['+'='*fn+'>'+'.'*hn+']'
    if False:
        stmp = '['+'#'*fn+''+'.'*hn+']'
    if type == 'high':
        stmp = f"{Colors.WHITE}"+'━'*fn+f"{Colors.RESET}"+\
			   f"{Colors.RED}"+'━'*hn+f"{Colors.RESET}"
    if type == 'low':
        stmp = '['+\
				f"{Colors.RED}{Colors.BOLD}"+'#'*fn+f"{Colors.RESET}"+\
				f"{Colors.WHITE}"+'.'*hn+f"{Colors.RESET}"+\
				']'
    stmp += ' '+str(int(ns/nsl*100))+'% ('+str(int(ns))+'/'+str(nsl)+')'
    return stmp
    # }}}


def clear_screen():
    """清屏并将光标移至顶部"""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def print_status(progress):
    # {{{
    """在终端底部打印进度状态"""
    term_height = get_terminal_height()

    # 定位到最后一行
    sys.stdout.write(f"\033[{term_height};0HProgress: {progress}%\033[K")  

    sys.stdout.flush()
    # }}}


def print_status_best(progress):
    # {{{
    """在终端底部打印进度状态"""
    if tmp_datas['simple']:
        print(progress, flush=True)
        return

    tmp_datas['status'] = progress
    term_height = get_terminal_height()
    sys.stdout.write(f"\033[{term_height};0H{progress}\033[K")
    sys.stdout.flush()
    # }}}


def print_output(line):
    # {{{
    """打印滚动输出内容"""
    if tmp_datas['simple']:
        print(line, flush=True)
        return

    sys.stdout.write("\033[H")  # 光标回到第一行
    displayed_lines.append(line)
    term_height = get_terminal_height()
    while len(displayed_lines) > term_height-1:
        displayed_lines.pop(0)
    for line in displayed_lines:
        sys.stdout.write(f"{line}\n")
    sys.stdout.flush()
    # }}}


def project(*args, **kw):
    p = PROJECT(*args, **kw)
    return p.say, p


class PROJECT():
    def __init__(self, inputjson, steps='初始化|输出',
        # {{{
                 pname='', prodir='', processtab='low',
                 simple=True):
        tmp_datas['simple'] = simple
        """TODO: to be defined. """
        self.processtab=processtab
        if pname == '':
            self.pname = 'tctb'
        else:
            self.pname = pname
        clear_screen()

        self.status = '成功'
        self.error = ''
        self.outputs = []
        self.time0 = time.time()
        self.outdir = '/tmp/'
        self.time00 = self.time0
        if prodir == '':
            self.prodir = os.path.dirname(
                    os.path.abspath(__file__))
        else:
            self.prodir = prodir

        if str(type(steps)) == str(type('-')):
            self.steps = re.split(r'\|', steps)
        else:
            self.steps = steps

        self.status_tab = gen_process_tab(0, len(self.steps), self.processtab)
        self.progress = [0, len(self.steps)]

        try:
            self.input = json2dict(inputjson)
        except Exception as e:
            if pname == '':
                self.pname = 'base'
            else:
                self.pname = pname
            inputjson = self.prodir+'/'+self.pname+'/input.json'
            self.input = json2dict(inputjson)

        try:
            settingsjson = self.prodir+'/'+\
                    self.pname+'/settings.json'
            self.settings = json2dict(settingsjson)
        except Exception as e:
            self.settings = {'info':''}

        try:
            self.outdir = self.input['resultPath']
            self.pfile = self.input['primaryFile']
        except Exception as e:
            pass

        try:
            self.flow_file = self.input['resultFlowFile']
            self.result_file = self.input['resultJsonFile']
            self.log_file = self.input['resultLogFile']
        except Exception as e:
            pass

        self.initjson()

    def initjson(self):
        # 初始化flowjson
        try:
            self.flow_dict = json2dict(self.prodir+'/'+self.pname+'/flow.json')
            self.step_dict = {} 
            num = 0
            for sname in self.steps:
                num += 1
                tmp = json2dict(self.prodir+'/'+self.pname+'/step.json')
                tmp['stepName'] = sname
                tmp['stepNo'] = str(num)
                self.flow_dict['step'].append(tmp)
                self.step_dict[sname] = tmp
            dict2json(self.flow_dict, self.flow_file)
            self.flow('初始化')

            # 初始化resultjson
            self.result_dict = json2dict(self.prodir+'/'+self.pname+'/result.json')
            self.result_dict['productionTime'] =\
                    htt.time2str(time.time()+8*3600, 'yyyy/mm/dd HH:MM:SS CST')
            dict2json(self.result_dict, self.result_file)
        except Exception as e:
            pass
        # }}}

    def flow(self, sname):
        # {{{
        if sname in self.step_dict:
            pass
        else:
            return

        if self.step_dict[sname]['status'] == 0:
            return

        ns = 0
        for s in self.steps:
            ns += 1
            if self.step_dict[s]['status'] == 0:
                continue
            stime = htt.time2str(time.time()+8*3600, 'yyyy/mm/dd HH:MM:SS CST')

            # 处理完成时间字符串
            dtime = str(time.time()-self.time0)
            dtime = re.sub('(^0\.0*\d{3}).*', r'\1', dtime)
            dtime = re.sub(r'(.*[^0].*\.\d{2})\d+', r'\1', dtime)
            dtime = re.sub(r'(\..*[^0])0+$', r'\1', dtime)
            dtime = re.sub(r'\.0+$', '.0', dtime)

            self.step_dict[s]['status'] = 0 
            self.step_dict[s]['log'] =\
                    s+'完成, 耗时'+dtime+'秒' 
            self.step_dict[s]['timeStamp'] = stime
            dict2json(self.flow_dict, self.flow_file)

            self.log(s+'完成')
            self.time0 = time.time()
            if s == sname:
                break

        self.progress[0] = ns
        stmp = gen_process_tab(ns, len(self.steps), 
                               type=self.processtab)
        print_status_best(stmp)
        self.status_tab = stmp
        # }}}

    def finish(self, info={}):
        # {{{
        if self.error == '':
            pass
        else:
            self.status = '失败'

        if self.status == '失败':
            self.result_dict['status'] = '1'
            self.result_dict['message'] = self.error
        if self.status == '成功':
            self.result_dict['status'] = '0'
            self.result_dict['message'] = '执行成功。'
            self.flow('输出')
        if self.status == '重做':
            self.result_dict['status'] = '9'
            self.result_dict['message'] =\
                    '需要重做。'+self.error
        dict2json(self.result_dict, self.result_file)
        return
        # }}}

    def result(self, outpath='', info={}):
        # {{{
        if outpath == '':
            if self.error == '':
                pass
            else:
                self.status = '失败'

            if self.status == '失败':
                self.result_dict['status'] = '1'
                self.result_dict['message'] = self.error
            if self.status == '成功':
                self.result_dict['status'] = '0'
                self.result_dict['message'] = '执行成功。'
                self.flow('输出')
            if self.status == '重做':
                self.result_dict['status'] = '9'
                self.result_dict['message'] =\
                        '需要重做。'+self.error
            dict2json(self.result_dict, self.result_file)
            self.log('运行完毕, 耗时'+\
                dtime2stime(time.time()-self.time00)+'秒')
            return

        self.flow('处理')
        product = json2dict(self.prodir+'/'+
                        self.pname+'/product.json')

        if str(type(info)) == str(type('')):
            info1 = {}
            for tmp in re.split(r'\|', info):
                try:
                    tmp1 = re.search('(.+):(.+)', tmp)
                    info1[tmp1.group(1)] = tmp1.group(2)
                except Exception as e:
                    pass
            info = info1
    
        self.outputs.append(outpath)
        if re.search(r'^:', outpath):
            outpath = re.sub(r'^:'+self.outdir, '', outpath)
        if re.search(r'^\|', outpath):
            outpath = re.sub(r'^\|'+self.outdir, '', outpath)
        if re.search(r'-norootpath-', self.settings['info']):
            outpath = re.sub(r'^'+self.outdir, '', outpath)

        product['filePath'] = outpath
        product.update(info)
        self.result_dict['result'].append(product)
        dict2json(self.result_dict, self.result_file)
        # }}}

    def log(self, stmp):
        # {{{
        stmp0 = stmp

        if stmp == '输出开始':
            self.flow('处理')

        if re.search(r'.*开始$', stmp):
            self.time0 = time.time()
            # print_output('/*----------------------------')

        if re.search(r'.*完成$', stmp):
            stime = dtime2stime(time.time()-self.time0)
            stmp = stmp + ', 耗时'+stime+'秒'
            self.time0 = time.time()

        with open(self.log_file, 'a') as f:
            s = htt.time2str(time.time()+8*3600, 
                             'yyyy/mm/dd HH:MM:SS CST: ')+stmp
            print_output(s)
            f.write(s+'\n')

        if re.search(r'.*完成$', stmp0):
            # print_output('----------------------------*/\n')
            pass
        
        if tmp_datas['simple']:
            return

        ns = self.progress[0]
        ns += (int(ns)+1-ns)/3
        if ns > self.progress[1]:
            ns = self.progress[1]
        self.progress[0] = ns
        stmp = gen_process_tab(ns, len(self.steps), 
                       type=self.processtab)
        print_status_best(stmp)
        self.status_tab = stmp
        # }}}

    def update(self):
        # {{{
        return
        # }}}

    def say(self, stmp='', info={}):
        # {{{
        if re.search('建立新项目:', stmp):
            outputpath = re.search(r':(.+)', stmp).group(1)
            os.system('cp -r '+self.prodir+'/tctb '+outputpath)

        if stmp == '更新结果状态' or\
                stmp == '' or stmp == 'update result':
            self.result()
            return

        if re.search(r'^错误:', stmp):
            print_output(stmp)
            self.error = stmp

        if re.search(r'^ERROR:', stmp):
            print_output(stmp)
            self.error = stmp

        if re.search(r'^error:', stmp):
            print_output(stmp)
            self.error = stmp

        if re.search(r'.+完成$', stmp):
            step = re.search(r'(.+)完成$', stmp).group(1)
            if step in self.step_dict:
                self.flow(step)
                return

        if re.search(r'^[p|o|r]?:', stmp):
            outfile = re.sub(r'^[p|o|r]?:', '', stmp)
            self.result(outfile, info)
            self.log('输出文件: '+outfile)
            return
 
        if re.search(r'^output:', stmp):
            outfile = re.sub(r'^output:', '', stmp)
            self.result(outfile, info)
            self.log('输出文件: '+outfile)
            return

        if re.search(r'^file:', stmp):
            outfile = re.sub(r'^output:', '', stmp)
            self.result(outfile, info)
            self.log('输出文件: '+outfile)
            return

        if re.search(r'^result:', stmp):
            outfile = re.sub(r'^result:', '', stmp)
            self.result(outfile, info)
            self.log('输出文件: '+outfile)
            return

        if re.search(r'^输出:', stmp):
            outfile = re.sub(r'^输出:', '', stmp)
            self.result(outfile, info)
            self.log('输出文件: '+outfile)
            return

        if stmp == 'INPUT' or\
                stmp == 'input' or\
                stmp == '显示输入:' or\
                stmp == '输入': 
            try:
                self.log('输入主文件: '+self.pfile)
            except Exception as e:
                pass
            try:
                self.log('输出根目录: '+self.outdir)
            except Exception as e:
                pass
            return
        self.log(stmp)
        # }}}
