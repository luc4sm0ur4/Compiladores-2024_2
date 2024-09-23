// PyC.g4 - Gramática da minha linguagem PyC
grammar PyC;

program       : statement+ ;
statement     : declaration           // Declaração de variáveis (int, string)
              | assignment            // Atribuição de valores a variáveis
              | ifStatement           // Estruturas de controle if/else
              | loop                  // Estruturas de repetição while/for
              | funcDeclaration       // Declaração de funções
              | funcCall              // Chamadas de funções
              | arrayDeclaration      // Declaração de arrays
              | memControl            // Comandos de gerenciamento de memória (malloc, free)
              | returnStatement       // Comando de retorno em funções
              ;

// Declaração de variáveis com tipos (int ou string), podendo ou não inicializar com um valor
declaration   : ('int' | 'string') ID ('=' expr)? ';' ;

// Atribuição de um valor a uma variável existente
assignment    : ID '=' expr ';' ;

// Estrutura de controle if/else que avalia uma condição e executa o bloco correspondente
ifStatement   : 'if' expr ':' block ('else:' block)? ;

// Definição das estruturas de repetição, incluindo while e for loops
loop          : 'while' expr ':' block               // Loop while
              | 'for' ID 'in' '[' expr (',' expr)* ']' ':' block ; // Loop for com iteração em uma lista de expressões

// Bloco de código delimitado por chaves, contendo zero ou mais comandos
block         : '{' statement* '}' ;

// Definição de uma função com tipo de retorno, nome, parâmetros e corpo
funcDeclaration : 'func' type ID '(' (type ID (',' type ID)*)? ')' block ;

// Chamada de função com argumentos opcionais
funcCall      : ID '(' (expr (',' expr)*)? ')' ';' ;

// Declaração de um array com tipo e tamanho especificado
arrayDeclaration : 'array' type ID '[' expr ']' ';' ;

// Comandos para alocação (malloc) e liberação (free) de memória
memControl    : ('malloc' '(' expr ')' | 'free' '(' ID ')') ';' ;

// Comando de retorno usado dentro de funções para retornar um valor
returnStatement : 'return' expr ';' ;

// Definição de expressões matemáticas, comparações, chamadas de funções e acessos a arrays
expr          : expr ('*' | '/' | '+' | '-') expr   // Operações aritméticas
              | expr ('<' | '>' | '<=' | '>=' | '==' | '!=') expr  // Comparações
              | funcCallExpr                         // Chamadas de funções dentro de expressões
              | arrayAccess                          // Acesso a elementos de arrays (ajustado)
              | ID                                   // Identificadores (variáveis)
              | NUMBER                               // Números inteiros
              | STRING                               // Strings
              ;

// Chamadas de funções como parte de expressões
funcCallExpr  : ID '(' (expr (',' expr)*)? ')' ;

// Acesso a elementos específicos de um array
arrayAccess   : ID '[' expr ']' ; // Acesso a arrays ajustado para ser tratado corretamente como expressão

// Definição dos tipos suportados: int e string
type          : 'int' | 'string' ;

// Definição dos identificadores (nomes de variáveis, funções, arrays) seguindo as regras de nomes válidos
ID            : [a-zA-Z_][a-zA-Z_0-9]* ;

// Definição de números inteiros
NUMBER        : [0-9]+ ;

// Definição de strings que podem ser delimitadas por aspas duplas ou simples
STRING        : ('"' .*? '"') | ('\'' .*? '\'') ;

// Ignora espaços em branco, tabulações e quebras de linha
WS            : [ \t\r\n]+ -> skip ;
