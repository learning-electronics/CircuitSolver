# Generated from spice.g4 by ANTLR 4.7.1
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\13")
        buf.write("b\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7")
        buf.write("\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\3\2")
        buf.write("\3\2\3\2\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\4\3\4\7\4(\n\4")
        buf.write("\f\4\16\4+\13\4\3\4\3\4\3\5\5\5\60\n\5\3\5\3\5\3\5\3\5")
        buf.write("\3\5\5\5\67\n\5\5\59\n\5\3\6\6\6<\n\6\r\6\16\6=\3\7\5")
        buf.write("\7A\n\7\3\7\3\7\5\7E\n\7\3\7\5\7H\n\7\3\b\6\bK\n\b\r\b")
        buf.write("\16\bL\3\t\5\tP\n\t\3\t\3\t\3\n\6\nU\n\n\r\n\16\nV\3\n")
        buf.write("\3\n\3\13\3\13\5\13]\n\13\3\f\3\f\3\r\3\r\2\2\16\3\3\5")
        buf.write("\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\2\27\2\31\2\3\2")
        buf.write("\7\4\2,,==\4\2\f\f\17\17\4\2\13\13\"\"\4\2C\\c|\3\2\62")
        buf.write(";\2j\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2")
        buf.write("\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23")
        buf.write("\3\2\2\2\3\33\3\2\2\2\5 \3\2\2\2\7%\3\2\2\2\t8\3\2\2\2")
        buf.write("\13;\3\2\2\2\r@\3\2\2\2\17J\3\2\2\2\21O\3\2\2\2\23T\3")
        buf.write("\2\2\2\25\\\3\2\2\2\27^\3\2\2\2\31`\3\2\2\2\33\34\7\60")
        buf.write("\2\2\34\35\7g\2\2\35\36\7p\2\2\36\37\7f\2\2\37\4\3\2\2")
        buf.write("\2 !\7\60\2\2!\"\7G\2\2\"#\7P\2\2#$\7F\2\2$\6\3\2\2\2")
        buf.write("%)\t\2\2\2&(\n\3\2\2\'&\3\2\2\2(+\3\2\2\2)\'\3\2\2\2)")
        buf.write("*\3\2\2\2*,\3\2\2\2+)\3\2\2\2,-\b\4\2\2-\b\3\2\2\2.\60")
        buf.write("\5\13\6\2/.\3\2\2\2/\60\3\2\2\2\60\61\3\2\2\2\61\62\7")
        buf.write("\60\2\2\629\5\13\6\2\63\64\5\13\6\2\64\66\7\60\2\2\65")
        buf.write("\67\5\13\6\2\66\65\3\2\2\2\66\67\3\2\2\2\679\3\2\2\28")
        buf.write("/\3\2\2\28\63\3\2\2\29\n\3\2\2\2:<\5\31\r\2;:\3\2\2\2")
        buf.write("<=\3\2\2\2=;\3\2\2\2=>\3\2\2\2>\f\3\2\2\2?A\7/\2\2@?\3")
        buf.write("\2\2\2@A\3\2\2\2AB\3\2\2\2BD\5\13\6\2CE\7\60\2\2DC\3\2")
        buf.write("\2\2DE\3\2\2\2EG\3\2\2\2FH\5\17\b\2GF\3\2\2\2GH\3\2\2")
        buf.write("\2H\16\3\2\2\2IK\5\25\13\2JI\3\2\2\2KL\3\2\2\2LJ\3\2\2")
        buf.write("\2LM\3\2\2\2M\20\3\2\2\2NP\7\17\2\2ON\3\2\2\2OP\3\2\2")
        buf.write("\2PQ\3\2\2\2QR\7\f\2\2R\22\3\2\2\2SU\t\4\2\2TS\3\2\2\2")
        buf.write("UV\3\2\2\2VT\3\2\2\2VW\3\2\2\2WX\3\2\2\2XY\b\n\2\2Y\24")
        buf.write("\3\2\2\2Z]\5\27\f\2[]\5\31\r\2\\Z\3\2\2\2\\[\3\2\2\2]")
        buf.write("\26\3\2\2\2^_\t\5\2\2_\30\3\2\2\2`a\t\6\2\2a\32\3\2\2")
        buf.write("\2\17\2)/\668=@DGLOV\\\3\b\2\2")
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

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'.end'", "'.END'" ]

    symbolicNames = [ "<INVALID>",
            "LINECOMMENT", "FLOAT", "INT", "VAL", "COMBS", "NL", "WS" ]

    ruleNames = [ "T__0", "T__1", "LINECOMMENT", "FLOAT", "INT", "VAL", 
                  "COMBS", "NL", "WS", "COMB", "LETTER", "NUMBER" ]

    grammarFileName = "spice.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


