# M101_受注 cp932
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
    cn = sqlite3.connect('./DB603DAT.db')
    cn.isolation_level = None
    cn.row_factory = sqlite3.Row
    return cn

#定数
c受注ID= 0
c受注No= 1
c入力日付= 2
c日付= 3
c顧客検索= 4
c顧客ID= 5
c社員検索= 6
c社員ID= 7
c金額= 8
c備考= 9
cStatus= 10
cPCID= 11
cUserName= 12
c登録日= 13
c修正日= 14
c作成= 15
c登録= 16
c削除= 17
cKK= 18
cSV= 19

def get_drop_sql():
    wsql= 'DROP TABLE IF EXISTS M101_受注 '
    return wsql

def get_create_sql():
    wsql ='CREATE TABLE IF NOT EXISTS M101_受注 ('
    wsql+='受注ID INTEGER  DEFAULT 0 PRIMARY KEY,'
    wsql+='受注No INTEGER  DEFAULT 0,'
    wsql+='入力日付 TEXT  DEFAULT NULL,'
    wsql+='日付 TEXT  DEFAULT NULL,'
    wsql+='顧客検索 TEXT  DEFAULT NULL,'
    wsql+='顧客ID INTEGER  DEFAULT 0,'
    wsql+='社員検索 TEXT  DEFAULT NULL,'
    wsql+='社員ID INTEGER  DEFAULT 0,'
    wsql+='金額 INTEGER  DEFAULT 0,'
    wsql+='備考 TEXT  DEFAULT NULL,'
    wsql+='Status INTEGER  DEFAULT 0,'
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
    wsql+='受注ID, '
    wsql+='受注No, '
    wsql+='入力日付, '
    wsql+='日付, '
    wsql+='顧客検索, '
    wsql+='顧客ID, '
    wsql+='社員検索, '
    wsql+='社員ID, '
    wsql+='金額, '
    wsql+='備考, '
    wsql+='Status, '
    wsql+='PCID, '
    wsql+='UserName, '
    wsql+='登録日, '
    wsql+='修正日, '
    wsql+='作成, '
    wsql+='登録, '
    wsql+='削除, '
    wsql+='KK, '
    wsql+='SV '
    wsql+=' FROM M101_受注 '
    return wsql

def get_insert_sql():
    wsql ='INSERT INTO M101_受注 VALUES ('
    wsql+=':受注ID, '
    wsql+=':受注No, '
    wsql+=':入力日付, '
    wsql+=':日付, '
    wsql+=':顧客検索, '
    wsql+=':顧客ID, '
    wsql+=':社員検索, '
    wsql+=':社員ID, '
    wsql+=':金額, '
    wsql+=':備考, '
    wsql+=':Status, '
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
    wsql ='UPDATE M101_受注 SET '
    wsql+='受注No=:受注No, '
    wsql+='入力日付=:入力日付, '
    wsql+='日付=:日付, '
    wsql+='顧客検索=:顧客検索, '
    wsql+='顧客ID=:顧客ID, '
    wsql+='社員検索=:社員検索, '
    wsql+='社員ID=:社員ID, '
    wsql+='金額=:金額, '
    wsql+='備考=:備考, '
    wsql+='Status=:Status, '
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
    wsql= 'DELETE FROM M101_受注 '
    return wsql

def get_primarykerfilter(ID):
    if not str.isdecimal(str(ID)):
        ID = -1
    wID = str(ID)
    wfilter=' WHERE 受注ID = ' + wID +' '
    return wfilter

def get_M101(ID):
    wsql =get_select_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cur = cn.execute(wsql)
    data = cur.fetchone()
    return data
    cn.close()

@app.route('/')
@app.route('/M101_index', methods=['GET'])
def get_M101_index():
    cn = cn_open()
    wsql = 'SELECT * FROM M101_受注 '
    wsql+= 'ORDER BY  受注ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M101_index.html',rows = rows )
    cn.close()

@app.route('/M101_insert', methods=['GET'])
def get_M101_insert():
    return render_template('M101_insert.html')

@app.route('/M101_insert', methods=['POST'])
def post_M101_insert():
    wsql = get_insert_sql()
    w受注ID = request.form.get('受注ID')    #0
    w受注No = request.form.get('受注No')    #1
    w入力日付 = request.form.get('入力日付')    #2
    w日付 = request.form.get('日付')    #3
    w顧客検索 = request.form.get('顧客検索')    #4
    w顧客ID = request.form.get('顧客ID')    #5
    w社員検索 = request.form.get('社員検索')    #6
    w社員ID = request.form.get('社員ID')    #7
    w金額 = request.form.get('金額')    #8
    w備考 = request.form.get('備考')    #9
    wStatus = request.form.get('Status')    #10
    wPCID = request.form.get('PCID')    #11
    wUserName = request.form.get('UserName')    #12
    w登録日 = request.form.get('登録日')    #13
    w修正日 = request.form.get('修正日')    #14
    w作成 = request.form.get('作成')    #15
    w登録 = request.form.get('登録')    #16
    w削除 = request.form.get('削除')    #17
    wKK = request.form.get('KK')    #18
    wSV = request.form.get('SV')    #19
    cn = cn_open()
    row = (
        w受注ID,
        w受注No,
        w入力日付,
        w日付,
        w顧客検索,
        w顧客ID,
        w社員検索,
        w社員ID,
        w金額,
        w備考,
        wStatus,
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
    wsql = 'SELECT * FROM M101_受注 '
    wsql+= 'ORDER BY  受注ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M101_index.html',rows = rows )
    cn.close()

@app.route('/M101_detail/<ID>', methods=['GET'])
def get_M101_detail(ID):
    data = get_M101(ID)
    return render_template('M101_detail.html', M101=data)

@app.route('/M101_update/<ID>', methods=['GET'])
def get_M101_update(ID):
    data = get_M101(ID)
    return render_template('M101_update.html', M101=data)

@app.route('/M101_update/<ID>', methods=['POST'])
def post_M101_update(ID):
    data = get_M101(ID)
    wsql = get_update_sql()
    wsql+=get_primarykerfilter(ID)
    w受注No = request.form.get('受注No')    #1
    w入力日付 = request.form.get('入力日付')    #2
    w日付 = request.form.get('日付')    #3
    w顧客検索 = request.form.get('顧客検索')    #4
    w顧客ID = request.form.get('顧客ID')    #5
    w社員検索 = request.form.get('社員検索')    #6
    w社員ID = request.form.get('社員ID')    #7
    w金額 = request.form.get('金額')    #8
    w備考 = request.form.get('備考')    #9
    wStatus = request.form.get('Status')    #10
    wPCID = request.form.get('PCID')    #11
    wUserName = request.form.get('UserName')    #12
    w登録日 = request.form.get('登録日')    #13
    w修正日 = request.form.get('修正日')    #14
    w作成 = request.form.get('作成')    #15
    w登録 = request.form.get('登録')    #16
    w削除 = request.form.get('削除')    #17
    wKK = request.form.get('KK')    #18
    wSV = request.form.get('SV')    #19
    cn = cn_open()
    row = {
        '受注No':w受注No,
        '入力日付':w入力日付,
        '日付':w日付,
        '顧客検索':w顧客検索,
        '顧客ID':w顧客ID,
        '社員検索':w社員検索,
        '社員ID':w社員ID,
        '金額':w金額,
        '備考':w備考,
        'Status':wStatus,
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

    data = get_M101(ID)
    return render_template('M101_detail.html', M101=data)


@app.route('/M101_delete/<ID>', methods=['GET'])
def get_M101_delete(ID):
    wsql = get_delete_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cn.execute(wsql)
    wsql = 'SELECT * FROM M101_受注 '
    wsql+= 'ORDER BY  受注ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M101_index.html',rows = rows )
    cn.close()

@app.route('/M101_importcsv',methods=['GET'])
def get_M101_importcsv():
    cn = cn_open()
    wsql=get_insert_sql()
    rows = pd.read_csv('M101.csv', encoding='cp932')
    for row in rows.values:
        print(row[0])
        cn.execute(wsql, row)
    cn.close()

@app.route('/M101_exportjson',methods=['GET'])
def get_M101_exportjson():
    wsql = M101_select_sql
    n = cn_open()
    rows = cn.execute(wsql)
    M101s=[
    dict(
        受注ID = row[0],
        受注No = row[1],
        入力日付 = row[2],
        日付 = row[3],
        顧客検索 = row[4],
        顧客ID = row[5],
        社員検索 = row[6],
        社員ID = row[7],
        金額 = row[8],
        備考 = row[9],
        Status = row[10],
        PCID = row[11],
        UserName = row[12],
        登録日 = row[13],
        修正日 = row[14],
        作成 = row[15],
        登録 = row[16],
        削除 = row[17],
        KK = row[18],
        SV = row[19]
        )
     for row in rows.fetchall()
    ]
    cn.close()
    if M101s is not None:
        return json.dump(M101s,ensure_ascii=False,indent=4)

@app.route('/M101_initialize',methods=['GET'])
def get_M101_initialize():

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
    M101s=[
        dict(
            受注ID = row[0],
            受注No = row[1],
            入力日付 = row[2],
            日付 = row[3],
            顧客検索 = row[4],
            顧客ID = row[5],
            社員検索 = row[6],
            社員ID = row[7],
            金額 = row[8],
            備考 = row[9],
            Status = row[10],
            PCID = row[11],
            UserName = row[12],
            登録日 = row[13],
            修正日 = row[14],
            作成 = row[15],
            登録 = row[16],
            削除 = row[17],
            KK = row[18],
            SV = row[19]
            )
        for row in rows.fetchall()
        ]
    if M101s is not None:
        dirname=os.path.dirname(__file__)
        path=os.path.join(dirname,'M101.json')
        outfile=open(path,'w',encoding='utf-8')
        json.dump(M101s,outfile,ensure_ascii=False,indent=4)
        outfile.close()


if __name__ == '__main__':
    app.debug = True
    #get_M101_initialize()

"""

@app.route('/M101_index', methods=['GET'])
def get_M101_index():
    return M101.get_M101_index()

@app.route('/M101_insert', methods=['GET'])
def get_M101_insert():
    return M101.get_M101_insert()

@app.route('/M101_insert', methods=['POST'])
def post_M101_insert():
    return M101.post_M101_insert()

@app.route('/M101_importcsv', methods=['GET'])
def get_M101_jimportcsv():
    M101.get_M101_importcsv()
    return M101.get_M101_index()

@app.route('/M101_json', methods=['GET'])
def get_M101_json():
    return M101.get_M101_json()

@app.route('/M101_detail/<ID>', methods=['GET'])
def get_M101_detail(ID):
    return M101.get_M101_detail(ID)

@app.route('/M101_update/<ID>', methods=['GET'])
def get_M101_update(ID):
    return M101.get_M101_update(ID)

@app.route('/M101_update/<ID>', methods=['POST'])
def post_M101_update(ID):
    return M101.post_M101_update(ID)

@app.route('/M101_delete/<ID>', methods=['GET'])
def get_M101_delete(ID):
    return M101.get_M101_index(ID)

#createtableM101.py
# -*- coding: utf-8 -*-

import sqlite3
        
dbname = './DB603DAT.db'
cn = sqlite3.connect(dbname)
cn.execute ('PRAGMA foreign_keys = 1')
#cn.execute ('DROP TABLE  M101_受注)

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
M101s=[
    dict(
        受注ID = row[0],
        受注No = row[1],
        入力日付 = row[2],
        日付 = row[3],
        顧客検索 = row[4],
        顧客ID = row[5],
        社員検索 = row[6],
        社員ID = row[7],
        金額 = row[8],
        備考 = row[9],
        Status = row[10],
        PCID = row[11],
        UserName = row[12],
        登録日 = row[13],
        修正日 = row[14],
        作成 = row[15],
        登録 = row[16],
        削除 = row[17],
        KK = row[18],
        SV = row[19]
        )
    for row in rows.fetchall()
    ]
if M101s is not None:
    dirname=os.path.dirname(__file__)
    path=os.path.join(dirname,'M101.json')
    outfile=open(path,'w',encoding='utf-8')
    json.dump(M101s,outfile,ensure_ascii=False,indent=4)
    outfile.close()
"""
