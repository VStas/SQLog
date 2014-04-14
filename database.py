#!/usr/bin/python
import MySQLdb

class Database:
    @staticmethod
    def execute(config, sql):

        # db = MySQLdb.connect(host="localhost", # your host, usually localhost
        #              user="root", # your username
        #               passwd="", # your password
        #               db="world") # name of the data base

        db = MySQLdb.connect(**config['connection']) # name of the data base
        cur = db.cursor()

# Use all the SQL you like
        cur.execute(sql)

# print all the first cell of all the rows
        for row in cur.fetchall() :
            print(row)