from parsing.grammar import *


def get_sample_1():
    # From http://web.cs.dal.ca/~sjackson/lalr1.html
    return Grammar([
        NonTerminal('N', [
            "V '=' E", "E"
        ]),
        NonTerminal('E', [
            "V"
        ]),
        NonTerminal('V', [
            "'x'", "'*' E"
        ])
    ])


def get_sample_2():
    # From Dragonbook, page 271, example 4.61
    return Grammar([
        NonTerminal('S', [
            "L '=' R", "R"
        ]),
        NonTerminal('L', [
            "'*' R", "ID"
        ]),
        NonTerminal('R', [
            "L"
        ])
    ])


def get_sample_3():
    # From Dragonbook, page 263, grammar 4.55 below example 4.54
    return Grammar([
        NonTerminal('S', [
            "C C"
        ]),
        NonTerminal('C', [
            "'c' C", "'d'"
        ])
    ])


def get_sample_4():
    # From Dragonbook, page 267, example 4.58
    return Grammar([
        NonTerminal('S', [
            "'a' A 'd'", "'b' B 'd'", "'a' B 'e'", "'b' A 'e'"
        ]),
        NonTerminal('A', [
            "'c'"
        ]),
        NonTerminal('B', [
            "'c'"
        ])
    ])


def get_sample_5():
    # Random grammar with a moderate amount of states
    return Grammar([
        NonTerminal('p', [
            "tit ss"
        ]),
        NonTerminal('tit', [
            "TITLE TEXT '\\n'"
        ]),
        NonTerminal('ss', [
            "s ss", "s"
        ]),
        NonTerminal('s', [
            "NOTE LEFT OF TEXT ':' TEXT '\\n'",
            "TEXT '->' TEXT ':' TEXT '\\n'",
            "LOOP TEXT '\\n' ss END '\\n'",
            "LOOP TEXT '\\n' END '\\n'",
            "ALT TEXT '\\n' ss ELSE '\\n' ss END '\\n'",
            "ALT TEXT '\\n' ss END '\\n'"
        ])
    ])


def get_sample_6():
    # Sample ambiguous grammar for Alex Aiken's COOL programming language
    return Grammar([
        NonTerminal('program', [
            "class_list"
        ]),
        NonTerminal('class_list', [
            "class", "class_list class"
        ]),
        NonTerminal('class', [
            "CLASS TYPEID '{' opt_feature_list '}' ';'",
            "CLASS TYPEID INHERITS TYPEID '{' opt_feature_list '}' ';'"
        ]),
        NonTerminal('feature', [
            "OBJECTID '(' opt_formal_list ')' ':' TYPEID '{' expr '}' ';'",
            "OBJECTID ':' TYPEID ASSIGN expr ';'",
            "OBJECTID ':' TYPEID ';'"
        ]),
        NonTerminal('feature_list', [
            "feature", "feature_list feature"
        ]),
        NonTerminal('opt_feature_list', [
            "feature_list", ""
        ]),
        NonTerminal('formal', [
            "OBJECTID ':' TYPEID"
        ]),
        NonTerminal('formal_list', [
            "formal",
            "formal_list ',' formal"
        ]),
        NonTerminal('opt_formal_list', [
            "formal_list", ""
        ]),
        NonTerminal('expr', [
            "BOOL_CONST", "STR_CONST", "INT_CONST", "OBJECTID", "'(' expr ')'",
            "NOT expr", "expr '=' expr", "expr LE expr", "expr '<' expr", "'~' expr",
            "expr '/' expr", "expr '*' expr", "expr '-' expr", "expr '+' expr", "ISVOID expr",
            "NEW TYPEID", "CASE expr OF branch_list ESAC", "'{' block_expr_list '}'",
            "WHILE expr LOOP expr POOL", "IF expr THEN expr ELSE expr FI",
            "OBJECTID '(' opt_dispatch_expr_list ')'",
            "expr '.' OBJECTID '(' opt_dispatch_expr_list ')'",
            "expr '@' TYPEID '.' OBJECTID '(' opt_dispatch_expr_list ')'",
            "OBJECTID ASSIGN expr", "LET let_expr_tail"
        ]),
        NonTerminal('branch', [
            "OBJECTID ':' TYPEID DARROW expr ';'"
        ]),
        NonTerminal('branch_list', [
            "branch", "branch_list branch"
        ]),
        NonTerminal('block_expr_list', [
            "expr ';'", "block_expr_list expr ';'"
        ]),
        NonTerminal('dispatch_expr_list', [
            "expr", "dispatch_expr_list ',' expr"
        ]),
        NonTerminal('opt_dispatch_expr_list', [
            "dispatch_expr_list", ""
        ]),
        NonTerminal('let_expr_tail', [
            "OBJECTID ':' TYPEID IN expr",
            "OBJECTID ':' TYPEID ASSIGN expr IN expr",
            "OBJECTID ':' TYPEID ',' let_expr_tail",
            "OBJECTID ':' TYPEID ASSIGN expr ',' let_expr_tail"
        ])
    ])


def get_sample_7():
    return Grammar([
        NonTerminal('S', [
            "'a' B S", "'a' 'a'", "'a'"
        ]),
        NonTerminal('B', [
            "'a'"
        ])
    ])


def get_sample_8():
    return Grammar([
        NonTerminal('S', [
            "'b' A 'b'", "'b' B 'a'"
        ]),
        NonTerminal('A', [
            "'a' S", "C B"
        ]),
        NonTerminal('B', [
            "'b'", "B 'c'"
        ]),
        NonTerminal('C', [
            "'c'", "'c' C"
        ])
    ])


def get_sample_9():
    return Grammar([
        NonTerminal('S', [
            "T 'a' T"
        ]),
        NonTerminal('T', [
            "", "'b' 'b' T"
        ])
    ])
