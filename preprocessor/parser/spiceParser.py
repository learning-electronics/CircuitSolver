# Generated from spice.g4 by ANTLR 4.6
# encoding: utf-8
from antlr4 import *
from io import StringIO

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u0430\ud6d1\u8206\uad2d\u4417\uaef1\u8d80\uaadd\3\13")
        buf.write(";\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\3\2\7\2\f\n\2\f\2\16")
        buf.write("\2\17\13\2\3\2\3\2\6\2\23\n\2\r\2\16\2\24\3\2\3\2\6\2")
        buf.write("\31\n\2\r\2\16\2\32\7\2\35\n\2\f\2\16\2 \13\2\3\2\3\2")
        buf.write("\6\2$\n\2\r\2\16\2%\3\2\3\2\3\3\6\3+\n\3\r\3\16\3,\3\4")
        buf.write("\3\4\3\4\3\4\5\4\63\n\4\3\4\5\4\66\n\4\3\5\3\5\3\5\3\5")
        buf.write("\2\2\6\2\4\6\b\2\4\3\2\3\4\3\2\6\b?\2\r\3\2\2\2\4*\3\2")
        buf.write("\2\2\6.\3\2\2\2\b\67\3\2\2\2\n\f\7\n\2\2\13\n\3\2\2\2")
        buf.write("\f\17\3\2\2\2\r\13\3\2\2\2\r\16\3\2\2\2\16\20\3\2\2\2")
        buf.write("\17\r\3\2\2\2\20\22\5\4\3\2\21\23\7\n\2\2\22\21\3\2\2")
        buf.write("\2\23\24\3\2\2\2\24\22\3\2\2\2\24\25\3\2\2\2\25\36\3\2")
        buf.write("\2\2\26\30\5\6\4\2\27\31\7\n\2\2\30\27\3\2\2\2\31\32\3")
        buf.write("\2\2\2\32\30\3\2\2\2\32\33\3\2\2\2\33\35\3\2\2\2\34\26")
        buf.write("\3\2\2\2\35 \3\2\2\2\36\34\3\2\2\2\36\37\3\2\2\2\37!\3")
        buf.write("\2\2\2 \36\3\2\2\2!#\t\2\2\2\"$\7\n\2\2#\"\3\2\2\2$%\3")
        buf.write("\2\2\2%#\3\2\2\2%&\3\2\2\2&\'\3\2\2\2\'(\7\2\2\3(\3\3")
        buf.write("\2\2\2)+\7\t\2\2*)\3\2\2\2+,\3\2\2\2,*\3\2\2\2,-\3\2\2")
        buf.write("\2-\5\3\2\2\2./\7\t\2\2/\62\5\b\5\2\60\63\5\b\5\2\61\63")
        buf.write("\7\t\2\2\62\60\3\2\2\2\62\61\3\2\2\2\62\63\3\2\2\2\63")
        buf.write("\65\3\2\2\2\64\66\t\3\2\2\65\64\3\2\2\2\65\66\3\2\2\2")
        buf.write("\66\7\3\2\2\2\678\7\7\2\289\7\7\2\29\t\3\2\2\2\n\r\24")
        buf.write("\32\36%,\62\65")
        return buf.getvalue()


class spiceParser ( Parser ):

    grammarFileName = "spice.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'.end'", "'.END'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "LINECOMMENT", 
                      "FLOAT", "INT", "VAL", "COMBS", "NL", "WS" ]

    RULE_netlist = 0
    RULE_title = 1
    RULE_element = 2
    RULE_nodes = 3

    ruleNames =  [ "netlist", "title", "element", "nodes" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    LINECOMMENT=3
    FLOAT=4
    INT=5
    VAL=6
    COMBS=7
    NL=8
    WS=9

    def __init__(self, input:TokenStream):
        super().__init__(input)
        self.checkVersion("4.6")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class NetlistContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def title(self):
            return self.getTypedRuleContext(spiceParser.TitleContext,0)


        def EOF(self):
            return self.getToken(spiceParser.EOF, 0)

        def NL(self, i:int=None):
            if i is None:
                return self.getTokens(spiceParser.NL)
            else:
                return self.getToken(spiceParser.NL, i)

        def element(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(spiceParser.ElementContext)
            else:
                return self.getTypedRuleContext(spiceParser.ElementContext,i)


        def getRuleIndex(self):
            return spiceParser.RULE_netlist

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNetlist" ):
                listener.enterNetlist(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNetlist" ):
                listener.exitNetlist(self)




    def netlist(self):

        localctx = spiceParser.NetlistContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_netlist)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 11
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==spiceParser.NL:
                self.state = 8
                self.match(spiceParser.NL)
                self.state = 13
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 14
            self.title()
            self.state = 16 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 15
                self.match(spiceParser.NL)
                self.state = 18 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==spiceParser.NL):
                    break

            self.state = 28
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==spiceParser.COMBS:
                self.state = 20
                self.element()
                self.state = 22 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 21
                    self.match(spiceParser.NL)
                    self.state = 24 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==spiceParser.NL):
                        break

                self.state = 30
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 31
            _la = self._input.LA(1)
            if not(_la==spiceParser.T__0 or _la==spiceParser.T__1):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 33 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 32
                self.match(spiceParser.NL)
                self.state = 35 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==spiceParser.NL):
                    break

            self.state = 37
            self.match(spiceParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class TitleContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COMBS(self, i:int=None):
            if i is None:
                return self.getTokens(spiceParser.COMBS)
            else:
                return self.getToken(spiceParser.COMBS, i)

        def getRuleIndex(self):
            return spiceParser.RULE_title

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTitle" ):
                listener.enterTitle(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTitle" ):
                listener.exitTitle(self)




    def title(self):

        localctx = spiceParser.TitleContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_title)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 40 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 39
                self.match(spiceParser.COMBS)
                self.state = 42 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==spiceParser.COMBS):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ElementContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # Token
            self.sn = None # NodesContext
            self.cd = None # Token
            self.value = None # Token

        def nodes(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(spiceParser.NodesContext)
            else:
                return self.getTypedRuleContext(spiceParser.NodesContext,i)


        def COMBS(self, i:int=None):
            if i is None:
                return self.getTokens(spiceParser.COMBS)
            else:
                return self.getToken(spiceParser.COMBS, i)

        def VAL(self):
            return self.getToken(spiceParser.VAL, 0)

        def FLOAT(self):
            return self.getToken(spiceParser.FLOAT, 0)

        def INT(self):
            return self.getToken(spiceParser.INT, 0)

        def getRuleIndex(self):
            return spiceParser.RULE_element

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElement" ):
                listener.enterElement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElement" ):
                listener.exitElement(self)




    def element(self):

        localctx = spiceParser.ElementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_element)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 44
            localctx.name = self.match(spiceParser.COMBS)
            self.state = 45
            self.nodes()
            self.state = 48
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.state = 46
                localctx.sn = self.nodes()

            elif la_ == 2:
                self.state = 47
                localctx.cd = self.match(spiceParser.COMBS)


            self.state = 51
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << spiceParser.FLOAT) | (1 << spiceParser.INT) | (1 << spiceParser.VAL))) != 0):
                self.state = 50
                localctx.value = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << spiceParser.FLOAT) | (1 << spiceParser.INT) | (1 << spiceParser.VAL))) != 0)):
                    localctx.value = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class NodesContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.n1 = None # Token
            self.n2 = None # Token

        def INT(self, i:int=None):
            if i is None:
                return self.getTokens(spiceParser.INT)
            else:
                return self.getToken(spiceParser.INT, i)

        def getRuleIndex(self):
            return spiceParser.RULE_nodes

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNodes" ):
                listener.enterNodes(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNodes" ):
                listener.exitNodes(self)




    def nodes(self):

        localctx = spiceParser.NodesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_nodes)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            localctx.n1 = self.match(spiceParser.INT)
            self.state = 54
            localctx.n2 = self.match(spiceParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





