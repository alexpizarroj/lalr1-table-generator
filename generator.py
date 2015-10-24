from parsing import *


def get_sample_1():
    nonterms = []
    nonterms += [NonTerminal('program', [
        "class_list"
    ])]
    nonterms += [NonTerminal('class_list', [
        "class", "class_list class"
    ])]
    nonterms += [NonTerminal('class', [
        "CLASS TYPEID '{' opt_feature_list '}' ';'",
        "CLASS TYPEID INHERITS TYPEID '{' opt_feature_list '}' ';'"
    ])]
    nonterms += [NonTerminal('feature', [
        "OBJECTID '(' opt_formal_list ')' ':' TYPEID '{' expr '}' ';'",
        "OBJECTID ':' TYPEID ASSIGN expr ';'",
        "OBJECTID ':' TYPEID ';'"
    ])]
    nonterms += [NonTerminal('feature_list', [
        "feature", "feature_list feature"
    ])]
    nonterms += [NonTerminal('opt_feature_list', [
        "feature_list", ""
    ])]
    nonterms += [NonTerminal('formal', [
        "OBJECTID ':' TYPEID"
    ])]
    nonterms += [NonTerminal('formal_list', [
        "formal",
        "formal_list ',' formal"
    ])]
    nonterms += [NonTerminal('opt_formal_list', [
        "formal_list", ""
    ])]
    nonterms += [NonTerminal('expr', [
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
    nonterms += [NonTerminal('branch', [
        "OBJECTID ':' TYPEID DARROW expr ';'"
    ])]
    nonterms += [NonTerminal('branch_list', [
        "branch", "branch_list branch"
    ])]
    nonterms += [NonTerminal('block_expr_list', [
        "expr ';'", "block_expr_list expr ';'"
    ])]
    nonterms += [NonTerminal('dispatch_expr_list', [
        "expr", "dispatch_expr_list ',' expr"
    ])]
    nonterms += [NonTerminal('opt_dispatch_expr_list', [
        "dispatch_expr_list", ""
    ])]
    nonterms += [NonTerminal('let_expr_tail', [
        "OBJECTID ':' TYPEID IN expr", "OBJECTID ':' TYPEID ASSIGN expr IN expr",
        "OBJECTID ':' TYPEID ',' let_expr_tail", "OBJECTID ':' TYPEID ASSIGN expr ',' let_expr_tail"
    ])]
    return Grammar(nonterms)


def get_sample_2():
    # From http://web.cs.dal.ca/~sjackson/lalr1.html
    nonterms = []
    nonterms += [NonTerminal('N', [
        "V '=' E", "E"
    ])]
    nonterms += [NonTerminal('E', [
        "V"
    ])]
    nonterms += [NonTerminal('V', [
        "'x'", "'*' E"
    ])]
    return Grammar(nonterms)


def get_sample_3():
    # From Dragonbook, page 271, example 4.61
    nonterms = []
    nonterms += [NonTerminal('S', [
        "L '=' R", "R"
    ])]
    nonterms += [NonTerminal('L', [
        "'*' R", "ID"
    ])]
    nonterms += [NonTerminal('R', [
        "L"
    ])]
    return Grammar(nonterms)


def get_sample_4():
    # From Dragonbook, page 263, grammar 4.55 below example 4.54
    nonterms = []
    nonterms += [NonTerminal('S', [
        "C C"
    ])]
    nonterms += [NonTerminal('C', [
        "'c' C", "'d'"
    ])]
    return Grammar(nonterms)


def main():
    gr = get_sample_4()

    print(gr)
    print('Grammar total productions:', len(gr.productions))
    print('Grammar symbols:', gr.symbols, '\n')

    for sym in gr.symbols:
        print('First(%s):' % repr(sym), gr.first(sym))
    print('')

    dfa = LrZero.get_automaton(gr)

    print('LR(0) canonical collection with', len(dfa.states), 'states')
    for itemSet in dfa.states:
        print('State', dfa.id_from_state[itemSet], 'with %d item(s)' % len(itemSet), '->', repr(itemSet))
    print('Goto Table:', dfa.goto, '\n')

    col = LalrOne.get_canonical_collection(gr)
    # id_from_state = {col[i]:i for i in range(len(col))}

    print('LARL(1) canonical collection with', len(col), 'states')
    for state_id in range(len(col)):
        print('State', state_id)
        for item, lookahead in col[state_id]:
            print('\tItem', item, 'lookahead', lookahead)


if __name__ == "__main__":
    main()

