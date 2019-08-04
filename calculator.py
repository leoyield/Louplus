#!/usr/bin/env python3

import sys
from multiprocessing import Queue, Process

class Calculator:
    def __init__(self):
        self.argv = sys.argv[1:]
        self.prm = {'-c': 'none', '-d': 'none', '-o': 'none'}
        self.queue1 = Queue()
        self.queue2 = Queue()
    def param(self):
        prm = {}
        if len(self.argv) != 6:
            raise 'erro'
        for a, i in enumerate(self.argv):
            if i in self.prm:
                prm[i] = self.argv[a+1]
        cfg_file = prm['-c']
        user_file = prm['-d']
        gongzi_file = prm['-o']
        cfg = {}
        user = {}
        try:
            with open(cfg_file, 'r') as f:
                for i in f.readlines():
                    cfg[i.split('=')[0].strip()] = float(i.split('=')[1].strip())
            with open(user_file, 'r') as f:
                for i in f.readlines():
                    user[i.split(',')[0]] = int(float(i.split(',')[1]))
        except:
            raise 'erro'
        self.queue1.put([cfg, user, gongzi_file])

    def calculat(self, queue):
        data = queue.get()
        cfg = data[0]
        users = data[1]
        gongzi_file = data[2]
        data_user = []
        for user in users:
            b_tax = users[user]
            ratio =  (cfg['YangLao'] + cfg['YiLiao']
                      + cfg['ShiYe'] + cfg['GongShang']
                      + cfg['ShengYu'] + cfg['GongJiJin'])
            if b_tax < cfg['JiShuL']:
                SheBao = cfg['JiShuL'] * ratio
            elif b_tax >cfg['JiShuH']:
                SheBao = cfg['JiShuH'] * ratio
            else:
                SheBao = b_tax * ratio
            if b_tax - SheBao > 5000:
                i_tax = b_tax - SheBao - 5000
            else:
                i_tax = 0
            if i_tax <= 3000:
                tax = i_tax * 0.03
            elif 3000 < i_tax <= 12000:
                tax = i_tax * 0.1 - 210
            elif 12000 < i_tax <= 25000:
                tax = i_tax * 0.2 - 1410
            elif 25000 < i_tax <= 35000:
                tax = i_tax * 0.25 - 2660
            elif 35000 < i_tax <= 55000:
                tax = i_tax * 0.3 - 4410
            elif 55000 < i_tax <= 80000:
                tax = i_tax * 0.35 - 7160
            elif i_tax > 80000:
                tax = i_tax * 0.45 - 15160
            a_tax = b_tax - tax - SheBao
            data_user.append('{},{},{:.2f},{:.2f},{:.2f}\n'.format(user, b_tax, SheBao, tax, a_tax))
        self.queue2.put([data_user, gongzi_file])
        
    def write(self, queue):
        data = queue.get()
        user = data[0]
        gongzi_file = data[1]
        try:
            with open(gongzi_file, 'w') as f:
                 f.writelines(user)
        except:
            return 'error'
    def main(self):
        p1 = Process(target=self.param).start()
        p2 = Process(target=self.calculat, args=(self.queue1,)).start()
        p3 = Process(target=self.write, args=(self.queue2,)).start()
if __name__ == '__main__':
    c = Calculator()
    c.main()

