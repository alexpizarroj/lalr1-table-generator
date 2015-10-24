from grammar import *

class LALR1:
  class LrZeroKernelItem:
    def __init__(self):
      self.propagatesTo = set()
      self.lookaheads = set()
    
    def __repr__(self):
      return '{ propagatesTo: %s, lookaheads: %s }' % (repr(self.propagatesTo), repr(self.lookaheads))
  
  @staticmethod
  def getCanonicalCollection(gr):
    # Algorithm 4.63 (Dragonbook, page 272)
    
    # STEP 1
    # ======
    dfa = LR0.getAutomaton(gr)
    kstates = [LR0.kernels(st) for st in dfa.states]
    
    # STEPS 2, 3
    # ==========
    table = [{item: LALR1.LrZeroKernelItem() for item in kstates[i]} for i in range(len(kstates))]
    table[0][(0, 0)].lookaheads.add(Grammar.endOfInput())
    
    for iState in range(len(kstates)):
      stateSymbols = [x[1] for x, y in dfa.goto.items() if x[0] == iState]
      #print('For state', iState, 'we have symbols', stateSymbols)
      
      for iItem in kstates[iState]:
        J = LALR1.closure(gr, [(iItem, Grammar.freeSymbol())])
        #print('\titem', iItem, 'closure', J)
        
        for sym in stateSymbols:
          jState = dfa.goto[(iState, sym)]
          
          # For each item in J whose . (dot) points to a symbol equal to 'sym'
          # i.e. a production expecting to see 'sym' next
          for ((prodIndex, dot), nextSymbol) in J:
            pname, pbody = gr.productions[prodIndex]
            if dot == len(pbody) or pbody[dot] != sym:
              continue
            
            jItem = (prodIndex, dot + 1)
            #print('\t\titem', jItem, 'state', jState, 'nextSymbol', nextSymbol)
            
            if nextSymbol == Grammar.freeSymbol():
              # Conclude that lookaheads propagate from iItem to jItem in jState
              table[iState][iItem].propagatesTo.add((jState, jItem))
            else:
              # Conclude that lookahead 'nextSymbol' is spontaneous for jItem in jState
              table[jState][jItem].lookaheads.add(nextSymbol)
    
    # STEP 4
    # ======
    repeat = True
    while repeat:
      repeat = False
      # For every item set, kernel item
      for iStateId in range(len(table)):
        for iItem, iCell in table[iStateId].items():
          # For every kernel item iItem's lookaheads propagate to
          for jStateId, jItem in iCell.propagatesTo:
            # Do propagate the lookaheads
            jCell = table[jStateId][jItem]
            jLookaheadsLen = len(jCell.lookaheads)
            jCell.lookaheads.update(iCell.lookaheads)
            # Check if they changed, so we can decide whether to iterate again
            if jLookaheadsLen < len(jCell.lookaheads):
              repeat = True
    
    '''
    # Pretty print the table to debug
    # ===============================
    print('TABLE')
    for i in range(len(table)):
      print('State', i)
      for item, cell in table[i].items():
        print('\tItem', item, '->', str(cell))
    '''
    
    # Build the collection
    # ====================
    result = [set() for i in range(len(table))]
    
    for iStateId in range(len(table)):
      # Add kernel items
      for iItem, iCell in table[iStateId].items():
        for sym in iCell.lookaheads:
          itemSet = (iItem, sym)
          result[iStateId].add(itemSet)
      # Add non-kernel kernel items
      result[iStateId] = LALR1.closure(gr, result[iStateId])
    
    return result
  
  @staticmethod
  def closure(gr, itemSet):
    result = set(itemSet)
    current = itemSet
    
    while len(current) > 0:
      newElements = []
      
      for ((itemProdId, dot), lookahead) in current:
        pname, pbody = gr.productions[itemProdId]
        if dot == len(pbody) or pbody[dot] not in gr.nonterms:
          continue
        
        nt = pbody[dot]
        ntOffset = gr.nontermOffset[nt]
        followingSymbols = pbody[dot+1:] + [lookahead]
        followingTerminals = gr.first(followingSymbols) - set([None])
        
        for idx in range(len(nt.productions)):
          for term in followingTerminals:
            newItemSet = ((ntOffset + idx, 0), term)
            if newItemSet not in result:
              result.add(newItemSet)
              newElements += [newItemSet]
      
      current = newElements
    
    return frozenset(result)

class LR0:
  class Automaton:
    def __init__(self):
      self.states = []
      self.idFromState = dict()
      self.goto = dict()
  
  @staticmethod
  def getAutomaton(gr):
    dfa = LR0.Automaton()
    dfa.states = [LR0.closure(gr, [(0, 0)])]
    nextId = 0
    
    dfa.idFromState[dfa.states[-1]] = nextId
    nextId += 1
    
    seen = set(dfa.states)
    setQueue = dfa.states
    while len(setQueue) > 0:
      newElements = []
      for itemSet in setQueue:
        itemSetId = dfa.idFromState[itemSet]
        
        for symbol in gr.symbols:
          nextItemSet = LR0.goto(gr, itemSet, symbol)
          if len(nextItemSet) == 0:
            continue
          
          if nextItemSet not in seen:
            newElements += [nextItemSet]
            seen.add(nextItemSet)
            
            dfa.states += [nextItemSet]
            dfa.idFromState[dfa.states[-1]] = nextId
            nextId += 1
          
          dfa.goto[(itemSetId, symbol)] = dfa.idFromState[nextItemSet]
      
      setQueue = newElements
    
    return dfa

  @staticmethod
  def closure(gr, itemSet):
    result = set(itemSet)
    itemSetsQueue = itemSet
    
    while len(itemSetsQueue) > 0:
      newElements = []
      
      for itemProdId, dot in itemSetsQueue:
        pname, pbody = gr.productions[itemProdId]
        if dot == len(pbody) or pbody[dot] not in gr.nonterms:
          continue
        
        nt = pbody[dot]
        ntOffset = gr.nontermOffset[nt]
        for idx in range(len(nt.productions)):
          newItemSet = (ntOffset + idx, 0)
          if newItemSet not in result:
            newElements += [newItemSet]
            result.add(newItemSet)
      
      itemSetsQueue = newElements
    
    return frozenset(result)

  @staticmethod
  def goto(gr, items, inp):
    kitems = set()
    
    for x, y in items:
      pname, pbody = gr.productions[x]
      if y < len(pbody) and pbody[y] == inp:
        kitems.add((x, y + 1))
    
    return LR0.closure(gr, kitems)
  
  @staticmethod
  def kernels(itemSet):
    return frozenset([(x, y) for x, y in itemSet if y > 0 or x == 0])
