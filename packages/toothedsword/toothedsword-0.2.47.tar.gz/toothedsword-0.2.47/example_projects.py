
import sys
import time
from toothedsword import project


say, p = project(sys.argv[-1], 
                 steps='输入|预处理|计算|产品制作|绘图|输出',
                 processtab='high', 
                 simple=False,
                )


def main():
    say('输入开始')
    time.sleep(0.1)
    infile = '/'
    outdir = '/tmp/'

    try:
        infile = p.pfile
        outdir = p.outdir
        say('输入')
    except Exception as e:
        pass
    say('输入完成')

    say('预处理开始')
    time.sleep(1.1)
    say('预处理完成')

    say('计算开始')
    time.sleep(1.23)
    say('计算完成')

    say('产品制作开始')
    time.sleep(1.6)
    say('产品制作完成')

    say('绘图开始')
    time.sleep(0.625)
    say('绘图完成')
 
    say('输出开始')
    time.sleep(0.412)
    say(':/tmp/nAMV_rACHN_t20240413120000_l4.png')
    say(':/tmp/test2.png')
    say('输出完成')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        say('error:'+str(e))
    say()
