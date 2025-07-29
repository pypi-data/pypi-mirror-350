# Generated from logic.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .logicParser import logicParser
else:
    from logicParser import logicParser

# This class defines a complete generic visitor for a parse tree produced by logicParser.

class logicVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by logicParser#function.
    def visitFunction(self, ctx:logicParser.FunctionContext):
        return self.visitChildren(ctx)



del logicParser