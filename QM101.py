# M101_受注 cp932
# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask, render_template, request, redirect, g
import os
import csv
import json
import sqlite3
import pprint
import logging
import M011

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

#drop
def get_drop_sql():
    wsql= 'DROP VIEW IF EXISTS QM101_受注 '
    return wsql

def get_create_sql():
    wsql='CREATE VIEW IF NOT EXISTS QM101_受注 AS SELECT '
    wsql+='M101.*,'
    wsql+='M011.顧客No,'
    wsql+='M011.顧客名,'
    wsql+='M011.ふりがな AS 顧客ふりがな '
    wsql+='FROM (M101_受注 AS M101 '
    wsql+='LEFT JOIN M011_顧客 AS M011 ON M101.顧客ID=M011.顧客ID '
    wsql+=') '
    return wsql

#select
def get_select_sql():
    wsql ='SELECT * FROM QM101_受注 '
    return wsql

def get_update_sql():
    wsql ='UPDATE M101_受注 SET '
    wsql+='受注No=:受注No, '
    wsql+='日付=:日付, '
    wsql+='顧客検索=:顧客検索, '
    wsql+='顧客ID=:顧客ID, '
    wsql+='金額=:金額, '
    wsql+='備考=:備考, '
    wsql+='明細数=:明細数, '
    wsql+='印刷済=:印刷済, '
    wsql+='UserName=:UserName, '
    wsql+='登録日=:登録日, '
    wsql+='修正日=:修正日 '
    return wsql

def get_primarykerfilter(ID):
    if not str.isdecimal(str(ID)):
        ID = -1
    wfilter=' WHERE 受注ID = ' + str(ID) +' '
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
    wsql = 'SELECT * FROM QM101_受注 '
    wsql+= 'ORDER BY  受注ID DESC '
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('M101_index.html',rows = rows )
    cn.close()

@app.route('/M101_insert', methods=['GET'])
def get_M101_insert():
    return render_template('M101_insert.html')

@app.route('/M101_detail/<ID>', methods=['GET'])
def get_M101_detail(ID):
    data = get_M101(ID)
    return render_template('M101_detail.html', M101=data)

@app.route('/M101_update/<ID>', methods=['GET'])
def get_M101_update(ID):
    data = get_M101(ID)

    cn = M011.cn_open()
    wsql = M011.get_select_sql()
    wsql+=' ORDER BY  顧客ID '
    cur = cn.execute(wsql)
    M011s = cur.fetchall()
    cn.close()
    contents='M011s_count:' + str(len(M011s))
    logger.info(contents)
    return render_template('M101_update.html', M101=data,M011s=M011s)


@app.route('/M101_update/<ID>', methods=['POST'])
def post_M101_update(ID):
    data = get_M101(ID)
    wsql = get_update_sql()
    wsql+=get_primarykerfilter(ID)
    w受注No = request.form.get('受注No')    #1
    w日付 = request.form.get('日付')    #2
    w顧客検索 = request.form.get('顧客検索')    #3
    w顧客ID = request.form.get('顧客ID')    #4
    w金額 = request.form.get('金額')    #5
    w備考 = request.form.get('備考')    #6
    w明細数 = request.form.get('明細数')    #7
    w印刷済 = request.form.get('印刷済')    #8
    wUserName = request.form.get('UserName')    #9
    w登録日 = request.form.get('登録日')    #10
    w修正日 = request.form.get('修正日')   #11
    cn = cn_open()
    row = {
        '受注No':w受注No,
        '日付':w日付,
        '顧客検索':w顧客検索,
        '顧客ID':w顧客ID,
        '金額':w金額,
        '備考':w備考,
        '明細数':w明細数,
        '印刷済':w印刷済,
        'UserName':wUserName,
        '登録日':w登録日,
        '修正日':w修正日
        }
    cn.execute(wsql,row)
    cn.close()

    data = get_M101(ID)
    return render_template('M101_detail.html', M101=data)


@app.route('/M101_exportjson',methods=['GET'])
def get_M101_exportjson():
    wsql = M101_select_sql
    rows = cn.execute(wsql)
    M101s=[
    dict(
        受注ID = row[0],
        受注No = row[1],
        日付 = row[2],
        顧客検索 = row[3],
        顧客ID = row[4],
        金額 = row[5],
        備考 = row[6],
        明細数 = row[7],
        印刷済 = row[8],
        UserName = row[9],
        登録日 = row[10],
        修正日 = row[11]
        )
     for row in rows.fetchall()
    ]
    if M101s is not None:
        return json.dump(M101s,ensure_ascii=False,indent=4)

if __name__ == '__main__':
    app.debug = True
    #get_M101_initialize()

"""
logger.debug("デバッグ出力")
logger.info("情報出力")
logger.warning("警告発生！")
logger.error("エラー発生！！")


@app.route('/M101_index', methods=['GET'])
def get_M101_index():
    return M101.get_M101_index()

@app.route('/M101_insert', methods=['GET'])
def get_M101_insert():
    return QM101.get_M101_insert()

@app.route('/M101_json', methods=['GET'])
def get_M101_json():
    return QM101.get_M101_json()

@app.route('/M101_detail/<ID>', methods=['GET'])
def get_M101_detail(ID):
    return QM101.get_M101_detail(ID)

@app.route('/M101_update/<ID>', methods=['GET'])
def get_M101_update(ID):
    return QM101.get_M101_update(ID)

#M101_index.html/{{ M101.受注ID }}
<table border=1>
    <thead>
    <tr>
        <th class='col1'>受注ID</th>
        <th class='col2'>顧客ID</th>
        <th class='col3'>NENNGETU</th>
    </tr>
    </thead>
        <tbody>
        {% for row in rows %}
        <tr onClick='location.href="/M101_detail/{{ row[0] }}"'>
            <td class='col1'> {{ row['受注ID'] }}</td>
            <td class='col2'> {{ row['顧客ID'] }}</td>
            <td class='col3'> {{ row['NENNGETU'] }}</td>
        </tr>
{% endfor %}
</tbody>
</table>

#M101_detail.html/{{ M101.受注ID }}

<table border=1>
    <tr>
        <th>受注ID</th>
        <td>{{ M101.受注ID }}</td>
    </tr>
    <tr>
        <th>顧客ID</th>
        <td>{{ M101.顧客ID }}</td>
    </tr>
    <tr>
        <th>NENNGETU</th>
        <td>{{ M101.NENNGETU }}</td>
    </tr>
</table>
"""