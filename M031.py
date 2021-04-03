# M031_社員 cp932
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
c社員ID= 0
c社員No= 1
c社員名= 2
cふりがな= 3
c表示= 4
cPCID= 5
cUserName= 6
c登録日= 7
c修正日= 8
c作成= 9
c登録= 10
c削除= 11
cKK= 12
cSV= 13

def get_drop_sql():
    wsql= 'DROP TABLE IF EXISTS M031_社員 '
    return wsql

def get_create_sql():
    wsql ='CREATE TABLE IF NOT EXISTS M031_社員 ('
    wsql+='社員ID INTEGER  DEFAULT 0 PRIMARY KEY,'
    wsql+='社員No INTEGER  DEFAULT 0,'
    wsql+='社員名 TEXT  DEFAULT NULL,'
    wsql+='ふりがな TEXT  DEFAULT NULL,'
    wsql+='表示 INTEGER  DEFAULT 0,'
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
    wsql+='社員ID, '
    wsql+='社員No, '
    wsql+='社員名, '
    wsql+='ふりがな, '
    wsql+='表示, '
    wsql+='PCID, '
    wsql+='UserName, '
    wsql+='登録日, '
    wsql+='修正日, '
    wsql+='作成, '
    wsql+='登録, '
    wsql+='削除, '
    wsql+='KK, '
    wsql+='SV '
    wsql+=' FROM M031_社員 '
    return wsql

def get_insert_sql():
    wsql ='INSERT INTO M031_社員 VALUES ('
    wsql+=':社員ID, '
    wsql+=':社員No, '
    wsql+=':社員名, '
    wsql+=':ふりがな, '
    wsql+=':表示, '
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
    wsql ='UPDATE M031_社員 SET '
    wsql+='社員No=:社員No, '
    wsql+='社員名=:社員名, '
    wsql+='ふりがな=:ふりがな, '
    wsql+='表示=:表示, '
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
    wsql= 'DELETE FROM M031_社員 '
    return wsql

def get_primarykerfilter(ID):
    if not str.isdecimal(str(ID)):
        ID = -1
    wID = str(ID)
    wfilter=' WHERE 社員ID = ' + wID +' '
    return wfilter

def get_M031(ID):
    wsql =get_select_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cur = cn.execute(wsql)
    data = cur.fetchone()
    return data
    cn.close()

@app.route('/')
@app.route('/M031_index', methods=['GET'])
def get_M031_index():
    cn = cn_open()
    wsql = 'SELECT * FROM M031_社員 '
    wsql+= 'ORDER BY  社員ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M031_index.html',rows = rows )
    cn.close()

@app.route('/M031_insert', methods=['GET'])
def get_M031_insert():
    return render_template('M031_insert.html')

@app.route('/M031_insert', methods=['POST'])
def post_M031_insert():
    wsql = get_insert_sql()
    w社員ID = request.form.get('社員ID')    #0
    w社員No = request.form.get('社員No')    #1
    w社員名 = request.form.get('社員名')    #2
    wふりがな = request.form.get('ふりがな')    #3
    w表示 = request.form.get('表示')    #4
    wPCID = request.form.get('PCID')    #5
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
        w社員ID,
        w社員No,
        w社員名,
        wふりがな,
        w表示,
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
    wsql = 'SELECT * FROM M031_社員 '
    wsql+= 'ORDER BY  社員ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M031_index.html',rows = rows )
    cn.close()

@app.route('/M031_detail/<ID>', methods=['GET'])
def get_M031_detail(ID):
    data = get_M031(ID)
    return render_template('M031_detail.html', M031=data)

@app.route('/M031_update/<ID>', methods=['GET'])
def get_M031_update(ID):
    data = get_M031(ID)
    return render_template('M031_update.html', M031=data)

@app.route('/M031_update/<ID>', methods=['POST'])
def post_M031_update(ID):
    data = get_M031(ID)
    wsql = get_update_sql()
    wsql+=get_primarykerfilter(ID)
    w社員No = request.form.get('社員No')    #1
    w社員名 = request.form.get('社員名')    #2
    wふりがな = request.form.get('ふりがな')    #3
    w表示 = request.form.get('表示')    #4
    wPCID = request.form.get('PCID')    #5
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
        '社員No':w社員No,
        '社員名':w社員名,
        'ふりがな':wふりがな,
        '表示':w表示,
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

    data = get_M031(ID)
    return render_template('M031_detail.html', M031=data)


@app.route('/M031_delete/<ID>', methods=['GET'])
def get_M031_delete(ID):
    wsql = get_delete_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cn.execute(wsql)
    wsql = 'SELECT * FROM M031_社員 '
    wsql+= 'ORDER BY  社員ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M031_index.html',rows = rows )
    cn.close()

@app.route('/M031_importcsv',methods=['GET'])
def get_M031_importcsv():
    cn = cn_open()
    wsql=get_insert_sql()
    rows = pd.read_csv('M031.csv', encoding='cp932')
    for row in rows.values:
        print(row[0])
        cn.execute(wsql, row)
    cn.close()

@app.route('/M031_exportjson',methods=['GET'])
def get_M031_exportjson():
    wsql = M031_select_sql
    n = cn_open()
    rows = cn.execute(wsql)
    M031s=[
    dict(
        社員ID = row[0],
        社員No = row[1],
        社員名 = row[2],
        ふりがな = row[3],
        表示 = row[4],
        PCID = row[5],
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
    if M031s is not None:
        return json.dump(M031s,ensure_ascii=False,indent=4)

@app.route('/M031_initialize',methods=['GET'])
def get_M031_initialize():

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
    M031s=[
        dict(
            社員ID = row[0],
            社員No = row[1],
            社員名 = row[2],
            ふりがな = row[3],
            表示 = row[4],
            PCID = row[5],
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
    if M031s is not None:
        dirname=os.path.dirname(__file__)
        path=os.path.join(dirname,'M031.json')
        outfile=open(path,'w',encoding='utf-8')
        json.dump(M031s,outfile,ensure_ascii=False,indent=4)
        outfile.close()


if __name__ == '__main__':
    app.debug = True
    #get_M031_initialize()

"""

@app.route('/M031_index', methods=['GET'])
def get_M031_index():
    return M031.get_M031_index()

@app.route('/M031_insert', methods=['GET'])
def get_M031_insert():
    return M031.get_M031_insert()

@app.route('/M031_insert', methods=['POST'])
def post_M031_insert():
    return M031.post_M031_insert()

@app.route('/M031_importcsv', methods=['GET'])
def get_M031_jimportcsv():
    M031.get_M031_importcsv()
    return M031.get_M031_index()

@app.route('/M031_json', methods=['GET'])
def get_M031_json():
    return M031.get_M031_json()

@app.route('/M031_detail/<ID>', methods=['GET'])
def get_M031_detail(ID):
    return M031.get_M031_detail(ID)

@app.route('/M031_update/<ID>', methods=['GET'])
def get_M031_update(ID):
    return M031.get_M031_update(ID)

@app.route('/M031_update/<ID>', methods=['POST'])
def post_M031_update(ID):
    return M031.post_M031_update(ID)

@app.route('/M031_delete/<ID>', methods=['GET'])
def get_M031_delete(ID):
    return M031.get_M031_index(ID)

#createtableM031.py
# -*- coding: utf-8 -*-

import sqlite3
        
dbname = 'DB603DAT.db'
cn = sqlite3.connect(dbname)
cn.execute ('PRAGMA foreign_keys = 1')
#cn.execute ('DROP TABLE  M031_社員)

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
M031s=[
    dict(
        社員ID = row[0],
        社員No = row[1],
        社員名 = row[2],
        ふりがな = row[3],
        表示 = row[4],
        PCID = row[5],
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
if M031s is not None:
    dirname=os.path.dirname(__file__)
    path=os.path.join(dirname,'M031.json')
    outfile=open(path,'w',encoding='utf-8')
    json.dump(M031s,outfile,ensure_ascii=False,indent=4)
    outfile.close()
"""
