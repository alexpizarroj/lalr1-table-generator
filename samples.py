from parsing.grammar import *


def get_sample_1():
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


def get_sample_2():
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


def get_sample_3():
    # From Dragonbook, page 263, grammar 4.55 below example 4.54
    nonterms = []
    nonterms += [NonTerminal('S', [
        "C C"
    ])]
    nonterms += [NonTerminal('C', [
        "'c' C", "'d'"
    ])]
    return Grammar(nonterms)


def get_sample_4():
    # From Dragonbook, page 267, example 4.58
    nonterms = []
    nonterms += [NonTerminal('S', [
        "'a' A 'd'", "'b' B 'd'", "'a' B 'e'", "'b' A 'e'"
    ])]
    nonterms += [NonTerminal('A', [
        "'c'"
    ])]
    nonterms += [NonTerminal('B', [
        "'c'"
    ])]
    return Grammar(nonterms)


def get_sample_5():
    nonterms = []

    nonterms += [NonTerminal('p', [
        "tit ss"
    ])]

    nonterms += [NonTerminal('tit', [
        "TITLE TEXT '\n'"
    ])]

    nonterms += [NonTerminal('ss', [
        "s ss", "s"
    ])]

    nonterms += [NonTerminal('s', [
        "NOTE LEFT OF TEXT ':' TEXT '\n'",
        "TEXT '->' TEXT ':' TEXT '\n'",
        "LOOP TEXT '\n' ss END '\n'",
        "LOOP TEXT '\n' END '\n'",
        "ALT TEXT '\n' ss ELSE '\n' ss END '\n'",
        "ALT TEXT '\n' ss END '\n'"
    ])]

    return Grammar(nonterms)
