# Generated from logic.g4 by ANTLR 4.9.3
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\f")
        buf.write("%\4\2\t\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\5\2\r\n\2\3")
        buf.write("\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2")
        buf.write("\3\2\3\2\3\2\7\2 \n\2\f\2\16\2#\13\2\3\2\2\3\2\3\2\2\2")
        buf.write("\2+\2\f\3\2\2\2\4\5\b\2\1\2\5\6\7\3\2\2\6\7\5\2\2\2\7")
        buf.write("\b\7\4\2\2\b\r\3\2\2\2\t\n\7\b\2\2\n\r\5\2\2\n\13\r\7")
        buf.write("\13\2\2\f\4\3\2\2\2\f\t\3\2\2\2\f\13\3\2\2\2\r!\3\2\2")
        buf.write("\2\16\17\f\t\2\2\17 \5\2\2\n\20\21\f\b\2\2\21\22\7\t\2")
        buf.write("\2\22 \5\2\2\t\23\24\f\7\2\2\24\25\7\n\2\2\25 \5\2\2\b")
        buf.write("\26\27\f\6\2\2\27\30\7\7\2\2\30 \5\2\2\7\31\32\f\5\2\2")
        buf.write("\32\33\7\5\2\2\33 \5\2\2\6\34\35\f\4\2\2\35\36\7\6\2\2")
        buf.write("\36 \5\2\2\5\37\16\3\2\2\2\37\20\3\2\2\2\37\23\3\2\2\2")
        buf.write("\37\26\3\2\2\2\37\31\3\2\2\2\37\34\3\2\2\2 #\3\2\2\2!")
        buf.write("\37\3\2\2\2!\"\3\2\2\2\"\3\3\2\2\2#!\3\2\2\2\5\f\37!")
        return buf.getvalue()


class logicParser ( Parser ):

    grammarFileName = "logic.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'+'", "'|'", "'^'", "'!'", 
                     "'&'", "'*'" ]

    symbolicNames = [ "<INVALID>", "LPAREN", "RPAREN", "OR", "OR2", "XOR", 
                      "NOT", "AND", "AND2", "INPUT", "WHITESPACE" ]

    RULE_function = 0

    ruleNames =  [ "function" ]

    EOF = Token.EOF
    LPAREN=1
    RPAREN=2
    OR=3
    OR2=4
    XOR=5
    NOT=6
    AND=7
    AND2=8
    INPUT=9
    WHITESPACE=10

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.3")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class FunctionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(logicParser.LPAREN, 0)

        def function(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(logicParser.FunctionContext)
            else:
                return self.getTypedRuleContext(logicParser.FunctionContext,i)


        def RPAREN(self):
            return self.getToken(logicParser.RPAREN, 0)

        def NOT(self):
            return self.getToken(logicParser.NOT, 0)

        def INPUT(self):
            return self.getToken(logicParser.INPUT, 0)

        def AND(self):
            return self.getToken(logicParser.AND, 0)

        def AND2(self):
            return self.getToken(logicParser.AND2, 0)

        def XOR(self):
            return self.getToken(logicParser.XOR, 0)

        def OR(self):
            return self.getToken(logicParser.OR, 0)

        def OR2(self):
            return self.getToken(logicParser.OR2, 0)

        def getRuleIndex(self):
            return logicParser.RULE_function

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunction" ):
                listener.enterFunction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunction" ):
                listener.exitFunction(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunction" ):
                return visitor.visitFunction(self)
            else:
                return visitor.visitChildren(self)



    def function(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = logicParser.FunctionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 0
        self.enterRecursionRule(localctx, 0, self.RULE_function, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [logicParser.LPAREN]:
                self.state = 3
                self.match(logicParser.LPAREN)
                self.state = 4
                self.function(0)
                self.state = 5
                self.match(logicParser.RPAREN)
                pass
            elif token in [logicParser.NOT]:
                self.state = 7
                self.match(logicParser.NOT)
                self.state = 8
                self.function(8)
                pass
            elif token in [logicParser.INPUT]:
                self.state = 9
                self.match(logicParser.INPUT)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 31
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 29
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = logicParser.FunctionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_function)
                        self.state = 12
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 13
                        self.function(8)
                        pass

                    elif la_ == 2:
                        localctx = logicParser.FunctionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_function)
                        self.state = 14
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 15
                        self.match(logicParser.AND)
                        self.state = 16
                        self.function(7)
                        pass

                    elif la_ == 3:
                        localctx = logicParser.FunctionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_function)
                        self.state = 17
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 18
                        self.match(logicParser.AND2)
                        self.state = 19
                        self.function(6)
                        pass

                    elif la_ == 4:
                        localctx = logicParser.FunctionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_function)
                        self.state = 20
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 21
                        self.match(logicParser.XOR)
                        self.state = 22
                        self.function(5)
                        pass

                    elif la_ == 5:
                        localctx = logicParser.FunctionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_function)
                        self.state = 23
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 24
                        self.match(logicParser.OR)
                        self.state = 25
                        self.function(4)
                        pass

                    elif la_ == 6:
                        localctx = logicParser.FunctionContext(self, _parentctx, _parentState)
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_function)
                        self.state = 26
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 27
                        self.match(logicParser.OR2)
                        self.state = 28
                        self.function(3)
                        pass

             
                self.state = 33
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[0] = self.function_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def function_sempred(self, localctx:FunctionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 2)
         




