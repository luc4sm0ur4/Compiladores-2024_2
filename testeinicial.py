import tkinter as tk
from tkinter import scrolledtext
from antlr4 import *
from PyCLexer import PyCLexer
from PyCParser import PyCParser
from PyCListener import PyCListener
from antlr4.error.ErrorListener import ErrorListener

# Classe para armazenar símbolos com suporte a escopos
class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # Escopo global inicialmente

    def add_symbol(self, name, symbol_type, value=None):
        current_scope = self.scopes[-1]
        if name in current_scope:
            raise ValueError(f"Erro: O símbolo '{name}' já existe no escopo atual.")
        current_scope[name] = {'type': symbol_type, 'value': value}

    def update_symbol(self, name, value):
        for scope in reversed(self.scopes):  # Procura do escopo mais interno ao mais externo
            if name in scope:
                scope[name]['value'] = value
                return
        raise ValueError(f"Erro: O símbolo '{name}' não está definido.")

    def get_symbol(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise ValueError(f"Erro: O símbolo '{name}' não está definido.")

    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise ValueError("Erro: Tentativa de remover o escopo global.")

    def print_table(self):
        result = "Tabela de Símbolos (Escopos):\n"
        for i, scope in enumerate(reversed(self.scopes)):
            result += f"Escopo {len(self.scopes) - i - 1}:\n"
            for name, info in scope.items():
                result += f"  Nome: {name}, Tipo: {info['type']}, Valor: {info['value']}\n"
        return result

# Classe de tratamento de erros personalizada
class CustomErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error_message = f"Erro de Sintaxe na linha {line}, coluna {column}: {msg}"
        raise RuntimeError(error_message)

# Classe para análise semântica
class SemanticAnalyzer:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.errors = []

    def check_assignment(self, var_name, value):
        try:
            var_symbol = self.symbol_table.get_symbol(var_name)
            var_type = var_symbol['type']

            if not self.is_type_compatible(var_type, value):
                self.errors.append(
                    f"Erro semântico: Atribuição incompatível para '{var_name}'. "
                    f"Esperado '{var_type}', mas recebido '{type(value).__name__}'"
                )
        except ValueError as e:
            self.errors.append(str(e))

    def check_declaration(self, var_name, var_type, value=None):
        if value is not None and not self.is_type_compatible(var_type, value):
            self.errors.append(
                f"Erro semântico: Valor inicial incompatível para '{var_name}'. "
                f"Esperado '{var_type}', mas recebido '{type(value).__name__}'"
            )

    def is_type_compatible(self, var_type, value):
        if var_type == "int" and isinstance(value, int):
            return True
        if var_type == "string" and isinstance(value, str):
            return True
        if var_type == "list" and isinstance(value, list):
            return True
        if var_type == "dict" and isinstance(value, dict):
            return True
        return False

# Classe para representar nós da Árvore Sintática Abstrata (AST)
class ASTNode:
    def __init__(self, node_type, children=None, value=None):
        self.node_type = node_type
        self.children = children if children else []
        self.value = value

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return f"{self.node_type}({self.value})"

# Classe que implementa o interpretador da linguagem PyC com melhorias
class PyCInterpreter(PyCListener):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.memory = {}
        self.return_value = None
        self.output = ""
        self.ast_root = ASTNode("program")
        self.semantic_analyzer = SemanticAnalyzer(self.symbol_table)

    def enterDeclaration(self, ctx):
        var_type = ctx.getChild(0).getText() if ctx.getChild(0) else None
        var_name = ctx.ID(0).getText() if ctx.ID(0) else None
        value = self.evaluate_expression(ctx.expr()) if ctx.expr() else None

        if var_type and var_name:
            self.semantic_analyzer.check_declaration(var_name, var_type, value)

            try:
                self.symbol_table.add_symbol(var_name, var_type, value)
                node = ASTNode("declaration", value=f"{var_type} {var_name} = {value}")
                self.ast_root.add_child(node)
                self.output += f"Declaração: {var_type} {var_name} = {value}\n"
            except ValueError as e:
                self.semantic_analyzer.errors.append(str(e))

    def enterAssignment(self, ctx):
        var_name = ctx.ID().getText()
        assign_op = ctx.getChild(1).getText()
        value = self.evaluate_expression(ctx.expr())

        try:
            current_value = self.symbol_table.get_symbol(var_name).get("value", 0)
            if assign_op == "+=":
                value += current_value
            elif assign_op == "-=":
                value -= current_value
            elif assign_op == "*=":
                value *= current_value
            elif assign_op == "/=":
                value //= current_value

            self.semantic_analyzer.check_assignment(var_name, value)

            self.symbol_table.update_symbol(var_name, value)
            node = ASTNode("assignment", value=f"{var_name} {assign_op} {value}")
            self.ast_root.add_child(node)
            self.output += f"Atribuição: {var_name} {assign_op} {value}\n"
        except ValueError as e:
            self.semantic_analyzer.errors.append(str(e))

    def enterBlock(self, ctx):
        self.symbol_table.push_scope()
        self.output += "Entrou em um novo escopo.\n"

    def exitBlock(self, ctx):
        self.symbol_table.pop_scope()
        self.output += "Saiu do escopo atual.\n"

    def evaluate_expression(self, expr_ctx):
        if not expr_ctx:
            return None
        if expr_ctx.NUMBER():
            return int(expr_ctx.NUMBER().getText())
        elif expr_ctx.STRING():
            return expr_ctx.STRING().getText().strip('"')
        elif expr_ctx.ID():
            try:
                symbol = self.symbol_table.get_symbol(expr_ctx.ID().getText())
                return symbol['value']
            except ValueError as e:
                self.semantic_analyzer.errors.append(str(e))
                return None

        left = self.evaluate_expression(expr_ctx.getChild(0))
        right = self.evaluate_expression(expr_ctx.getChild(2))
        operator = expr_ctx.getChild(1).getText()
        return self._evaluate_operator(left, right, operator)

    def _evaluate_operator(self, left, right, operator):
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            return left // right
        elif operator == '%':
            return left % right

# Função para mostrar tokens para depuração
def show_tokens(input_code):
    input_stream = InputStream(input_code)
    lexer = PyCLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    token_stream.fill()
    
    tokens_output = "Tokens:\n"
    for token in token_stream.tokens:
        token_name = lexer.symbolicNames[token.type] if 0 <= token.type < len(lexer.symbolicNames) else "UNKNOWN"
        
        # Ignorar tokens desconhecidos para a saída
        if token_name == "UNKNOWN":
            continue

        tokens_output += f"{token_name} ({token.text})\n"
    
    return tokens_output

# Função para processar código e incluir análise semântica e escopos
def process_code():
    input_code = code_input.get("1.0", tk.END).strip()
    if not input_code:
        code_output.insert(tk.END, "Nenhum código foi inserido.\n")
        return

    try:
        # Exibir tokens para depuração
        tokens_output = show_tokens(input_code)
        code_output.insert(tk.END, tokens_output + "\n")

        input_stream = InputStream(input_code)
        lexer = PyCLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(CustomErrorListener())

        token_stream = CommonTokenStream(lexer)
        parser = PyCParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(CustomErrorListener())

        tree = parser.program()

        interpreter = PyCInterpreter()
        walker = ParseTreeWalker()
        walker.walk(interpreter, tree)

        if interpreter.semantic_analyzer.errors:
            code_output.insert(tk.END, "Erros semânticos encontrados:\n")
            for error in interpreter.semantic_analyzer.errors:
                code_output.insert(tk.END, error + "\n")
        else:
            result = interpreter.output + "\n" + interpreter.symbol_table.print_table()
            code_output.insert(tk.END, result)

    except RuntimeError as e:
        code_output.insert(tk.END, f"Erro ao processar o código: {str(e)}\n")
    except Exception as e:
        code_output.insert(tk.END, f"Erro inesperado: {str(e)}\n")

def limpar_tela():
    code_input.delete("1.0", tk.END)
    code_output.delete("1.0", tk.END)

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Interpretador e Analisador PyC - v4.0")

code_input_label = tk.Label(root, text="Insira o código PyC abaixo:")
code_input_label.pack()
code_input = scrolledtext.ScrolledText(root, width=60, height=10)
code_input.pack()

process_button = tk.Button(root, text="Interpretar e Analisar", command=process_code)
process_button.pack()

limpar_button = tk.Button(root, text="Limpar Telas", command=limpar_tela)
limpar_button.pack()

code_output_label = tk.Label(root, text="Saída:")
code_output_label.pack()
code_output = scrolledtext.ScrolledText(root, width=60, height=10)
code_output.pack()

root.mainloop()
