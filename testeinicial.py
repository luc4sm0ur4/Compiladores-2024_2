from antlr4 import *
from PyCLexer import PyCLexer
from PyCParser import PyCParser
from PyCListener import PyCListener

# Classe que define o comportamento do interpretador da linguagem PyC
class PyCInterpreter(PyCListener):
    def __init__(self):
        # Dicionários para armazenar variáveis, funções, memória alocada e arrays
        self.variables = {}      # Armazena variáveis e seus valores
        self.functions = {}      # Armazena funções declaradas
        self.memory = {}         # Simula o gerenciamento de memória com alocações e liberações
        self.arrays = {}         # Armazena arrays e elementos
        self.return_value = None # Variável de captura de valor de retorno de funções

    # Método para tratar a declaração de variáveis
    def enterDeclaration(self, ctx):
        # Obtém o tipo da variável (int ou string)
        var_type = ctx.getChild(0).getText()
        # Obtém o nome da variável
        var_name = ctx.ID().getText()
        value = None  # Inicializa o valor da variável como None

        # Se a declaração inclui uma expressão (ex: int x = 5), avalia o valor
        if ctx.expr():
            value = self.evaluate_expression(ctx.expr())

        # Armazena a variável e seu valor no dicionário de variáveis
        self.variables[var_name] = value
        print(f"Declaração: {var_type} {var_name} = {value}")

    # Método para tratar a atribuição de valores a variáveis
    def enterAssignment(self, ctx):
        # Obtém o nome da variável a ser atribuída
        var_name = ctx.ID().getText()
        # Avalia a expressão para obter o valor a ser atribuído
        value = self.evaluate_expression(ctx.expr())
        # Atualiza o valor da variável no dicionário
        self.variables[var_name] = value
        print(f"Atribuição: {var_name} = {value}")

    # Método para tratar a declaração de funções
    def enterFuncDeclaration(self, ctx):
        # Obtém o nome da função declarada
        func_name = ctx.ID(0).getText()
        # Armazena o contexto da função para uso posterior (quando for chamada)
        self.functions[func_name] = ctx
        print(f"Função declarada: {func_name}")

    # Método para tratar chamadas de funções
    def enterFuncCall(self, ctx):
        # Obtém o nome da função a ser chamada
        func_name = ctx.ID().getText()
        # Verifica se a função foi previamente declarada
        if func_name in self.functions:
            func_ctx = self.functions[func_name]  # Obtém o contexto da função
            # Executa o bloco da função
            self.enterBlock(func_ctx.block())
            print(f"Função {func_name} chamada")
            # Imprime o valor de retorno se existir
            if self.return_value is not None:
                print(f"Valor retornado: {self.return_value}")
                self.return_value = None  # Reseta o valor de retorno após o uso

    # Método para tratar a declaração de arrays
    def enterArrayDeclaration(self, ctx):
        # Obtém o nome do array
        array_name = ctx.ID().getText()
        # Avalia a expressão para determinar o tamanho do array
        size = self.evaluate_expression(ctx.expr())
        # Inicializa o array com zeros
        self.arrays[array_name] = [0] * size
        print(f"Array {array_name} criado com tamanho {size}")

    # Método para tratar comandos de alocação e liberação de memória
    def enterMemControl(self, ctx):
        # Verifica se o comando é 'malloc' para alocar memória
        if ctx.getChild(0).getText() == 'malloc':
            # Avalia o tamanho da memória a ser alocada
            size = self.evaluate_expression(ctx.expr())
            # Cria um identificador único para a memória alocada
            ptr = f"ptr{len(self.memory)}"
            # Simula a alocação de memória com um bytearray
            self.memory[ptr] = bytearray(size)
            print(f"Memória alocada: {ptr} com {size} bytes")
        # Verifica se o comando é 'free' para liberar memória
        elif ctx.getChild(0).getText() == 'free':
            ptr = ctx.ID().getText()  # Obtém o identificador da memória a ser liberada
            # Libera a memória se o identificador existir
            if ptr in self.memory:
                del self.memory[ptr]
                print(f"Memória liberada: {ptr}")

    # Método para tratar o comando 'return' dentro de funções
    def enterReturnStatement(self, ctx):
        # Avalia a expressão e armazena o valor na variável de retorno
        self.return_value = self.evaluate_expression(ctx.expr())
        print(f"Comando return executado com valor: {self.return_value}")

    # Método para avaliar expressões matemáticas e de variáveis
    def evaluate_expression(self, expr_ctx):
        # Avalia se a expressão é um número
        if expr_ctx.NUMBER():
            return int(expr_ctx.NUMBER().getText())
        # Avalia se a expressão é uma string
        elif expr_ctx.STRING():
            return expr_ctx.STRING().getText().strip('"')
        # Avalia se a expressão é uma variável
        elif expr_ctx.ID():
            return self.variables.get(expr_ctx.ID().getText(), 0)
        # Avalia se a expressão é uma chamada de função
        elif expr_ctx.funcCallExpr():
            self.enterFuncCall(expr_ctx.funcCallExpr())
            return 0  # Valor padrão para funções que não retornam explicitamente
        # Avalia se a expressão é um acesso a array
        elif expr_ctx.arrayAccess():
            array_name = expr_ctx.arrayAccess().ID().getText()
            index = self.evaluate_expression(expr_ctx.arrayAccess().expr())
            return self.arrays[array_name][index]

        # Avalia expressões aritméticas
        left = self.evaluate_expression(expr_ctx.getChild(0))  # Avalia o operando esquerdo
        right = self.evaluate_expression(expr_ctx.getChild(2)) # Avalia o operando direito
        operator = expr_ctx.getChild(1).getText()  # Obtém o operador

        # Executa a operação aritmética conforme o operador
        if operator == '+':
            return left + right
        elif operator == '-':
            return left - right
        elif operator == '*':
            return left * right
        elif operator == '/':
            return left // right  # Divisão inteira

    # Método para entrar em blocos de código e executar as instruções internas
    def enterBlock(self, ctx):
        print("Entrando em um bloco de código")
        # Executa todas as instruções dentro do bloco
        for statement in ctx.statement():
            self.enterStatement(statement)

# Função principal que configura e executa o interpretador
def main():
    # Código de entrada que será interpretado
    input_code = """
    int x = 10;
    string y = "Hello";
    array int numbers[5];
    func int add(int a, int b) { return a + b; }
    x = x + 20;
    if x > 15: { x = x - 5; }
    numbers[0] = 10;
    malloc(150);
    free(ptr0);
    add(3, 5);
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

# Ponto de entrada do script
if __name__ == '__main__':
    main()
