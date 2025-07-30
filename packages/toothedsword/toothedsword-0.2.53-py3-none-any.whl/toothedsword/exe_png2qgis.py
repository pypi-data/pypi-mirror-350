import time
import time_htht as htt
print(htt.time2str(time.time(), 'yyyy:mm:dd HH:MM:SS'))
import sys
import re
import argparse
import os

print(htt.time2str(time.time(), 'yyyy:mm:dd HH:MM:SS'))

from png2qgis import fig

def parse_args():
    # {{{
    """
    Parse input arguments
    """
    parser = argparse.ArgumentParser(description='FY3D conv')
    parser.add_argument('--png', dest='png',
                        help='input png file',
                        default=None, type=str)
    parser.add_argument('--qgs', dest='qgs',
                        help='qgs template',
                        default=None, type=str)
    parser.add_argument('--png_json', dest='png_json',
                        help='png json',
                        default=None, type=str)
    parser.add_argument('--qgs_json', dest='qgs_json',
                        help='qgs json',
                        default=None, type=str)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args
    # }}}

# 获取参数
args = parse_args()

f = fig()
f.pngfile = args.png
f.qgs_template = args.qgs
if args.qgs_json is None:
    f.qgs_json_file = f.qgs_template+'.json'
else:
    f.qgs_json_file = args.qgs_json

if args.png_json is None:
    f.png_json_file = f.pngfile+'.json'
else:
    f.png_json_file = args.png_json

if re.search(',', f.pngfile):
    f.pngs2qgs_json()
else:
    f.png2qgs_json()
