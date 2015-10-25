from parsing import *
import samples


def get_grammar():
    return samples.get_sample_6()


def main():
    gr = get_grammar()

    print('Indexed grammar rules (%d in total):' % len(gr.productions))
    print(gr)
    print()

    print('Grammar non-terminals (%d in total):' % len(gr.nonterms))
    print('\n'.join('\t' + str(s) for s in gr.symbols if isinstance(s, grammar.NonTerminal)))
    print()

    print('Grammar terminals (%d in total):' % len(gr.terminals))
    print('\n'.join('\t' + str(s) for s in gr.symbols if isinstance(s, str)))
    print()

    print('Working on parsing table... ')

    parsing_table = lalr_one.ParsingTable(gr)
    table_str = parsing_table.stringify()
    gr_is_lalr_one = parsing_table.is_lalr_one()
    state_status = [parsing_table.get_state_status(i) for i in range(parsing_table.n_states)]

    print("I'm done.\n")

    print('SUMMARY')
    print('Is the given grammar LALR(1)? %s' % ('Yes' if gr_is_lalr_one else 'No'))
    for state_id in range(parsing_table.n_states):
        if state_status[state_id] == lalr_one.STATUS_OK:
            continue
        status_str = ('shift-reduce' if state_status[state_id] == lalr_one.STATUS_SR_CONFLICT
                      else 'reduce-reduce')
        print('State %d has a %s conflict' % (state_id, status_str))
    print()
    print(table_str)


if __name__ == "__main__":
    main()
