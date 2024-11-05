// PyC.g4 - Gramática da linguagem PyC atualizada
grammar PyC;

program       : statement+ ;  // Um programa é composto por vários statements

// Definição de statements (comandos)
statement     
    : declaration           // Declaração de variáveis
    | assignment            // Atribuição de valores
    | ifStatement           // Estruturas de controle if/else
    | loop                  // Estruturas de repetição while/for
    | funcDeclaration       // Declaração de funções
    | funcCall              // Chamadas de funções
    | arrayDeclaration      // Declaração de arrays
    | memControl            // Gerenciamento de memória (malloc, free)
    | returnStatement       // Comando de retorno em funções
    | SEMI                  // Permite ";" sozinho para compatibilidade
    ;

// Declaração de variáveis com inicialização opcional e múltiplas variáveis
declaration   
    : ('int' | 'string' | 'void') ID (COMMA ID)* ('=' expr)? SEMI ;

// Atribuição de valores a variáveis
assignment    
    : ID ASSIGN expr SEMI ;

// Estruturas de controle if/else com suporte a blocos vazios
ifStatement   
    : 'if' expr block ('else' block)? ;

// Definição de loops (while e for)
loop          
    : 'while' expr block
    | 'for' ID 'in' LBRACK expr (COMMA expr)* RBRACK block ;

// Bloco de statements
block         
    : LBRACE statement* RBRACE ;

// Declaração de funções com suporte a void (sem retorno)
funcDeclaration 
    : 'func' type ID LPAREN (type ID (COMMA type ID)*)? RPAREN block ;

// Chamadas de funções com argumentos opcionais
funcCall      
    : ID LPAREN (expr (COMMA expr)*)? RPAREN SEMI ;

// Declaração de arrays com tipo e tamanho
arrayDeclaration 
    : 'array' type ID LBRACK expr RBRACK SEMI ;

// Gerenciamento de memória (malloc e free)
memControl    
    : ('malloc' LPAREN expr RPAREN | 'free' LPAREN ID RPAREN) SEMI ;

// Comando de retorno em funções
returnStatement 
    : 'return' expr? SEMI ;

// Expressões matemáticas, comparações, chamadas de funções e ternárias
expr          
    : expr (PLUS | MINUS | MULT | DIV) expr   // Operações aritméticas
    | expr (GT | LT | GE | LE | EQ | NEQ) expr  // Comparações
    | expr ('&&' | '||') expr                 // Operações lógicas
    | '!' expr                                // Negação lógica
    | funcCallExpr                            // Chamadas de funções dentro de expressões
    | arrayAccess                             // Acesso a elementos de arrays
    | LPAREN expr RPAREN                      // Expressões entre parênteses
    | ID                                      // Identificadores (variáveis)
    | NUMBER                                  // Números inteiros
    | STRING                                  // Strings
    | expr '?' expr ':' expr                  // Expressão ternária
    ;

// Chamadas de funções como parte de expressões
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

// Definição de strings
STRING        
    : '"' .*? '"' | '\'' .*? '\'' ;

// Ignorar espaços em branco e quebras de linha
WS            
    : [ \t\r\n]+ -> skip ;

// Comentários de linha
COMMENT       
    : '//' ~[\r\n]* -> skip ;

// Comentários de bloco
COMMENT_BLOCK 
    : '/*' .*? '*/' -> skip ;

// Delimitadores
LPAREN        : '(' ;
RPAREN        : ')' ;
LBRACE        : '{' ;
RBRACE        : '}' ;
LBRACK        : '[' ;
RBRACK        : ']' ;
SEMI          : ';' ;
COMMA         : ',' ;

// Operadores matemáticos e comparações
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
