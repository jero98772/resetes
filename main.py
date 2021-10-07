#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
resetes - 2021 - por jero98772
resetes - 2021 - by jero98772
"""
from flask import Flask, render_template, request, flash, redirect ,session
from tools.dbInteracion import dbInteracion
from tools.tools import *
app = Flask(__name__)
DBPATH = "data/"
DBNAMEGAS = DBPATH + "login"
TABLEGAS = ""
class resetes():
    WEBPAGE = "/"
    @app.route(WEBPAGE+"resetes.html", methods = ['GET','POST'])
    def resetes():
        return render_template("resetes.html")	
if __name__=='__main__':
	app.run(debug=True,host="0.0.0.0",port=9600)