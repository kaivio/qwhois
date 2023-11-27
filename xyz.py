from itertools import product
import subprocess
import datetime
import time

CHR = 'abcdefghijklmnopqrstuvwxyz'
DIG = '0123456789'

# 后缀，匹配文本，迭代器，起名函数，过滤器
_sf = 'xyz'
_qs = 'DOMAIN NOT FOUND'
_it = product(DIG, repeat=6)
_iq = lambda i: ''.join(i)
_ft = lambda s: s > '000520'


def query(target, qs=_qs):
    retry = 0
    while True:
        try:
            output = subprocess.check_output(['whois', target], shell=False, text=True)
            break
        except Exception as e:
            print(e)
            retry += 1
            time.sleep(retry * 2)


    return qs in output #.split('\n')[0]



current_time = datetime.datetime.now()
logname = current_time.strftime(_sf+"_%y-%m-%d_%H%M%S.txt")

file = open(logname, "w")

for i in _it:
    q = _iq(i)
    name = q + '.' + _sf
    if _ft(q):
        s = query(name)
    else:
        s = None

    file.write(f'{name} {s} \n')
    file.flush()

    print(f'  {name} {s}      \r', end='')
    if s:
        print(f'  {name}          ')



file.close()

