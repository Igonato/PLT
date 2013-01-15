#!/usr/bin/python
# -*- coding: utf-8 -*-

class LL1PDA:
    """Pushdown automaton for LL(1) grammar"""

    def __init__(self, G):
        self.__dict__.update(G)
        table = dict([(A, dict()) for A in self.N])
        for nonterm, rules in self.P.items():
            for rule in rules:
                if rule == '':
                    for term in self.follow(nonterm):
                        table[nonterm][term] = tuple()
                    continue
                for term in filter(lambda e: e in self.T, self.first(rule)):
                    table[nonterm][term] = rule
                if '' in self.first(rule):
                    for term in self.follow(nonterm):
                        table[nonterm][term] = rule
        self.table = table

    def first(self, alpha):
        s = set()
        # if symbol
        if type(alpha) is str:
            # if terminal
            if alpha in self.T:
                return set([alpha])
            # else checking rules
            for rule in self.P[alpha]:
                if rule == '':
                    s.add('')
                else:
                    s.update(self.first(rule))
        # if chain
        else:
            for i, symbol in enumerate(alpha):
                symbols_first = self.first(symbol)
                s.update(symbols_first.difference(['']))
                if '' not in symbols_first:
                    break
                if i == len(alpha) - 1 and '' in symbols_first:
                    s.add('')
        return s

    def follow(self, X):
        s = set()
        # if X is axiom
        if X == self.S:
            s.add('$')
        # for each rule that have X in right part
        for nonterm, rules in self.P.items():
            for rule in filter(lambda e: X in e, rules):
                # for each X in rule
                for i, x in filter(lambda e: e[1] == X, enumerate(rule)):
                    # if it isn't last one
                    if i < len(rule) - 1:
                        # for rule like A -> aXb b is the following chain
                        following_chain = rule[i + 1:]
                        following_first = self.first(following_chain)
                        s.update(following_first.difference(['']))
                        # if folowing chain can become empty
                        if '' in following_first:
                            # do the same thing as X was at the end
                            s.update(self.follow(nonterm))
                    # if X at the end, than it can have same follow as 
                    # nondeterminate on the left side
                    else:
                        if nonterm != X:
                            s.update(self.follow(nonterm))
        return s

    def check_chain(self, chain):
        chain = chain.split() + ['$']
        stack = [self.S, '$']
        
        while True:
            if stack[0] in self.N:
                try:
                    rule = self.table[stack[0]][chain[0]]
                    stack.pop(0)
                    stack = list(rule) + stack
                except KeyError:
                    return False
            elif stack[0] in self.T:
                if stack.pop(0) != chain.pop(0):
                    return False
            elif stack[0] == '$':
                return stack[0] == chain[0]


# Grammar 1
G1 = {
    'T' : ('or', 'and', 'not', 'true', 'false', '(', ')'), 
    'N' : ('E', 'E`', 'T', 'T`', 'F'), 
    'P' : {
        'E'  : [('T', 'E`')],
        'E`' : [('or', 'T', 'E`'), ''],
        'T'  : [('F', 'T`')],
        'T`' : [('and', 'F', 'T`'), ''],
        'F'  : [('not', 'F'), ('(', 'E', ')'), ('true', ), ('false', )]}, 
    'S' : 'E'}

# Grammar 2
G2 = {
    'T' : ('+', '-', 'a', 'b', '(', ')', '^', '*'), 
    'N' : ('R', 'R`', 'F', 'T'), 
    'P' : {
        'R'  : [('F', 'R`'), ('F', 'R`'), ('(', 'R', ')')],
        'R`' : [('^', 'F', 'R`'), ('T', 'R`'),  ('*', 'R`'), ''],
        'F'  : [('T', ), ('b', )],
        'T' : [('+', 'a'), ('-', 'a')]}, 
    'S' : 'R'}


if __name__ == '__main__':
    automaton1 = LL1PDA(G1)
    automaton2 = LL1PDA(G2)

    with open("test.txt") as f:
        chains = f.read().split('\n')

    chains1 = filter(automaton1.check_chain, chains)
    chains2 = filter(automaton2.check_chain, chains)

    other = filter(lambda x: x not in chains1 and x not in chains2, chains)

    with open("1.txt", "w") as f:
        f.write('\n'.join(chains1))
    with open("2.txt", "w") as f:
        f.write('\n'.join(chains2))
    with open("!.txt", "w") as f:
        f.write('\n'.join(other))
