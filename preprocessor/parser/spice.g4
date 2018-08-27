grammar spice;

//Grammar designed to handle the simpler declarations of the SPICE standard
//The only command implemented is .END
//Passive compoents are allowed and parsed
//Coupled windings (and related components) are NOT accepted by this grammar.
//Dependent fonts are allowed and parsed

netlist: NL* title NL+ (element NL+)* ('.end'|'.END') NL+ EOF; 

title: COMBS+; 

element: name=COMBS nodes (sn=nodes|cd=COMBS)? value=(VAL|FLOAT|INT)?;

nodes: n1=INT n2=INT;


LINECOMMENT:[;*] ~[\r\n]* -> skip; 
FLOAT: INT? '.' INT | INT '.' INT?;
INT: NUMBER+;
VAL: INT'.'?COMBS?;
COMBS: COMB+;
NL:	'\r'?'\n';
WS: [ \t]+ -> skip;
fragment COMB: LETTER|NUMBER;
fragment LETTER: [a-zA-Z];
fragment NUMBER: [0-9];
