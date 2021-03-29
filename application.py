from datetime import datetime
from flask import Flask, render_template, request, redirect, g

import json
import sqlite3
import os
import logging

import K000
import M011
import M031
import M101
import QM101
import X001
import X002
import X003
import ZIP0
import ZIP1
import ZIP2

format_str = '%(asctime)s - %(process)d - %(thread)d - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=format_str, level=logging.INFO)
logger = logging.getLogger(__name__)

LayerNum=0
LayerStr=[]

app = Flask(__name__)

logger.info('start')

def Layer_add(naiyou):
    global LayerNum,LayerStr
    LayerNum+=1
    LayerStr.append(str(LayerNum) + naiyou +'_') 

def Layer_pop():
    global LayerNum,LayerStr
    LayerNum-=1
    LayerStr.pop(LayerNum) 

@app.route('/', methods=['GET'])
def get_MENU_index():
    wsql = ' SELECT * FROM K000_MENU'
    wsql+= ' ORDER BY  MENUNO '
    cn = K000.cn_open()
    cur = cn.execute(wsql)
    rows = cur.fetchall()
    return render_template('menu.html',rows = rows)
    cn.close()

@app.route('/K000_index', methods=['GET'])
def get_K000_index():
    return K000.get_K000_index()


@app.route('/K000_insert', methods=['GET'])
def get_K000_insert():
    return K000.get_K000_insert()

@app.route('/K000_insert', methods=['POST'])
def post_K000_insert():
    return K000.post_K000_insert()

@app.route('/K000_importcsv', methods=['GET'])
def get_K000_jimportcsv():
    K000.get_K000_importcsv()
    return K000.get_K000_index()

@app.route('/K000_json', methods=['GET'])
def get_K000_json():
    return K000.get_K000_json()

@app.route('/K000_detail/<ID>', methods=['GET'])
def get_K000_detail(ID):
    return K000.get_K000_detail(ID)

@app.route('/K000_update/<ID>', methods=['GET'])
def get_K000_update(ID):
    return K000.get_K000_update(ID)

@app.route('/K000_update/<ID>', methods=['POST'])
def post_K000_update(ID):
    return K000.post_K000_update(ID)

@app.route('/K000_delete/<ID>', methods=['GET'])
def get_K000_delete(ID):
    return K000.get_K000_index(ID)


@app.route('/M011_index', methods=['GET'])
def get_M011_index():
    return M011.get_M011_index()

@app.route('/M011_insert', methods=['GET'])
def get_M011_insert():
    return M011.get_M011_insert()

@app.route('/M011_insert', methods=['POST'])
def post_M011_insert():
    return M011.post_M011_insert()

@app.route('/M011_importcsv',methods=['GET'])
def get_M011_importcsv():
    return M011.get_M011_importcsv()

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
    return M011.get_M011_delete(ID)

@app.route('/M031_index', methods=['GET'])
def get_M031_index():
    return M031.get_M031_index()

@app.route('/M031_insert', methods=['GET'])
def get_M031_insert():
    return M031.get_M031_insert()

@app.route('/M031_insert', methods=['POST'])
def post_M031_insert():
    return M031.post_M031_index()

@app.route('/M031_importcsv',methods=['GET'])
def get_M031_importcsv():
    return M031.get_M031_importcsv()

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
    return M031.get_M031_delete(ID)

@app.route('/M101_index', methods=['GET'])
def get_M101_index():
    return QM101.get_M101_index()

@app.route('/M101_insert', methods=['GET'])
def get_M101_insert():
    return M101.get_M101_insert()

@app.route('/M101_insert', methods=['POST'])
def post_M101_insert():
    return M101.post_M101_insert()

@app.route('/M101_importcsv', methods=['GET'])
def get_M101_jimportcsv():
    return M101.get_M101_importcsv()

@app.route('/M101_json', methods=['GET'])
def get_M101_json():
    return M101.get_M101_json()

@app.route('/M101_detail/<ID>', methods=['GET'])
def get_M101_detail(ID):
    return QM101.get_M101_detail(ID)

@app.route('/M101_update/<ID>', methods=['GET'])
def get_M101_update(ID):
    return QM101.get_M101_update(ID)

@app.route('/M101_update/<ID>', methods=['POST'])
def post_M101_update(ID):
    return QM101.post_M101_update(ID)

@app.route('/M101_delete/<ID>', methods=['GET'])
def get_M101_delete(ID):
    return M101.get_M101_index(ID)


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


@app.route('/X001_index', methods=['GET'])
def get_X001_index():
    return X001.get_X001_index()

@app.route('/X001_insert', methods=['GET'])
def get_X001_insert():
    return X001.get_X001_insert()

@app.route('/X001_insert', methods=['POST'])
def post_X001_insert():
    return X001.post_X001_insert()

@app.route('/X001_importcsv', methods=['GET'])
def get_X001_jimportcsv():
    X001.get_X001_importcsv()
    return X001.get_X001_index()

@app.route('/X001_json', methods=['GET'])
def get_X001_json():
    return X001.get_X001_json()

@app.route('/X001_detail/<ID>', methods=['GET'])
def get_X001_detail(ID):
    return X001.get_X001_detail(ID)

@app.route('/X001_update/<ID>', methods=['GET'])
def get_X001_update(ID):
    return X001.get_X001_update(ID)

@app.route('/X001_update/<ID>', methods=['POST'])
def post_X001_update(ID):
    return X001.post_X001_update(ID)

@app.route('/X001_delete/<ID>', methods=['GET'])
def get_X001_delete(ID):
    return X001.get_X001_index(ID)


@app.route('/X002_index', methods=['GET'])
def get_X002_index():
    return X002.get_X002_index()

@app.route('/X002_insert', methods=['GET'])
def get_X002_insert():
    return X002.get_X002_insert()

@app.route('/X002_insert', methods=['POST'])
def post_X002_insert():
    return X002.post_X002_insert()

@app.route('/X002_importcsv', methods=['GET'])
def get_X002_jimportcsv():
    X002.get_X002_importcsv()
    return X002.get_X002_index()

@app.route('/X002_json', methods=['GET'])
def get_X002_json():
    return X002.get_X002_json()

@app.route('/X002_detail/<ID>', methods=['GET'])
def get_X002_detail(ID):
    return X002.get_X002_detail(ID)

@app.route('/X002_update/<ID>', methods=['GET'])
def get_X002_update(ID):
    return X002.get_X002_update(ID)

@app.route('/X002_update/<ID>', methods=['POST'])
def post_X002_update(ID):
    return X002.post_X002_update(ID)

@app.route('/X002_delete/<ID>', methods=['GET'])
def get_X002_delete(ID):
    return X002.get_X002_index(ID)


@app.route('/X003_index', methods=['GET'])
def get_X003_index():
    return X003.get_X003_index()

@app.route('/X003_insert', methods=['GET'])
def get_X003_insert():
    return X003.get_X003_insert()

@app.route('/X003_insert', methods=['POST'])
def post_X003_insert():
    return X003.post_X003_insert()

@app.route('/X003_importcsv', methods=['GET'])
def get_X003_jimportcsv():
    X003.get_X003_importcsv()
    return X003.get_X003_index()

@app.route('/X003_json', methods=['GET'])
def get_X003_json():
    return X003.get_X003_json()

@app.route('/X003_detail/<ID>', methods=['GET'])
def get_X003_detail(ID):
    return X003.get_X003_detail(ID)

@app.route('/X003_update/<ID>', methods=['GET'])
def get_X003_update(ID):
    return X003.get_X003_update(ID)

@app.route('/X003_update/<ID>', methods=['POST'])
def post_X003_update(ID):
    return X003.post_X003_update(ID)

@app.route('/X003_delete/<ID>', methods=['GET'])
def get_X003_delete(ID):
    return X003.get_X003_index(ID)


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

@app.route('/S001_sample')
def get_S001_sample():
    return '<h1>Hello</h1>'

@app.route('/S002_sample')
def get_S002_sample(user=''):
    req = request.args
    username = req.get('user')    
    return render_template('S002_sample.html', user=username)

@app.route('/S003_sample')
def get_S003_sample(user=''):
    req = request.args
    username = req.get('user') 
    html = "<h2> Hello {name} </h2>".format(name=username)
    return html
 
if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=5000)