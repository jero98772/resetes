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
DBNAMEGAS = DBPATH + "gas_db"
TABLEGAS = ""
class resetes():
	WEBPAGE = "/"
	@app.route(WEBPAGE+"register.html", methods = ['GET','POST'])
	def register():
		if request.method == 'POST':
			pwd = request.form["pwd"]
			pwd2 = request.form["pwd2"]
			if pwd == pwd2 :
				usr = request.form["usr"]
				db = dbInteracion(DBNAMEGAS)
				db.connect(GASLOGINTABLE)
				if db.userAvailable(usr,"usr") :
					encpwd = enPassowrdStrHex(pwd+usr) 
					db.saveUser(usr,enPassowrdStrHex(pwd))
					try:
						db.createUser(usr)
						session['loged'] = True
						session['user'] = usr
						session['encpwd'] = encpwd
					except db.userError():
						return "invalid user , please try with other username and password"		
		return render_template("register.html")
	@app.route(WEBPAGE+"resetes.html", methods = ['GET','POST'])
	def resetes():
		return render_template(".html")	
	@app.route(WEBPAGE+"gas_login.html", methods=['GET', 'POST'])
	def gaslogin():	
		usr = request.form['username']
		pwd = request.form["password"]
		encpwd = enPassowrdStrHex(pwd+usr)
		protectpwd = enPassowrdStrHex(pwd)
		db = dbInteracion(DBNAMEGAS)
		db.connect(GASLOGINTABLE)
		if db.findUser(usr) and db.findPassword(protectpwd)  :
			session['loged'] = True
			session['user'] = usr
			session['encpwd'] = encpwd
			return redirect("/gas.html")
		else:
			flash('wrong password!')
		return gas.gas()
	@app.route(WEBPAGE+'gas/actualisar<string:id>', methods = ['GET','POST'])
	def update_gas(id):
		user = session.get('user')
		db = dbInteracion(DBNAMEGAS)
		db.connect(TABLEGAS+user)
		key = session.get('encpwd')
		keys = len(DATANAMEGAS)*[key]
		if request.method == 'POST':
			data = multrequest(DATANAMEGAS)
			encdata = list(map(encryptAES , data, keys))
			encdata = list(map(str,encdata))
			del key,keys,data
			sentence = setUpdate(DATANAMEGAS,encdata)
			db.updateGas(sentence,id)
			flash(' Updated Successfully')
		return redirect('/gas.html')
	@app.route(WEBPAGE+'gas/editar<string:id>', methods = ['POST', 'GET'])
	def get_gas(id):
		user = session.get('user')
		db = dbInteracion(DBNAMEGAS)
		db.connect(TABLEGAS+user)
		key = session.get('encpwd')
		keys = len(DATANAMEGAS)*[key]
		rows = db.getDataGasWhere("item_id",id)[0]
		idData = [id]+list(map(decryptAES,rows,keys))
		del key,keys , user , rows
		return render_template('gas_update.html', purchase = idData )
	@app.route(WEBPAGE+"gas/eliminar/<string:id>", methods = ['GET','POST'])
	def gassdelete(id):
		user = session.get('user')
		db = dbInteracion(DBNAMEGAS)
		db.connect(TABLEGAS+user)
		db.deleteWhere("item_id",id)
		#flash('you delete that')
		return redirect('/gas.html')
if __name__=='__main__':
	app.run(debug=True,host="0.0.0.0",port=9600)