from ds import *
from grammars import *
# --------------------------------------------------------------------------------------------------

def getLalrOneAutomaton(gr):
  dfa = getLrZeroAutomaton(gr)
  kSet = [lr0Kernels(st) for st in dfa.states]
  return kSet

def getLrZeroAutomaton(gr):
  dfa = LrZeroAutomaton()
  dfa.states = [lr0Closure(gr, [(0, 0)])]
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
        nextItemSet = lr0Goto(gr, itemSet, symbol)
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

def lr0Closure(gr, items):
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

def lr0Goto(gr, items, inp):
  kitems = set()
  
  for x, y in items:
    pname, pbody = gr.productions[x]
    if y < len(pbody) and pbody[y] == inp:
      kitems.add((x, y + 1))
  
  return lr0Closure(gr, kitems)

def lr0Kernels(itemSet):
  return frozenset([(x, y) for x, y in itemSet if y > 0 or x == 0])
  
# --------------------------------------------------------------------------------------------------

def main():
  gr = getExampleGrammar1() # getCoolGrammar()
  
  print('Grammar total productions:', len(gr.productions))
  print('Grammar symbols:', gr.symbols)
  print('Grammar:\n')
  print(str(gr) + '\n')

  for sym in gr.symbols:
    print('First(%s): ' % repr(sym), gr.first(sym))
  print('')
  
  dfa = getLrZeroAutomaton(gr)
  print(len(dfa.states), 'states in the canonical LR0 collection')
  for itemSet in dfa.states:
    print('State', dfa.idFromState[itemSet], 'with %d item(s)' % len(itemSet), '->', repr(itemSet))
  print('Goto Table:', dfa.goto, '\n')
  
  # dfa2 = getLalrOneAutomaton(gr)
  # print(dfa2)
# --------------------------------------------------------------------------------------------------

if __name__ == "__main__":
  main()
  