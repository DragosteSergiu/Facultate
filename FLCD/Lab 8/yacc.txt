%{
#include <stdio.h>
#include <stdlib.h>

#define YYDEBUG 1
%}

%token PROGRAM
%token BEGINN
%token END
%token VAR
%token IDENTIFIER
%token CONSTANT
%token INTEGER
%token CHAR
%token ARRAY
%token WHILE
%token DO
%token READ
%token WRITE
%token IF
%token THEN
%token ELSE
%token OF
%token COLON
%token SEMI_COLON
%token COMA
%token DOT
%token PLUS
%token MINUS
%token MULTIPLY
%token DIVISION
%token LEFT_ROUND_PARENTHESIS
%token RIGHT_ROUND_PARENTHESIS
%token LEFT_SQUARE_PARENTHESIS
%token RIGHT_SQUARE_PARENTHESIS
%token LESS_THAN
%token GREATER_THAN
%token LESS_OR_EQUAL_THAN
%token GREATER_OR_EQUAL_THAN
%token DIFFERENT
%token EQUAL
%token ASSIGNMENT

%start program

%%

program : PROGRAM declarationList compoundStatement ;
declarationList : declaration SEMI_COLON declarationList | declaration SEMI_COLON;
declaration :  VAR IDENTIFIER COLON type;
type : primitiveType | arrayDeclaration ;
primitiveType : CHAR | INTEGER ;
arrayDeclaration : ARRAY LEFT_SQUARE_PARENTHESIS CONSTANT RIGHT_SQUARE_PARENTHESIS OF primitiveType ;
compoundStatement : BEGINN statementList END ;
statementList : statement SEMI_COLON statementList | statement SEMI_COLON;
statement : assignemntStatement | ioStatement | whileStatement | ifStatement;
assignemntStatement : IDENTIFIER ASSIGNMENT expression;
expression : term | term PLUS expression | term MINUS expression | term MULTIPLY expression | term DIVISION expression | LEFT_ROUND_PARENTHESIS expression RIGHT_SQUARE_PARENTHESIS ;
term : IDENTIFIER | CONSTANT ;
ioStatement : READ LEFT_ROUND_PARENTHESIS IDENTIFIER RIGHT_SQUARE_PARENTHESIS| WRITE LEFT_ROUND_PARENTHESIS IDENTIFIER RIGHT_SQUARE_PARENTHESIS;
ifStatement : IF condition THEN compoundStatement ELSE compoundStatement | IF condition THEN compoundStatement;
whileStatement : WHILE condition DO compoundStatement;
condition : expression relation expression ;
relation : LESS_THAN | GREATER_THAN | LESS_OR_EQUAL_THAN | GREATER_OR_EQUAL_THAN | DIFFERENT | EQUAL ;

%%

yyerror(char *s)
{
  printf("%s\n", s);
}

extern FILE *yyin;

main(int argc, char **argv)
{
  if (argc > 1) 
    yyin = fopen(argv[1], "r");
  if ( (argc > 2) && ( !strcmp(argv[2], "-d") ) ) 
    yydebug = 1;
  if ( !yyparse() ) 
    fprintf(stderr,"\t Merge !!!\n");
}