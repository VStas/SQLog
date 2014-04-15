#!/usr/bin/python

import MySQLdb
from lexer import Lexer
from parser import Parser
from database import Database
import sys

class SQLog:

    tokens_to_symbols = {
        Lexer.PLUS: '+',
        Lexer.MIN: '-',
        Lexer.MUL: '*',
        Lexer.DEL: '/',
        Lexer.EQU: '=',
        Lexer.MORE: '>',
        Lexer.LESS: '<',
        Lexer.NOTEQU: '!=',
        Lexer.MOREEQU: '>=',
        Lexer.LESSEQU: '<=',
        Lexer.LPAR: '(',
        Lexer.RPAR: ')'
    }

    def __init__(self, parser):
        self.parser = parser

    def err(self, msg):
        print("SQLog error: " + msg)
        sys.exit(1)

    def start(self):
        self.model = self.parser.parse()
        #print(self.model)
        sql = self.compose_sql()
        print('')
        print(sql)
        print('')
        Database.execute(self.parser.config, sql)

    def compose_sql(self):
        sql = 'SELECT ' + self.compose_sql_select() + ' FROM ' + self.compose_sql_from() + ' '+  self.compose_sql_where()
        return sql


    def compose_sql_select(self):
        select_vars = self.model['select_vars']
        select_cols = []
        for var_name in select_vars:
            select_cols.append(self.get_var_definition(var_name))

        return ','.join(select_cols)

    def compose_sql_from(self):
        from_tables = self.model['from_tables']
        return ','.join(from_tables)

    def compose_sql_where(self):
        need_where = len(self.model['comparisons']) > 0 or self.model['same_var_diff_cols'] or any(self.model['not_exists'])
        if not need_where:
            return ''

        where_clauses = []

        if len(self.model['comparisons']) > 0:
            for comp in self.model['comparisons']:
                where_clauses.append(self.compose_comparison(comp))

        if self.model['same_var_diff_cols']:
            for var_name in self.model['var_definitions']:
                columns = self.model['var_definitions'][var_name]
                if len(columns) > 1:
                    for i in range(1, len(columns)):
                        where_clauses.append(columns[0] + "=" + columns[i])

        if any(self.model['not_exists']):
            for table in self.model['not_exists']:
                table_arr = self.model['not_exists'][table]
                if len(table_arr) > 0:
                    clauses = []
                    for clause in table_arr:
                        clauses.append(self.get_var_definition(clause[0]) + ' = ' + clause[1])


                    sql = 'NOT EXISTS (SELECT 1 FROM ' + table + ' WHERE ' + ' AND '.join(clauses) + ')'
                    where_clauses.append(sql)


        return 'WHERE ' + ' AND '.join(where_clauses)



    # test:
    # A(x,t)<- x = 'RUS' AND Country(x,_ , t) AND +-*/=><()'hehe'x50
    def compose_comparison(self, tokens_arr):
        comp = ''
        for i in range(len(tokens_arr)):
            if tokens_arr[i][0] in SQLog.tokens_to_symbols:
                comp = comp + SQLog.tokens_to_symbols[tokens_arr[i][0]]
            elif tokens_arr[i][0] == Lexer.NUMBER:
                comp = comp + str(tokens_arr[i][1])
            elif tokens_arr[i][0] == Lexer.STRING:
                comp = comp + '\'' + tokens_arr[i][1] + '\''
            elif tokens_arr[i][0] == Lexer.VARIABLE:
                comp = comp + self.get_var_definition(tokens_arr[i][1])
            else:
                self.err("unexpected error in compose_comparison")

        return comp


    def get_var_definition(self, var_name):
        if var_name not in self.model['var_definitions']:
            self.err("safety rule violated for var " + var_name)
        return self.model['var_definitions'][var_name][0]



config = {}
execfile("db_config.conf", config)
lex = Lexer()
parser = Parser(lex, config)
sqlog = SQLog(parser)
sqlog.start()

# Test

# CountriesFromX(code, name) <- Country(code, name) AND code > 'X'
# CountriesEqContinent(name, region) <- Country (_, name, name, region)
# CitiesInRUS(name, district, population) <- City(_, name, code, district, population) AND code = 'RUS'

# CitiesMillion(cityname, countryname) <- City(_, cityname, code, _, pop) AND Country(code, countryname) AND pop > 5000000

# NotCapitals(cityname, code) <- City(id, cityname, code) AND NOT Country(_, _, _, _, _, _, _, _, _, _, _, _, _, id)