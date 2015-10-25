from parsing import *
import samples


def get_grammar():
    return samples.get_sample_5()


def main():
    gr = get_grammar()

    print(gr)
    print('Grammar total productions:', len(gr.productions))
    print('Grammar symbols:', gr.symbols, '\n')

    print('Working on parsing table...')
    parsing_table = lalr_one.ParsingTable(gr)
    print('Finished!\n')

    table = parsing_table.stringify()
    print(table)
    print('')

    gr_is_lalr_one = parsing_table.is_lalr_one()
    state_status = [parsing_table.get_state_status(i) for i in range(parsing_table.n_states)]

    print('SUMMARY')
    print('Is the given grammar LALR(1)? %s' % ('Yes' if gr_is_lalr_one else 'No'))
    for state_id in range(parsing_table.n_states):
        if state_status[state_id] == lalr_one.STATUS_OK:
            continue
        status_str = ('shift-reduce' if state_status[state_id] == lalr_one.STATUS_SR_CONFLICT
                      else 'reduce-reduce')
        print('State %d has a %s conflict' % (state_id, status_str))


if __name__ == "__main__":
    main()
