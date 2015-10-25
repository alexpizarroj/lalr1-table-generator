from parsing import *
import samples


def get_grammar():
    return samples.get_sample_1()


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

if __name__ == "__main__":
    main()
