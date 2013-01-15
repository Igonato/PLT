#!/usr/bin/python
# -*- coding: utf-8 -*-

class PPDA:
    """Pushdown automaton for precedence grammar"""
    def __init__(self, grammar, precedence_matrix):
        self.__dict__.update(grammar)
        self.T.add('|')

        rows = map(str.split, precedence_matrix.split('\n')[1:-1])
        precedences = dict()
        for row in rows[1:]:
            precedences[row[0]] = dict()
            for relation, symbol in zip(row[1:], rows[0][1:]):
                if relation != '.':
                    precedences[row[0]][symbol] = relation

        rules = dict()
        for rule in self.P:
            L, D = rule.replace(' ', '').split('->')
            rules[L] = set(D.split('|'))

        self.rules = rules
        self.precedences = precedences


    def check_chain(self, chain):
        result = chain
        chain += '|'
        stack = '|'
        while True:
            if stack + chain == '|' + self.S + '|':
                return result + ' SUCCESS!'
            try:
                if self.precedences[stack[-1]][chain[0]] == '>': #reduce
                    i = -1
                    while self.precedences[stack[i - 1]][stack[i]] == '=':
                        i -= 1
                    chain_to_reduce = stack[i:]
                    for nonterm, rules in self.rules.items():
                        if chain_to_reduce in rules:
                            stack = stack[:i] + nonterm
                            result += ' -> ' + (stack + chain)[1:-1]
                            break
                else: #shift
                   stack += chain[0]
                   chain = chain[1:]

            except (KeyError, IndexError):
                return result + ' -> FAIL!'
# Grammar 1
G1 = { 
    'T': {'a', 'b', 'c', 'd'}, 
    'N': {'S', 'A'}, 
    'P': {  
        'S -> aSbA | bc',
        'A -> aSb | d'},
    'S': 'S'}
MATRIX1 = """
.   S   A   a   b   c   d   |
S   .   .   .   =   .   .   =
A   .   .   .   >   .   .   >
a   =   .   <   <   .   .   .
b   .   =   <   >   =   <   >
c   .   .   .   >   .   .   >
d   .   .   .   >   .   .   >
|   =   .   <   <   .   .   .
"""

# Grammar 2
G2 = {
    'T': {'+', '-', '*', '/', '(', ')', 'a', 'b'}, 
    'N': {'S', 'R', 'T', 'F', 'E'}, 
    'P': {
        'S -> TR | T',
        'R -> +T | -T | +TR | -TR',
        'T -> EF | E',
        'F -> *E | /E | *EF | /EF',
        'E -> (S) | a | b'
        }, 
    'S': 'S'}
MATRIX2 = """
.   +   -   *   /   (   )   a   b   S   R   T   F   E   |
+   .   .   .   .   <   .   <   <   .   .   =   .   <   .
-   .   .   .   .   <   .   <   <   .   .   =   .   <   .
*   .   .   .   .   <   .   <   <   .   .   .   .   =   .
/   .   .   .   .   <   .   <   <   .   .   .   .   =   .
(   .   .   .   .   <   .   <   <   =   .   <   .   <   .
)   >   >   >   >   .   >   .   .   .   >   .   >   .   >
a   >   >   >   >   .   >   .   .   .   >   .   >   .   >
b   >   >   >   >   .   >   .   .   .   >   .   >   .   >
S   .   .   .   .   .   =   .   .   .   .   .   .   .   .
R   .   .   .   .   .   >   .   .   .   .   .   .   .   >
T   <   <   .   .   .   >   .   .   .   =   .   .   .   >
F   >   >   .   .   .   >   .   .   .   >   .   .   .   >
E   >   >   <   <   .   >   .   .   .   >   .   =   .   >
|   .   .   .   .   <   .   <   <   .   .   <   .   <   .
"""

if __name__ == '__main__':
    automaton1 = PPDA(G1, MATRIX1)
    automaton2 = PPDA(G2, MATRIX2)

    with open("test.txt") as f:
        chains = f.read().split('\n')

    result = '\n'.join(["First grammar:"] + map(automaton1.check_chain, chains)) + '\n'
    result += '\n'.join(["Second grammar:"] + map(automaton2.check_chain, chains))

    with open("results.txt", "w") as f:
        f.write(result)