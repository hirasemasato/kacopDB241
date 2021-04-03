# M901_端末 cp932
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
cPCID= 0
cDEFALTPRINTER= 1
cDOTPRINTER= 2
cVERSION= 3
cVERSIONID= 4
c更新済= 5
cUserName= 6
c登録日= 7
c修正日= 8
c作成= 9
c登録= 10
c削除= 11
cKK= 12
cSV= 13

def get_drop_sql():
    wsql= 'DROP TABLE IF EXISTS M901_端末 '
    return wsql

def get_create_sql():
    wsql ='CREATE TABLE IF NOT EXISTS M901_端末 ('
    wsql+='PCID INTEGER  DEFAULT 0 PRIMARY KEY,'
    wsql+='DEFALTPRINTER TEXT  DEFAULT NULL,'
    wsql+='DOTPRINTER TEXT  DEFAULT NULL,'
    wsql+='VERSION TEXT  DEFAULT NULL,'
    wsql+='VERSIONID INTEGER  DEFAULT 0,'
    wsql+='更新済 INTEGER  DEFAULT 0,'
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
    wsql+='PCID, '
    wsql+='DEFALTPRINTER, '
    wsql+='DOTPRINTER, '
    wsql+='VERSION, '
    wsql+='VERSIONID, '
    wsql+='更新済, '
    wsql+='UserName, '
    wsql+='登録日, '
    wsql+='修正日, '
    wsql+='作成, '
    wsql+='登録, '
    wsql+='削除, '
    wsql+='KK, '
    wsql+='SV '
    wsql+=' FROM M901_端末 '
    return wsql

def get_insert_sql():
    wsql ='INSERT INTO M901_端末 VALUES ('
    wsql+=':PCID, '
    wsql+=':DEFALTPRINTER, '
    wsql+=':DOTPRINTER, '
    wsql+=':VERSION, '
    wsql+=':VERSIONID, '
    wsql+=':更新済, '
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
    wsql ='UPDATE M901_端末 SET '
    wsql+='DEFALTPRINTER=:DEFALTPRINTER, '
    wsql+='DOTPRINTER=:DOTPRINTER, '
    wsql+='VERSION=:VERSION, '
    wsql+='VERSIONID=:VERSIONID, '
    wsql+='更新済=:更新済, '
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
    wsql= 'DELETE FROM M901_端末 '
    return wsql

def get_primarykerfilter(ID):
    if not str.isdecimal(str(ID)):
        ID = -1
    wID = str(ID)
    wfilter=' WHERE PCID = ' + wID +' '
    return wfilter

def get_M901(ID):
    wsql =get_select_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cur = cn.execute(wsql)
    data = cur.fetchone()
    return data
    cn.close()

@app.route('/')
@app.route('/M901_index', methods=['GET'])
def get_M901_index():
    cn = cn_open()
    wsql = 'SELECT * FROM M901_端末 '
    wsql+= 'ORDER BY  PCID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M901_index.html',rows = rows )
    cn.close()

@app.route('/M901_insert', methods=['GET'])
def get_M901_insert():
    return render_template('M901_insert.html')

@app.route('/M901_insert', methods=['POST'])
def post_M901_insert():
    wsql = get_insert_sql()
    wPCID = request.form.get('PCID')    #0
    wDEFALTPRINTER = request.form.get('DEFALTPRINTER')    #1
    wDOTPRINTER = request.form.get('DOTPRINTER')    #2
    wVERSION = request.form.get('VERSION')    #3
    wVERSIONID = request.form.get('VERSIONID')    #4
    w更新済 = request.form.get('更新済')    #5
    wUserName = request.form.get('UserName')    #6
    w登録日 = request.form.get('登録日')    #7
    w修正日 = request.form.get('修正日')    #8
    w作成 = request.form.get('作成')    #9
    w登録 = request.form.get('登録')    #10
    w削除 = request.form.get('削除')    #11
    wKK = request.form.get('KK')    #12
    wSV = request.form.get('SV')    #13
    cn = cn_open()
    row = (
        wPCID,
        wDEFALTPRINTER,
        wDOTPRINTER,
        wVERSION,
        wVERSIONID,
        w更新済,
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
    wsql = 'SELECT * FROM M901_端末 '
    wsql+= 'ORDER BY  PCID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M901_index.html',rows = rows )
    cn.close()

@app.route('/M901_detail/<ID>', methods=['GET'])
def get_M901_detail(ID):
    data = get_M901(ID)
    return render_template('M901_detail.html', M901=data)

@app.route('/M901_update/<ID>', methods=['GET'])
def get_M901_update(ID):
    data = get_M901(ID)
    return render_template('M901_update.html', M901=data)

@app.route('/M901_update/<ID>', methods=['POST'])
def post_M901_update(ID):
    data = get_M901(ID)
    wsql = get_update_sql()
    wsql+=get_primarykerfilter(ID)
    wDEFALTPRINTER = request.form.get('DEFALTPRINTER')    #1
    wDOTPRINTER = request.form.get('DOTPRINTER')    #2
    wVERSION = request.form.get('VERSION')    #3
    wVERSIONID = request.form.get('VERSIONID')    #4
    w更新済 = request.form.get('更新済')    #5
    wUserName = request.form.get('UserName')    #6
    w登録日 = request.form.get('登録日')    #7
    w修正日 = request.form.get('修正日')    #8
    w作成 = request.form.get('作成')    #9
    w登録 = request.form.get('登録')    #10
    w削除 = request.form.get('削除')    #11
    wKK = request.form.get('KK')    #12
    wSV = request.form.get('SV')    #13
    cn = cn_open()
    row = {
        'DEFALTPRINTER':wDEFALTPRINTER,
        'DOTPRINTER':wDOTPRINTER,
        'VERSION':wVERSION,
        'VERSIONID':wVERSIONID,
        '更新済':w更新済,
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

    data = get_M901(ID)
    return render_template('M901_detail.html', M901=data)


@app.route('/M901_delete/<ID>', methods=['GET'])
def get_M901_delete(ID):
    wsql = get_delete_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cn.execute(wsql)
    wsql = 'SELECT * FROM M901_端末 '
    wsql+= 'ORDER BY  PCID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M901_index.html',rows = rows )
    cn.close()

@app.route('/M901_importcsv',methods=['GET'])
def get_M901_importcsv():
    cn = cn_open()
    wsql=get_insert_sql()
    rows = pd.read_csv('M901.csv', encoding='cp932')
    for row in rows.values:
        print(row[0])
        cn.execute(wsql, row)
    cn.close()

@app.route('/M901_exportjson',methods=['GET'])
def get_M901_exportjson():
    wsql = M901_select_sql
    n = cn_open()
    rows = cn.execute(wsql)
    M901s=[
    dict(
        PCID = row[0],
        DEFALTPRINTER = row[1],
        DOTPRINTER = row[2],
        VERSION = row[3],
        VERSIONID = row[4],
        更新済 = row[5],
        UserName = row[6],
        登録日 = row[7],
        修正日 = row[8],
        作成 = row[9],
        登録 = row[10],
        削除 = row[11],
        KK = row[12],
        SV = row[13]
        )
     for row in rows.fetchall()
    ]
    cn.close()
    if M901s is not None:
        return json.dump(M901s,ensure_ascii=False,indent=4)

@app.route('/M901_initialize',methods=['GET'])
def get_M901_initialize():

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
    M901s=[
        dict(
            PCID = row[0],
            DEFALTPRINTER = row[1],
            DOTPRINTER = row[2],
            VERSION = row[3],
            VERSIONID = row[4],
            更新済 = row[5],
            UserName = row[6],
            登録日 = row[7],
            修正日 = row[8],
            作成 = row[9],
            登録 = row[10],
            削除 = row[11],
            KK = row[12],
            SV = row[13]
            )
        for row in rows.fetchall()
        ]
    if M901s is not None:
        dirname=os.path.dirname(__file__)
        path=os.path.join(dirname,'M901.json')
        outfile=open(path,'w',encoding='utf-8')
        json.dump(M901s,outfile,ensure_ascii=False,indent=4)
        outfile.close()


if __name__ == '__main__':
    app.debug = True
    #get_M901_initialize()

"""

@app.route('/M901_index', methods=['GET'])
def get_M901_index():
    return M901.get_M901_index()

@app.route('/M901_insert', methods=['GET'])
def get_M901_insert():
    return M901.get_M901_insert()

@app.route('/M901_insert', methods=['POST'])
def post_M901_insert():
    return M901.post_M901_insert()

@app.route('/M901_importcsv', methods=['GET'])
def get_M901_jimportcsv():
    M901.get_M901_importcsv()
    return M901.get_M901_index()

@app.route('/M901_json', methods=['GET'])
def get_M901_json():
    return M901.get_M901_json()

@app.route('/M901_detail/<ID>', methods=['GET'])
def get_M901_detail(ID):
    return M901.get_M901_detail(ID)

@app.route('/M901_update/<ID>', methods=['GET'])
def get_M901_update(ID):
    return M901.get_M901_update(ID)

@app.route('/M901_update/<ID>', methods=['POST'])
def post_M901_update(ID):
    return M901.post_M901_update(ID)

@app.route('/M901_delete/<ID>', methods=['GET'])
def get_M901_delete(ID):
    return M901.get_M901_index(ID)

#createtableM901.py
# -*- coding: utf-8 -*-

import sqlite3
        
dbname = 'DB603DAT.db'
cn = sqlite3.connect(dbname)
cn.execute ('PRAGMA foreign_keys = 1')
#cn.execute ('DROP TABLE  M901_端末)

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
M901s=[
    dict(
        PCID = row[0],
        DEFALTPRINTER = row[1],
        DOTPRINTER = row[2],
        VERSION = row[3],
        VERSIONID = row[4],
        更新済 = row[5],
        UserName = row[6],
        登録日 = row[7],
        修正日 = row[8],
        作成 = row[9],
        登録 = row[10],
        削除 = row[11],
        KK = row[12],
        SV = row[13]
        )
    for row in rows.fetchall()
    ]
if M901s is not None:
    dirname=os.path.dirname(__file__)
    path=os.path.join(dirname,'M901.json')
    outfile=open(path,'w',encoding='utf-8')
    json.dump(M901s,outfile,ensure_ascii=False,indent=4)
    outfile.close()
"""
