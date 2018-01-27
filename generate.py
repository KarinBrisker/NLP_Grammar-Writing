from collections import defaultdict
import random

class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)
        self.keep_der_tree = []
        self.sent = []

    def add_rule(self, lhs, rhs, weight):
        assert(isinstance(lhs, str))
        assert(isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w,l,r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l,r,w)
        return grammar

    def is_terminal(self, symbol): return symbol not in self._rules

    def gen(self, symbol):
        if self.is_terminal(symbol):
            self.keep_der_tree.extend([" ", symbol])
            self.sent.append(symbol)
        else:
            self.keep_der_tree.extend([' ', '(', symbol])
            expansion = self.random_expansion(symbol)
            for s in expansion:
                self.gen(s)
            self.keep_der_tree.extend([")"])

    def random_sent(self):
        self.keep_der_tree = []
        self.sent = []
        self.gen("ROOT")
        sentence = ' '.join(self.sent)
        del self.keep_der_tree[0]
        return sentence

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r,w in self._rules[symbol]:
            p = p - w
            if p < 0: return r
        return r

    def tree_derivative(self):
        # from a list to a sentence
        res = ''.join(self.keep_der_tree)
        return res

if __name__ == '__main__':

    import sys
    t_flag = False
    g_flag=False
    file = open('grammar1.gen', 'w')
    pcfg = PCFG.from_file(sys.argv[1])
    num_inputs = len(sys.argv)
    for i in range(2, num_inputs):
        curr = (sys.argv[i])
        if curr == '-t':
            t_flag = True
        elif curr == '-n':
            n_flag = True
            num, = (sys.argv[i+1])
            i += 1
    for i in range(0, 10):
        file.write(pcfg.random_sent())
        file.write('\n')
        # file.write(pcfg.tree_derivative())
        # file.write('\n')
        print (pcfg.random_sent())
    #
    # for i in range(0, 19):
    #     print pcfg1.random_sent()

    # for i in range(0, 19):
    #     print pcfg2.random_sent()