# M902_User cp932
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
    cn = sqlite3.connect('DB603DAT.db')
    cn.isolation_level = None
    cn.row_factory = sqlite3.Row
    return cn

#定数
cUserID= 0
cClass= 1
cPCID= 2
cUserName= 3
c登録日= 4
c修正日= 5
c作成= 6
c登録= 7
c削除= 8
cKK= 9
cSV= 10

def get_drop_sql():
    wsql= 'DROP TABLE IF EXISTS M902_User '
    return wsql

def get_create_sql():
    wsql ='CREATE TABLE IF NOT EXISTS M902_User ('
    wsql+='UserID TEXT  DEFAULT NULL PRIMARY KEY,'
    wsql+='Class INTEGER  DEFAULT 0,'
    wsql+='PCID INTEGER  DEFAULT 0,'
    wsql+='UserName TEXT  DEFAULT NULL,'
    wsql+='登録日 TEXT  DEFAULT NULL,'
    wsql+='修正日 TEXT  DEFAULT NULL,'
    wsql+='作成 INTEGER  DEFAULT 0,'
    wsql+='登録 INTEGER  DEFAULT 0,'
    wsql+='削除 INTEGER  DEFAULT 0,'
    wsql+='KK TEXT  DEFAULT NULL,'
    wsql+='SV TEXT  DEFAULT NULL'
    wsql+=') '
    return wsql

def get_select_sql():
    wsql ='SELECT '
    wsql+='UserID, '
    wsql+='Class, '
    wsql+='PCID, '
    wsql+='UserName, '
    wsql+='登録日, '
    wsql+='修正日, '
    wsql+='作成, '
    wsql+='登録, '
    wsql+='削除, '
    wsql+='KK, '
    wsql+='SV '
    wsql+=' FROM M902_User '
    return wsql

def get_insert_sql():
    wsql ='INSERT INTO M902_User VALUES ('
    wsql+=':UserID, '
    wsql+=':Class, '
    wsql+=':PCID, '
    wsql+=':UserName, '
    wsql+=':登録日, '
    wsql+=':修正日, '
    wsql+=':作成, '
    wsql+=':登録, '
    wsql+=':削除, '
    wsql+=':KK, '
    wsql+=':SV '
    wsql+=') '
    return wsql

def get_update_sql():
    wsql ='UPDATE M902_User SET '
    wsql+='Class=:Class, '
    wsql+='PCID=:PCID, '
    wsql+='UserName=:UserName, '
    wsql+='登録日=:登録日, '
    wsql+='修正日=:修正日, '
    wsql+='作成=:作成, '
    wsql+='登録=:登録, '
    wsql+='削除=:削除, '
    wsql+='KK=:KK, '
    wsql+='SV=:SV '
    return wsql

def get_delete_sql():
    wsql= 'DELETE FROM M902_User '
    return wsql

def get_primarykerfilter(ID):
    wID = '"' + ID + '"'
    wfilter=' WHERE UserID = ' + wID +' '
    return wfilter

def get_M902(ID):
    wsql =get_select_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cur = cn.execute(wsql)
    data = cur.fetchone()
    return data
    cn.close()

@app.route('/')
@app.route('/M902_index', methods=['GET'])
def get_M902_index():
    cn = cn_open()
    wsql = 'SELECT * FROM M902_User '
    wsql+= 'ORDER BY  UserID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M902_index.html',rows = rows )
    cn.close()

@app.route('/M902_insert', methods=['GET'])
def get_M902_insert():
    return render_template('M902_insert.html')

@app.route('/M902_insert', methods=['POST'])
def post_M902_insert():
    wsql = get_insert_sql()
    wUserID = request.form.get('UserID')    #0
    wClass = request.form.get('Class')    #1
    wPCID = request.form.get('PCID')    #2
    wUserName = request.form.get('UserName')    #3
    w登録日 = request.form.get('登録日')    #4
    w修正日 = request.form.get('修正日')    #5
    w作成 = request.form.get('作成')    #6
    w登録 = request.form.get('登録')    #7
    w削除 = request.form.get('削除')    #8
    wKK = request.form.get('KK')    #9
    wSV = request.form.get('SV')    #10
    cn = cn_open()
    row = (
        wUserID,
        wClass,
        wPCID,
        wUserName,
        w登録日,
        w修正日,
        w作成,
        w登録,
        w削除,
        wKK,
        wSV
        )
    cn.execute(wsql,row)
    wsql = 'SELECT * FROM M902_User '
    wsql+= 'ORDER BY  UserID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M902_index.html',rows = rows )
    cn.close()

@app.route('/M902_detail/<ID>', methods=['GET'])
def get_M902_detail(ID):
    data = get_M902(ID)
    return render_template('M902_detail.html', M902=data)

@app.route('/M902_update/<ID>', methods=['GET'])
def get_M902_update(ID):
    data = get_M902(ID)
    return render_template('M902_update.html', M902=data)

@app.route('/M902_update/<ID>', methods=['POST'])
def post_M902_update(ID):
    data = get_M902(ID)
    wsql = get_update_sql()
    wsql+=get_primarykerfilter(ID)
    wClass = request.form.get('Class')    #1
    wPCID = request.form.get('PCID')    #2
    wUserName = request.form.get('UserName')    #3
    w登録日 = request.form.get('登録日')    #4
    w修正日 = request.form.get('修正日')    #5
    w作成 = request.form.get('作成')    #6
    w登録 = request.form.get('登録')    #7
    w削除 = request.form.get('削除')    #8
    wKK = request.form.get('KK')    #9
    wSV = request.form.get('SV')    #10
    cn = cn_open()
    row = {
        'Class':wClass,
        'PCID':wPCID,
        'UserName':wUserName,
        '登録日':w登録日,
        '修正日':w修正日,
        '作成':w作成,
        '登録':w登録,
        '削除':w削除,
        'KK':wKK,
        'SV':wSV
        }
    cn.execute(wsql,row)
    cn.close()

    data = get_M902(ID)
    return render_template('M902_detail.html', M902=data)


@app.route('/M902_delete/<ID>', methods=['GET'])
def get_M902_delete(ID):
    wsql = get_delete_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cn.execute(wsql)
    wsql = 'SELECT * FROM M902_User '
    wsql+= 'ORDER BY  UserID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M902_index.html',rows = rows )
    cn.close()

@app.route('/M902_importcsv',methods=['GET'])
def get_M902_importcsv():
    cn = cn_open()
    wsql=get_insert_sql()
    rows = pd.read_csv('M902.csv', encoding='cp932')
    for row in rows.values:
        print(row[0])
        cn.execute(wsql, row)
    cn.close()

@app.route('/M902_exportjson',methods=['GET'])
def get_M902_exportjson():
    wsql = M902_select_sql
    n = cn_open()
    rows = cn.execute(wsql)
    M902s=[
    dict(
        UserID = row[0],
        Class = row[1],
        PCID = row[2],
        UserName = row[3],
        登録日 = row[4],
        修正日 = row[5],
        作成 = row[6],
        登録 = row[7],
        削除 = row[8],
        KK = row[9],
        SV = row[10]
        )
     for row in rows.fetchall()
    ]
    cn.close()
    if M902s is not None:
        return json.dump(M902s,ensure_ascii=False,indent=4)

@app.route('/M902_initialize',methods=['GET'])
def get_M902_initialize():

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
    M902s=[
        dict(
            UserID = row[0],
            Class = row[1],
            PCID = row[2],
            UserName = row[3],
            登録日 = row[4],
            修正日 = row[5],
            作成 = row[6],
            登録 = row[7],
            削除 = row[8],
            KK = row[9],
            SV = row[10]
            )
        for row in rows.fetchall()
        ]
    if M902s is not None:
        dirname=os.path.dirname(__file__)
        path=os.path.join(dirname,'M902.json')
        outfile=open(path,'w',encoding='utf-8')
        json.dump(M902s,outfile,ensure_ascii=False,indent=4)
        outfile.close()


if __name__ == '__main__':
    app.debug = True
    #get_M902_initialize()

"""

@app.route('/M902_index', methods=['GET'])
def get_M902_index():
    return M902.get_M902_index()

@app.route('/M902_insert', methods=['GET'])
def get_M902_insert():
    return M902.get_M902_insert()

@app.route('/M902_insert', methods=['POST'])
def post_M902_insert():
    return M902.post_M902_insert()

@app.route('/M902_importcsv', methods=['GET'])
def get_M902_jimportcsv():
    M902.get_M902_importcsv()
    return M902.get_M902_index()

@app.route('/M902_json', methods=['GET'])
def get_M902_json():
    return M902.get_M902_json()

@app.route('/M902_detail/<ID>', methods=['GET'])
def get_M902_detail(ID):
    return M902.get_M902_detail(ID)

@app.route('/M902_update/<ID>', methods=['GET'])
def get_M902_update(ID):
    return M902.get_M902_update(ID)

@app.route('/M902_update/<ID>', methods=['POST'])
def post_M902_update(ID):
    return M902.post_M902_update(ID)

@app.route('/M902_delete/<ID>', methods=['GET'])
def get_M902_delete(ID):
    return M902.get_M902_index(ID)

#createtableM902.py
# -*- coding: utf-8 -*-

import sqlite3
        
dbname = 'DB603DAT.db'
cn = sqlite3.connect(dbname)
cn.execute ('PRAGMA foreign_keys = 1')
#cn.execute ('DROP TABLE  M902_User)

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
M902s=[
    dict(
        UserID = row[0],
        Class = row[1],
        PCID = row[2],
        UserName = row[3],
        登録日 = row[4],
        修正日 = row[5],
        作成 = row[6],
        登録 = row[7],
        削除 = row[8],
        KK = row[9],
        SV = row[10]
        )
    for row in rows.fetchall()
    ]
if M902s is not None:
    dirname=os.path.dirname(__file__)
    path=os.path.join(dirname,'M902.json')
    outfile=open(path,'w',encoding='utf-8')
    json.dump(M902s,outfile,ensure_ascii=False,indent=4)
    outfile.close()
"""
