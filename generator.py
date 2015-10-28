from parsing import *
import samples


def get_grammar():
    return samples.get_sample_6()


def describe_grammar(gr):
    print('Indexed grammar rules (%d in total):' % len(gr.productions))
    print(gr)
    print()

    print('Grammar non-terminals (%d in total):' % len(gr.nonterms))
    print('\n'.join('\t' + str(s) for s in gr.nonterms))
    print()

    print('Grammar terminals (%d in total):' % len(gr.terminals))
    print('\n'.join('\t' + str(s) for s in gr.terminals))


def describe_parsing_table(table):
    print('SUMMARY')
    print('Is the given grammar LALR(1)? %s' % ('Yes' if table.is_lalr_one() else 'No'))

    conflict_status = table.get_conflict_status()
    for state_id in range(table.n_states):
        if conflict_status[state_id] == lalr_one.STATUS_OK:
            continue

        has_sr_conflict = (conflict_status[state_id] == lalr_one.STATUS_SR_CONFLICT)
        status_str = ('shift-reduce' if has_sr_conflict else 'reduce-reduce')
        print('State %d has a %s conflict' % (state_id, status_str))

    print()
    print(table.stringify())


def main():
    gr = get_grammar()

    describe_grammar(gr)

    print()
    print('Working on parsing table... ')
    table = lalr_one.ParsingTable(gr)
    print("I'm done.\n")

    describe_parsing_table(table)


if __name__ == "__main__":
    main()
