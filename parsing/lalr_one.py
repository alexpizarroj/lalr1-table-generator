import parsing.lr_zero as lr_zero


class LrZeroItemTableEntry:
    def __init__(self):
        self.propagates_to = set()
        self.lookaheads = set()

    def __repr__(self):
        pattern = '{ propagatesTo: %s, lookaheads: %s }'
        return pattern % (repr(self.propagates_to), repr(self.lookaheads))


def get_canonical_collection(gr):
    # Algorithm 4.63 (Dragonbook, page 272)

    # STEP 1
    # ======
    dfa = lr_zero.get_automaton(gr)
    kstates = [lr_zero.kernels(st) for st in dfa.states]
    n_states = len(kstates)

    # STEPS 2, 3
    # ==========
    table = [{item: LrZeroItemTableEntry() for item in kstates[i]} for i in range(n_states)]
    table[0][(0, 0)].lookaheads.add(gr.end_of_input())

    for i_state_id in range(n_states):
        state_symbols = [x[1] for x, y in dfa.goto.items() if x[0] == i_state_id]

        for i_item in kstates[i_state_id]:
            closure_set = closure(gr, [(i_item, gr.free_symbol())])

            for sym in state_symbols:
                j_state_id = dfa.goto[(i_state_id, sym)]

                # For each item in closure_set whose . (dot) points to a symbol equal to 'sym'
                # i.e. a production expecting to see 'sym' next
                for ((prod_index, dot), next_symbol) in closure_set:
                    pname, pbody = gr.productions[prod_index]
                    if dot == len(pbody) or pbody[dot] != sym:
                        continue

                    j_item = (prod_index, dot + 1)
                    if next_symbol == gr.free_symbol():
                        table[i_state_id][i_item].propagates_to.add((j_state_id, j_item))
                    else:
                        table[j_state_id][j_item].lookaheads.add(next_symbol)

    # STEP 4
    # ======
    repeat = True
    while repeat:
        repeat = False
        # For every item set, kernel item
        for i_state_id in range(len(table)):
            for i_item, i_cell in table[i_state_id].items():
                # For every kernel item i_item's lookaheads propagate to
                for j_state_id, j_item in i_cell.propagates_to:
                    # Do propagate the lookaheads
                    j_cell = table[j_state_id][j_item]
                    j_cell_lookaheads_len = len(j_cell.lookaheads)
                    j_cell.lookaheads.update(i_cell.lookaheads)
                    # Check if they changed, so we can decide whether to iterate again
                    if j_cell_lookaheads_len < len(j_cell.lookaheads):
                        repeat = True

    # Build the collection
    # ====================
    result = [set() for i in range(n_states)]
    for i_state_id in range(n_states):
        # Add kernel items
        for i_item, i_cell in table[i_state_id].items():
            for sym in i_cell.lookaheads:
                item_set = (i_item, sym)
                result[i_state_id].add(item_set)
        # Add non-kernel kernel items
        result[i_state_id] = closure(gr, result[i_state_id])

    return result


def closure(gr, item_set):
    result = set(item_set)
    current = item_set

    while len(current) > 0:
        new_elements = []

        for ((item_prod_id, dot), lookahead) in current:
            pname, pbody = gr.productions[item_prod_id]
            if dot == len(pbody) or pbody[dot] not in gr.nonterms:
                continue

            nt = pbody[dot]
            nt_offset = gr.nonterm_offset[nt]
            following_symbols = pbody[dot+1:] + [lookahead]
            following_terminals = gr.first_set(following_symbols) - {None}

            for idx in range(len(nt.productions)):
                for term in following_terminals:
                    new_item_set = ((nt_offset + idx, 0), term)
                    if new_item_set not in result:
                        result.add(new_item_set)
                        new_elements += [new_item_set]

        current = new_elements

    return frozenset(result)


def goto(gr, item_set, inp):
    result_set = set()
    for (item, lookahead) in item_set:
        prod_id, dot = item
        pname, pbody = gr.productions[prod_id]
        if dot == len(pbody) or pbody[dot] != inp:
            continue

        new_item = ((prod_id, dot + 1), lookahead)
        result_set.add(new_item)

    result_set = closure(gr, result_set)
    return result_set
