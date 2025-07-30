# Generated from logic.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .logicParser import logicParser
else:
    from logicParser import logicParser

# This class defines a complete listener for a parse tree produced by logicParser.
class logicListener(ParseTreeListener):

    # Enter a parse tree produced by logicParser#function.
    def enterFunction(self, ctx:logicParser.FunctionContext):
        pass

    # Exit a parse tree produced by logicParser#function.
    def exitFunction(self, ctx:logicParser.FunctionContext):
        pass



del logicParser