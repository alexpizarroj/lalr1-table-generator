from grammar import *

class LALR1:
  @staticmethod
  def buildAutomaton(gr):
    dfa = LR0.buildAutomaton(gr)
    kSet = [LR0.kernels(st) for st in dfa.states]
    
    k0 = [((0, 0), '#')]
    i0 = LALR1.closure(gr, k0)
    
    return i0
  
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
      """TO DO: Add documentation
      """
      self.states = []
      self.idFromState = dict()
      self.goto = dict()
  
  @staticmethod
  def buildAutomaton(gr):
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
