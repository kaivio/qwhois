#!/usr/bin/env python3

from itertools import product
from datetime import datetime
from time import sleep
import subprocess
WORD = 'abcdefghijklmnopqrstuvwxyz'
DIG = '0123456789'

# Begin of params
sample = 'was not found.'
sample_fail = ''
suffix = 'im'
length = 3
chars = WORD
# chars = DIG
# chars = DIG+WORD

# End of params


def check(target, sample, sample_fail='', retry_rule=[5, 5, 20]):
    retry = 0
    while True:
        try:
            output = subprocess.check_output(
                ['whois', target], shell=False, text=True)
            if sample in output:
                return 'ok'
            if sample_fail in output:
                return 'fail'

            raise Exception('unknown ')

        except Exception as e:
            print(e)
            retry += 1
            sleep(retry_rule[retry])

        if retry > len(retry_rule):
            return 'unknown'


def run(chars, length, suffix, sample, sample_fail='', retry_rule=[5, 5, 20], save=True):
    filename = save == True and datetime.now().strftime(
        f"{suffix}-{length}_%y-%m-%d_%H%M%S.txt")
    file = save and open(filename, "w")
    log = save and (lambda s: (file.write(s+'\n'),
                    file.flush())) or (lambda s: s)

    print('# Targets:')
    print('[%s]{%d}.%s\n' % (chars, length, suffix))
    print('# Report:', save and f'(save to {filename})' or '')

    it = product(chars, repeat=length)
    for i in it:
        name = ''.join(i) + '.' + suffix
        print(f'   {name}  checking...\r', end='')

        res = check(name, sample, sample_fail, retry_rule)
        if res == 'ok':
            print(f'   {name}              ')
            log(name)
        elif res == 'unknown':
            print(f'   {name}  [?]         ')
            log(name+' [?]')

    save and file.close()


run(chars, length, suffix, sample, sample_fail)
