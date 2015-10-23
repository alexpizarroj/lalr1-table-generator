from ds import *
from grammars import *
# --------------------------------------------------------------------------------------------------

def getLrZeroAutomaton(gr):
  dfa = LrZeroAutomaton()
  dfa.states = [closure(gr, [(0, 0)])]
  nextId = 0
  dfa.idFromState[dfa.states[-1]] = nextId
  nextId += 1
  
  seen = set(dfa.states)
  setQueue = dfa.states
  while True:
    newElements = []
    for itemSet in setQueue:
      itemSetId = dfa.idFromState[itemSet]
      
      for symbol in gr.symbols:
        nextItemSet = goto(gr, itemSet, symbol)
        if len(nextItemSet) == 0:
          continue
        
        if nextItemSet not in seen:
          newElements += [nextItemSet]
          seen.add(nextItemSet)
          
          dfa.states += [nextItemSet]
          dfa.idFromState[dfa.states[-1]] = nextId
          nextId += 1
        
        dfa.goto[(itemSetId, symbol)] = dfa.idFromState[nextItemSet]
    
    if len(newElements) == 0:
      break
    setQueue = newElements
  
  return dfa

def closure(gr, items):
  result = set(items)
  current = result
  
  while True:
    newElements = []
    
    for i, j in current:
      pname, pbody = gr.productions[i]
      if j < len(pbody) and isinstance(pbody[j], Nonterm):
        nt = pbody[j]
        ntOffset = gr.nontermOffset[nt.name]
        for k in range(len(nt.productions)):
          a, b = (ntOffset + k, 0)
          if not (a, b) in result:
            newElements += [(a, b)]
    
    if len(newElements) == 0:
      break
    
    current = set(newElements)
    result |= current
  
  return frozenset(result)

def goto(gr, items, inp):
  kitems = set()
  
  for x, y in items:
    pname, pbody = gr.productions[x]
    if y < len(pbody) and pbody[y] == inp:
      kitems.add((x, y + 1))
  
  return closure(gr, kitems)
# --------------------------------------------------------------------------------------------------

def main():
  gr = getExampleGrammar1() # getCoolGrammar()
  
  print('Grammar total productions:', len(gr.productions))
  print('Grammar symbols:', gr.symbols)
  print('Grammar:')
  print(str(gr) + '\n')

  dfa = getLrZeroAutomaton(gr)
  
  print(len(dfa.states), 'states in the canonical LR0 collection')
  for items in dfa.states:
    print('state', dfa.idFromState[items], 'with %d item(s)' % (len(items)), '->', repr(items))
  print('Goto Table:', dfa.goto)

if __name__ == "__main__":
  main()