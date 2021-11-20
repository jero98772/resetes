#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
resetes - 2021 - por jero98772
resetes - 2021 - by jero98772
"""
from flask import Flask, render_template, request, flash, redirect ,session
from tools.dbInteracion import dbInteracion
from tools.tools import *
DBPATH="data/"
DBNAME=DBPATH+"general_use"
USERDB=DBPATH+"general_use"
LOGINTABLE="login"
TABLESALT="resetes"
app=Flask(__name__)
app.secret_key = str(enPassowrdHash(generatePassword()))
ingredients=["amout","amoutUnit","ingredient","notes"]
generalInfoItems=["typeFood","amoutPersons","origin"]
class resetes():
    WEBPAGE = "/"
    @app.route(WEBPAGE)
    def resetes():
        return render_template("resetes.html")
    @app.route(WEBPAGE+"addResetes.html", methods=['GET','POST'])
    def addResipe():
        if not session.get('loged'):
            return redirect("login.html")    
        else:
            db=dbInteracion(DBNAME)
            db.connect(TABLESALT+session["user"])
            if request.method=='POST':
                rows=int(request.form['amoutRows'])
                ingredientsData=requestIngredients(ingredients,rows)
                generalInfoData=multRequest(generalInfoItems)
                preparationProcess=request.form['preparationProcess']
                print("notas de preparacion")
                print(preparationProcess,generalInfoData,ingredientsData)
        return render_template("add_recipe.html")
    @app.route(WEBPAGE+"resetes.html", methods=['GET','POST'])
    def publicResipes():
        return render_template("public_recipes.html")
    @app.route(WEBPAGE+"login_.html", methods=['GET', 'POST'])
    def loginInterface():
        if not session.get('loged'):
            return redirect("login.html")
        else:
            return "<center><h1>Ya estas logeado</h1></center>"
    @app.route(WEBPAGE+"login.html", methods=['GET', 'POST'])
    def login():
        if request.method=='POST':
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
                flash("Contraseña invalida!")
            return resetes.resetes()
        return render_template("login.html") 
    @app.route(WEBPAGE+"register.html", methods = ['GET','POST'])
    def register():
        if request.method == 'POST':
            pwd=request.form["pwd"]
            pwd2=request.form["pwd2"]
            if pwd==pwd2 :
                usr=request.form["usr"]
                db=dbInteracion(DBNAME)
                db.connect(LOGINTABLE)
                if db.userAvailable(usr,"usr") :
                    print(pwd,enPassowrdStrHex(pwd))
                    db.saveUser(usr,enPassowrdStrHex(pwd))
                    try:
                        usersdb=dbInteracion(USERDB)
                        usersdb.connect(INITTABLE)
                        usersdb.createUser(usr,"resetes")
                        session['loged'] = True
                        session['user'] = usr
                        return redirect("/")
                    except db.userError():
                        return "Usuario invalido , por favor intente con otro usuario y clave"		
        return render_template("register.html")
if __name__=='__main__':
    app.run(debug=True,host="0.0.0.0",port=9600)