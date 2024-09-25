// PyC.g4 - Gramática da linguagem PyC
grammar PyC;

program       : statement+ ;

// Definição de statements (comandos)
statement     : declaration           // Declaração de variáveis
              | assignment            // Atribuição de valores
              | ifStatement           // Estruturas de controle if/else
              | loop                  // Estruturas de repetição while/for
              | funcDeclaration       // Declaração de funções
              | funcCall              // Chamadas de funções
              | arrayDeclaration      // Declaração de arrays
              | memControl            // Gerenciamento de memória
              | returnStatement       // Comando de retorno em funções
              ;

// Declaração de variáveis com inicialização opcional
declaration   : ('int' | 'string') ID ('=' expr)? ';' ;

// Atribuição de valores a variáveis
assignment    : ID '=' expr ';' ;

// Estruturas de controle if/else
ifStatement   : 'if' expr ':' block ('else:' block)? ;

// Definição de loops (while e for)
loop          : 'while' expr ':' block
              | 'for' ID 'in' '[' expr (',' expr)* ']' ':' block ;

block         : '{' statement* '}' ;

// Definição de funções
funcDeclaration : 'func' type ID '(' (type ID (',' type ID)*)? ')' block ;

// Chamadas de funções com argumentos opcionais
funcCall      : ID '(' (expr (',' expr)*)? ')' ';' ;

// Declaração de arrays com tipo e tamanho
arrayDeclaration : 'array' type ID '[' expr ']' ';' ;

// Gerenciamento de memória (malloc e free)
memControl    : ('malloc' '(' expr ')' | 'free' '(' ID ')') ';' ;

// Comando de retorno em funções
returnStatement : 'return' expr ';' ;

// Expressões matemáticas, comparações, chamadas de funções e acessos a arrays
expr          : expr ('*' | '/' | '+' | '-') expr   // Operações aritméticas
              | expr ('<' | '>' | '<=' | '>=' | '==' | '!=') expr  // Comparações
              | funcCallExpr                         // Chamadas de funções dentro de expressões
              | arrayAccess                          // Acesso a elementos de arrays
              | ID                                   // Identificadores (variáveis)
              | NUMBER                               // Números inteiros
              | STRING                               // Strings
              ;

// Chamadas de funções como parte de expressões
funcCallExpr  : ID '(' (expr (',' expr)*)? ')' ;

// Acesso a elementos de arrays
arrayAccess   : ID '[' expr ']' ;

// Definição de tipos suportados (int e string)
type          : 'int' | 'string' ;

// Definição de identificadores (nomes de variáveis, funções, arrays)
ID            : [a-zA-Z_][a-zA-Z_0-9]* ;

// Definição de números inteiros
NUMBER        : [0-9]+ ;

// Definição de strings (aspas duplas ou simples)
STRING        : ('"' .*? '"') | ('\'' .*? '\'');

// Ignora espaços em branco, tabulações e quebras de linha
WS            : [ \t\r\n]+ -> skip ;

// Comentários de linha (começam com // e vão até o fim da linha)
COMMENT       : '//' ~[\r\n]* -> skip ;

// Comentários de bloco (começam com /* e terminam com */)
COMMENT_BLOCK : '/*' .*? '*/' -> skip ;

// Delimitadores
LPAREN        : '(' ;
RPAREN        : ')' ;
LBRACE        : '{' ;
RBRACE        : '}' ;
LBRACK        : '[' ;
RBRACK        : ']' ;
SEMI          : ';' ;
COMMA         : ',' ;

// Operadores matemáticos e de comparação
PLUS          : '+' ;
MINUS         : '-' ;
MULT          : '*' ;
DIV           : '/' ;
GT            : '>' ;
LT            : '<' ;
GE            : '>=' ;
LE            : '<=' ;
EQ            : '==' ;
NEQ           : '!=' ;
ASSIGN        : '=' ;
