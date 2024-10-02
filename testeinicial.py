import tkinter as tk
from tkinter import scrolledtext
from antlr4 import *
from PyCLexer import PyCLexer
from PyCParser import PyCParser
from PyCListener import PyCListener
from antlr4.error.ErrorListener import ErrorListener

# Classe para armazenar símbolos (variáveis, funções, arrays, etc.), além de exibir erros, caso exista
class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, symbol_type, value=None):
        if name in self.symbols:
            raise ValueError(f"Erro: O símbolo '{name}' já existe.")
        self.symbols[name] = {'type': symbol_type, 'value': value}

    def update_symbol(self, name, value):
        if name not in self.symbols:
            raise ValueError(f"Erro: O símbolo '{name}' não está definido.")
        self.symbols[name]['value'] = value

    def get_symbol(self, name):
        if name not in self.symbols:
            raise ValueError(f"Erro: O símbolo '{name}' não está definido.")
        return self.symbols[name]

    def print_table(self):
        result = "Tabela de Símbolos:\n"
        for name, info in self.symbols.items():
            result += f"Nome: {name}, Tipo: {info['type']}, Valor: {info['value']}\n"
        return result

# Classe de tratamento de erros personalizada
class CustomErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        raise RuntimeError(f"Erro de Sintaxe: {msg} na linha {line}, coluna {column}")

# Classe que implementa o interpretador da linguagem PyC
class PyCInterpreter(PyCListener):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.memory = {}
        self.return_value = None
        self.output = ""  # Faz o armazenamento do resultado do processamento

    def enterDeclaration(self, ctx):
        var_type = ctx.getChild(0).getText()
        var_name = ctx.ID().getText()
        value = self.evaluate_expression(ctx.expr()) if ctx.expr() else None
        self.symbol_table.add_symbol(var_name, var_type, value)
        self.output += f"Declaração: {var_type} {var_name} = {value}\n"

    def enterAssignment(self, ctx):
        var_name = ctx.ID().getText()
        value = self.evaluate_expression(ctx.expr())
        self.symbol_table.update_symbol(var_name, value)
        self.output += f"Atribuição: {var_name} = {value}\n"

    def enterArrayDeclaration(self, ctx):
        array_name = ctx.ID().getText()
        size = self.evaluate_expression(ctx.expr())
        self.symbol_table.add_symbol(array_name, 'array', [0] * size)
        self.output += f"Array {array_name} criado com tamanho {size}\n"

    def enterMemControl(self, ctx):
        command = ctx.getChild(0).getText()
        if command == 'malloc':
            size = self.evaluate_expression(ctx.expr())
            ptr = f"ptr{len(self.memory)}"
            self.memory[ptr] = bytearray(size)
            self.output += f"Memória alocada: {ptr} com {size} bytes\n"
        elif command == 'free':
            ptr = ctx.ID().getText()
            if ptr in self.memory:
                del self.memory[ptr]
                self.output += f"Memória liberada: {ptr}\n"
            else:
                self.output += f"Erro: Ponteiro '{ptr}' não encontrado\n"

    def evaluate_expression(self, expr_ctx):
        if expr_ctx.NUMBER():
            return int(expr_ctx.NUMBER().getText())
        elif expr_ctx.STRING():
            return expr_ctx.STRING().getText().strip('"')
        elif expr_ctx.ID():
            symbol = self.symbol_table.get_symbol(expr_ctx.ID().getText())
            return symbol['value']
        elif expr_ctx.funcCallExpr():
            return self.evaluate_function_call(expr_ctx.funcCallExpr())
        elif expr_ctx.arrayAccess():
            array_name = expr_ctx.arrayAccess().ID().getText()
            index = self.evaluate_expression(expr_ctx.arrayAccess().expr())
            array_symbol = self.symbol_table.get_symbol(array_name)
            return array_symbol['value'][index]

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

    def evaluate_function_call(self, func_call_ctx):
        func_name = func_call_ctx.ID().getText()
        func_symbol = self.symbol_table.get_symbol(func_name)
        func_ctx = func_symbol['value']

        args = []
        if func_call_ctx.expr():
            for expr in func_call_ctx.expr():
                args.append(self.evaluate_expression(expr))

        self.enterBlock(func_ctx.block())

        if self.return_value is not None:
            result = self.return_value
            self.return_value = None  # A função faz o reset do valor de retorno
            return result

        return 0  # Caso a função não retorne nada, retorna o 0 por padrão

# Função para processar o código inserido pelo usuario e retornar lista de tokens
def process_code():
    input_code = code_input.get("1.0", tk.END).strip()

    if not input_code:
        code_output.insert(tk.END, "Nenhum código foi inserido.\n")
        return

    try:
        input_stream = InputStream(input_code)
        lexer = PyCLexer(input_stream)

        # Adicionando tratamento de erros
        lexer.removeErrorListeners()  # Remove os ouvintes de erro padrão
        lexer.addErrorListener(CustomErrorListener())  # Adiciona o ouvinte de erro customizado

        token_stream = CommonTokenStream(lexer)
        token_stream.fill()  # Carrega todos os tokens

        # Exibindo os tokens diretamente
        tokens = token_stream.tokens
        
        token_output = "Lista de tokens:\n"
        for token in tokens:
            # Ignorar tokens invisíveis (como espaços em branco e comentários)
            if token.type == Token.EOF or token.channel == Token.HIDDEN_CHANNEL:
                continue

            # Verifica se o token tem um nome simbólico válido
            if 0 <= token.type < len(lexer.symbolicNames):
                token_name = lexer.symbolicNames[token.type]
            else:
                token_name = "TOKEN_DESCONHECIDO"

            token_output += f"{token_name} ({token.text})\n"

        # Exibindo na interface
        code_output.delete("1.0", tk.END)
        code_output.insert(tk.END, token_output)

    except RuntimeError as e:
        # Captura erros léxicos
        code_output.delete("1.0", tk.END)
        code_output.insert(tk.END, f"Erro ao processar o código: {str(e)}\n")
    except Exception as e:
        code_output.insert(tk.END, f"Erro ao processar o código: {str(e)}\n")

# Função para limpar as caixas de entrada e saída
def limpar_tela():
    code_input.delete("1.0", tk.END)
    code_output.delete("1.0", tk.END)

# Interface gráfica com Tkinter
root = tk.Tk()
root.title("Interpretador da Linguagem PyC")

# Caixa de texto para o usuario inserir o código
code_input_label = tk.Label(root, text="Insira o código PyC abaixo:")
code_input_label.pack()
code_input = scrolledtext.ScrolledText(root, width=60, height=10)
code_input.pack()

# Botão para enviar o código
process_button = tk.Button(root, text="Interpretar código", command=process_code)
process_button.pack()

# Botão para limpar as telas
limpar_button = tk.Button(root, text="Limpar Telas", command=limpar_tela)
limpar_button.pack()

# Caixa de texto para exibir o resultado do código do usuario
code_output_label = tk.Label(root, text="Saída do código:")
code_output_label.pack()
code_output = scrolledtext.ScrolledText(root, width=60, height=10)
code_output.pack()

# Inicia o loop da interface gráfica
root.mainloop()
