class Nonterm:
  def __init__(self, name, productions):
    """Creates an instance of Nonterm to represent a set of grammar productions for a non terminal.
    
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
  
  def __str__(self):
    return self.__toStr(False)
  
  def __toStr(self, oneLinePerProduction = True):
    altProductionIndent = '\n' + ' ' * len(self.name) + '|'
    firstProduction = True
    
    output = self.name + ':'
    for prod in self.productions:
      if not firstProduction:
        output += (altProductionIndent if oneLinePerProduction else ' |')
      
      firstProduction = False
      output += ''.join(' ' + (x.name if isinstance(x, Nonterm) else str(x)) for x in prod)
    
    return output

class Grammar:
  def __init__(self, nonterms, startNonterm = None):
    """TO DO: Add documentation
    """
    if startNonterm is None or startNonterm not in nonterms:
      startNonterm = nonterms[0]
    
    # Non-terminals and their productions
    self.nonterms = [Nonterm('$accept', [[startNonterm.name]])] + nonterms
    # List of terminals of the grammar (the set will be turned into a list later on)
    self.terminals = set()
    # List of symbols of the grammar
    self.symbols = []
    # Enumeration offset for a given NT
    self.nontermOffset = dict()
    # Enumerated NT's productions
    self.productions = []
    
    nontermsDict = {}
    for nt in self.nonterms:
      nontermsDict[nt.name] = nt
    
    # Update the reference of each production + Recognize terminals + Get all the symbols
    self.symbols += sorted([y for x, y in nontermsDict.items()], key=lambda nt: nt.name)
    for nt in self.nonterms:
      for prod in nt.productions:
        for idx in range(len(prod)):
          symbol = prod[idx]
          if isinstance(symbol, str):
            if symbol in nontermsDict:
              prod[idx] = nontermsDict[symbol]
            else:
              self.terminals.add(symbol)
          elif isinstance(symbol, Nonterm):
            if symbol not in self.nonterms:
              raise KeyError('Non-terminal', repr(symbol), ' is not in the grammar')
          else:
            raise TypeError("Unsupported type '%s' inside of production" % (type(symbol).__name__))
    
    self.terminals = sorted(list(self.terminals))
    self.symbols += self.terminals
    
    # List all the productions
    for nt in self.nonterms:
      self.nontermOffset[nt] = len(self.productions)
      for prod in nt.productions:
        self.productions += [(nt.name, prod)]
    
    # Self-explanatory
    self.__buildFirstSets()
    
  def __buildFirstSets(self):
    # Build First Sets iteratively (see Dragon Book, page 221)
    self.__firstSets = {}
    #  Starting Values
    for s in self.symbols:
      if isinstance(s, str):
        self.__firstSets[s] = set([s])
      else:
        self.__firstSets[s] = set()
        if [] in s.productions:
          self.__firstSets[s].add(None)
    # Iterative Updating
    repeat = True
    while repeat:
      repeat = False
      for nt in self.nonterms:
        curfs = self.__firstSets[nt]
        curfsLen = len(curfs)
        
        for prod in nt.productions:
          skippable_symbols = 0
          for sym in prod:
            fs = self.__firstSets[sym]
            curfs.update(fs - set([None]))
            if None in fs:
              skippable_symbols += 1
            else:
              break
          if skippable_symbols == len(prod):
            curfs.add(None)
        
        if len(curfs) > curfsLen:
          repeat = True
  
  def __str__(self):
    output = ''
    addEndl = False
    for nt in self.nonterms:
      output += ('\n' if addEndl else '') + str(nt)
      addEndl = True
    return output
  
  def first(self, x):
    res = set()
    
    if isinstance(x, str):
      res.add(x)
    elif isinstance(x, Nonterm):
      res = self.__firstSets[x]
    else:
      skippable_symbols = 0
      for sym in x:
        fs = self.first(sym)
        res.update(fs - set([None]))
        if None in fs:
          skippable_symbols += 1
        else:
          break
      
      if skippable_symbols == len(x):
        res.add(None)
    
    return res
