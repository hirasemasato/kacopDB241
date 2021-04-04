# X003_LogIn cp932
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask, render_template, request, redirect, g
import os
import csv
import json
import sqlite3
import pandas as pd
import logging

format_str = '%(asctime)s - %(process)d - %(thread)d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=format_str, level=logging.INFO)
logger = logging.getLogger(__name__)

format_date='%Y-%m-%d'

app = Flask(__name__)

def cn_open():
    cn = sqlite3.connect('./DB603LCK.db')
    cn.isolation_level = None
    cn.row_factory = sqlite3.Row
    return cn

#定数
cX003ID= 0
c日付= 1
cPCID= 2
cUserName= 3
cVersion= 4
cKK= 5
cSV= 6

def get_drop_sql():
    wsql= 'DROP TABLE IF EXISTS X003_LogIn '
    return wsql

def get_create_sql():
    wsql ='CREATE TABLE IF NOT EXISTS X003_LogIn ('
    wsql+='X003ID TEXT  DEFAULT NULL PRIMARY KEY,'
    wsql+='日付 TEXT  DEFAULT NULL,'
    wsql+='PCID INTEGER  DEFAULT 0,'
    wsql+='UserName TEXT  DEFAULT NULL,'
    wsql+='Version TEXT  DEFAULT NULL,'
    wsql+='KK INTEGER  DEFAULT 0,'
    wsql+='SV INTEGER  DEFAULT 0'
    wsql+=') '
    return wsql

def get_select_sql():
    wsql ='SELECT '
    wsql+='X003ID, '
    wsql+='日付, '
    wsql+='PCID, '
    wsql+='UserName, '
    wsql+='Version, '
    wsql+='KK, '
    wsql+='SV '
    wsql+=' FROM X003_LogIn '
    return wsql

def get_insert_sql():
    wsql ='INSERT INTO X003_LogIn VALUES ('
    wsql+=':X003ID, '
    wsql+=':日付, '
    wsql+=':PCID, '
    wsql+=':UserName, '
    wsql+=':Version, '
    wsql+=':KK, '
    wsql+=':SV '
    wsql+=') '
    return wsql

def get_update_sql():
    wsql ='UPDATE X003_LogIn SET '
    wsql+='日付=:日付, '
    wsql+='PCID=:PCID, '
    wsql+='UserName=:UserName, '
    wsql+='Version=:Version, '
    wsql+='KK=:KK, '
    wsql+='SV=:SV '
    return wsql

def get_delete_sql():
    wsql= 'DELETE FROM X003_LogIn '
    return wsql

def get_primarykerfilter(ID):
    wID = '"' + ID + '"'
    wfilter=' WHERE X003ID = ' + wID +' '
    return wfilter

def get_X003(ID):
    wsql =get_select_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cur = cn.execute(wsql)
    data = cur.fetchone()
    return data
    cn.close()

@app.route('/')
@app.route('/X003_index', methods=['GET'])
def get_X003_index():
    cn = cn_open()
    wsql = 'SELECT * FROM X003_LogIn '
    wsql+= 'ORDER BY  X003ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('X003_index.html',rows = rows )
    cn.close()

@app.route('/X003_insert', methods=['GET'])
def get_X003_insert():
    return render_template('X003_insert.html')

@app.route('/X003_insert', methods=['POST'])
def post_X003_insert():
    wsql = get_insert_sql()
    wX003ID = request.form.get('X003ID')    #0
    w日付 = request.form.get('日付')    #1
    wPCID = request.form.get('PCID')    #2
    wUserName = request.form.get('UserName')    #3
    wVersion = request.form.get('Version')    #4
    wKK = request.form.get('KK')    #5
    wSV = request.form.get('SV')    #6
    cn = cn_open()
    row = (
        wX003ID,
        w日付,
        wPCID,
        wUserName,
        wVersion,
        wKK,
        wSV
        )
    cn.execute(wsql,row)
    wsql = 'SELECT * FROM X003_LogIn '
    wsql+= 'ORDER BY  X003ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('X003_index.html',rows = rows )
    cn.close()

@app.route('/X003_detail/<ID>', methods=['GET'])
def get_X003_detail(ID):
    data = get_X003(ID)
    return render_template('X003_detail.html', X003=data)

@app.route('/X003_update/<ID>', methods=['GET'])
def get_X003_update(ID):
    data = get_X003(ID)
    return render_template('X003_update.html', X003=data)

@app.route('/X003_update/<ID>', methods=['POST'])
def post_X003_update(ID):
    data = get_X003(ID)
    wsql = get_update_sql()
    wsql+=get_primarykerfilter(ID)
    w日付 = request.form.get('日付')    #1
    wPCID = request.form.get('PCID')    #2
    wUserName = request.form.get('UserName')    #3
    wVersion = request.form.get('Version')    #4
    wKK = request.form.get('KK')    #5
    wSV = request.form.get('SV')    #6
    cn = cn_open()
    row = {
        '日付':w日付,
        'PCID':wPCID,
        'UserName':wUserName,
        'Version':wVersion,
        'KK':wKK,
        'SV':wSV
        }
    cn.execute(wsql,row)
    cn.close()

    data = get_X003(ID)
    return render_template('X003_detail.html', X003=data)


@app.route('/X003_delete/<ID>', methods=['GET'])
def get_X003_delete(ID):
    wsql = get_delete_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cn.execute(wsql)
    wsql = 'SELECT * FROM X003_LogIn '
    wsql+= 'ORDER BY  X003ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('X003_index.html',rows = rows )
    cn.close()

@app.route('/X003_importcsv',methods=['GET'])
def get_X003_importcsv():
    cn = cn_open()
    wsql=get_insert_sql()
    rows = pd.read_csv('X003.csv', encoding='cp932')
    for row in rows.values:
        print(row[0])
        cn.execute(wsql, row)
    cn.close()

@app.route('/X003_exportjson',methods=['GET'])
def get_X003_exportjson():
    wsql = X003_select_sql
    n = cn_open()
    rows = cn.execute(wsql)
    X003s=[
    dict(
        X003ID = row[0],
        日付 = row[1],
        PCID = row[2],
        UserName = row[3],
        Version = row[4],
        KK = row[5],
        SV = row[6]
        )
     for row in rows.fetchall()
    ]
    cn.close()
    if X003s is not None:
        return json.dump(X003s,ensure_ascii=False,indent=4)

@app.route('/X003_initialize',methods=['GET'])
def get_X003_initialize():

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
    X003s=[
        dict(
            X003ID = row[0],
            日付 = row[1],
            PCID = row[2],
            UserName = row[3],
            Version = row[4],
            KK = row[5],
            SV = row[6]
            )
        for row in rows.fetchall()
        ]
    if X003s is not None:
        dirname=os.path.dirname(__file__)
        path=os.path.join(dirname,'X003.json')
        outfile=open(path,'w',encoding='utf-8')
        json.dump(X003s,outfile,ensure_ascii=False,indent=4)
        outfile.close()


if __name__ == '__main__':
    app.debug = True
    #get_X003_initialize()

"""

@app.route('/X003_index', methods=['GET'])
def get_X003_index():
    return X003.get_X003_index()

@app.route('/X003_insert', methods=['GET'])
def get_X003_insert():
    return X003.get_X003_insert()

@app.route('/X003_insert', methods=['POST'])
def post_X003_insert():
    return X003.post_X003_insert()

@app.route('/X003_importcsv', methods=['GET'])
def get_X003_jimportcsv():
    X003.get_X003_importcsv()
    return X003.get_X003_index()

@app.route('/X003_json', methods=['GET'])
def get_X003_json():
    return X003.get_X003_json()

@app.route('/X003_detail/<ID>', methods=['GET'])
def get_X003_detail(ID):
    return X003.get_X003_detail(ID)

@app.route('/X003_update/<ID>', methods=['GET'])
def get_X003_update(ID):
    return X003.get_X003_update(ID)

@app.route('/X003_update/<ID>', methods=['POST'])
def post_X003_update(ID):
    return X003.post_X003_update(ID)

@app.route('/X003_delete/<ID>', methods=['GET'])
def get_X003_delete(ID):
    return X003.get_X003_index(ID)

#createtableX003.py
# -*- coding: utf-8 -*-

import sqlite3
        
dbname = './DB603LCK.db'
cn = sqlite3.connect(dbname)
cn.execute ('PRAGMA foreign_keys = 1')
#cn.execute ('DROP TABLE  X003_LogIn)

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
X003s=[
    dict(
        X003ID = row[0],
        日付 = row[1],
        PCID = row[2],
        UserName = row[3],
        Version = row[4],
        KK = row[5],
        SV = row[6]
        )
    for row in rows.fetchall()
    ]
if X003s is not None:
    dirname=os.path.dirname(__file__)
    path=os.path.join(dirname,'X003.json')
    outfile=open(path,'w',encoding='utf-8')
    json.dump(X003s,outfile,ensure_ascii=False,indent=4)
    outfile.close()
"""
