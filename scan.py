#!/usr/bin/env python3

import socket
import sys

def count(num):
    return len(num)
def t_int(num):
    return int(num)
def arg():
    a = sys.argv[1:]
    lh = a[a.index('--host') + 1].split('.')
    try:
        if len(a) != 4:
            raise 'erro num'
        elif '--host' not in a:
            raise 'erro arg'
        elif '--port' not in a:
            raise 'erro arg'
        elif len(lh) != 4 or (0 in list(map(count,lh))):
            raise 'erro host'
    except:
        print('Parameter Error')

    try:
        port = a[a.index('--port') + 1].split('-')
        port = list(map(t_int,port))
    except:
        print('Paramerter Error')
    if len(port) >= 2:
        port = list(range(port[0],port[1]))
    host = a[a.index('--host') + 1]
    return host, port

def scan():
    host, port = arg()
    for i in port:
        s = socket.socket()
        try:
            s.connect((host, i))
        except:
            print('{} closed'.format(i))
        else:
            print('{} open'.format(i))
        finally:
            s.close()

if __name__ == '__main__':
    scan()
