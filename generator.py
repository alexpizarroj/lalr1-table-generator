from grammar import *
from parsing import *

def getSample1():
  nonterms = []
  nonterms += [Nonterm('program', [
    "class_list"
  ])]
  nonterms += [Nonterm('class_list', [
    "class", "class_list class"
  ])]
  nonterms += [Nonterm('class', [
    "CLASS TYPEID '{' opt_feature_list '}' ';'",
    "CLASS TYPEID INHERITS TYPEID '{' opt_feature_list '}' ';'"
  ])]
  nonterms += [Nonterm('feature', [
    "OBJECTID '(' opt_formal_list ')' ':' TYPEID '{' expr '}' ';'",
    "OBJECTID ':' TYPEID ASSIGN expr ';'",
    "OBJECTID ':' TYPEID ';'"
  ])]
  nonterms += [Nonterm('feature_list', [
    "feature", "feature_list feature"
  ])]
  nonterms += [Nonterm('opt_feature_list', [
    "feature_list", ""
  ])]
  nonterms += [Nonterm('formal', [
    "OBJECTID ':' TYPEID"
  ])]
  nonterms += [Nonterm('formal_list', [
    "formal",
    "formal_list ',' formal"
  ])]
  nonterms += [Nonterm('opt_formal_list', [
    "formal_list", ""
  ])]
  nonterms += [Nonterm('expr', [
    "BOOL_CONST", "STR_CONST", "INT_CONST", "OBJECTID", "'(' expr ')'",
    "NOT expr", "expr '=' expr", "expr LE expr", "expr '<' expr", "'~' expr",
    "expr '/' expr", "expr '*' expr", "expr '-' expr", "expr '+' expr", "ISVOID expr",
    "NEW TYPEID", "CASE expr OF branch_list ESAC", "'{' block_expr_list '}'",
    "WHILE expr LOOP expr POOL", "IF expr THEN expr ELSE expr FI",
    "OBJECTID '(' opt_dispatch_expr_list ')'",
    "expr '.' OBJECTID '(' opt_dispatch_expr_list ')'",
    "expr '@' TYPEID '.' OBJECTID '(' opt_dispatch_expr_list ')'",
    "OBJECTID ASSIGN expr", "LET let_expr_tail"
  ])]
  nonterms += [Nonterm('branch', [
    "OBJECTID ':' TYPEID DARROW expr ';'"
  ])]
  nonterms += [Nonterm('branch_list', [
    "branch", "branch_list branch"
  ])]
  nonterms += [Nonterm('block_expr_list', [
    "expr ';'", "block_expr_list expr ';'"
  ])]
  nonterms += [Nonterm('dispatch_expr_list', [
    "expr", "dispatch_expr_list ',' expr"
  ])]
  nonterms += [Nonterm('opt_dispatch_expr_list', [
    "dispatch_expr_list", ""
  ])]
  nonterms += [Nonterm('let_expr_tail', [
    "OBJECTID ':' TYPEID IN expr", "OBJECTID ':' TYPEID ASSIGN expr IN expr",
    "OBJECTID ':' TYPEID ',' let_expr_tail", "OBJECTID ':' TYPEID ASSIGN expr ',' let_expr_tail"
  ])]
  return Grammar(nonterms)

def getSample2():
  nonterms = []  
  nonterms += [Nonterm('N', [
    "V '=' E", "E"
  ])]
  nonterms += [Nonterm('E', [
    "V"
  ])]
  nonterms += [Nonterm('V', [
    "'x'", "'*' E"
  ])]
  return Grammar(nonterms)


def getSample3():
  nonterms = []  
  nonterms += [Nonterm('S', [
    "L '=' R", "R"
  ])]
  nonterms += [Nonterm('L', [
    "'*' R", "ID"
  ])]
  nonterms += [Nonterm('R', [
    "L"
  ])]
  return Grammar(nonterms)

# --------------------------------------------------------------------------------------------------

def main():
  gr = getSample3()
  
  print(gr)
  print('Grammar total productions:', len(gr.productions))
  print('Grammar symbols:', gr.symbols, '\n')
  
  for sym in gr.symbols:
    print('First(%s): ' % repr(sym), gr.first(sym))
  print('')
  
  dfa = LR0.buildAutomaton(gr)
  print(len(dfa.states), 'states in the canonical LR0 collection')
  for itemSet in dfa.states:
    print('State', dfa.idFromState[itemSet], 'with %d item(s)' % len(itemSet), '->', repr(itemSet))
  print('Goto Table:', dfa.goto, '\n')
  
  dfa2 = LALR1.buildAutomaton(gr)
  print(dfa2)

if __name__ == "__main__":
  main()
