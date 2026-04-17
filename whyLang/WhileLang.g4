grammar WhileLang;

program: statement+ EOF;

statement
    : declaration
    | assignment
    | whileStatement
    | ifStatement
    | breakStatement
    | continueStatement
    ;

declaration: (INT | STRING_T) ID ASSIGN expr SEMI;

assignment: ID ASSIGN expr SEMI;

whileStatement: WHILE LPAREN condition RPAREN LBRACE statement* RBRACE;

ifStatement: IF LPAREN condition RPAREN LBRACE statement* RBRACE (ELSE LBRACE statement* RBRACE)?;

breakStatement: BREAK SEMI;

continueStatement: CONTINUE SEMI;

condition
    : expr                                   # exprCondition
    | expr (GT | LT | EQ | NE) expr          # comparisonCondition
    ;

expr
    : ID                                       # idExpr
    | NUMBER                                   # numberExpr
    | STRING                                   # stringExpr
    | expr (LT | GT | EQ | NE) expr            # comparisonExpr
    | expr (PLUS | MINUS | MULT | DIV) expr    # arithmeticExpr
    | LPAREN expr RPAREN                       # parenExpr
    ;

// TOKENS
INT: 'int';
STRING_T: 'string';

WHILE: 'while';
IF: 'if';
ELSE: 'else';
BREAK: 'break';
CONTINUE: 'continue';

LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
SEMI: ';';
ASSIGN: '=';

GT: '>';
LT: '<';
EQ: '==';
NE: '!=';

PLUS: '+';
MINUS: '-';
MULT: '*';
DIV: '/';

ID: [a-zA-Z_][a-zA-Z_0-9]*;
NUMBER: [0-9]+;
STRING: '"' .*? '"';

WS: [ \t\r\n]+ -> skip;