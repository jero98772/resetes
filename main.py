#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
resetes - 2021 - por jero98772
resetes - 2021 - by jero98772
"""
from flask import Flask, render_template, request, flash, redirect ,session,render_template_string
from tools.dbInteracion import dbInteracion
from tools.tools import *

global WEBPAGE
DBPATH="data/"
DBNAME=DBPATH+"general_use"
USERDB=DBPATH+"general_use"
LOGINTABLE="login"
TABLE="publicResipes"
app=Flask(__name__)
app.secret_key = str(enPassowrdHash(generatePassword()))
generalInfoItems=["typeFood","amoutPersons","origin"]
ingredients=["amout","amoutUnit","ingredient","notes"]
WEBPAGE="/"
dbitems=["title"]+generalInfoItems+ingredients+["preparationProcess"]+["user"]
class resetes():
    @app.route(WEBPAGE)
    def resetes():
        #ok
        db=dbInteracion(DBNAME)
        db.connect(TABLE)
        data=db.getData()
        return render_template("resetes.html",data=data)
    @app.route(WEBPAGE+"addResetes.html", methods=['GET','POST'])
    def addResipe():
        #ok
        if not session.get('loged'):
            return redirect("login.html")    
        else:
            db=dbInteracion(DBNAME)
            db.connect(TABLE)
            if request.method=='POST':
                rows=int(request.form['amoutRows'])
                title=request.form['title']
                preparationProcess=request.form['preparationProcess']
                generalInfoData=multRequest(generalInfoItems)
                ingredientsData=requestIngredients(ingredients,rows)
                print("\n",ingredients,rows,"\n")
                #remvomeChars=maketrans("\n\t\r","   ")
                #request.form['preparationProcess']#.translate(remvomeChars)

                print("titulo",title)
                print("notas de preparacion",preparationProcess)
                print("general info",generalInfoData)
                print("ingredient",ingredientsData)
                db.addRestes(dbitems,[title]+generalInfoData+ingredientsData+[preparationProcess]+[session["user"]])
        return render_template("add_recipe.html")
    @app.route(WEBPAGE+"login_.html", methods=['GET', 'POST'])
    def loginInterface():
        #ok
        if not session.get('loged'):
            return redirect("login.html")
        else:
            return "<center><h1>Ya estas logeado</h1></center>"
    @app.route(WEBPAGE+"login.html", methods=['GET', 'POST'])
    def login():
        msjError=""
        if request.method=="POST":
            usr=request.form["username"]
            pwd=request.form["password"]
            protectpwd=enPassowrdStrHex(pwd)
            db=dbInteracion(DBNAME)
            db.connect(LOGINTABLE)
            if db.findUser(usr) and db.findPassword(protectpwd)  :
                session["loged"]=True
                session["user"]=usr
                return redirect("/")
            else:
                msjError="Contraseña invalida!"
        return render_template("login.html",error=msjError) 
    @app.route(WEBPAGE+"register.html", methods = ['GET','POST'])
    def register():
        #ok
        msjError=""
        if request.method=="POST":
            pwd=request.form["pwd"]
            pwd2=request.form["pwd2"]
            if pwd==pwd2 :
                usr=request.form["usr"]
                db=dbInteracion(DBNAME)
                db.connect(LOGINTABLE)
                if db.userAvailable(usr,"usr") :
                    try:
                        db.saveUser(usr,enPassowrdStrHex(pwd))
                        #db.createUser(usr,"resetes")
                        session["loged"]=True
                        session["user"]=usr
                        return redirect("/")
                    except db.userError():
                        return "Usuario invalido , por favor intente con otro usuario y clave"		
            else:msjError="passwords are diferent"
        return render_template("register.html",error=msjError)
    @app.route(WEBPAGE+"byebye.html")
    def closeSession():
        #ok
        session['loged']=False
        session['user']=""
        return redirect("/")
#to check
    @app.route(WEBPAGE+"actualisar<string:id>", methods = ['GET','POST'])
    def update(id):
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
    @app.route(WEBPAGE+"editar<string:id>", methods = ['POST', 'GET'])
    def get_gas(id):
        user = session.get('user')
        db = dbInteracion(DBNAMEGAS)
        db.connect(TABLEGAS+user)
        key = session.get('encpwd')
        keys = len(DATANAMEGAS)*[key]
        rows = db.getDataGasWhere(id,"id")[0]
        idData = [id]+list(map(decryptAES,rows,keys))
        del key,keys , user , rows
        return render_template('gas_update.html', purchase = idData )
    @app.route(WEBPAGE+"eliminar/<string:id>", methods = ['GET','POST'])
    def delete(id):
        db=dbInteracion(DBNAME)
        db.connect(TABLE)
        print("get req")
        print(session.get('user'),db.authChange(id))
        if session.get('user')==db.authChange(id):
            db.deleteWhere(id)
            flash("Delete success")
        else:
            
             #redirect(WEBPAGE+"login.html")
            return render_template_string("{% extends  'template.html'%}{% block content %}<center><br><br><br><br><h1>You need autheticate to delete something<br><br><a href='/login.html'>Autheticate here</a></h1></center>{% endblock%}")
        return redirect(WEBPAGE)

#finish cheking
if __name__=='__main__':
    app.run(debug=True,host="127.0.0.1",port=9600)