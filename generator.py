from parsing import *
from samples import *


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
    gr = get_sample_2()

    print(gr)
    print('Grammar total productions:', len(gr.productions))
    print('Grammar symbols:', gr.symbols, '\n')

    # print_lr_zero_automaton(gr)
    # print()

    # canonical_col = lalr_one.get_canonical_collection(gr)
    # print_lalr_one_canonical_col(canonical_col)
    # print()

    print('Working on parsing table...')
    parsing_table = lalr_one.ParsingTable(gr)
    print('Finished!\n')

    table = parsing_table.stringify()
    print(table)

if __name__ == "__main__":
    main()
