#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3

def getSummaryInfoFromSqlite3DB(name):
    summary_info = []
    
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()
    
    name = ' '+name

    sql = """SELECT * FROM basic_info WHERE 영업표지= '{}'""".format(name)

    cursor.execute(sql)

    while True:
        row = cursor.fetchone()
        if row == None:
#             print('NONE')
            break
        summary_info = list(row)

    cursor.close()
    conn.close()
    
    return summary_info


def getMoneyInfoFromSqlite3DB(name):
    money_info = []
    
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    sql = """SELECT * FROM cost_info WHERE 영업표지= '{}'""".format(name)

    cursor.execute(sql)

    while True:
        row = cursor.fetchone()
        if row == None:
#             print('NONE')
            break
        money_info = list(row)

    cursor.close()
    conn.close()
    
    return money_info


def getBranchInfoFromSqlite3DB(name):
    branch_info = []
    
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    sql = """SELECT * FROM branch_info WHERE 영업표지= '{}'""".format(name)

    cursor.execute(sql)

    while True:
        row = cursor.fetchone()
        if row == None:
#             print('NONE')
            break
        branch_info.append(list(row))

    cursor.close()
    conn.close()
    
    return branch_info

def getFinanInfoFromSqlite3DB(name):
    finan_info = []
    
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    sql = """SELECT * FROM branch_info WHERE 영업표지= '{}'""".format(name)

    cursor.execute(sql)

    while True:
        row = cursor.fetchone()
        if row == None:
#             print('NONE')
            break
        finan_info.append(list(row))

    cursor.close()
    conn.close()
    
    return finan_info

def getSalesInfoFromSqlite3DB(name):
    sales_info = []
    
    conn = sqlite3.connect('database.db')

    cursor = conn.cursor()

    sql = """SELECT * FROM branch_info WHERE 영업표지= '{}'""".format(name)

    cursor.execute(sql)

    while True:
        row = cursor.fetchone()
        if row == None:
#             print('NONE')
            break
        sales_info.append(list(row))

    cursor.close()
    conn.close()
    
    return sales_info

