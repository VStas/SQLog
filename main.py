#!/usr/bin/env python
# -*- coding: utf-8 -*-

# test
# ( ) <-   _ AND NOT +  - * / =  > <  <=  >=  !=  var Pred   954 ,  'Hello 4343' (

import sys

class Lexer:
    # Константы
    LPAR, RPAR, ARR, UND, AND, NOT, PLUS, MIN, MUL, DEL, EQU, MORE, LESS, LESSEQU, MOREEQU, NOTEQU, VARIABLE, PRED, NUMBER, EXCL, EOF, COMM, QUO, STRING = range(24)

    # Специальные символы языка
    SYMBOLS = {
        '(': LPAR,
        ')': RPAR,
        '_': UND,
        '+': PLUS,
        '-': MIN,
        '*': MUL,
        '/': DEL,
        '=': EQU,
        '>': MORE,
        '<': LESS,
        '!': EXCL,   # Недопустимый символ, ожидаем !=
        ',': COMM
    }

    # Еще есть      '<-': ARR
    #               '<=': LESSEQU
    #               '>=': MOREEQU
    #               '!=': NOTEQU

    # Слова языка
    WORDS = {
        'AND': AND,
        'NOT': NOT
    }

    # Очередной символ. Пусть первый символ - пробел.
    ch = ' '

    def getchar(self):
        self.ch = sys.stdin.read(1)

    def err(self, msg):
        print("Lexer error: " + msg)
        sys.exit(1)


    def next_tok(self):
        self.value = None   # Значение токена (если переменная или имя предиката)
        self.sym = None     # Тип токена

        while self.sym == None:

            #if len(self.ch) == 0: # FOR DEBUG
            if self.ch == '\n':
                self.sym = Lexer.EOF

            elif self.ch.isspace():
                self.getchar()

            elif self.ch in Lexer.SYMBOLS:
                if self.ch == '<':
                    self.getchar()
                    if self.ch == '-':          # Проверка на <-
                        self.sym = Lexer.ARR
                        self.getchar()
                    elif self.ch == '=':        # Проверка на <=
                        self.sym = Lexer.LESSEQU
                        self.getchar()
                    else:
                        self.sym = Lexer.LESS

                elif self.ch == '>':
                    self.getchar()
                    if self.ch == '=':          # Проверка на >=
                        self.sym = Lexer.MOREEQU
                        self.getchar()
                    else:
                        self.sym = Lexer.MORE

                elif self.ch == '!':
                    self.getchar()
                    if self.ch == '=':
                        self.sym = Lexer.NOTEQU
                        self.getchar()
                    else:
                        self.err("expected !=")

                else:
                    self.sym = Lexer.SYMBOLS[self.ch]
                    self.getchar()

            elif self.ch.isdigit():
                intval = 0
                while self.ch.isdigit():
                    intval = intval * 10 + int(self.ch)
                    self.getchar()

                self.sym = Lexer.NUMBER
                self.value = intval

            elif self.ch.isalpha():
                word = ''
                isVariable = self.ch.islower() # переменные начинаются с маленькой буквы

                while self.ch.isalpha():
                    word = word + self.ch
                    self.getchar()

                if word in Lexer.WORDS:
                    self.sym = Lexer.WORDS[word]
                else:
                    if isVariable:
                        self.sym = Lexer.VARIABLE
                    else:
                        self.sym = Lexer.PRED
                    self.value = word

            elif self.ch == '\'':
                str = ''
                self.getchar()

                while self.ch != '\'':
                    str = str + self.ch
                    self.getchar()

                self.getchar()

                self.sym = Lexer.STRING
                self.value = str

            else:
                self.err("unknown symbol " + self.ch)
                self.getchar()

# DEBUG
#
# lex = Lexer()
# while True:
#     lex.next_tok()
#     print("token: " + str(lex.sym) + " value: " + str(lex.value))


