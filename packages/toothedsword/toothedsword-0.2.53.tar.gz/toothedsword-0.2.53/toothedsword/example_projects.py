
import sys
import time


try:
    from projects import project
    say, p = project(sys.argv[-1], steps='输入|计算|输出')
except Exception as e:
    print(e)
    say = print 


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

    say('计算开始')
    time.sleep(1)
    say('计算完成')
    

    say('绘图开始')
    time.sleep(0.625)
    say('绘图完成')
 
    say('输出开始')
    time.sleep(0.412)
    say(':/tmp/test1.png')
    say(':/tmp/test2.png')
    say('输出完成')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        say('error:'+str(e))
    say()
