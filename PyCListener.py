# Generated from PyC.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PyCParser import PyCParser
else:
    from PyCParser import PyCParser

# This class defines a complete listener for a parse tree produced by PyCParser.
class PyCListener(ParseTreeListener):

    # Enter a parse tree produced by PyCParser#program.
    def enterProgram(self, ctx:PyCParser.ProgramContext):
        pass

    # Exit a parse tree produced by PyCParser#program.
    def exitProgram(self, ctx:PyCParser.ProgramContext):
        pass


    # Enter a parse tree produced by PyCParser#statement.
    def enterStatement(self, ctx:PyCParser.StatementContext):
        pass

    # Exit a parse tree produced by PyCParser#statement.
    def exitStatement(self, ctx:PyCParser.StatementContext):
        pass


    # Enter a parse tree produced by PyCParser#declaration.
    def enterDeclaration(self, ctx:PyCParser.DeclarationContext):
        pass

    # Exit a parse tree produced by PyCParser#declaration.
    def exitDeclaration(self, ctx:PyCParser.DeclarationContext):
        pass


    # Enter a parse tree produced by PyCParser#assignment.
    def enterAssignment(self, ctx:PyCParser.AssignmentContext):
        pass

    # Exit a parse tree produced by PyCParser#assignment.
    def exitAssignment(self, ctx:PyCParser.AssignmentContext):
        pass


    # Enter a parse tree produced by PyCParser#ifStatement.
    def enterIfStatement(self, ctx:PyCParser.IfStatementContext):
        pass

    # Exit a parse tree produced by PyCParser#ifStatement.
    def exitIfStatement(self, ctx:PyCParser.IfStatementContext):
        pass


    # Enter a parse tree produced by PyCParser#loop.
    def enterLoop(self, ctx:PyCParser.LoopContext):
        pass

    # Exit a parse tree produced by PyCParser#loop.
    def exitLoop(self, ctx:PyCParser.LoopContext):
        pass


    # Enter a parse tree produced by PyCParser#block.
    def enterBlock(self, ctx:PyCParser.BlockContext):
        pass

    # Exit a parse tree produced by PyCParser#block.
    def exitBlock(self, ctx:PyCParser.BlockContext):
        pass


    # Enter a parse tree produced by PyCParser#funcDeclaration.
    def enterFuncDeclaration(self, ctx:PyCParser.FuncDeclarationContext):
        pass

    # Exit a parse tree produced by PyCParser#funcDeclaration.
    def exitFuncDeclaration(self, ctx:PyCParser.FuncDeclarationContext):
        pass


    # Enter a parse tree produced by PyCParser#funcCall.
    def enterFuncCall(self, ctx:PyCParser.FuncCallContext):
        pass

    # Exit a parse tree produced by PyCParser#funcCall.
    def exitFuncCall(self, ctx:PyCParser.FuncCallContext):
        pass


    # Enter a parse tree produced by PyCParser#arrayDeclaration.
    def enterArrayDeclaration(self, ctx:PyCParser.ArrayDeclarationContext):
        pass

    # Exit a parse tree produced by PyCParser#arrayDeclaration.
    def exitArrayDeclaration(self, ctx:PyCParser.ArrayDeclarationContext):
        pass


    # Enter a parse tree produced by PyCParser#memControl.
    def enterMemControl(self, ctx:PyCParser.MemControlContext):
        pass

    # Exit a parse tree produced by PyCParser#memControl.
    def exitMemControl(self, ctx:PyCParser.MemControlContext):
        pass


    # Enter a parse tree produced by PyCParser#returnStatement.
    def enterReturnStatement(self, ctx:PyCParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by PyCParser#returnStatement.
    def exitReturnStatement(self, ctx:PyCParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by PyCParser#expr.
    def enterExpr(self, ctx:PyCParser.ExprContext):
        pass

    # Exit a parse tree produced by PyCParser#expr.
    def exitExpr(self, ctx:PyCParser.ExprContext):
        pass


    # Enter a parse tree produced by PyCParser#funcCallExpr.
    def enterFuncCallExpr(self, ctx:PyCParser.FuncCallExprContext):
        pass

    # Exit a parse tree produced by PyCParser#funcCallExpr.
    def exitFuncCallExpr(self, ctx:PyCParser.FuncCallExprContext):
        pass


    # Enter a parse tree produced by PyCParser#arrayAccess.
    def enterArrayAccess(self, ctx:PyCParser.ArrayAccessContext):
        pass

    # Exit a parse tree produced by PyCParser#arrayAccess.
    def exitArrayAccess(self, ctx:PyCParser.ArrayAccessContext):
        pass


    # Enter a parse tree produced by PyCParser#type.
    def enterType(self, ctx:PyCParser.TypeContext):
        pass

    # Exit a parse tree produced by PyCParser#type.
    def exitType(self, ctx:PyCParser.TypeContext):
        pass



del PyCParser