from parsing import *
import samples


def get_grammar():
    return samples.get_sample_1()


def describe_grammar(gr):
    print('Indexed grammar rules (%d in total):' % len(gr.productions))
    print(gr)
    print()

    print('Grammar non-terminals (%d in total):' % len(gr.nonterms))
    print('\n'.join('\t' + str(s) for s in gr.nonterms))
    print()

    print('Grammar terminals (%d in total):' % len(gr.terminals))
    print('\n'.join('\t' + str(s) for s in gr.terminals))


def main():
    gr = get_grammar()

    describe_grammar(gr)

    print()
    print('Working on parsing table... ')

    table = lalr_one.ParsingTable(gr)
    table_str = table.stringify()
    gr_is_lalr_one = table.is_lalr_one()
    state_status = [table.get_state_status(i) for i in range(table.n_states)]

    print("I'm done.\n")
    print('SUMMARY')

    print('Is the given grammar LALR(1)? %s' % ('Yes' if gr_is_lalr_one else 'No'))

    for state_id in range(table.n_states):
        if state_status[state_id] == lalr_one.STATUS_OK:
            continue
        has_sr_conflict = (state_status[state_id] == lalr_one.STATUS_SR_CONFLICT)
        status_str = ('shift-reduce' if has_sr_conflict else 'reduce-reduce')
        print('State %d has a %s conflict' % (state_id, status_str))

    print()
    print(table_str)


if __name__ == "__main__":
    main()
