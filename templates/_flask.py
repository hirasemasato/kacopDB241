
Flaskのバージョンの確認方法
Flaskのバージョンの確認方法
Flaskのバージョンを調べるためには、 flaskモジュールの__version__を使用します。
pythonとタイプして、 Pythonプロンプトから flaskをインポートし使用します。

$ python
>> import flask
>> flask.__version__

  

 
Flaskのバージョンが0.7より古い場合
Flaskの0.7より古いバージョンでは、以下のようにpkg_resourcesを使用してそのバージョンを特定可能性があります。

$ python
>>> import pkg_resources
>>> pkg_resources.get_distribution('flask').version

'0.6.1'
PythonのWebフレームワークFlaskを使用しており、現在のバージョンを知りたい際には参考にしてください。


note.nkmk.me
Top Python pandas
pandasのバージョンを確認（pd.show_versions）
Posted: 2018-04-09 / Tags: Python, pandas
  
スクリプトで使用されているpandasのバージョンを確認するには以下の方法がある。

バージョン番号を取得: __version__属性
依存パッケージなどの詳細情報を表示: show_versions()関数
環境にインストールされているpandasのバージョンをpipコマンドで確認する方法は以下の記事を参照。

関連記事: Pythonのパッケージ（ライブラリ）のバージョンを確認
スポンサーリンク

 
バージョン番号を取得: version属性
ほかの多くのパッケージのように、pandasでも__version__属性によってバージョン番号が取得できる。

import pandas as pd

print(pd.__version__)
# 0.22.0
source: pandas_version.py
依存パッケージなどの詳細情報を表示: show_versions()関数
pandas.show_versions()関数で、Python本体や依存パッケージのバージョン、OSの種類などを含む詳細な情報が表示される。

pd.show_versions()
# INSTALLED VERSIONS
# ------------------
# commit: None
# python: 3.6.5.final.0
# python-bits: 64
# OS: Darwin
# OS-release: 17.5.0
# machine: x86_64
# processor: i386
# byteorder: little
# LC_ALL: None
# LANG: ja_JP.UTF-8
# LOCALE: ja_JP.UTF-8
# pandas: 0.22.0
# pytest: None
# pip: 9.0.3
# setuptools: 39.0.1
# Cython: 0.26
# numpy: 1.14.1
# scipy: 0.18.1
# pyarrow: None
# xarray: None
# IPython: 6.1.0
# sphinx: None
# patsy: None
# dateutil: 2.6.1
# pytz: 2018.3
# blosc: None
# bottleneck: None
# tables: None
# numexpr: None
# feather: None
# matplotlib: 2.0.0
# openpyxl: 2.4.8
# xlrd: 1.0.0
# xlwt: None
# xlsxwriter: None
# lxml: 4.1.1
# bs4: 4.6.0
# html5lib: 0.9999999
# sqlalchemy: 1.1.10
# pymysql: None
# psycopg2: None
# jinja2: 2.9.6
# s3fs: None
# fastparquet: None
# pandas_gbq: None
# pandas_datareader: 0.6.0

source: pandas_version.py
バグ報告などにはshow_versions()の出力結果を記載することが求められている。
