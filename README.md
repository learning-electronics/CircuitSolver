# CircuitSolver

This repository is the collection of all the modules necessary for the Elecosystem Problem Creation Datapath to work. Inside the `preprocessor` folder, we can find all the 3 main modules in the folders named:
* `parser`: *SPICE* Netlist Parser Module;
* `mna`: Modified Nodal Analysis Module;
* `explainer`: Circuit Explainer Module.

We can also find a folder called `examples` which has multiple SPICE circuits useful for testing all the modules, especially the `parser` module.
The two last files are:
* `database.sql`: *MySQL*-compatible circuit and problem database declaration;
* `datastructure.py`: Datastructure used to store temporarely a circuit while it is being processed;
* `preprocessor.py`: Top-level module that offers a simple interface to the foreign modules (ex: web server calls).

NOTE: This project was developed using Python 3.0, not Python 2.0.


## Top level (`preprocessor.py`)
The interface offered to the `CircuitSolver` caller is the following:

`def handler(circpath,imgpath,questtext,questtype,compname,freq)`

The arguments are:
* `circpath`: Path to the SPICE circuit;
* `imgpath`: Path to the image of the circuit;
* `questtext`: General question text;
* `questtype`: Type of question, either 'V' (Tension) , 'I' (Current), 'P' (Power);
* `compname`: Name of the component that the question is about;
* `freq`: Circuit freq in hertz (freq=0 -> DC);

This function handles all the back-end operations to solve and store a question.


NOTE: It is strongly advised to surround this function with a try..except block.


## Datastructure (`datastructure.py`)

## Database (`database.sql`)


## *SPICE* Parser Module (`parser`)

The *SPICE* parser was implemented using *ANTLR4*. *ANTLR4* is a tool that generates a parser and a lexer for a given grammar for a specified target language (in this case Python3).

### Reference

Not all the *SPICE* specification was implemented: only the subset of useful and needed directives was implemented. These are:
* `V` Voltage Source (Rule: `V<name> <(+) node> <(-) node> <value>`, Example: `VTHR 2 0 20V`);
* `I` Current Source (Rule: `I<name> <(+) node> <(-) node> <value>`, Example: `IBIAS 13 0 2.3mA`);
* `R` Resistor (Rule: `R<name> <(+) node> <(-) node> <value>`, Example: `R2 2 0 2k`);
* `C` Capacitor (Rule: `C<name> <(+) node> <(-) node> <value>`, Example: `C1 2 0 20pF`);
* `L` Inductor (Rule: `L<name> <(+) node> <(-) node> <value>`, Example: `L2 2 0 20mH`);
* `E` Voltage Controlled Voltage Source (Rule: `E<name> <(+) node> <(-) node> <(+) controlling node> <(-) controlling node> <gain>`, Example: `EAMP 1 2 10 11 5`);
* `F` Current Controlled Current Source (Rule: `F<name> <(+) node> <(-) node> <controlling V device name> <gain>`, Example: `FSENSE 1 2 VSENSE 10.0`);
* `G` Voltage Controlled Current Source (Rule: `G<name> <(+) node> <(-) node> <(+) controlling node> <(-) controlling node> <gain>`, Example: `GAMP 1 2 10 11 5`);
* `H` Current Controlled Voltage Source (Rule: `H<name> <(+) node> <(-) node> <controlling V device name> <gain>`, Example: `HSENSE 1 2 VSENSE 10.0`);
* `.END` Command (Used to mark the end of the netlist).
* Although the `<title>` field was also implemented (as the specification requires it to be for a stable grammar) it is simply ignored.

For a in-depth look at the *SPICE* standard, use [this manual](https://www.seas.upenn.edu/~jan/spice/PSpice_ReferenceguideOrCAD.pdf) (this manual was also used as the reference for this module).

### Files


Inside this folder there are a lot of files, but the majority of them are auto-generated files:
* `spiceProcessor.py`: Top-level code that calls all the submodules of the `parser`, giving a clean interface to its caller (the top-level of `CircuitSolver`, `preprocessor.py`);
* `spice.g4`: Grammar specification file. In this file, the *SPICE* grammar is implemented. All possible accepted input combinations are/must be described in this file;
* `spiceListener.py`: Auto-generated file that has the grammar interaction (in this case, a listener) interface;
* `spiceExtractor.py`: Module that reads from the parsed netlist's token tree, using the listener interface (`spiceListener.py`);
* `spiceLexer.py`: Auto-generated Lexer module used for tokenization; 
* `spiceLexer.tokens` and `spice.tokens`: Auto-generated file that identifies all tokens accepted by the Lexer;
* `spiceParser.py`: Auto-generated module that serves as the generic parser for the listener.


## Modified Nodal Analysis Module (`mna`)


## Circuit Explainer Module (`explainer`)


