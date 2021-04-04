# X002_FormLog cp932
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
cX002ID= 0
c日付= 1
cTickCount= 2
cPCID= 3
cUserName= 4
cVersion= 5
cMode= 6
cDescription= 7
cST= 8
cID= 9
cKK= 10
cSV= 11

def get_drop_sql():
    wsql= 'DROP TABLE IF EXISTS X002_FormLog '
    return wsql

def get_create_sql():
    wsql ='CREATE TABLE IF NOT EXISTS X002_FormLog ('
    wsql+='X002ID TEXT  DEFAULT NULL PRIMARY KEY,'
    wsql+='日付 TEXT  DEFAULT NULL,'
    wsql+='TickCount INTEGER  DEFAULT 0,'
    wsql+='PCID INTEGER  DEFAULT 0,'
    wsql+='UserName TEXT  DEFAULT NULL,'
    wsql+='Version TEXT  DEFAULT NULL,'
    wsql+='Mode INTEGER  DEFAULT 0,'
    wsql+='Description TEXT  DEFAULT NULL,'
    wsql+='ST INTEGER  DEFAULT 0,'
    wsql+='ID INTEGER  DEFAULT 0,'
    wsql+='KK INTEGER  DEFAULT 0,'
    wsql+='SV INTEGER  DEFAULT 0'
    wsql+=') '
    return wsql

def get_select_sql():
    wsql ='SELECT '
    wsql+='X002ID, '
    wsql+='日付, '
    wsql+='TickCount, '
    wsql+='PCID, '
    wsql+='UserName, '
    wsql+='Version, '
    wsql+='Mode, '
    wsql+='Description, '
    wsql+='ST, '
    wsql+='ID, '
    wsql+='KK, '
    wsql+='SV '
    wsql+=' FROM X002_FormLog '
    return wsql

def get_insert_sql():
    wsql ='INSERT INTO X002_FormLog VALUES ('
    wsql+=':X002ID, '
    wsql+=':日付, '
    wsql+=':TickCount, '
    wsql+=':PCID, '
    wsql+=':UserName, '
    wsql+=':Version, '
    wsql+=':Mode, '
    wsql+=':Description, '
    wsql+=':ST, '
    wsql+=':ID, '
    wsql+=':KK, '
    wsql+=':SV '
    wsql+=') '
    return wsql

def get_update_sql():
    wsql ='UPDATE X002_FormLog SET '
    wsql+='日付=:日付, '
    wsql+='TickCount=:TickCount, '
    wsql+='PCID=:PCID, '
    wsql+='UserName=:UserName, '
    wsql+='Version=:Version, '
    wsql+='Mode=:Mode, '
    wsql+='Description=:Description, '
    wsql+='ST=:ST, '
    wsql+='ID=:ID, '
    wsql+='KK=:KK, '
    wsql+='SV=:SV '
    return wsql

def get_delete_sql():
    wsql= 'DELETE FROM X002_FormLog '
    return wsql

def get_primarykerfilter(ID):
    wID = '"' + ID + '"'
    wfilter=' WHERE X002ID = ' + wID +' '
    return wfilter

def get_X002(ID):
    wsql =get_select_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cur = cn.execute(wsql)
    data = cur.fetchone()
    return data
    cn.close()

@app.route('/')
@app.route('/X002_index', methods=['GET'])
def get_X002_index():
    cn = cn_open()
    wsql = 'SELECT * FROM X002_FormLog '
    wsql+= 'ORDER BY  X002ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('X002_index.html',rows = rows )
    cn.close()

@app.route('/X002_insert', methods=['GET'])
def get_X002_insert():
    return render_template('X002_insert.html')

@app.route('/X002_insert', methods=['POST'])
def post_X002_insert():
    wsql = get_insert_sql()
    wX002ID = request.form.get('X002ID')    #0
    w日付 = request.form.get('日付')    #1
    wTickCount = request.form.get('TickCount')    #2
    wPCID = request.form.get('PCID')    #3
    wUserName = request.form.get('UserName')    #4
    wVersion = request.form.get('Version')    #5
    wMode = request.form.get('Mode')    #6
    wDescription = request.form.get('Description')    #7
    wST = request.form.get('ST')    #8
    wID = request.form.get('ID')    #9
    wKK = request.form.get('KK')    #10
    wSV = request.form.get('SV')    #11
    cn = cn_open()
    row = (
        wX002ID,
        w日付,
        wTickCount,
        wPCID,
        wUserName,
        wVersion,
        wMode,
        wDescription,
        wST,
        wID,
        wKK,
        wSV
        )
    cn.execute(wsql,row)
    wsql = 'SELECT * FROM X002_FormLog '
    wsql+= 'ORDER BY  X002ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('X002_index.html',rows = rows )
    cn.close()

@app.route('/X002_detail/<ID>', methods=['GET'])
def get_X002_detail(ID):
    data = get_X002(ID)
    return render_template('X002_detail.html', X002=data)

@app.route('/X002_update/<ID>', methods=['GET'])
def get_X002_update(ID):
    data = get_X002(ID)
    return render_template('X002_update.html', X002=data)

@app.route('/X002_update/<ID>', methods=['POST'])
def post_X002_update(ID):
    data = get_X002(ID)
    wsql = get_update_sql()
    wsql+=get_primarykerfilter(ID)
    w日付 = request.form.get('日付')    #1
    wTickCount = request.form.get('TickCount')    #2
    wPCID = request.form.get('PCID')    #3
    wUserName = request.form.get('UserName')    #4
    wVersion = request.form.get('Version')    #5
    wMode = request.form.get('Mode')    #6
    wDescription = request.form.get('Description')    #7
    wST = request.form.get('ST')    #8
    wID = request.form.get('ID')    #9
    wKK = request.form.get('KK')    #10
    wSV = request.form.get('SV')    #11
    cn = cn_open()
    row = {
        '日付':w日付,
        'TickCount':wTickCount,
        'PCID':wPCID,
        'UserName':wUserName,
        'Version':wVersion,
        'Mode':wMode,
        'Description':wDescription,
        'ST':wST,
        'ID':wID,
        'KK':wKK,
        'SV':wSV
        }
    cn.execute(wsql,row)
    cn.close()

    data = get_X002(ID)
    return render_template('X002_detail.html', X002=data)


@app.route('/X002_delete/<ID>', methods=['GET'])
def get_X002_delete(ID):
    wsql = get_delete_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cn.execute(wsql)
    wsql = 'SELECT * FROM X002_FormLog '
    wsql+= 'ORDER BY  X002ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('X002_index.html',rows = rows )
    cn.close()

@app.route('/X002_importcsv',methods=['GET'])
def get_X002_importcsv():
    cn = cn_open()
    wsql=get_insert_sql()
    rows = pd.read_csv('X002.csv', encoding='cp932')
    for row in rows.values:
        print(row[0])
        cn.execute(wsql, row)
    cn.close()

@app.route('/X002_exportjson',methods=['GET'])
def get_X002_exportjson():
    wsql = X002_select_sql
    n = cn_open()
    rows = cn.execute(wsql)
    X002s=[
    dict(
        X002ID = row[0],
        日付 = row[1],
        TickCount = row[2],
        PCID = row[3],
        UserName = row[4],
        Version = row[5],
        Mode = row[6],
        Description = row[7],
        ST = row[8],
        ID = row[9],
        KK = row[10],
        SV = row[11]
        )
     for row in rows.fetchall()
    ]
    cn.close()
    if X002s is not None:
        return json.dump(X002s,ensure_ascii=False,indent=4)

@app.route('/X002_initialize',methods=['GET'])
def get_X002_initialize():

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
    X002s=[
        dict(
            X002ID = row[0],
            日付 = row[1],
            TickCount = row[2],
            PCID = row[3],
            UserName = row[4],
            Version = row[5],
            Mode = row[6],
            Description = row[7],
            ST = row[8],
            ID = row[9],
            KK = row[10],
            SV = row[11]
            )
        for row in rows.fetchall()
        ]
    if X002s is not None:
        dirname=os.path.dirname(__file__)
        path=os.path.join(dirname,'X002.json')
        outfile=open(path,'w',encoding='utf-8')
        json.dump(X002s,outfile,ensure_ascii=False,indent=4)
        outfile.close()


if __name__ == '__main__':
    app.debug = True
    #get_X002_initialize()

"""

@app.route('/X002_index', methods=['GET'])
def get_X002_index():
    return X002.get_X002_index()

@app.route('/X002_insert', methods=['GET'])
def get_X002_insert():
    return X002.get_X002_insert()

@app.route('/X002_insert', methods=['POST'])
def post_X002_insert():
    return X002.post_X002_insert()

@app.route('/X002_importcsv', methods=['GET'])
def get_X002_jimportcsv():
    X002.get_X002_importcsv()
    return X002.get_X002_index()

@app.route('/X002_json', methods=['GET'])
def get_X002_json():
    return X002.get_X002_json()

@app.route('/X002_detail/<ID>', methods=['GET'])
def get_X002_detail(ID):
    return X002.get_X002_detail(ID)

@app.route('/X002_update/<ID>', methods=['GET'])
def get_X002_update(ID):
    return X002.get_X002_update(ID)

@app.route('/X002_update/<ID>', methods=['POST'])
def post_X002_update(ID):
    return X002.post_X002_update(ID)

@app.route('/X002_delete/<ID>', methods=['GET'])
def get_X002_delete(ID):
    return X002.get_X002_index(ID)

#createtableX002.py
# -*- coding: utf-8 -*-

import sqlite3
        
dbname = './DB603LCK.db'
cn = sqlite3.connect(dbname)
cn.execute ('PRAGMA foreign_keys = 1')
#cn.execute ('DROP TABLE  X002_FormLog)

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
X002s=[
    dict(
        X002ID = row[0],
        日付 = row[1],
        TickCount = row[2],
        PCID = row[3],
        UserName = row[4],
        Version = row[5],
        Mode = row[6],
        Description = row[7],
        ST = row[8],
        ID = row[9],
        KK = row[10],
        SV = row[11]
        )
    for row in rows.fetchall()
    ]
if X002s is not None:
    dirname=os.path.dirname(__file__)
    path=os.path.join(dirname,'X002.json')
    outfile=open(path,'w',encoding='utf-8')
    json.dump(X002s,outfile,ensure_ascii=False,indent=4)
    outfile.close()
"""
