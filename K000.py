# K000_MENU cp932
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask, render_template, request, redirect, g
import os
import csv
import json
import sqlite3
#import pandas as pd
import logging

format_str = '%(asctime)s - %(process)d - %(thread)d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=format_str, level=logging.INFO)
logger = logging.getLogger(__name__)

format_date='%Y-%m-%d'

app = Flask(__name__)

def cn_open():
    cn = sqlite3.connect('./DB603DAT.db')
    cn.isolation_level = None
    cn.row_factory = sqlite3.Row
    return cn

#定数
cMENUID= 0
cMENUNO= 1
cMENUNAME= 2
cHREF= 3
cMEMO= 4
cENABLED= 5
cCATEGORY= 6
cSECURITYLEVEL= 7

def get_drop_sql():
    wsql= 'DROP TABLE IF EXISTS K000_MENU '
    return wsql

def get_create_sql():
    wsql ='CREATE TABLE IF NOT EXISTS K000_MENU ('
    wsql+='MENUID INTEGER  DEFAULT 0 PRIMARY KEY,'
    wsql+='MENUNO INTEGER  DEFAULT 0,'
    wsql+='MENUNAME TEXT  DEFAULT NULL,'
    wsql+='HREF TEXT  DEFAULT NULL,'
    wsql+='MEMO TEXT  DEFAULT NULL,'
    wsql+='ENABLED INTEGER  DEFAULT 0,'
    wsql+='CATEGORY INTEGER  DEFAULT 0,'
    wsql+='SECURITYLEVEL INTEGER  DEFAULT 0'
    wsql+=') '
    return wsql

def get_select_sql():
    wsql ='SELECT '
    wsql+='MENUID, '
    wsql+='MENUNO, '
    wsql+='MENUNAME, '
    wsql+='HREF, '
    wsql+='MEMO, '
    wsql+='ENABLED, '
    wsql+='CATEGORY, '
    wsql+='SECURITYLEVEL '
    wsql+=' FROM K000_MENU '
    return wsql

def get_insert_sql():
    wsql ='INSERT INTO K000_MENU VALUES ('
    wsql+=':MENUID, '
    wsql+=':MENUNO, '
    wsql+=':MENUNAME, '
    wsql+=':HREF, '
    wsql+=':MEMO, '
    wsql+=':ENABLED, '
    wsql+=':CATEGORY, '
    wsql+=':SECURITYLEVEL '
    wsql+=') '
    return wsql

def get_update_sql():
    wsql ='UPDATE K000_MENU SET '
    wsql+='MENUNO=:MENUNO, '
    wsql+='MENUNAME=:MENUNAME, '
    wsql+='HREF=:HREF, '
    wsql+='MEMO=:MEMO, '
    wsql+='ENABLED=:ENABLED, '
    wsql+='CATEGORY=:CATEGORY, '
    wsql+='SECURITYLEVEL=:SECURITYLEVEL '
    return wsql

def get_delete_sql():
    wsql= 'DELETE FROM K000_MENU '
    return wsql

def get_primarykerfilter(ID):
    if not str.isdecimal(str(ID)):
        ID = -1
    wID = str(ID)
    wfilter=' WHERE  = ' + wID +' '
    return wfilter

def get_K000(ID):
    wsql =get_select_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cur = cn.execute(wsql)
    data = cur.fetchone()
    return data
    cn.close()

@app.route('/')
@app.route('/K000_index', methods=['GET'])
def get_K000_index():
    cn = cn_open()
    wsql = 'SELECT * FROM K000_MENU '
    wsql+= 'ORDER BY   DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('K000_index.html',rows = rows )
    cn.close()

@app.route('/K000_insert', methods=['GET'])
def get_K000_insert():
    return render_template('K000_insert.html')

@app.route('/K000_insert', methods=['POST'])
def post_K000_insert():
    wsql = get_insert_sql()
    wMENUID = request.form.get('MENUID')    #0
    wMENUNO = request.form.get('MENUNO')    #1
    wMENUNAME = request.form.get('MENUNAME')    #2
    wHREF = request.form.get('HREF')    #3
    wMEMO = request.form.get('MEMO')    #4
    wENABLED = request.form.get('ENABLED')    #5
    wCATEGORY = request.form.get('CATEGORY')    #6
    wSECURITYLEVEL = request.form.get('SECURITYLEVEL')    #7
    cn = cn_open()
    row = (
        wMENUID,
        wMENUNO,
        wMENUNAME,
        wHREF,
        wMEMO,
        wENABLED,
        wCATEGORY,
        wSECURITYLEVEL
        )
    cn.execute(wsql,row)
    wsql = 'SELECT * FROM K000_MENU '
    wsql+= 'ORDER BY   DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('K000_index.html',rows = rows )
    cn.close()

@app.route('/K000_detail/<ID>', methods=['GET'])
def get_K000_detail(ID):
    data = get_K000(ID)
    return render_template('K000_detail.html', K000=data)

@app.route('/K000_update/<ID>', methods=['GET'])
def get_K000_update(ID):
    data = get_K000(ID)
    return render_template('K000_update.html', K000=data)

@app.route('/K000_update/<ID>', methods=['POST'])
def post_K000_update(ID):
    data = get_K000(ID)
    wsql = get_update_sql()
    wsql+=get_primarykerfilter(ID)
    wMENUNO = request.form.get('MENUNO')    #1
    wMENUNAME = request.form.get('MENUNAME')    #2
    wHREF = request.form.get('HREF')    #3
    wMEMO = request.form.get('MEMO')    #4
    wENABLED = request.form.get('ENABLED')    #5
    wCATEGORY = request.form.get('CATEGORY')    #6
    wSECURITYLEVEL = request.form.get('SECURITYLEVEL')    #7
    cn = cn_open()
    row = {
        'MENUNO':wMENUNO,
        'MENUNAME':wMENUNAME,
        'HREF':wHREF,
        'MEMO':wMEMO,
        'ENABLED':wENABLED,
        'CATEGORY':wCATEGORY,
        'SECURITYLEVEL':wSECURITYLEVEL
        }
    cn.execute(wsql,row)
    cn.close()

    data = get_K000(ID)
    return render_template('K000_detail.html', K000=data)


@app.route('/K000_delete/<ID>', methods=['GET'])
def get_K000_delete(ID):
    wsql = get_delete_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cn.execute(wsql)
    wsql = 'SELECT * FROM K000_MENU '
    wsql+= 'ORDER BY   DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('K000_index.html',rows = rows )
    cn.close()

@app.route('/K000_importcsv',methods=['GET'])
def get_K000_importcsv():
    cn = cn_open()
    wsql=get_insert_sql()
#    rows = pd.read_csv('K000.csv', encoding='cp932')
    for row in rows.values:
        print(row[0])
        cn.execute(wsql, row)
    cn.close()

@app.route('/K000_exportjson',methods=['GET'])
def get_K000_exportjson():
    wsql = K000_select_sql
    n = cn_open()
    rows = cn.execute(wsql)
    K000s=[
    dict(
        MENUID = row[0],
        MENUNO = row[1],
        MENUNAME = row[2],
        HREF = row[3],
        MEMO = row[4],
        ENABLED = row[5],
        CATEGORY = row[6],
        SECURITYLEVEL = row[7]
        )
     for row in rows.fetchall()
    ]
    cn.close()
    if K000s is not None:
        return json.dump(K000s,ensure_ascii=False,indent=4)

@app.route('/K000_initialize',methods=['GET'])
def get_K000_initialize():

    cn = cn_open()

    # Drop
    wsql = get_drop_sql()
    cn.execute(wsql)

    #Create
    wsql = get_create_sql()
    cn.execute(wsql)

    #Insert
    wsql = get_insert_sql()
    for row in rows:
        cn.execute(wsql, row)

    #Select to ,jsonformat
    wsql = get_select_sql()
    rows =cn.execute(wsql)
    K000s=[
        dict(
            MENUID = row[0],
            MENUNO = row[1],
            MENUNAME = row[2],
            HREF = row[3],
            MEMO = row[4],
            ENABLED = row[5],
            CATEGORY = row[6],
            SECURITYLEVEL = row[7]
            )
        for row in rows.fetchall()
        ]
    if K000s is not None:
        dirname=os.path.dirname(__file__)
        path=os.path.join(dirname,'K000.json')
        outfile=open(path,'w',encoding='utf-8')
        json.dump(K000s,outfile,ensure_ascii=False,indent=4)
        outfile.close()


if __name__ == '__main__':
    app.debug = True
    #get_K000_initialize()

"""

@app.route('/K000_index', methods=['GET'])
def get_K000_index():
    return K000.get_K000_index()

@app.route('/K000_insert', methods=['GET'])
def get_K000_insert():
    return K000.get_K000_insert()

@app.route('/K000_insert', methods=['POST'])
def post_K000_insert():
    return K000.post_K000_insert()

@app.route('/K000_importcsv', methods=['GET'])
def get_K000_jimportcsv():
    K000.get_K000_importcsv()
    return K000.get_K000_index()

@app.route('/K000_json', methods=['GET'])
def get_K000_json():
    return K000.get_K000_json()

@app.route('/K000_detail/<ID>', methods=['GET'])
def get_K000_detail(ID):
    return K000.get_K000_detail(ID)

@app.route('/K000_update/<ID>', methods=['GET'])
def get_K000_update(ID):
    return K000.get_K000_update(ID)

@app.route('/K000_update/<ID>', methods=['POST'])
def post_K000_update(ID):
    return K000.post_K000_update(ID)

@app.route('/K000_delete/<ID>', methods=['GET'])
def get_K000_delete(ID):
    return K000.get_K000_index(ID)

#createtableK000.py
# -*- coding: utf-8 -*-

import sqlite3
        
dbname = './DB603DAT.db'
cn = sqlite3.connect(dbname)
cn.execute ('PRAGMA foreign_keys = 1')
#cn.execute ('DROP TABLE  K000_MENU)

# Drop
wsql = get_drop_sql()
cn.execute(wsql)

#Create
wsql = get_create_sql()
cn.execute(wsql)

#data
rows = (
    {'ID': 1, 'NAME': '受注入力', 'HREF':'/M011_index','CATEGORY': 1, 'ENABLED': 1, 'SECURITYLEVEL': 0, 'MEMO': '受注書、発注書'},
    {'ID': 2, 'NAME': '売上入力', 'HREF':'/M111_index','CATEGORY': 1, 'ENABLED': 1, 'SECURITYLEVEL': 0, 'MEMO': '納品書、納品請求書'},
    )

#Insert
wsql = get_insert_sql()
for row in rows:
    cn.execute(wsql, row)

#Select to ,jsonformat
wsql = get_select_sql()
rows = cn.execute(wsql)
K000s=[
    dict(
        MENUID = row[0],
        MENUNO = row[1],
        MENUNAME = row[2],
        HREF = row[3],
        MEMO = row[4],
        ENABLED = row[5],
        CATEGORY = row[6],
        SECURITYLEVEL = row[7]
        )
    for row in rows.fetchall()
    ]
if K000s is not None:
    dirname=os.path.dirname(__file__)
    path=os.path.join(dirname,'K000.json')
    outfile=open(path,'w',encoding='utf-8')
    json.dump(K000s,outfile,ensure_ascii=False,indent=4)
    outfile.close()
"""
