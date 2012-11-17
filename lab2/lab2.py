#!/usr/bin/python
# -*- coding: utf-8 -*-

MP_TABLE = { 
    '_' : [  '+',      '*',      '(',      ')',      'i',       '|'  ],
    'E' : ['REJECT', 'REJECT', 'PPHR'  , 'REJECT', 'PPHR'  , 'REJECT'],
    'H' : ['PRN'   , 'REJECT', 'REJECT', 'POP'   , 'REJECT', 'POP'   ],
    'R' : ['REJECT', 'REJECT', 'PPTF'  , 'REJECT', 'PPTF'  , 'REJECT'],
    'T' : ['POP'   , 'PFN'   , 'REJECT', 'POP'   , 'REJECT', 'POP'   ],
    'F' : ['REJECT', 'REJECT', 'PP)EN' , 'REJECT', 'PN'    , 'REJECT'],
    ')' : ['REJECT', 'REJECT', 'REJECT', 'PN'    , 'REJECT', 'REJECT'],
    '#' : ['REJECT', 'REJECT', 'REJECT', 'REJECT', 'REJECT', 'ACCEPT'],
}

ACTIONS = {
    'PPHR': lambda s, i: (s[:-1] + 'HR', i),
     'POP': lambda s, i: (s[:-1], i),
     'PRN': lambda s, i: (s + 'R', i[1:]),
    'PPTF': lambda s, i: (s[:-1] + 'TF', i),
     'PFN': lambda s, i: (s + 'F', i[1:]),
   'PP)EN': lambda s, i: (s[:-1] + ')E', i[1:]),
      'PN': lambda s, i: (s[:-1], i[1:]),
      'PN': lambda s, i: (s[:-1], i[1:])
}


class SSPDA:
    """Single state pushdown automaton"""
    def __init__(self, table=MP_TABLE, actions=ACTIONS):
        self._stack = "#E"
        self._table = dict(table)
        self._symbols = self._table.pop('_')
        self._actions = actions
    
    def reset(self):
        self._stack = "#E"

    def check_chain(self, chain):
        chain += '|'
        self.reset()
        while True:
            action = self._table[self._stack[-1]][self._symbols.index(chain[0])]
            if action == 'REJECT':
                return False
            if action == 'ACCEPT':
                return True        
            if len(self._stack) > 9000:
                raise OverflowError()
            self._stack, chain = self._actions[action](self._stack, chain)


if __name__ == '__main__':
    A = SSPDA()
    with open("test.txt") as f:
        chains = f.read().replace(" ", "").split('\n')

    accepted = []
    rejected = []
    for c in chains:
        if A.check_chain(c):
            accepted.append(c)
        else:
            rejected.append(c)

    with open("accepted.txt", "w") as f:
        f.write('\n'.join(accepted))
    with open("rejected.txt", "w") as f:
        f.write('\n'.join(rejected))
    

