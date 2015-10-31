# lalr1-table-generator

In order to use the generator, you only need to know a couple of things:

* To build a parsing table, run *generator.py*. This file contains a function called *get_grammar()*, which is responsible of returning a Grammar object from which the generator will do its work. By default, it returns a sample Grammar object.
* Sample grammar definitions can be found in *samples.py*. Defining your own should be easy if you look carefully at the existing ones.
* After running the generator, two new files will appear in the same folder: *parsing-table.txt* and *parsing-table.csv*.
  * parsing-table.txt contains both a summary of the given grammar and a human-readable parsing table.
  * parsing-table.csv contains just the parsing table, written in the Excel-style CSV file format.
