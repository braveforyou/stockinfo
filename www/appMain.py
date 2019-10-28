#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'zhiting yu'

import logging;
import multiprocessing
from multiprocessing import Lock, Manager
from process.services.loadAllStock import *
import www.stList as consts
from www.handlers import *
from flask import Flask, render_template, redirect, url_for, request, make_response, session, flash
from datetime import timedelta
import os
from flask_restful import Api
import www.handlers as handlers

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 设置session的保存时间。
api = Api(app)


@app.route('/success/<name>')
def success(name):
    resp = make_response(render_template('loginSuccess.html', userID=name))
    session.permanent = True  # 默认session的时间持续31天
    session['username'] = name
    return resp


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        if (user != '123456'):
            flash('You were successfully logged in')
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        if (user != '123456'):
            flash('You were successfully logged in 2')
            return redirect(url_for('login'))
        return redirect(url_for('success', name=user))


@app.route('/')
def pageIndex():
    # loadHis.process()  # 读取现有数据
    manager = Manager()
    cpu_count = multiprocessing.cpu_count()
    lock = Lock()
    needList = manager.list()
    filterContent = manager.list()
    needLabel = manager.list()
    filterLabel = manager.list()
    pool = multiprocessing.Pool(cpu_count, initializer=initStParam,
                                initargs=(lock, needList, filterContent, needLabel, filterLabel,))
    pool.map(inner, consts.needStockM)
    needList = np.array(needList)
    if(len(needList)==0):
        needList=[['300193',[1]]]
    saveInfo = pd.DataFrame(needList, columns=['stname', 'info'])
    saveInfo.to_csv("D:\\needStList.csv")
    return render_template('search.html')


@app.route('/sampleList', methods=['POST', 'GET'])
def getHandler():
    blog = indexParrel()
    return render_template('stockinfo.html', page=blog['page'], blogs=blog['blogs'])



@app.route('/sampleSingle', methods=['POST'])
def searchStinfo():
    stname = request.form['stname']
    blog = stSingle(stname)
    return render_template('stockinfoSingle.html',  blog=blog['stinfo'])




# 用于数据返回，而非页面返回
api.add_resource(handlers.Rest, '/sample2')

if __name__ == '__main__':
    app.run(port=5000)
