from antlr4 import *
from PyCLexer import PyCLexer
from PyCParser import PyCParser
from PyCListener import PyCListener

# Definição da tabela de símbolos
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
        print("Tabela de Símbolos:")
        for name, info in self.symbols.items():
            print(f"Nome: {name}, Tipo: {info['type']}, Valor: {info['value']}")

# Classe que define o interpretador da linguagem PyC
class PyCInterpreter(PyCListener):
    def __init__(self):
        self.symbol_table = SymbolTable()  # Instancia a tabela de símbolos
        self.memory = {}         # Simula o gerenciamento de memória
        self.return_value = None # Variável de captura de valor de retorno de funções

    # Método para tratar a declaração de variáveis
    def enterDeclaration(self, ctx):
        var_type = ctx.getChild(0).getText()  # Tipo da variável (int ou string)
        var_name = ctx.ID().getText()         # Nome da variável
        value = None
        if ctx.expr():  # Avalia o valor da expressão, se houver
            value = self.evaluate_expression(ctx.expr())
        self.symbol_table.add_symbol(var_name, var_type, value)
        print(f"Declaração: {var_type} {var_name} = {value}")

    # Método para tratar a atribuição de valores a variáveis
    def enterAssignment(self, ctx):
        var_name = ctx.ID().getText()
        value = self.evaluate_expression(ctx.expr())
        self.symbol_table.update_symbol(var_name, value)
        print(f"Atribuição: {var_name} = {value}")

    # Método para tratar a declaração de arrays
    def enterArrayDeclaration(self, ctx):
        array_name = ctx.ID().getText()
        size = self.evaluate_expression(ctx.expr())
        self.symbol_table.add_symbol(array_name, 'array', [0]*size)
        print(f"Array {array_name} criado com tamanho {size}")

    # Método para tratar a avaliação de expressões
    def evaluate_expression(self, expr_ctx):
        if expr_ctx.NUMBER():
            return int(expr_ctx.NUMBER().getText())
        elif expr_ctx.STRING():
            return expr_ctx.STRING().getText().strip('"')
        elif expr_ctx.ID():
            symbol = self.symbol_table.get_symbol(expr_ctx.ID().getText())
            return symbol['value']
        elif expr_ctx.arrayAccess():
            array_name = expr_ctx.arrayAccess().ID().getText()
            index = self.evaluate_expression(expr_ctx.arrayAccess().expr())
            array_symbol = self.symbol_table.get_symbol(array_name)
            return array_symbol['value'][index]
        # Aqui trataremos os operadores (+, -, *, /)
        left = self.evaluate_expression(expr_ctx.getChild(0))
        right = self.evaluate_expression(expr_ctx.getChild(2))
        operator = expr_ctx.getChild(1).getText()
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            return left // right

# Função principal que configura e executa o interpretador
def main():
    input_code = """
    int x = 10;
    string y = "Hello";
    array int numbers[5];
    numbers[0] = 10;
    x = x + 20;
    if x > 15: { x = x - 5; }
    malloc(150);
    free(ptr0);
    """
    
    # Cria um stream de entrada a partir do código
    input_stream = InputStream(input_code)
    
    # Inicializa o lexer para tokenizar o código
    lexer = PyCLexer(input_stream)
    
    # Cria um stream de tokens a partir do lexer
    stream = CommonTokenStream(lexer)
    
    # Inicializa o parser com os tokens para criar a árvore sintática
    parser = PyCParser(stream)
    tree = parser.program()  # Define o ponto inicial do parser

    # Cria uma instância do interpretador
    interpreter = PyCInterpreter()
    
    # Cria um walker para percorrer a árvore de sintaxe
    walker = ParseTreeWalker()
    
    # Executa o interpretador percorrendo a árvore de sintaxe
    walker.walk(interpreter, tree)
    
    # Exibe a tabela de símbolos após a execução
    interpreter.symbol_table.print_table()

# Ponto de entrada do script
if __name__ == '__main__':
    main()
