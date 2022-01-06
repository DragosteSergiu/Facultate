/* A Bison parser, made by GNU Bison 3.0.4.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015 Free Software Foundation, Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

#ifndef YY_YY_Y_TAB_H_INCLUDED
# define YY_YY_Y_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    PROGRAM = 258,
    BEGINN = 259,
    END = 260,
    VAR = 261,
    IDENTIFIER = 262,
    CONSTANT = 263,
    INTEGER = 264,
    CHAR = 265,
    ARRAY = 266,
    WHILE = 267,
    DO = 268,
    READ = 269,
    WRITE = 270,
    IF = 271,
    THEN = 272,
    ELSE = 273,
    OF = 274,
    COLON = 275,
    SEMI_COLON = 276,
    COMA = 277,
    DOT = 278,
    PLUS = 279,
    MINUS = 280,
    MULTIPLY = 281,
    DIVISION = 282,
    LEFT_ROUND_PARENTHESIS = 283,
    RIGHT_ROUND_PARENTHESIS = 284,
    LEFT_SQUARE_PARENTHESIS = 285,
    RIGHT_SQUARE_PARENTHESIS = 286,
    LESS_THAN = 287,
    GREATER_THAN = 288,
    LESS_OR_EQUAL_THAN = 289,
    GREATER_OR_EQUAL_THAN = 290,
    DIFFERENT = 291,
    EQUAL = 292,
    ASSIGNMENT = 293
  };
#endif
/* Tokens.  */
#define PROGRAM 258
#define BEGINN 259
#define END 260
#define VAR 261
#define IDENTIFIER 262
#define CONSTANT 263
#define INTEGER 264
#define CHAR 265
#define ARRAY 266
#define WHILE 267
#define DO 268
#define READ 269
#define WRITE 270
#define IF 271
#define THEN 272
#define ELSE 273
#define OF 274
#define COLON 275
#define SEMI_COLON 276
#define COMA 277
#define DOT 278
#define PLUS 279
#define MINUS 280
#define MULTIPLY 281
#define DIVISION 282
#define LEFT_ROUND_PARENTHESIS 283
#define RIGHT_ROUND_PARENTHESIS 284
#define LEFT_SQUARE_PARENTHESIS 285
#define RIGHT_SQUARE_PARENTHESIS 286
#define LESS_THAN 287
#define GREATER_THAN 288
#define LESS_OR_EQUAL_THAN 289
#define GREATER_OR_EQUAL_THAN 290
#define DIFFERENT 291
#define EQUAL 292
#define ASSIGNMENT 293

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;

int yyparse (void);

#endif /* !YY_YY_Y_TAB_H_INCLUDED  */
