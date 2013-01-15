#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
from multiprocessing import Process, Pool
from collections import defaultdict
from itertools import combinations, permutations, chain, ifilter


def show_graph(dotdata, title="xdot viewer"):
    import gtk
    import gtk.gdk
    import xdot

    window = xdot.DotWindow()
    window.set_dotcode(dotdata)
    window.connect('destroy', gtk.main_quit)
    window.set_title(title)
    gtk.main()   

        
  ##                                             
 #  #                                            
 #      # #     ###   ## #   ## #    ###   # #   
 # ##   ## #   #  #   # # #  # # #  #  #   ## #  
 #  #   #      #  #   # # #  # # #  #  #   #     
  ##    #       ####  #   #  #   #   ####  #           

class G:
    """Representation of a formal grammar G = (N, T, P, S).

    G(N, T, P, S) -> grammar
    * N - set of nonterminal symbols
    * T - set of terminal symbols
    * P - set of production rules
    * S - start symbol
    Any symbol must be a string of length one. Rule is a string with nonterminal 
    symbol, symol "->" and >= 1 strings composed of terminals and nonterminals 
    separateg by "|".
    """
    def __init__(self, T, N, P, S):
        self.T = set(T)
        self.N = set(N)
        self.P = set(P)
        self.S = S
        self.validate()


    def __str__(self):
        s = 'G = (T, N, P, S)\n'
        s += '    T = {' + ', '.join((t for t in self.T)) + '}\n'
        s += '    N = {' + ', '.join((t for t in self.N)) + '}\n'
        s += '    P = {' + ',\n         '.join((t for t in self.P)) + '}\n'
        s += '    S = ' + self.S + "\n"
        return s

    def validate(self):
        """G.validate() -> True

        Return validness of the grammar. True if every symbol is length one str,
        NUT is empty, S in N and every rule match specified format. Owerwise 
        raise ValueError.
        """
        # every symbol is length one str
        invalid_symbols = list(filter(
            lambda x: (type(x) != str and type(x) != unicode) or len(x) != 1,
            chain(self.N, self.T))) 
        # intersection must be empty
        invalid_symbols.extend(self.N.intersection(self.T))
        # every rule must match specified format
        invalid_rules = list()
        for rule in self.P:
            L, D = rule.replace(" ", "").split('->')
            D = D.replace("|", "")
            if list(filter(lambda x: x not in self.N.union(self.T), D)) \
            or L not in self.N:
                print L not in self.N
                print list(filter(lambda x: x not in self.N.union(self.T), D))
                invalid_rules.append(rule) 

        if invalid_symbols or invalid_rules:
            raise ValueError("Invalid symbols: " + str(invalid_symbols) + " " +
                             "Invalid rules: " + str(invalid_rules))

                     
 ####    ##    #   # 
 #      #  #   ## ## 
 ###     #     # # # 
 #        #    # # # 
 #      #  #   #   # 
 #       ##    #   # 

class FSM:
    """Finite state machine 

    FSM(G) -> finite state machine
    * G - right linear grammar.

    FSM(sigma, Q, q, delta, F) -> finite state machine
    * sigma - input alphabet (a finite, non-empty set of symbols).
    * Q - a finite, non-empty set of states.
    * q - an initial state, an element of Q.
    * delta - state-transition dictionary: delta[state1][input] -> set of states
    * F - set of final states, subset of Q.
    """
    def __init__(self, *args):
        if len(args) is 5: # FSM(sigma, Q, q, delta, F)
            sigma, Q, q, delta, F = args
            self.sigma = sigma
            self.Q = Q
            self.q = q
            self.delta = delta
            self.F = F
            self._state = q

        elif len(args) is 1: # FSM(G)
            G, = args
            sigma = set()
            Q = set()
            q = G.S
            delta = dict()
            F = set()
            self.__init__(sigma, Q, q, delta, F)

            for state in G.N:
                self.add_state(state)
            self.add_state('Z')
            self.set_final_states(set('Z'))

            for input_ in G.T:
                self.add_input(input_)

            for rule in G.P:
                extra_state_index = 1
                L, D = rule.replace(" ", "").split('->')
                for d in D.split('|'):
                    state_before_last_unput = L
                    if d[-1] not in self.Q:
                        d += 'Z'
                    for input_ in d[:-2]: # add extra states if necessary 
                        state_before_last_unput = L + str(extra_state_index)
                        self.add_state(state_before_last_unput)
                        self.add_command(L, input_, state_before_last_unput)
                        extra_state_index += 1
                    self.add_command(state_before_last_unput, d[-2], d[-1])

    def add_state(self, state):
        """m.add_state(str) Add state in Q"""
        self.Q.add(state)
        self.delta[state] = defaultdict(set)

    def add_final_state(self, state):
        """m.add_final_state(str) Add state in F"""
        if state in self.Q:
            self.F.add(state)
        else:
            raise ValueError('Automaton does not have specified state!')

    def add_input(self, input_):
        """m.add_input(str) Add input in sigma"""
        self.sigma.add(input_)

    def set_initial_state(self, state):
        """m.set_initial_state(str)

        Set q
        """
        if state in self.Q:
            self._state = state
        else:
            raise ValueError('Automaton does not have specified state!')

    def set_final_states(self, states):
        """m.set_final_states(set) Set F"""
        if states.issubset(self.Q):
            self.F = states
        else:
            raise ValueError('Automaton does not have specified state!')

    def add_command(self, state1, input_, state2):      
        """m.add_command(state1, input, state2) Add command"""
        if state1 in self.Q and state2 in self.Q and input_ in self.sigma:
            self.delta[state1][input_].add(state2)
        else:
            raise ValueError("Automaton doesn't have specified state or input!")

    def get_state(self):
        """m.get_state() -> current state"""
        return self._state

    def reset(self):
        """m.reset() set curent state to q"""
        self._state = self.q

    def apply_input(self, input_):
        """m.apply_input(input) change state according to input"""
        self._state = random.choice(list(self.delta[self._state][input_]))

    def check_chain(self, chain_):
        """m.check_chain(chain) -> True if chain matches grammar, else False"""
        self.reset()
        for i in chain_:
            try:
                self.apply_input(i)
            except IndexError, e:
                return False
        return self._state in self.F

    def get_dot_data(self):
        """m.get_dot_data() -> graphviz dot data"""
        
        def sts(state): # state to string
            if type(state) is frozenset:
                if not state: # empty set
                    return 'Ø'
                symbols = list(state)
                symbols.sort()
                return ''.join(symbols)
            return state

        dotdata = ('digraph finite_state_machine {\n'
         + 'rankdir=LR;\n'
         + 'size="8,5"\n'
         + 'node [shape = doublecircle]; ' + sts(self.q) + ' ' 
         + ' '.join((sts(x) for x in self.F)) + '\n'
         + 'node [shape = circle];'
         )
        for state1, inputs in self.delta.items():
            for input_, states in inputs.items():
                for state2 in states:
                    dotdata += '{s1} -> {s2} [ label = "{i}" ];\n'.format(
                                 s1=sts(state1), s2=sts(state2), i=input_)
        return dotdata + '}'

    def get_DFA(self):
        """m.get_to_DFA() -> determenitive automaton"""
        DFA = FSM(set(), set(), frozenset([self.q]), dict(), set())

        for i in range(len(self.Q)):
            for state in combinations(self.Q, i+1):
                DFA.add_state(frozenset(state))
                if 'Z' in state:
                    DFA.add_final_state(frozenset(state))
        DFA.add_state(frozenset())
        for input_ in self.sigma:
            DFA.add_input(input_)

        for dstate in DFA.Q:
            if dstate == frozenset():
                continue
            for input_ in self.sigma:
                dstate2 = set()
                for state in dstate:
                    dstate2.update(self.delta[state][input_])
                DFA.add_command(dstate, input_, frozenset(dstate2))
        # remove unreachable states
        reachable = set([DFA.q])
        search_queue = [DFA.q]
        while search_queue:
            state = search_queue.pop()
            for input_ in DFA.sigma:
                for state2 in DFA.delta[state][input_]:
                    if state2 not in reachable:
                        reachable.add(state2)
                        search_queue.append(state2)
        
        if frozenset() in reachable:
            reachable.remove(frozenset())
        DFA.delta = dict((k, v) for k, v in DFA.delta.items() if k in reachable)
        DFA.Q = DFA.Q.intersection(reachable)
        DFA.F = DFA.F.intersection(reachable)
        # there are still empty state
        for state1 in DFA.delta:
            for input_ in DFA.delta[state1].keys():
                if DFA.delta[state1][input_] == set([frozenset([])]):
                    DFA.delta[state1].pop(input_)

        return DFA
       

# Вариант 1
G1 = G({'0', '1', '#'}, {'S', 'N'}, {  
        'S -> 0S | 1S | 0#N | 1#N',
        'N -> 0 | 1 | 11 | 0N | 1N' 
    }, 'S')
# Вариант 2
G2 = G({'0', '1'}, {'S', 'B', 'C'}, { 
        'S -> 0B | 1S ',
        'B -> 0C | 1B | 01 ',
        'C -> 0B | 1S '
    }, 'S')
# Вариант 3 
G3 = G({'a', 'b', '+'}, {'S', 'A', 'B'}, { 
        'S -> aA | aB | bA ',
        'A -> b+S ',
        'B -> a+S | bB | a '
    }, 'S')
# Вариант 4 
G4 = G({'0', '1', '+'}, {'S', 'M', 'N'}, { 
        'S -> 0S | 1S | 0M | 1M ',
        'M -> +N ',
        'N -> 0 | 1 | 0N | 1N '
    }, 'S')
# Вариант 5 
G5 = G({'x', 'y', '+'}, {'S', 'B', 'C'}, { 
        'S -> xB ',
        'B -> yC | y+S ',
        'C -> x '
    }, 'S')
# Вариант 6 
G6 = G({'m', 'n', '-', '*'}, {'S', 'B', 'C'}, { 
        'S -> -B ',
        'B -> m*C | m | nB ',
        'C -> nB ',
    }, 'S')
# Вариант 7 
G7 = G({'0', '1', '+'}, {'H', 'A', 'B'}, { 
        'H -> 0A | 1A ',
        'A -> 0A | 1A | +B | 0 | 1 ',
        'B -> 0+A | 1A '
    }, 'H')
# Вариант 8 
G8 = G({'a', 'b'}, {'S', 'B', 'C', 'D'}, { 
        'S -> bC ',
        'B -> aB | ab | bD ',
        'C -> aB | aaC     ',
        'D -> bD | b '
    }, 'S')

if __name__ == '__main__':
    M1 = FSM(G7)
    M2 = FSM(G8)
    D1 = M1.get_DFA()
    D2 = M2.get_DFA()
    args = [(M1.get_dot_data(), u"НДКА первой грамматики"),
            (M2.get_dot_data(), u"НДКА второй грамматики"),
            (D1.get_dot_data(), u"ДКА первой грамматики"),
            (D2.get_dot_data(), u"ДКА второй грамматики")]
    threads = [Process(target=show_graph, args=a) for a in args] 
    map(Process.start, threads)
    map(Process.join, threads)
    from pygraphviz import AGraph
    for data, name in args:
        G = AGraph(data)
        G.draw(name + '.png', prog='dot') 

    with open("test.txt") as f:
        chains = f.read().replace(" ", "").split('\n')

    chains1 = []
    chains2 = []
    chains_no_one = []
    for c in chains:
        if D1.check_chain(c):
            chains1.append(c)
        elif D2.check_chain(c):
            chains2.append(c)
        else:
            chains_no_one.append(c)
              
    with open("1.txt", "w") as f:
        f.write('\n'.join(chains1))
    with open("2.txt", "w") as f:
        f.write('\n'.join(chains2))
    with open("!.txt", "w") as f:
        f.write('\n'.join(chains_no_one))