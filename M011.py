# M011_顧客 cp932
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
c顧客ID= 0
c顧客No= 1
c顧客名= 2
cふりがな= 3
c郵便番号= 4
c住所1= 5
c住所2= 6
cTEL= 7
cFAX= 8
c備考= 9
c表示= 10
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
    wsql= 'DROP TABLE IF EXISTS M011_顧客 '
    return wsql

def get_create_sql():
    wsql ='CREATE TABLE IF NOT EXISTS M011_顧客 ('
    wsql+='顧客ID INTEGER  DEFAULT 0 PRIMARY KEY,'
    wsql+='顧客No INTEGER  DEFAULT 0,'
    wsql+='顧客名 TEXT  DEFAULT NULL,'
    wsql+='ふりがな TEXT  DEFAULT NULL,'
    wsql+='郵便番号 TEXT  DEFAULT NULL,'
    wsql+='住所1 TEXT  DEFAULT NULL,'
    wsql+='住所2 TEXT  DEFAULT NULL,'
    wsql+='TEL TEXT  DEFAULT NULL,'
    wsql+='FAX TEXT  DEFAULT NULL,'
    wsql+='備考 TEXT  DEFAULT NULL,'
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
    wsql+='顧客ID, '
    wsql+='顧客No, '
    wsql+='顧客名, '
    wsql+='ふりがな, '
    wsql+='郵便番号, '
    wsql+='住所1, '
    wsql+='住所2, '
    wsql+='TEL, '
    wsql+='FAX, '
    wsql+='備考, '
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
    wsql+=' FROM M011_顧客 '
    return wsql

def get_insert_sql():
    wsql ='INSERT INTO M011_顧客 VALUES ('
    wsql+=':顧客ID, '
    wsql+=':顧客No, '
    wsql+=':顧客名, '
    wsql+=':ふりがな, '
    wsql+=':郵便番号, '
    wsql+=':住所1, '
    wsql+=':住所2, '
    wsql+=':TEL, '
    wsql+=':FAX, '
    wsql+=':備考, '
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
    wsql ='UPDATE M011_顧客 SET '
    wsql+='顧客No=:顧客No, '
    wsql+='顧客名=:顧客名, '
    wsql+='ふりがな=:ふりがな, '
    wsql+='郵便番号=:郵便番号, '
    wsql+='住所1=:住所1, '
    wsql+='住所2=:住所2, '
    wsql+='TEL=:TEL, '
    wsql+='FAX=:FAX, '
    wsql+='備考=:備考, '
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
    wsql= 'DELETE FROM M011_顧客 '
    return wsql

def get_primarykerfilter(ID):
    if not str.isdecimal(str(ID)):
        ID = -1
    wID = str(ID)
    wfilter=' WHERE 顧客ID = ' + wID +' '
    return wfilter

def get_M011(ID):
    wsql =get_select_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cur = cn.execute(wsql)
    data = cur.fetchone()
    return data
    cn.close()

@app.route('/')
@app.route('/M011_index', methods=['GET'])
def get_M011_index():
    cn = cn_open()
    wsql = 'SELECT * FROM M011_顧客 '
    wsql+= 'ORDER BY  顧客ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M011_index.html',rows = rows )
    cn.close()

@app.route('/M011_insert', methods=['GET'])
def get_M011_insert():
    return render_template('M011_insert.html')

@app.route('/M011_insert', methods=['POST'])
def post_M011_insert():
    wsql = get_insert_sql()
    w顧客ID = request.form.get('顧客ID')    #0
    w顧客No = request.form.get('顧客No')    #1
    w顧客名 = request.form.get('顧客名')    #2
    wふりがな = request.form.get('ふりがな')    #3
    w郵便番号 = request.form.get('郵便番号')    #4
    w住所1 = request.form.get('住所1')    #5
    w住所2 = request.form.get('住所2')    #6
    wTEL = request.form.get('TEL')    #7
    wFAX = request.form.get('FAX')    #8
    w備考 = request.form.get('備考')    #9
    w表示 = request.form.get('表示')    #10
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
        w顧客ID,
        w顧客No,
        w顧客名,
        wふりがな,
        w郵便番号,
        w住所1,
        w住所2,
        wTEL,
        wFAX,
        w備考,
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
    wsql = 'SELECT * FROM M011_顧客 '
    wsql+= 'ORDER BY  顧客ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M011_index.html',rows = rows )
    cn.close()

@app.route('/M011_detail/<ID>', methods=['GET'])
def get_M011_detail(ID):
    data = get_M011(ID)
    return render_template('M011_detail.html', M011=data)

@app.route('/M011_update/<ID>', methods=['GET'])
def get_M011_update(ID):
    data = get_M011(ID)
    return render_template('M011_update.html', M011=data)

@app.route('/M011_update/<ID>', methods=['POST'])
def post_M011_update(ID):
    data = get_M011(ID)
    wsql = get_update_sql()
    wsql+=get_primarykerfilter(ID)
    w顧客No = request.form.get('顧客No')    #1
    w顧客名 = request.form.get('顧客名')    #2
    wふりがな = request.form.get('ふりがな')    #3
    w郵便番号 = request.form.get('郵便番号')    #4
    w住所1 = request.form.get('住所1')    #5
    w住所2 = request.form.get('住所2')    #6
    wTEL = request.form.get('TEL')    #7
    wFAX = request.form.get('FAX')    #8
    w備考 = request.form.get('備考')    #9
    w表示 = request.form.get('表示')    #10
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
        '顧客No':w顧客No,
        '顧客名':w顧客名,
        'ふりがな':wふりがな,
        '郵便番号':w郵便番号,
        '住所1':w住所1,
        '住所2':w住所2,
        'TEL':wTEL,
        'FAX':wFAX,
        '備考':w備考,
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

    data = get_M011(ID)
    return render_template('M011_detail.html', M011=data)


@app.route('/M011_delete/<ID>', methods=['GET'])
def get_M011_delete(ID):
    wsql = get_delete_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cn.execute(wsql)
    wsql = 'SELECT * FROM M011_顧客 '
    wsql+= 'ORDER BY  顧客ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M011_index.html',rows = rows )
    cn.close()

@app.route('/M011_importcsv',methods=['GET'])
def get_M011_importcsv():
    cn = cn_open()
    wsql=get_insert_sql()
    rows = pd.read_csv('M011.csv', encoding='cp932')
    for row in rows.values:
        print(row[0])
        cn.execute(wsql, row)
    cn.close()

@app.route('/M011_exportjson',methods=['GET'])
def get_M011_exportjson():
    wsql = M011_select_sql
    n = cn_open()
    rows = cn.execute(wsql)
    M011s=[
    dict(
        顧客ID = row[0],
        顧客No = row[1],
        顧客名 = row[2],
        ふりがな = row[3],
        郵便番号 = row[4],
        住所1 = row[5],
        住所2 = row[6],
        TEL = row[7],
        FAX = row[8],
        備考 = row[9],
        表示 = row[10],
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
    if M011s is not None:
        return json.dump(M011s,ensure_ascii=False,indent=4)

@app.route('/M011_initialize',methods=['GET'])
def get_M011_initialize():

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
    M011s=[
        dict(
            顧客ID = row[0],
            顧客No = row[1],
            顧客名 = row[2],
            ふりがな = row[3],
            郵便番号 = row[4],
            住所1 = row[5],
            住所2 = row[6],
            TEL = row[7],
            FAX = row[8],
            備考 = row[9],
            表示 = row[10],
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
    if M011s is not None:
        dirname=os.path.dirname(__file__)
        path=os.path.join(dirname,'M011.json')
        outfile=open(path,'w',encoding='utf-8')
        json.dump(M011s,outfile,ensure_ascii=False,indent=4)
        outfile.close()


if __name__ == '__main__':
    app.debug = True
    #get_M011_initialize()

"""

@app.route('/M011_index', methods=['GET'])
def get_M011_index():
    return M011.get_M011_index()

@app.route('/M011_insert', methods=['GET'])
def get_M011_insert():
    return M011.get_M011_insert()

@app.route('/M011_insert', methods=['POST'])
def post_M011_insert():
    return M011.post_M011_insert()

@app.route('/M011_importcsv', methods=['GET'])
def get_M011_jimportcsv():
    M011.get_M011_importcsv()
    return M011.get_M011_index()

@app.route('/M011_json', methods=['GET'])
def get_M011_json():
    return M011.get_M011_json()

@app.route('/M011_detail/<ID>', methods=['GET'])
def get_M011_detail(ID):
    return M011.get_M011_detail(ID)

@app.route('/M011_update/<ID>', methods=['GET'])
def get_M011_update(ID):
    return M011.get_M011_update(ID)

@app.route('/M011_update/<ID>', methods=['POST'])
def post_M011_update(ID):
    return M011.post_M011_update(ID)

@app.route('/M011_delete/<ID>', methods=['GET'])
def get_M011_delete(ID):
    return M011.get_M011_index(ID)

#createtableM011.py
# -*- coding: utf-8 -*-

import sqlite3
        
dbname = 'DB603DAT.db'
cn = sqlite3.connect(dbname)
cn.execute ('PRAGMA foreign_keys = 1')
#cn.execute ('DROP TABLE  M011_顧客)

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
M011s=[
    dict(
        顧客ID = row[0],
        顧客No = row[1],
        顧客名 = row[2],
        ふりがな = row[3],
        郵便番号 = row[4],
        住所1 = row[5],
        住所2 = row[6],
        TEL = row[7],
        FAX = row[8],
        備考 = row[9],
        表示 = row[10],
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
if M011s is not None:
    dirname=os.path.dirname(__file__)
    path=os.path.join(dirname,'M011.json')
    outfile=open(path,'w',encoding='utf-8')
    json.dump(M011s,outfile,ensure_ascii=False,indent=4)
    outfile.close()
"""
