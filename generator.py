from grammar import *
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


def print_lr_zero_automaton(gr):
    dfa = lr_zero.get_automaton(gr)
    print('LR(0) canonical collection with %d states' % len(dfa.states))
    for item_set in dfa.states:
        print('State %s with %d item(s) -> %s' %
              (dfa.id_from_state[item_set], len(item_set), repr(item_set)))
    print('Goto Table:', dfa.goto)


def print_lalr_one_canonical_col(canonical_col):
    print('LARL(1) canonical collection with %d states' % len(canonical_col))
    for state_id in range(len(canonical_col)):
        print('Item Set #%d' % state_id)
        # for item, lookahead in canonical_col[state_id]:
        #     print('\tItem', item, 'lookahead', lookahead)
        print(canonical_col[state_id])


def main():
    gr = get_sample_3()

    print(gr)
    print('Grammar total productions:', len(gr.productions))
    print('Grammar symbols:', gr.symbols, '\n')

    # print_lr_zero_automaton(gr)
    # print()

    # canonical_col = lalr_one.get_canonical_collection(gr)
    # print_lalr_one_canonical_col(canonical_col)
    # print()

    parsing_table = lalr_one.ParsingTable(gr)
    print(parsing_table.stringify())

if __name__ == "__main__":
    main()

