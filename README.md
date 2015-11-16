# lalr1-table-generator

### What is this?

A tool that generates a LALR(1) parsing table given a formal grammar as input. It follows the procedures and algorithms discussed in the "Purple Dragon Book".

### How do I use it?

* This tool has been tested and executed with Python 3.4.2. Therefore, you should have Python 3 installed on your machine.
* To build a parsing table, run **generator.py**. This file contains a function called *get_grammar()*, which is responsible of returning a Grammar object from which the generator will do its work. By default, it returns a sample Grammar object from **samples.py**.
* Several samples of grammar definitions can be found in **samples.py**. To define your own, just follow the syntax from the examples.
* After running the generator, two new files will be created:
  * **parsing-table.txt**. It contains a summary of the input grammar and a human-readable LALR(1) parsing table.
  * **parsing-table.csv**. It contains just a LARL(1) parsing table for the input grammar, written in an Excel-style CSV file format. It should be read along with parsing-table.txt.
