# Generated from spice.g4 by ANTLR 4.6
from antlr4 import *
from io import StringIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\2\13")
        buf.write("_\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\3\2")
        buf.write("\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\4\3\4\7\4(\n\4")
        buf.write("\f\4\16\4+\13\4\3\4\3\4\3\5\5\5\60\n\5\3\5\3\5\3\5\3\5")
        buf.write("\3\5\5\5\67\n\5\5\59\n\5\3\6\6\6<\n\6\r\6\16\6=\3\7\3")
        buf.write("\7\5\7B\n\7\3\7\5\7E\n\7\3\b\6\bH\n\b\r\b\16\bI\3\t\5")
        buf.write("\tM\n\t\3\t\3\t\3\n\6\nR\n\n\r\n\16\nS\3\n\3\n\3\13\3")
        buf.write("\13\5\13Z\n\13\3\f\3\f\3\r\3\r\2\2\16\3\3\5\4\7\5\t\6")
        buf.write("\13\7\r\b\17\t\21\n\23\13\25\2\27\2\31\2\3\2\7\4\2,,=")
        buf.write("=\4\2\f\f\17\17\4\2\13\13\"\"\4\2C\\c|\3\2\62;f\2\3\3")
        buf.write("\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2")
        buf.write("\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2")
        buf.write("\3\33\3\2\2\2\5 \3\2\2\2\7%\3\2\2\2\t8\3\2\2\2\13;\3\2")
        buf.write("\2\2\r?\3\2\2\2\17G\3\2\2\2\21L\3\2\2\2\23Q\3\2\2\2\25")
        buf.write("Y\3\2\2\2\27[\3\2\2\2\31]\3\2\2\2\33\34\7\60\2\2\34\35")
        buf.write("\7g\2\2\35\36\7p\2\2\36\37\7f\2\2\37\4\3\2\2\2 !\7\60")
        buf.write("\2\2!\"\7G\2\2\"#\7P\2\2#$\7F\2\2$\6\3\2\2\2%)\t\2\2\2")
        buf.write("&(\n\3\2\2\'&\3\2\2\2(+\3\2\2\2)\'\3\2\2\2)*\3\2\2\2*")
        buf.write(",\3\2\2\2+)\3\2\2\2,-\b\4\2\2-\b\3\2\2\2.\60\5\13\6\2")
        buf.write("/.\3\2\2\2/\60\3\2\2\2\60\61\3\2\2\2\61\62\7\60\2\2\62")
        buf.write("9\5\13\6\2\63\64\5\13\6\2\64\66\7\60\2\2\65\67\5\13\6")
        buf.write("\2\66\65\3\2\2\2\66\67\3\2\2\2\679\3\2\2\28/\3\2\2\28")
        buf.write("\63\3\2\2\29\n\3\2\2\2:<\5\31\r\2;:\3\2\2\2<=\3\2\2\2")
        buf.write("=;\3\2\2\2=>\3\2\2\2>\f\3\2\2\2?A\5\13\6\2@B\7\60\2\2")
        buf.write("A@\3\2\2\2AB\3\2\2\2BD\3\2\2\2CE\5\17\b\2DC\3\2\2\2DE")
        buf.write("\3\2\2\2E\16\3\2\2\2FH\5\25\13\2GF\3\2\2\2HI\3\2\2\2I")
        buf.write("G\3\2\2\2IJ\3\2\2\2J\20\3\2\2\2KM\7\17\2\2LK\3\2\2\2L")
        buf.write("M\3\2\2\2MN\3\2\2\2NO\7\f\2\2O\22\3\2\2\2PR\t\4\2\2QP")
        buf.write("\3\2\2\2RS\3\2\2\2SQ\3\2\2\2ST\3\2\2\2TU\3\2\2\2UV\b\n")
        buf.write("\2\2V\24\3\2\2\2WZ\5\27\f\2XZ\5\31\r\2YW\3\2\2\2YX\3\2")
        buf.write("\2\2Z\26\3\2\2\2[\\\t\5\2\2\\\30\3\2\2\2]^\t\6\2\2^\32")
        buf.write("\3\2\2\2\16\2)/\668=ADILSY\3\b\2\2")
        return buf.getvalue()


class spiceLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]


    T__0 = 1
    T__1 = 2
    LINECOMMENT = 3
    FLOAT = 4
    INT = 5
    VAL = 6
    COMBS = 7
    NL = 8
    WS = 9

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'.end'", "'.END'" ]

    symbolicNames = [ "<INVALID>",
            "LINECOMMENT", "FLOAT", "INT", "VAL", "COMBS", "NL", "WS" ]

    ruleNames = [ "T__0", "T__1", "LINECOMMENT", "FLOAT", "INT", "VAL", 
                  "COMBS", "NL", "WS", "COMB", "LETTER", "NUMBER" ]

    grammarFileName = "spice.g4"

    def __init__(self, input=None):
        super().__init__(input)
        self.checkVersion("4.6")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


