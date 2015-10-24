class NonTerminal:
    def __init__(self, name, productions):
        """Represents a set of grammar productions for a non-terminal.

        Keyword arguments:
        name -- the left hand side of the set of nonterms, a.k.a. the name of the non terminal
        productions -- a list with elements which should be either:
          1. a list of objects of type NTerm or type str. The str elements represent grammar symbols.
          2. a str with space-separated words. These words represent grammar symbols (T and NT)
        """
        self.name = name
        self.productions = [(x.split() if isinstance(x, str) else x) for x in productions]

    def __repr__(self):
        return self.name

    def stringify(self, pretty=True):
        title = '%s: ' % self.name

        if pretty:
            separator = '\n%s| ' % (' ' * len(self.name))
        else:
            separator = ' | '

        strprod = lambda prod: ' '.join(str(sym) for sym in prod)

        rules = separator.join(strprod(prod) for prod in self.productions)

        return title + rules


class Grammar:
    def __init__(self, nonterms, start_nonterminal = None):
        # Grammar start symbol
        if start_nonterminal is None or start_nonterminal not in nonterms:
            start_nonterminal = nonterms[0]

        # List of non-terminals
        self.nonterms = [NonTerminal(Grammar.start(), [[start_nonterminal.name]])] + nonterms
        # List of terminals
        self.terminals = []
        # List of symbols (non-terminals + terminals)
        self.symbols = []
        # Enumeration offset for a given NT
        self.nonterm_offset = dict()
        # Enumerated NT's productions
        self.productions = []
        # First sets for every grammar symbol
        self.__first_sets = {}

        # Update the reference of each production and, while at it, recognize terminal symbols
        nonterminal_by_name = {nt.name: nt for nt in self.nonterms}
        self.symbols += sorted([x for x in self.nonterms], key=lambda nt: nt.name)

        for nt in self.nonterms:
            for prod in nt.productions:
                for idx in range(len(prod)):
                    symbol = prod[idx]

                    if isinstance(symbol, str):
                        if symbol in nonterminal_by_name:
                            prod[idx] = nonterminal_by_name[symbol]
                        else:
                            self.terminals.append(symbol)
                    elif isinstance(symbol, NonTerminal):
                        if symbol not in self.nonterms:
                            msg = 'Non-terminal %s is not in the grammar' % repr(symbol)
                            raise KeyError(msg)
                    else:
                        msg = "Unsupported type '%s' inside of production" % type(symbol).__name__
                        raise TypeError(msg)

        self.terminals = sorted(list(set(self.terminals)))
        self.symbols += self.terminals

        # Enumerate grammar productions
        for nt in self.nonterms:
            self.nonterm_offset[nt] = len(self.productions)
            self.productions += [(nt.name, prod) for prod in nt.productions]

        self.__build_first_sets()

    def first_set(self, x):
        result = set()

        if isinstance(x, str):
            result.add(x)
        elif isinstance(x, NonTerminal):
            result = self.__first_sets[x]
        else:
            skippable_symbols = 0
            for sym in x:
                fs = self.first_set(sym)
                result.update(fs - {None})
                if None in fs:
                    skippable_symbols += 1
                else:
                    break

            if skippable_symbols == len(x):
                result.add(None)

        return result

    def __build_first_sets(self):
        #  Starting First sets values
        for s in self.symbols:
            if isinstance(s, str):
                self.__first_sets[s] = {s}
            else:
                self.__first_sets[s] = set()
                if [] in s.productions:
                    self.__first_sets[s].add(None)

        # Update the sets iteratively (see Dragon Book, page 221)
        repeat = True
        while repeat:
            repeat = False
            for nt in self.nonterms:
                curfs = self.__first_sets[nt]
                curfs_len = len(curfs)

                for prod in nt.productions:
                    skippable_symbols = 0
                    for sym in prod:
                        fs = self.__first_sets[sym]
                        curfs.update(fs - {None})
                        if None in fs:
                            skippable_symbols += 1
                        else:
                            break
                    if skippable_symbols == len(prod):
                        curfs.add(None)

                if len(curfs) > curfs_len:
                    repeat = True

        # Freeze the sets
        self.__first_sets = {x: frozenset(y) for x, y in self.__first_sets.items()}

    def stringify(self, indexes=True):
        lines = '\n'.join(nt.stringify() for nt in self.nonterms)
        if indexes:
            lines = '\n'.join('%-6d%s' % (x, y) for x, y in enumerate(lines.split('\n')))
        return lines

    def __str__(self):
        return self.stringify()

    @staticmethod
    def start():
        return '$accept'

    @staticmethod
    def end_of_input():
        return '$end'

    @staticmethod
    def free_symbol():
        return '$#'
