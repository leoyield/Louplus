#!/usr/bin/env python3

import sys

class calculator:
    def __init__(self):
        self.argv = sys.argv[1:].split(' ')
        self.prm = {'-c': 'none', '-d': 'none', '-o': 'none'}

    def param(self):
        if len(self.argv) != 6:
            raise 'erro'
        for a, i in enumerate(self.argv[::2]):
            if i in self.prm:
                self.prm[i] = self.argv[a+1]
        if 'none' in self.prm.values:
            raise 'erro'
        return self.prm

    def calculat(self):
        param = self.param()
        cfg_file = param['-c']
        user_file = param['-d']
        gongzi_file = param['-o']

