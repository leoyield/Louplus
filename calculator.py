#!/usr/bin/env python3

import sys

class Calculator:
    def __init__(self):
        self.argv = sys.argv[1:]
        self.prm = {'-c': 'none', '-d': 'none', '-o': 'none'}

    def param(self):
        prm = {}
        if len(self.argv) != 6:
            raise 'erro'
        for a, i in enumerate(self.argv):
            if i in self.prm:
                prm[i] = self.argv[a+1]
        #if 'none' in self.prm.values():
        #    raise 'erro'
        return prm

    def cfg_udata(self):
        param = self.param()
        cfg_file = param['-c']
        user_file = param['-d']
        gongzi_file = param['-o']
        cfg = {}
        user = {}
        try:
            with open(cfg_file, 'r') as f:
                for i in f.readlines():
                    cfg[i.split('=')[0].strip()] = int(float(i.split('=')[1].strip()))
            with open(user_file, 'r') as f:
                for i in f.readlines():
                    user[i.split(',')[0]] = int(float(i.split(',')[1]))
        except:
            raise 'erro'
        return cfg, user, gongzi_file

    def calculat(self, cfg, user):
        #cfg, user = self.cfg_udata()
        uid = user.keys()[0]
        b_tax = user.values()[0]
        ratio =  (cfg['YangLao'] + cfg['YiLiao']
                  + cfg['ShiYe'] + cfg['GongShang']
                  + cfg['ShengYu'] + cfg['GongJiJin'])
        if b_tax < cfg['JiShuL']:
            SheBao = cfg['JiShuL'] * ratio
        elif b_tax >cfg['JiShuH']:
            SheBao = cfg['JiShuH'] * ratio
        else:
            SheBao = b_tax * ratio
        i_tax = b_tax - SheBao
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
        a_tax = i_tax - tax
        return uid, b_tax, SheBao, tax, a_tax

    def write(self):
        cfg, user, gongzi_file = self.cfg_udata()
        try:
            with open(gongzi_file, 'w') as f:
                for i in user:
                    a, b, c, d, e = self.calculat(cfg, user[i])
                    data = '{},{},{:.2f},{:.2f},{:.2f}\n'.format(a,b,c,d,e)
                    f.write(data)
        except:
            return 'error'

if __name__ == '__main__':
    c = Calculator()
    c.write()

