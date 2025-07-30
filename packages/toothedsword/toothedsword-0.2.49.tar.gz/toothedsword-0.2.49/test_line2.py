
import time
import sys
from toothedsword import print_status_best, print_output,\
        gen_process_tab, clear_screen

clear_screen()

for i in range(1, 101):
    time.sleep(0.1)
    # sys.stdout.write("\033[10;0H")
    # sys.stdout.write(f"{i}\n")
    # sys.stdout.flush()
    print_output(i)
    print_status_best(gen_process_tab(i, 100, type='low'))
