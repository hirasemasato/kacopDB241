# ZIP1_県名 cp932
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
    cn = sqlite3.connect('./DBZIP.db')
    cn.isolation_level = None
    cn.row_factory = sqlite3.Row
    return cn

#定数
c県No= 0
c検索文字= 1
c県名= 2
c県名除外= 3
c地価指数= 4

def get_drop_sql():
    wsql= 'DROP TABLE IF EXISTS ZIP1_県名 '
    return wsql

def get_create_sql():
    wsql ='CREATE TABLE IF NOT EXISTS ZIP1_県名 ('
    wsql+='県No INTEGER  DEFAULT 0 PRIMARY KEY,'
    wsql+='検索文字 TEXT  DEFAULT NULL,'
    wsql+='県名 TEXT  DEFAULT NULL,'
    wsql+='県名除外 INTEGER  DEFAULT 0,'
    wsql+='地価指数 INTEGER  DEFAULT 0'
    wsql+=') '
    return wsql

def get_select_sql():
    wsql ='SELECT '
    wsql+='県No, '
    wsql+='検索文字, '
    wsql+='県名, '
    wsql+='県名除外, '
    wsql+='地価指数 '
    wsql+=' FROM ZIP1_県名 '
    return wsql

def get_insert_sql():
    wsql ='INSERT INTO ZIP1_県名 VALUES ('
    wsql+=':県No, '
    wsql+=':検索文字, '
    wsql+=':県名, '
    wsql+=':県名除外, '
    wsql+=':地価指数 '
    wsql+=') '
    return wsql

def get_update_sql():
    wsql ='UPDATE ZIP1_県名 SET '
    wsql+='検索文字=:検索文字, '
    wsql+='県名=:県名, '
    wsql+='県名除外=:県名除外, '
    wsql+='地価指数=:地価指数 '
    return wsql

def get_delete_sql():
    wsql= 'DELETE FROM ZIP1_県名 '
    return wsql

def get_primarykerfilter(ID):
    wID = '"' + ID + '"'
    wfilter=' WHERE 県No = ' + wID +' '
    return wfilter

def get_ZIP1(ID):
    wsql =get_select_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cur = cn.execute(wsql)
    data = cur.fetchone()
    return data
    cn.close()

@app.route('/')
@app.route('/ZIP1_index', methods=['GET'])
def get_ZIP1_index():
    cn = cn_open()
    wsql = 'SELECT * FROM ZIP1_県名 '
    wsql+= 'ORDER BY  県No DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('ZIP1_index.html',rows = rows )
    cn.close()

@app.route('/ZIP1_insert', methods=['GET'])
def get_ZIP1_insert():
    return render_template('ZIP1_insert.html')

@app.route('/ZIP1_insert', methods=['POST'])
def post_ZIP1_insert():
    wsql = get_insert_sql()
    w県No = request.form.get('県No')    #0
    w検索文字 = request.form.get('検索文字')    #1
    w県名 = request.form.get('県名')    #2
    w県名除外 = request.form.get('県名除外')    #3
    w地価指数 = request.form.get('地価指数')    #4
    cn = cn_open()
    row = (
        w県No,
        w検索文字,
        w県名,
        w県名除外,
        w地価指数
        )
    cn.execute(wsql,row)
    wsql = 'SELECT * FROM ZIP1_県名 '
    wsql+= 'ORDER BY  県No DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('ZIP1_index.html',rows = rows )
    cn.close()

@app.route('/ZIP1_detail/<ID>', methods=['GET'])
def get_ZIP1_detail(ID):
    data = get_ZIP1(ID)
    return render_template('ZIP1_detail.html', ZIP1=data)

@app.route('/ZIP1_update/<ID>', methods=['GET'])
def get_ZIP1_update(ID):
    data = get_ZIP1(ID)
    return render_template('ZIP1_update.html', ZIP1=data)

@app.route('/ZIP1_update/<ID>', methods=['POST'])
def post_ZIP1_update(ID):
    data = get_ZIP1(ID)
    wsql = get_update_sql()
    wsql+=get_primarykerfilter(ID)
    w検索文字 = request.form.get('検索文字')    #1
    w県名 = request.form.get('県名')    #2
    w県名除外 = request.form.get('県名除外')    #3
    w地価指数 = request.form.get('地価指数')    #4
    cn = cn_open()
    row = {
        '検索文字':w検索文字,
        '県名':w県名,
        '県名除外':w県名除外,
        '地価指数':w地価指数
        }
    cn.execute(wsql,row)
    cn.close()

    data = get_ZIP1(ID)
    return render_template('ZIP1_detail.html', ZIP1=data)


@app.route('/ZIP1_delete/<ID>', methods=['GET'])
def get_ZIP1_delete(ID):
    wsql = get_delete_sql()
    wsql+=get_primarykerfilter(ID)
    cn = cn_open()
    cn.execute(wsql)
    wsql = 'SELECT * FROM ZIP1_県名 '
    wsql+= 'ORDER BY  県No DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('ZIP1_index.html',rows = rows )
    cn.close()

@app.route('/ZIP1_importcsv',methods=['GET'])
def get_ZIP1_importcsv():
    cn = cn_open()
    wsql=get_insert_sql()
    rows = pd.read_csv('ZIP1.csv', encoding='cp932')
    for row in rows.values:
        print(row[0])
        cn.execute(wsql, row)
    cn.close()

@app.route('/ZIP1_exportjson',methods=['GET'])
def get_ZIP1_exportjson():
    wsql = ZIP1_select_sql
    n = cn_open()
    rows = cn.execute(wsql)
    ZIP1s=[
    dict(
        県No = row[0],
        検索文字 = row[1],
        県名 = row[2],
        県名除外 = row[3],
        地価指数 = row[4]
        )
     for row in rows.fetchall()
    ]
    cn.close()
    if ZIP1s is not None:
        return json.dump(ZIP1s,ensure_ascii=False,indent=4)

@app.route('/ZIP1_initialize',methods=['GET'])
def get_ZIP1_initialize():

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
    ZIP1s=[
        dict(
            県No = row[0],
            検索文字 = row[1],
            県名 = row[2],
            県名除外 = row[3],
            地価指数 = row[4]
            )
        for row in rows.fetchall()
        ]
    if ZIP1s is not None:
        dirname=os.path.dirname(__file__)
        path=os.path.join(dirname,'ZIP1.json')
        outfile=open(path,'w',encoding='utf-8')
        json.dump(ZIP1s,outfile,ensure_ascii=False,indent=4)
        outfile.close()


if __name__ == '__main__':
    app.debug = True
    #get_ZIP1_initialize()

"""

@app.route('/ZIP1_index', methods=['GET'])
def get_ZIP1_index():
    return ZIP1.get_ZIP1_index()

@app.route('/ZIP1_insert', methods=['GET'])
def get_ZIP1_insert():
    return ZIP1.get_ZIP1_insert()

@app.route('/ZIP1_insert', methods=['POST'])
def post_ZIP1_insert():
    return ZIP1.post_ZIP1_insert()

@app.route('/ZIP1_importcsv', methods=['GET'])
def get_ZIP1_jimportcsv():
    ZIP1.get_ZIP1_importcsv()
    return ZIP1.get_ZIP1_index()

@app.route('/ZIP1_json', methods=['GET'])
def get_ZIP1_json():
    return ZIP1.get_ZIP1_json()

@app.route('/ZIP1_detail/<ID>', methods=['GET'])
def get_ZIP1_detail(ID):
    return ZIP1.get_ZIP1_detail(ID)

@app.route('/ZIP1_update/<ID>', methods=['GET'])
def get_ZIP1_update(ID):
    return ZIP1.get_ZIP1_update(ID)

@app.route('/ZIP1_update/<ID>', methods=['POST'])
def post_ZIP1_update(ID):
    return ZIP1.post_ZIP1_update(ID)

@app.route('/ZIP1_delete/<ID>', methods=['GET'])
def get_ZIP1_delete(ID):
    return ZIP1.get_ZIP1_index(ID)

#createtableZIP1.py
# -*- coding: utf-8 -*-

import sqlite3
        
dbname = './DBZIP.db'
cn = sqlite3.connect(dbname)
cn.execute ('PRAGMA foreign_keys = 1')
#cn.execute ('DROP TABLE  ZIP1_県名)

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
ZIP1s=[
    dict(
        県No = row[0],
        検索文字 = row[1],
        県名 = row[2],
        県名除外 = row[3],
        地価指数 = row[4]
        )
    for row in rows.fetchall()
    ]
if ZIP1s is not None:
    dirname=os.path.dirname(__file__)
    path=os.path.join(dirname,'ZIP1.json')
    outfile=open(path,'w',encoding='utf-8')
    json.dump(ZIP1s,outfile,ensure_ascii=False,indent=4)
    outfile.close()
"""
