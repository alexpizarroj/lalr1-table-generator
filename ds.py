class Nonterm:
  def __init__(self, name, productions):
    """Creates an instance of Nonterm to represent a set of grammar productiosn for a non terminal.
    
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
    return self.__toStr()
  
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
    self.nonterms = [Nonterm('$accept', [[startNonterm.name, '$end']])] + nonterms
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
          if not isinstance(symbol, str):
            continue
          
          if symbol in nontermsDict:
            prod[idx] = nontermsDict[symbol]
          else:
            self.terminals.add(symbol)
    
    self.terminals = sorted(list(self.terminals))
    self.symbols += self.terminals
    
    # List all the productions
    for nt in self.nonterms:
      self.nontermOffset[nt.name] = len(self.productions)
      for prod in nt.productions:
        self.productions += [(nt.name, prod)]
  
  def __str__(self):
    output = ''
    addEndl = False
    
    for nt in self.nonterms:
      output += ('\n\n' if addEndl else '') + str(nt)
      addEndl = True
      
    return output

class LrZeroAutomaton:
  def __init__(self):
    """TO DO: Add documentation
    """
    self.states = []
    self.idFromState = dict()
    self.goto = dict()
