# ZIP0_住所 cp932
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
    cn = sqlite3.connect('DBZIP.db')
    cn.isolation_level = None
    cn.row_factory = sqlite3.Row
    return cn

#定数
c郵便番号= 0
c住所= 1
cふりがな= 2
c県No= 3
c都市No= 4
c全住所= 5

def get_drop_sql():
    wsql= 'DROP TABLE IF EXISTS ZIP0_住所 '
    return wsql

def get_create_sql():
    wsql ='CREATE TABLE IF NOT EXISTS ZIP0_住所 ('
    wsql+='郵便番号 TEXT  DEFAULT NULL PRIMARY KEY,'
    wsql+='住所 TEXT  DEFAULT NULL,'
    wsql+='ふりがな TEXT  DEFAULT NULL,'
    wsql+='県No INTEGER  DEFAULT 0,'
    wsql+='都市No INTEGER  DEFAULT 0,'
    wsql+='全住所 TEXT  DEFAULT NULL'
    wsql+=') '
    return wsql

def get_select_sql():
    wsql ='SELECT '
    wsql+='郵便番号, '
    wsql+='住所, '
    wsql+='ふりがな, '
    wsql+='県No, '
    wsql+='都市No, '
    wsql+='全住所 '
    wsql+=' FROM ZIP0_住所 '
    return wsql

def get_insert_sql():
    wsql ='INSERT INTO ZIP0_住所 VALUES ('
    wsql+=':郵便番号, '
    wsql+=':住所, '
    wsql+=':ふりがな, '
    wsql+=':県No, '
    wsql+=':都市No, '
    wsql+=':全住所 '
    wsql+=') '
    return wsql

def get_update_sql():
    wsql ='UPDATE ZIP0_住所 SET '
    wsql+='住所=:住所, '
    wsql+='ふりがな=:ふりがな, '
    wsql+='県No=:県No, '
    wsql+='都市No=:都市No, '
    wsql+='全住所=:全住所 '
    return wsql

def get_delete_sql():
    wsql= 'DELETE FROM ZIP0_住所 '
    return wsql

def get_primarykerfilter(ID):
    wID = '"' + ID + '"'
    wfilter=' WHERE 郵便番号 = ' + wID +' '
    return wfilter

def get_ZIP0(ID):
    wsql =get_select_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cur = cn.execute(wsql)
    data = cur.fetchone()
    return data
    cn.close()

@app.route('/')
@app.route('/ZIP0_index', methods=['GET'])
def get_ZIP0_index():
    cn = cn_open()
    wsql = 'SELECT * FROM ZIP0_住所 '
    wsql+= 'ORDER BY  郵便番号 DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('ZIP0_index.html',rows = rows )
    cn.close()

@app.route('/ZIP0_insert', methods=['GET'])
def get_ZIP0_insert():
    return render_template('ZIP0_insert.html')

@app.route('/ZIP0_insert', methods=['POST'])
def post_ZIP0_insert():
    wsql = get_insert_sql()
    w郵便番号 = request.form.get('郵便番号')    #0
    w住所 = request.form.get('住所')    #1
    wふりがな = request.form.get('ふりがな')    #2
    w県No = request.form.get('県No')    #3
    w都市No = request.form.get('都市No')    #4
    w全住所 = request.form.get('全住所')    #5
    cn = cn_open()
    row = (
        w郵便番号,
        w住所,
        wふりがな,
        w県No,
        w都市No,
        w全住所
        )
    cn.execute(wsql,row)
    wsql = 'SELECT * FROM ZIP0_住所 '
    wsql+= 'ORDER BY  郵便番号 DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('ZIP0_index.html',rows = rows )
    cn.close()

@app.route('/ZIP0_detail/<ID>', methods=['GET'])
def get_ZIP0_detail(ID):
    data = get_ZIP0(ID)
    return render_template('ZIP0_detail.html', ZIP0=data)

@app.route('/ZIP0_update/<ID>', methods=['GET'])
def get_ZIP0_update(ID):
    data = get_ZIP0(ID)
    return render_template('ZIP0_update.html', ZIP0=data)

@app.route('/ZIP0_update/<ID>', methods=['POST'])
def post_ZIP0_update(ID):
    data = get_ZIP0(ID)
    wsql = get_update_sql()
    wsql+=get_primarykerfilter(ID)
    w住所 = request.form.get('住所')    #1
    wふりがな = request.form.get('ふりがな')    #2
    w県No = request.form.get('県No')    #3
    w都市No = request.form.get('都市No')    #4
    w全住所 = request.form.get('全住所')    #5
    cn = cn_open()
    row = {
        '住所':w住所,
        'ふりがな':wふりがな,
        '県No':w県No,
        '都市No':w都市No,
        '全住所':w全住所
        }
    cn.execute(wsql,row)
    cn.close()

    data = get_ZIP0(ID)
    return render_template('ZIP0_detail.html', ZIP0=data)


@app.route('/ZIP0_delete/<ID>', methods=['GET'])
def get_ZIP0_delete(ID):
    wsql = get_delete_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cn.execute(wsql)
    wsql = 'SELECT * FROM ZIP0_住所 '
    wsql+= 'ORDER BY  郵便番号 DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('ZIP0_index.html',rows = rows )
    cn.close()

@app.route('/ZIP0_importcsv',methods=['GET'])
def get_ZIP0_importcsv():
    cn = cn_open()
    wsql=get_insert_sql()
    rows = pd.read_csv('ZIP0.csv', encoding='cp932')
    for row in rows.values:
        print(row[0])
        cn.execute(wsql, row)
    cn.close()

@app.route('/ZIP0_exportjson',methods=['GET'])
def get_ZIP0_exportjson():
    wsql = ZIP0_select_sql
    n = cn_open()
    rows = cn.execute(wsql)
    ZIP0s=[
    dict(
        郵便番号 = row[0],
        住所 = row[1],
        ふりがな = row[2],
        県No = row[3],
        都市No = row[4],
        全住所 = row[5]
        )
     for row in rows.fetchall()
    ]
    cn.close()
    if ZIP0s is not None:
        return json.dump(ZIP0s,ensure_ascii=False,indent=4)

@app.route('/ZIP0_initialize',methods=['GET'])
def get_ZIP0_initialize():

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
    ZIP0s=[
        dict(
            郵便番号 = row[0],
            住所 = row[1],
            ふりがな = row[2],
            県No = row[3],
            都市No = row[4],
            全住所 = row[5]
            )
        for row in rows.fetchall()
        ]
    if ZIP0s is not None:
        dirname=os.path.dirname(__file__)
        path=os.path.join(dirname,'ZIP0.json')
        outfile=open(path,'w',encoding='utf-8')
        json.dump(ZIP0s,outfile,ensure_ascii=False,indent=4)
        outfile.close()


if __name__ == '__main__':
    app.debug = True
    #get_ZIP0_initialize()

"""

@app.route('/ZIP0_index', methods=['GET'])
def get_ZIP0_index():
    return ZIP0.get_ZIP0_index()

@app.route('/ZIP0_insert', methods=['GET'])
def get_ZIP0_insert():
    return ZIP0.get_ZIP0_insert()

@app.route('/ZIP0_insert', methods=['POST'])
def post_ZIP0_insert():
    return ZIP0.post_ZIP0_insert()

@app.route('/ZIP0_importcsv', methods=['GET'])
def get_ZIP0_jimportcsv():
    ZIP0.get_ZIP0_importcsv()
    return ZIP0.get_ZIP0_index()

@app.route('/ZIP0_json', methods=['GET'])
def get_ZIP0_json():
    return ZIP0.get_ZIP0_json()

@app.route('/ZIP0_detail/<ID>', methods=['GET'])
def get_ZIP0_detail(ID):
    return ZIP0.get_ZIP0_detail(ID)

@app.route('/ZIP0_update/<ID>', methods=['GET'])
def get_ZIP0_update(ID):
    return ZIP0.get_ZIP0_update(ID)

@app.route('/ZIP0_update/<ID>', methods=['POST'])
def post_ZIP0_update(ID):
    return ZIP0.post_ZIP0_update(ID)

@app.route('/ZIP0_delete/<ID>', methods=['GET'])
def get_ZIP0_delete(ID):
    return ZIP0.get_ZIP0_index(ID)

#createtableZIP0.py
# -*- coding: utf-8 -*-

import sqlite3
        
dbname = 'DBZIP.db'
cn = sqlite3.connect(dbname)
cn.execute ('PRAGMA foreign_keys = 1')
#cn.execute ('DROP TABLE  ZIP0_住所)

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
ZIP0s=[
    dict(
        郵便番号 = row[0],
        住所 = row[1],
        ふりがな = row[2],
        県No = row[3],
        都市No = row[4],
        全住所 = row[5]
        )
    for row in rows.fetchall()
    ]
if ZIP0s is not None:
    dirname=os.path.dirname(__file__)
    path=os.path.join(dirname,'ZIP0.json')
    outfile=open(path,'w',encoding='utf-8')
    json.dump(ZIP0s,outfile,ensure_ascii=False,indent=4)
    outfile.close()
"""
