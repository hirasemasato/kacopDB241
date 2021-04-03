# ZIP2_都市名 cp932
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
c県No= 0
c都市No= 1
c都市名= 2
cふりがな= 3
c変更日= 4
c変更後都市名= 5
c変更後ふりがな= 6
c都市ID= 7

def get_drop_sql():
    wsql= 'DROP TABLE IF EXISTS ZIP2_都市名 '
    return wsql

def get_create_sql():
    wsql ='CREATE TABLE IF NOT EXISTS ZIP2_都市名 ('
    wsql+='県No INTEGER  DEFAULT 0 PRIMARY KEY,'
    wsql+='都市No INTEGER  DEFAULT 0,'
    wsql+='都市名 TEXT  DEFAULT NULL,'
    wsql+='ふりがな TEXT  DEFAULT NULL,'
    wsql+='変更日 TEXT  DEFAULT NULL,'
    wsql+='変更後都市名 TEXT  DEFAULT NULL,'
    wsql+='変更後ふりがな TEXT  DEFAULT NULL,'
    wsql+='都市ID INTEGER  DEFAULT 0'
    wsql+=') '
    return wsql

def get_select_sql():
    wsql ='SELECT '
    wsql+='県No, '
    wsql+='都市No, '
    wsql+='都市名, '
    wsql+='ふりがな, '
    wsql+='変更日, '
    wsql+='変更後都市名, '
    wsql+='変更後ふりがな, '
    wsql+='都市ID '
    wsql+=' FROM ZIP2_都市名 '
    return wsql

def get_insert_sql():
    wsql ='INSERT INTO ZIP2_都市名 VALUES ('
    wsql+=':県No, '
    wsql+=':都市No, '
    wsql+=':都市名, '
    wsql+=':ふりがな, '
    wsql+=':変更日, '
    wsql+=':変更後都市名, '
    wsql+=':変更後ふりがな, '
    wsql+=':都市ID '
    wsql+=') '
    return wsql

def get_update_sql():
    wsql ='UPDATE ZIP2_都市名 SET '
    wsql+='都市No=:都市No, '
    wsql+='都市名=:都市名, '
    wsql+='ふりがな=:ふりがな, '
    wsql+='変更日=:変更日, '
    wsql+='変更後都市名=:変更後都市名, '
    wsql+='変更後ふりがな=:変更後ふりがな, '
    wsql+='都市ID=:都市ID '
    return wsql

def get_delete_sql():
    wsql= 'DELETE FROM ZIP2_都市名 '
    return wsql

def get_primarykerfilter(ID):
    wID = '"' + ID + '"'
    wfilter=' WHERE 県No = ' + wID +' '
    return wfilter

def get_ZIP2(ID):
    wsql =get_select_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cur = cn.execute(wsql)
    data = cur.fetchone()
    return data
    cn.close()

@app.route('/')
@app.route('/ZIP2_index', methods=['GET'])
def get_ZIP2_index():
    cn = cn_open()
    wsql = 'SELECT * FROM ZIP2_都市名 '
    wsql+= 'ORDER BY  県No DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('ZIP2_index.html',rows = rows )
    cn.close()

@app.route('/ZIP2_insert', methods=['GET'])
def get_ZIP2_insert():
    return render_template('ZIP2_insert.html')

@app.route('/ZIP2_insert', methods=['POST'])
def post_ZIP2_insert():
    wsql = get_insert_sql()
    w県No = request.form.get('県No')    #0
    w都市No = request.form.get('都市No')    #1
    w都市名 = request.form.get('都市名')    #2
    wふりがな = request.form.get('ふりがな')    #3
    w変更日 = request.form.get('変更日')    #4
    w変更後都市名 = request.form.get('変更後都市名')    #5
    w変更後ふりがな = request.form.get('変更後ふりがな')    #6
    w都市ID = request.form.get('都市ID')    #7
    cn = cn_open()
    row = (
        w県No,
        w都市No,
        w都市名,
        wふりがな,
        w変更日,
        w変更後都市名,
        w変更後ふりがな,
        w都市ID
        )
    cn.execute(wsql,row)
    wsql = 'SELECT * FROM ZIP2_都市名 '
    wsql+= 'ORDER BY  県No DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('ZIP2_index.html',rows = rows )
    cn.close()

@app.route('/ZIP2_detail/<ID>', methods=['GET'])
def get_ZIP2_detail(ID):
    data = get_ZIP2(ID)
    return render_template('ZIP2_detail.html', ZIP2=data)

@app.route('/ZIP2_update/<ID>', methods=['GET'])
def get_ZIP2_update(ID):
    data = get_ZIP2(ID)
    return render_template('ZIP2_update.html', ZIP2=data)

@app.route('/ZIP2_update/<ID>', methods=['POST'])
def post_ZIP2_update(ID):
    data = get_ZIP2(ID)
    wsql = get_update_sql()
    wsql+=get_primarykerfilter(ID)
    w都市No = request.form.get('都市No')    #1
    w都市名 = request.form.get('都市名')    #2
    wふりがな = request.form.get('ふりがな')    #3
    w変更日 = request.form.get('変更日')    #4
    w変更後都市名 = request.form.get('変更後都市名')    #5
    w変更後ふりがな = request.form.get('変更後ふりがな')    #6
    w都市ID = request.form.get('都市ID')    #7
    cn = cn_open()
    row = {
        '都市No':w都市No,
        '都市名':w都市名,
        'ふりがな':wふりがな,
        '変更日':w変更日,
        '変更後都市名':w変更後都市名,
        '変更後ふりがな':w変更後ふりがな,
        '都市ID':w都市ID
        }
    cn.execute(wsql,row)
    cn.close()

    data = get_ZIP2(ID)
    return render_template('ZIP2_detail.html', ZIP2=data)


@app.route('/ZIP2_delete/<ID>', methods=['GET'])
def get_ZIP2_delete(ID):
    wsql = get_delete_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cn.execute(wsql)
    wsql = 'SELECT * FROM ZIP2_都市名 '
    wsql+= 'ORDER BY  県No DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('ZIP2_index.html',rows = rows )
    cn.close()

@app.route('/ZIP2_importcsv',methods=['GET'])
def get_ZIP2_importcsv():
    cn = cn_open()
    wsql=get_insert_sql()
    rows = pd.read_csv('ZIP2.csv', encoding='cp932')
    for row in rows.values:
        print(row[0])
        cn.execute(wsql, row)
    cn.close()

@app.route('/ZIP2_exportjson',methods=['GET'])
def get_ZIP2_exportjson():
    wsql = ZIP2_select_sql
    n = cn_open()
    rows = cn.execute(wsql)
    ZIP2s=[
    dict(
        県No = row[0],
        都市No = row[1],
        都市名 = row[2],
        ふりがな = row[3],
        変更日 = row[4],
        変更後都市名 = row[5],
        変更後ふりがな = row[6],
        都市ID = row[7]
        )
     for row in rows.fetchall()
    ]
    cn.close()
    if ZIP2s is not None:
        return json.dump(ZIP2s,ensure_ascii=False,indent=4)

@app.route('/ZIP2_initialize',methods=['GET'])
def get_ZIP2_initialize():

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
    ZIP2s=[
        dict(
            県No = row[0],
            都市No = row[1],
            都市名 = row[2],
            ふりがな = row[3],
            変更日 = row[4],
            変更後都市名 = row[5],
            変更後ふりがな = row[6],
            都市ID = row[7]
            )
        for row in rows.fetchall()
        ]
    if ZIP2s is not None:
        dirname=os.path.dirname(__file__)
        path=os.path.join(dirname,'ZIP2.json')
        outfile=open(path,'w',encoding='utf-8')
        json.dump(ZIP2s,outfile,ensure_ascii=False,indent=4)
        outfile.close()


if __name__ == '__main__':
    app.debug = True
    #get_ZIP2_initialize()

"""

@app.route('/ZIP2_index', methods=['GET'])
def get_ZIP2_index():
    return ZIP2.get_ZIP2_index()

@app.route('/ZIP2_insert', methods=['GET'])
def get_ZIP2_insert():
    return ZIP2.get_ZIP2_insert()

@app.route('/ZIP2_insert', methods=['POST'])
def post_ZIP2_insert():
    return ZIP2.post_ZIP2_insert()

@app.route('/ZIP2_importcsv', methods=['GET'])
def get_ZIP2_jimportcsv():
    ZIP2.get_ZIP2_importcsv()
    return ZIP2.get_ZIP2_index()

@app.route('/ZIP2_json', methods=['GET'])
def get_ZIP2_json():
    return ZIP2.get_ZIP2_json()

@app.route('/ZIP2_detail/<ID>', methods=['GET'])
def get_ZIP2_detail(ID):
    return ZIP2.get_ZIP2_detail(ID)

@app.route('/ZIP2_update/<ID>', methods=['GET'])
def get_ZIP2_update(ID):
    return ZIP2.get_ZIP2_update(ID)

@app.route('/ZIP2_update/<ID>', methods=['POST'])
def post_ZIP2_update(ID):
    return ZIP2.post_ZIP2_update(ID)

@app.route('/ZIP2_delete/<ID>', methods=['GET'])
def get_ZIP2_delete(ID):
    return ZIP2.get_ZIP2_index(ID)

#createtableZIP2.py
# -*- coding: utf-8 -*-

import sqlite3
        
dbname = 'DBZIP.db'
cn = sqlite3.connect(dbname)
cn.execute ('PRAGMA foreign_keys = 1')
#cn.execute ('DROP TABLE  ZIP2_都市名)

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
ZIP2s=[
    dict(
        県No = row[0],
        都市No = row[1],
        都市名 = row[2],
        ふりがな = row[3],
        変更日 = row[4],
        変更後都市名 = row[5],
        変更後ふりがな = row[6],
        都市ID = row[7]
        )
    for row in rows.fetchall()
    ]
if ZIP2s is not None:
    dirname=os.path.dirname(__file__)
    path=os.path.join(dirname,'ZIP2.json')
    outfile=open(path,'w',encoding='utf-8')
    json.dump(ZIP2s,outfile,ensure_ascii=False,indent=4)
    outfile.close()
"""
