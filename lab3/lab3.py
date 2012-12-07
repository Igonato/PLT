#!/usr/bin/python
# -*- coding: utf-8 -*-

# Рекурсивный анализатор 
class RecursiveAnalyzer:

    def analyse(self, string):
        self.string = string
        self.index = 0
        try:
            self.S()
        except ValueError:
            return False
        return self.index == len(string)

    def error(self):
        raise ValueError()

    def next_symbol(self):
        self.index += 1

    @property
    def current_symbol(self):
        try:
            return self.string[self.index]
        except IndexError:
            return None

    def S(self):
        raise NotImplemented()

# для первого варианта
class RecursiveAnalyzer1(RecursiveAnalyzer):

    def S(self):
        self.E()

    def E(self):
        self.T()
        self.Es()

    def Es(self):
        if self.current_symbol in ('+', '-'):
            self.next_symbol()
            self.T()
            self.Es()

    def T(self):
        self.F()
        self.Ts()

    def Ts(self):
        if self.current_symbol in ('*', '/'):
            self.next_symbol()
            self.F()
            self.Ts()

    def F(self):
        if self.current_symbol is '(':
            self.next_symbol()
            self.E()
            if self.current_symbol is ')':
                self.next_symbol()
            else:
                self.error()
        else:
            self.I()
            self.Fs()

    def Fs(self):
        if self.current_symbol is '^':
            self.next_symbol()
            self.N()
           

    def I(self):
        if self.current_symbol in ('a', 'b', 'c', 'd'):
            self.next_symbol()
        else:
            self.error()

    def N(self):
        if self.current_symbol in ('2', '3', '4'):
            self.next_symbol()
        else:
            self.error()

# для второго варианта
class RecursiveAnalyzer2(RecursiveAnalyzer):

    def S(self):
        if self.current_symbol is '?':
            self.next_symbol()
            self.E()
            if self.current_symbol is ':':
                self.next_symbol()
                self.S()
                if self.current_symbol is '^':
                    self.next_symbol()
                else:
                    self.error()
            else:
                self.error()
        else:
            self.R()
            if self.current_symbol is '=':
                self.next_symbol()
                self.E()
                if self.current_symbol is '^':
                    self.next_symbol()
                else:
                    self.error()
            else:
                self.error()

    def R(self):
        self.I()
        self.Rs()


    def Rs(self):
        if self.current_symbol is '(':
            self.next_symbol()
            self.G()
            if self.current_symbol is ')':
                self.next_symbol()
            else:
                self.error()
  
    def G(self):
        self.E()
        self.Gs()

    def Gs(self):
        if self.current_symbol is ',':
            self.next_symbol()
            self.G()

    def E(self):
        self.T()
        self.Es()

    def Es(self):
        if self.current_symbol is '+':
            self.next_symbol()            
            self.T()
            self.Es()

    def T(self):
        self.F()
        self.Ts()

    def Ts(self):
        if self.current_symbol is '*':
            self.next_symbol()
            self.F()
            self.Ts()
            
    def F(self):
        if self.current_symbol is '(':
            self.next_symbol()
            self.E()
            if self.current_symbol is ')':
                self.next_symbol()
            else:
                self.error()
        else:
            self.R()

    def I(self):
        if self.current_symbol in ('a', 'b', 'c'):
            self.next_symbol()
        else:
            self.error()

if __name__ == '__main__':
    with open("test.txt") as f:
        chains = f.read().replace(" ", "").split('\n')
    rc1 = RecursiveAnalyzer1()
    rc2 = RecursiveAnalyzer2()

    chains1 = filter(rc1.analyse, chains)
    chains2 = filter(rc2.analyse, chains)
    other = filter(lambda x: not (rc1.analyse(x) or rc2.analyse(x)), chains)
    
    with open("1.txt", "w") as f:
        f.write('\n'.join(chains1))
    with open("2.txt", "w") as f:
        f.write('\n'.join(chains2))
    with open("!.txt", "w") as f:
        f.write('\n'.join(other))


   