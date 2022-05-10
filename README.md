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



                                                    
## Installation guide


This project was designed to run under GNU/Linux. Windows and Mac were *NOT* tested but might be functional. 

First of all, you need Python 3:

* For Debian-based distros: `$ apt-get install python3`;
* For Arch-based distros: `$ pacman -S python3`;
* [For manual installation](https://www.python.org/downloads/).

For the CircuitSolver to run, you need to install the `antlr4`, `numpy` and `MySQLdb` modules:

`$ pip install antlr4-python3-runtime numpy mysqlclient`

NOTE: To avoid packet collision and dependency problems, using virtual environments might be a good practice.


To compile the grammar you also need a copy of *ANTLR4*:

* For Debian-based distros: `$ apt-get install antlr4`;
* For Arch-based distros: `$ pacman -S antlr4`;
* [For manual installation](http://www.antlr.org/).


                                                                                                                                                                            
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


This database is used to store one circuit in volatile memory while it is are still being processed.
The structure is divided in 3 classes:

* class `Circuit`: Contains a list of `Branch` and `Branch` count;
* class `Branch`: Contains a list of two nodes and a `Component`;
* class `Component`: Characterizes a component (contains a name, value, impedance (used only in AC), type and an optional dependent `Component`).

### Methods of `Circuit`

The most important methods (interface methods) of this class are:
* `removeBadBranches(Circuit)`: This function removes typical hacks from the *SPICE* netlist and handles them; 
*  `fixnodes(Circuit)`: This function makes the node number sequential;
*  `updNodeCnt()`: This method updates the node count variable (`nodeCnt`);
*  `calcImpedances(freq)`: This method calculates the impedance off all components within the circuit, given the frequency is greater than zero.


NOTE: For more detailed method documentation, it's recommended to read the pre-function comments in the source code.




## Database (`database.sql`)


This database is used to make exercises, circuits and all the related data persistent.

The cirucit and exercise database schema was made using the *MySQL* dialect, so expect it to run in *MySQL*-compatible DBMSs.
The database is composed by 4 tables and 2 stored procedures:

* Table `CHAPTER`: Stores the main subjects of the exercises. It's composed by an ID and a Name;
* Table `SUBCHAPTER`: Stores the sub topics of incidence of the  exercises. It's Composed by an ID, the parent chapter ID and a Name;
* Table `CIRCUIT`: This table is used to keep track of each electrical circuit used by the system. It points to the syspath of the *SPICE* netlist and to the syspath of the Image/Diagram of the system. It also has an unique ID per circuit, a base resolution for the circuit (MNA related, how to reach the tensions for each component) and the base statement of the circuit (`BaseEnu`);
* Table `EXERCISE`: This table is used to make exercises persistent. It has the following fields:
	* `ID`: Unique exercise identifier;
	* `CircuitID`: Identifier of the circuit used in the exercise;
	* `Type`: Stores the type of exercise. It can be `V` for Tension, `I` for Current or `P` for Power;
	* `CompName`: Name of the component used in the exercise;
	* `CorrectSol`: Correct answer for the exercise.
	* `WrongAns1`, `WrongAns2` and `WrongAns3`: The wrong answers for the exercise;
	* `SpecificRes`: The rest of the resolution, specific to the exercise. This concatenated after the `BaseRes` form the complete resolution for the exercise;
	* `SubChapID`: The identifier of the SubChapter this exercise falls onto;
	* `ChapID`: The identifier of the Chapter this exercise falls onto;
	* This table doesn't need a specific exercise statement field, because the specific exercise statement is generated automatically.
* Stored Procedure `sp_CreateExercise`: This stored procedure creates a new entry on the `EXERCISE` table and returns the `ID` used;
* Stored Procedure `sp_CreateCircuit`: This stored procedure creates a new entry on the `CIRCUIT` table and returns the `ID` used.




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
* Although the `<title>` field was also implemented (as the specification requires it to be for a correct grammar) it is simply ignored.

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


### Compiling the grammar

Running `$ antlr4 -Dlanguage=Python3 spice.g4` inside the `parser` folder will generate new `spiceLexer.py` `spiceLexer.tokens` `spiceListener.py` `spiceParser.py` and `spice.tokens` files.




## Modified Nodal Analysis Module (`mna`)



## Circuit Explainer Module (`explainer`)



## License

## Example Test
Go to 'preprocessor/' directory.
* To get the of the voltage of component `C1`: `python3 mytopcaller.py examples/example2_AC.cir 1 1 question1 test.png V 0 C1 400`.
* To get the resolution of the nodal analysis: `python3 mytopcaller.py examples/example2_AC.cir 1 1 question1 test.png 0 C1 400`.
