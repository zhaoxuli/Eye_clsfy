import multiprocessing
import os
import time

CPU_NUM = 8
fn_disturb = 'disturb_in_pic.sh'


def f(cmd):
    #if hasattr(os, 'getppid'):  # only available on Unix
    #    print 'parent process:', os.getppid()
    print 'process id:', os.getpid()
    os.system(cmd)
    #output = os.popen(cmd)
    #print output.read()
    

def skip_comments_and_blank(file, cm='#'):
    lines = list()
    for line in file:
        if not line.strip().startswith(cm) and not line.isspace():
            lines.append(line)
    return lines


if __name__ == '__main__':
    lines = skip_comments_and_blank(open(fn_disturb))
    #lines = open(fn_disturb).readlines()
    p = multiprocessing.Pool(8)
    p.map(f, lines)
    p.close()
    p.join()
