// PyC.g4 - Gramática da linguagem PyC com melhorias significativas
grammar PyC;

program       : statement+ ;  // Programa composto por múltiplos statements

// Definição de statements (comandos)
statement     
    : declaration           // Declaração de variáveis
    | assignment            // Atribuição de valores
    | ifStatement           // Estrutura de controle if/else
    | loop                  // Estruturas de repetição while/for
    | funcDeclaration       // Declaração de funções
    | funcCall              // Chamadas de funções
    | arrayDeclaration      // Declaração de arrays
    | memControl            // Gerenciamento de memória (malloc, free)
    | returnStatement       // Comando de retorno
    | SEMI                  // Permite ";" sozinho para compatibilidade
    ;

// Declaração de variáveis com inicialização e múltiplas variáveis
declaration   
    : type ID (COMMA ID)* ('=' expr)? SEMI ;

// Atribuição de valores, com operadores compostos (ex: +=)
assignment    
    : ID (ASSIGN | ADD_ASSIGN | SUB_ASSIGN | MULT_ASSIGN | DIV_ASSIGN) expr SEMI ;

// Estruturas de controle if/else com blocos opcionais
ifStatement   
    : 'if' LPAREN expr RPAREN block ('else' block)? ;

// Definição de loops while e for
loop          
    : 'while' LPAREN expr RPAREN block
    | 'for' type ID 'in' LBRACK expr (COMMA expr)* RBRACK block ;

// Bloco de statements, incluindo blocos vazios
block         
    : LBRACE statement* RBRACE ;

// Declaração de funções com suporte a tipo void (sem retorno)
funcDeclaration 
    : 'func' type ID LPAREN (type ID (COMMA type ID)*)? RPAREN block ;

// Chamadas de funções com parâmetros opcionais
funcCall      
    : ID LPAREN (expr (COMMA expr)*)? RPAREN SEMI ;

// Declaração de arrays com tipo e tamanho fixo
arrayDeclaration 
    : 'array' type ID LBRACK expr RBRACK SEMI ;

// Gerenciamento de memória: malloc e free
memControl    
    : ('malloc' LPAREN expr RPAREN | 'free' LPAREN ID RPAREN) SEMI ;

// Comando de retorno com valor opcional
returnStatement 
    : 'return' expr? SEMI ;

// Expressões: Operadores aritméticos, lógicos, comparações, ternário
expr          
    : expr (PLUS | MINUS | MULT | DIV | MOD) expr          // Operações aritméticas
    | expr (GT | LT | GE | LE | EQ | NEQ) expr             // Comparações
    | expr ('&&' | '||') expr                              // Operadores lógicos
    | '!' expr                                            // Negação lógica
    | funcCallExpr                                        // Chamadas de função em expressões
    | arrayAccess                                         // Acesso a elementos de array
    | LPAREN expr RPAREN                                  // Parênteses
    | ID                                                  // Identificadores
    | NUMBER                                              // Números inteiros
    | STRING                                              // Strings
    | expr '?' expr ':' expr                              // Operador ternário
    ;

// Chamada de função dentro de expressões
funcCallExpr  
    : ID LPAREN (expr (COMMA expr)*)? RPAREN ;

// Acesso a elementos de arrays
arrayAccess   
    : ID LBRACK expr RBRACK ;

// Definição de tipos suportados
type          
    : 'int' | 'string' | 'void' ;

// Definição de identificadores
ID            
    : [a-zA-Z_][a-zA-Z_0-9]* ;

// Definição de números inteiros
NUMBER        
    : [0-9]+ ;

// Definição de strings (aspas duplas ou simples)
STRING        
    : '"' .*? '"' | '\'' .*? '\'' ;

// Ignorar espaços em branco e quebras de linha
WS            
    : [ \t\r\n]+ -> skip ;

// Comentários de linha e de bloco
COMMENT       
    : '//' ~[\r\n]* -> skip ;
COMMENT_BLOCK 
    : '/*' .*? '*/' -> skip ;

// Palavras-chave reservadas para evitar serem tratadas como ID
IF            : 'if' ;
ELSE          : 'else' ;
FOR           : 'for' ;
WHILE         : 'while' ;
RETURN        : 'return' ;
FUNC          : 'func' ;
ARRAY         : 'array' ;
MALLOC        : 'malloc' ;
FREE          : 'free' ;

// Operadores compostos e de atribuição
ASSIGN        : '=' ;
ADD_ASSIGN    : '+=' ;
SUB_ASSIGN    : '-=' ;
MULT_ASSIGN   : '*=' ;
DIV_ASSIGN    : '/=' ;

// Operadores aritméticos e lógicos
PLUS          : '+' ;
MINUS         : '-' ;
MULT          : '*' ;
DIV           : '/' ;
MOD           : '%' ;
GT            : '>' ;
LT            : '<' ;
GE            : '>=' ;
LE            : '<=' ;
EQ            : '==' ;
NEQ           : '!=' ;

// Delimitadores
LPAREN        : '(' ;
RPAREN        : ')' ;
LBRACE        : '{' ;
RBRACE        : '}' ;
LBRACK        : '[' ;
RBRACK        : ']' ;
SEMI          : ';' ;
COMMA         : ',' ;
