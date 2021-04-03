# M900_自社 cp932
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
c自社ID= 0
c自社名= 1
c代表者名= 2
c郵便番号= 3
c住所= 4
cTEL= 5
cFAX= 6
c振込先1= 7
c振込先2= 8
c振込先3= 9
c振込先4= 10
c振込先5= 11
c振込先6= 12
c締日= 13
c一般原価率= 14
cASKL原価率= 15
cロゴ印刷= 16
c決算確定日= 17
c終了処理= 18
cPCID= 19
cUserName= 20
c登録日= 21
c修正日= 22
c作成= 23
c登録= 24
c削除= 25
cKK= 26
cSV= 27

def get_drop_sql():
    wsql= 'DROP TABLE IF EXISTS M900_自社 '
    return wsql

def get_create_sql():
    wsql ='CREATE TABLE IF NOT EXISTS M900_自社 ('
    wsql+='自社ID INTEGER  DEFAULT 0 PRIMARY KEY,'
    wsql+='自社名 TEXT  DEFAULT NULL,'
    wsql+='代表者名 TEXT  DEFAULT NULL,'
    wsql+='郵便番号 TEXT  DEFAULT NULL,'
    wsql+='住所 TEXT  DEFAULT NULL,'
    wsql+='TEL TEXT  DEFAULT NULL,'
    wsql+='FAX TEXT  DEFAULT NULL,'
    wsql+='振込先1 TEXT  DEFAULT NULL,'
    wsql+='振込先2 TEXT  DEFAULT NULL,'
    wsql+='振込先3 TEXT  DEFAULT NULL,'
    wsql+='振込先4 TEXT  DEFAULT NULL,'
    wsql+='振込先5 TEXT  DEFAULT NULL,'
    wsql+='振込先6 TEXT  DEFAULT NULL,'
    wsql+='締日 INTEGER  DEFAULT 0,'
    wsql+='一般原価率 INTEGER  DEFAULT 0,'
    wsql+='ASKL原価率 INTEGER  DEFAULT 0,'
    wsql+='ロゴ印刷 INTEGER  DEFAULT 0,'
    wsql+='決算確定日 TEXT  DEFAULT NULL,'
    wsql+='終了処理 TEXT  DEFAULT NULL,'
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
    wsql+='自社ID, '
    wsql+='自社名, '
    wsql+='代表者名, '
    wsql+='郵便番号, '
    wsql+='住所, '
    wsql+='TEL, '
    wsql+='FAX, '
    wsql+='振込先1, '
    wsql+='振込先2, '
    wsql+='振込先3, '
    wsql+='振込先4, '
    wsql+='振込先5, '
    wsql+='振込先6, '
    wsql+='締日, '
    wsql+='一般原価率, '
    wsql+='ASKL原価率, '
    wsql+='ロゴ印刷, '
    wsql+='決算確定日, '
    wsql+='終了処理, '
    wsql+='PCID, '
    wsql+='UserName, '
    wsql+='登録日, '
    wsql+='修正日, '
    wsql+='作成, '
    wsql+='登録, '
    wsql+='削除, '
    wsql+='KK, '
    wsql+='SV '
    wsql+=' FROM M900_自社 '
    return wsql

def get_insert_sql():
    wsql ='INSERT INTO M900_自社 VALUES ('
    wsql+=':自社ID, '
    wsql+=':自社名, '
    wsql+=':代表者名, '
    wsql+=':郵便番号, '
    wsql+=':住所, '
    wsql+=':TEL, '
    wsql+=':FAX, '
    wsql+=':振込先1, '
    wsql+=':振込先2, '
    wsql+=':振込先3, '
    wsql+=':振込先4, '
    wsql+=':振込先5, '
    wsql+=':振込先6, '
    wsql+=':締日, '
    wsql+=':一般原価率, '
    wsql+=':ASKL原価率, '
    wsql+=':ロゴ印刷, '
    wsql+=':決算確定日, '
    wsql+=':終了処理, '
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
    wsql ='UPDATE M900_自社 SET '
    wsql+='自社名=:自社名, '
    wsql+='代表者名=:代表者名, '
    wsql+='郵便番号=:郵便番号, '
    wsql+='住所=:住所, '
    wsql+='TEL=:TEL, '
    wsql+='FAX=:FAX, '
    wsql+='振込先1=:振込先1, '
    wsql+='振込先2=:振込先2, '
    wsql+='振込先3=:振込先3, '
    wsql+='振込先4=:振込先4, '
    wsql+='振込先5=:振込先5, '
    wsql+='振込先6=:振込先6, '
    wsql+='締日=:締日, '
    wsql+='一般原価率=:一般原価率, '
    wsql+='ASKL原価率=:ASKL原価率, '
    wsql+='ロゴ印刷=:ロゴ印刷, '
    wsql+='決算確定日=:決算確定日, '
    wsql+='終了処理=:終了処理, '
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
    wsql= 'DELETE FROM M900_自社 '
    return wsql

def get_primarykerfilter(ID):
    if not str.isdecimal(str(ID)):
        ID = -1
    wID = str(ID)
    wfilter=' WHERE 自社ID = ' + wID +' '
    return wfilter

def get_M900(ID):
    wsql =get_select_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cur = cn.execute(wsql)
    data = cur.fetchone()
    return data
    cn.close()

@app.route('/')
@app.route('/M900_index', methods=['GET'])
def get_M900_index():
    cn = cn_open()
    wsql = 'SELECT * FROM M900_自社 '
    wsql+= 'ORDER BY  自社ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M900_index.html',rows = rows )
    cn.close()

@app.route('/M900_insert', methods=['GET'])
def get_M900_insert():
    return render_template('M900_insert.html')

@app.route('/M900_insert', methods=['POST'])
def post_M900_insert():
    wsql = get_insert_sql()
    w自社ID = request.form.get('自社ID')    #0
    w自社名 = request.form.get('自社名')    #1
    w代表者名 = request.form.get('代表者名')    #2
    w郵便番号 = request.form.get('郵便番号')    #3
    w住所 = request.form.get('住所')    #4
    wTEL = request.form.get('TEL')    #5
    wFAX = request.form.get('FAX')    #6
    w振込先1 = request.form.get('振込先1')    #7
    w振込先2 = request.form.get('振込先2')    #8
    w振込先3 = request.form.get('振込先3')    #9
    w振込先4 = request.form.get('振込先4')    #10
    w振込先5 = request.form.get('振込先5')    #11
    w振込先6 = request.form.get('振込先6')    #12
    w締日 = request.form.get('締日')    #13
    w一般原価率 = request.form.get('一般原価率')    #14
    wASKL原価率 = request.form.get('ASKL原価率')    #15
    wロゴ印刷 = request.form.get('ロゴ印刷')    #16
    w決算確定日 = request.form.get('決算確定日')    #17
    w終了処理 = request.form.get('終了処理')    #18
    wPCID = request.form.get('PCID')    #19
    wUserName = request.form.get('UserName')    #20
    w登録日 = request.form.get('登録日')    #21
    w修正日 = request.form.get('修正日')    #22
    w作成 = request.form.get('作成')    #23
    w登録 = request.form.get('登録')    #24
    w削除 = request.form.get('削除')    #25
    wKK = request.form.get('KK')    #26
    wSV = request.form.get('SV')    #27
    cn = cn_open()
    row = (
        w自社ID,
        w自社名,
        w代表者名,
        w郵便番号,
        w住所,
        wTEL,
        wFAX,
        w振込先1,
        w振込先2,
        w振込先3,
        w振込先4,
        w振込先5,
        w振込先6,
        w締日,
        w一般原価率,
        wASKL原価率,
        wロゴ印刷,
        w決算確定日,
        w終了処理,
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
    wsql = 'SELECT * FROM M900_自社 '
    wsql+= 'ORDER BY  自社ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M900_index.html',rows = rows )
    cn.close()

@app.route('/M900_detail/<ID>', methods=['GET'])
def get_M900_detail(ID):
    data = get_M900(ID)
    return render_template('M900_detail.html', M900=data)

@app.route('/M900_update/<ID>', methods=['GET'])
def get_M900_update(ID):
    data = get_M900(ID)
    return render_template('M900_update.html', M900=data)

@app.route('/M900_update/<ID>', methods=['POST'])
def post_M900_update(ID):
    data = get_M900(ID)
    wsql = get_update_sql()
    wsql+=get_primarykerfilter(ID)
    w自社名 = request.form.get('自社名')    #1
    w代表者名 = request.form.get('代表者名')    #2
    w郵便番号 = request.form.get('郵便番号')    #3
    w住所 = request.form.get('住所')    #4
    wTEL = request.form.get('TEL')    #5
    wFAX = request.form.get('FAX')    #6
    w振込先1 = request.form.get('振込先1')    #7
    w振込先2 = request.form.get('振込先2')    #8
    w振込先3 = request.form.get('振込先3')    #9
    w振込先4 = request.form.get('振込先4')    #10
    w振込先5 = request.form.get('振込先5')    #11
    w振込先6 = request.form.get('振込先6')    #12
    w締日 = request.form.get('締日')    #13
    w一般原価率 = request.form.get('一般原価率')    #14
    wASKL原価率 = request.form.get('ASKL原価率')    #15
    wロゴ印刷 = request.form.get('ロゴ印刷')    #16
    w決算確定日 = request.form.get('決算確定日')    #17
    w終了処理 = request.form.get('終了処理')    #18
    wPCID = request.form.get('PCID')    #19
    wUserName = request.form.get('UserName')    #20
    w登録日 = request.form.get('登録日')    #21
    w修正日 = request.form.get('修正日')    #22
    w作成 = request.form.get('作成')    #23
    w登録 = request.form.get('登録')    #24
    w削除 = request.form.get('削除')    #25
    wKK = request.form.get('KK')    #26
    wSV = request.form.get('SV')    #27
    cn = cn_open()
    row = {
        '自社名':w自社名,
        '代表者名':w代表者名,
        '郵便番号':w郵便番号,
        '住所':w住所,
        'TEL':wTEL,
        'FAX':wFAX,
        '振込先1':w振込先1,
        '振込先2':w振込先2,
        '振込先3':w振込先3,
        '振込先4':w振込先4,
        '振込先5':w振込先5,
        '振込先6':w振込先6,
        '締日':w締日,
        '一般原価率':w一般原価率,
        'ASKL原価率':wASKL原価率,
        'ロゴ印刷':wロゴ印刷,
        '決算確定日':w決算確定日,
        '終了処理':w終了処理,
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

    data = get_M900(ID)
    return render_template('M900_detail.html', M900=data)


@app.route('/M900_delete/<ID>', methods=['GET'])
def get_M900_delete(ID):
    wsql = get_delete_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cn.execute(wsql)
    wsql = 'SELECT * FROM M900_自社 '
    wsql+= 'ORDER BY  自社ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M900_index.html',rows = rows )
    cn.close()

@app.route('/M900_importcsv',methods=['GET'])
def get_M900_importcsv():
    cn = cn_open()
    wsql=get_insert_sql()
    rows = pd.read_csv('M900.csv', encoding='cp932')
    for row in rows.values:
        print(row[0])
        cn.execute(wsql, row)
    cn.close()

@app.route('/M900_exportjson',methods=['GET'])
def get_M900_exportjson():
    wsql = M900_select_sql
    n = cn_open()
    rows = cn.execute(wsql)
    M900s=[
    dict(
        自社ID = row[0],
        自社名 = row[1],
        代表者名 = row[2],
        郵便番号 = row[3],
        住所 = row[4],
        TEL = row[5],
        FAX = row[6],
        振込先1 = row[7],
        振込先2 = row[8],
        振込先3 = row[9],
        振込先4 = row[10],
        振込先5 = row[11],
        振込先6 = row[12],
        締日 = row[13],
        一般原価率 = row[14],
        ASKL原価率 = row[15],
        ロゴ印刷 = row[16],
        決算確定日 = row[17],
        終了処理 = row[18],
        PCID = row[19],
        UserName = row[20],
        登録日 = row[21],
        修正日 = row[22],
        作成 = row[23],
        登録 = row[24],
        削除 = row[25],
        KK = row[26],
        SV = row[27]
        )
     for row in rows.fetchall()
    ]
    cn.close()
    if M900s is not None:
        return json.dump(M900s,ensure_ascii=False,indent=4)

@app.route('/M900_initialize',methods=['GET'])
def get_M900_initialize():

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
    M900s=[
        dict(
            自社ID = row[0],
            自社名 = row[1],
            代表者名 = row[2],
            郵便番号 = row[3],
            住所 = row[4],
            TEL = row[5],
            FAX = row[6],
            振込先1 = row[7],
            振込先2 = row[8],
            振込先3 = row[9],
            振込先4 = row[10],
            振込先5 = row[11],
            振込先6 = row[12],
            締日 = row[13],
            一般原価率 = row[14],
            ASKL原価率 = row[15],
            ロゴ印刷 = row[16],
            決算確定日 = row[17],
            終了処理 = row[18],
            PCID = row[19],
            UserName = row[20],
            登録日 = row[21],
            修正日 = row[22],
            作成 = row[23],
            登録 = row[24],
            削除 = row[25],
            KK = row[26],
            SV = row[27]
            )
        for row in rows.fetchall()
        ]
    if M900s is not None:
        dirname=os.path.dirname(__file__)
        path=os.path.join(dirname,'M900.json')
        outfile=open(path,'w',encoding='utf-8')
        json.dump(M900s,outfile,ensure_ascii=False,indent=4)
        outfile.close()


if __name__ == '__main__':
    app.debug = True
    #get_M900_initialize()

"""

@app.route('/M900_index', methods=['GET'])
def get_M900_index():
    return M900.get_M900_index()

@app.route('/M900_insert', methods=['GET'])
def get_M900_insert():
    return M900.get_M900_insert()

@app.route('/M900_insert', methods=['POST'])
def post_M900_insert():
    return M900.post_M900_insert()

@app.route('/M900_importcsv', methods=['GET'])
def get_M900_jimportcsv():
    M900.get_M900_importcsv()
    return M900.get_M900_index()

@app.route('/M900_json', methods=['GET'])
def get_M900_json():
    return M900.get_M900_json()

@app.route('/M900_detail/<ID>', methods=['GET'])
def get_M900_detail(ID):
    return M900.get_M900_detail(ID)

@app.route('/M900_update/<ID>', methods=['GET'])
def get_M900_update(ID):
    return M900.get_M900_update(ID)

@app.route('/M900_update/<ID>', methods=['POST'])
def post_M900_update(ID):
    return M900.post_M900_update(ID)

@app.route('/M900_delete/<ID>', methods=['GET'])
def get_M900_delete(ID):
    return M900.get_M900_index(ID)

#createtableM900.py
# -*- coding: utf-8 -*-

import sqlite3
        
dbname = 'DB603DAT.db'
cn = sqlite3.connect(dbname)
cn.execute ('PRAGMA foreign_keys = 1')
#cn.execute ('DROP TABLE  M900_自社)

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
M900s=[
    dict(
        自社ID = row[0],
        自社名 = row[1],
        代表者名 = row[2],
        郵便番号 = row[3],
        住所 = row[4],
        TEL = row[5],
        FAX = row[6],
        振込先1 = row[7],
        振込先2 = row[8],
        振込先3 = row[9],
        振込先4 = row[10],
        振込先5 = row[11],
        振込先6 = row[12],
        締日 = row[13],
        一般原価率 = row[14],
        ASKL原価率 = row[15],
        ロゴ印刷 = row[16],
        決算確定日 = row[17],
        終了処理 = row[18],
        PCID = row[19],
        UserName = row[20],
        登録日 = row[21],
        修正日 = row[22],
        作成 = row[23],
        登録 = row[24],
        削除 = row[25],
        KK = row[26],
        SV = row[27]
        )
    for row in rows.fetchall()
    ]
if M900s is not None:
    dirname=os.path.dirname(__file__)
    path=os.path.join(dirname,'M900.json')
    outfile=open(path,'w',encoding='utf-8')
    json.dump(M900s,outfile,ensure_ascii=False,indent=4)
    outfile.close()
"""
