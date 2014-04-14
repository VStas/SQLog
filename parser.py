#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lexer import Lexer
import sys

class Parser:

    def __init__(self, lexer, config):
        self.config = config

        self.model = {
            'select_vars': [],
            'same_var_diff_cols': False,
            'var_definitions': {},
            'from_tables': [],
            'comparisons': [],
            'not_exists': {}
        }

        self.lexer = lexer
        self.lexer.next_tok()

    def parse_rule(self):
        self.parse_left()

        if self.lexer.sym != Lexer.ARR:
            self.err("expected <-")
        self.lexer.next_tok()

        self.parse_atom()
        while self.lexer.sym == Lexer.AND:
            self.lexer.next_tok()
            self.parse_atom()

    def parse_left(self):
        pred = self.parse_rel_atom()
        arglist = pred[1]
        if None in arglist:
            self.err("cannot use _ in left part arguments")

        self.model['select_vars'] = arglist

    def parse_atom(self):
        notflag = False #есть ли NOT перед предикатом
        if self.lexer.sym == Lexer.NOT:
            notflag = True
            self.lexer.next_tok()

        if self.lexer.sym == Lexer.PRED:
            pred = self.parse_rel_atom()
            tableName = pred[0]
            arglist = pred[1]

            if notflag:
                var_column = [] #пары (переменная, имя столбца)

                for i in range(len(arglist)):
                    if arglist[i] is not None: # не _
                        colName = tableName + '.' + self.config['tables'][tableName][i]
                        var_column.append((arglist[i], colName))

                self.model['not_exists'][tableName] = var_column
            else:
                self.model['from_tables'].append(tableName) # если таблица уже есть, то будет 2 раза. Надо подумать, ок ли это

                for i in range(len(arglist)):
                    varname = arglist[i]
                    if varname is not None: # не _
                        colName = tableName + '.' + self.config['tables'][tableName][i]

                        if varname in self.model['var_definitions']:
                            self.model['var_definitions'][varname].append(colName)
                            self.model['same_var_diff_cols'] = True
                        else:
                            self.model['var_definitions'][varname] = [colName]

        elif notflag:
            self.err("cannot use NOT before comparisons, use != instead of =, for example")
        else:
            expr = self.parse_expr()
            self.model['comparisons'].append(expr)



    def err(self, msg):
        print("Parser error: " + msg)
        sys.exit(1)

    # returns [None, 'x', 'y' , 'z', None, None]
    def parse_varlist(self):
        varlist = []

        if self.lexer.sym not in [Lexer.VARIABLE, Lexer.UND]:
            self.err("variable list should start with variable name")

        varlist.append(self.lexer.value)

        self.lexer.next_tok()

        while self.lexer.sym == Lexer.COMM:
            self.lexer.next_tok()
            if self.lexer.sym in [Lexer.VARIABLE, Lexer.UND]:
                varlist.append(self.lexer.value)
            else:
                self.err("variable name expected after ,")
            self.lexer.next_tok()

        return varlist

    #returns ('Table', ['x', 'r', None])
    def parse_rel_atom(self):
        if self.lexer.sym != Lexer.PRED:
            self.err("expected predicate name")
        pred_name = self.lexer.value

        self.lexer.next_tok()
        if self.lexer.sym != Lexer.LPAR:
            self.err("expected (")

        self.lexer.next_tok()
        varlist = self.parse_varlist()

        if self.lexer.sym != Lexer.RPAR:
            self.err("expected )")

        self.lexer.next_tok()

        return pred_name, varlist

    #returns [(16, 'dfmfos'), (6, None), (7, None), (9, None), (18, 323), (1, None)]
    def parse_expr(self):
        expr = []
        while self.lexer.sym in [Lexer.NUMBER, Lexer.VARIABLE,
                                 Lexer.PLUS, Lexer.MIN, Lexer.MUL, Lexer.DEL,
                                 Lexer.EQU, Lexer.MORE, Lexer.LESS, Lexer.NOTEQU, Lexer.MOREEQU, Lexer.LESSEQU,
                                 Lexer.LPAR, Lexer.RPAR,
                                 Lexer.STRING]:
            expr.append((self.lexer.sym, self.lexer.value))
            self.lexer.next_tok()

        return expr

    def parse(self):
        self.parse_rule()
        return self.model

#config = {}
#execfile("db_config.conf", config)

#lex = Lexer()
#parser = Parser(lex, config)
#print(parser.parse_varlist())
#print(parser.parse_rel_atom())
#print(parser.parse_expr())

#parser.parse_atom()
#parser.parse_left()
#parser.parse()
# test:
# A(x,t)<- x = 3 AND Country(x,_ , t) AND t < 'Gena' AND City(t)
# A(x,t)<- x = 'RUS' AND Country(x,_ , t) AND t < 'Gena' AND City(t)
# A(x,t)<- x = 'RUS' AND Country(x,_ , t)

#print(parser.model)
