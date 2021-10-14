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
INITTABLE="init"
app = Flask(__name__)
app.secret_key = str(enPassowrdHash(generatePassword()))
class resetes():
    generalInfoItems=["typeFood","amoutPersons","origin"]
    ingredients=["amout","amoutUnit","ingredient","notes"]
    WEBPAGE = "/"
    @app.route(WEBPAGE)
    def resetes():
        return render_template("resetes.html")
    @app.route(WEBPAGE+"addResetes.html", methods=['GET','POST'])
    def addResipe():
        if not session.get('loged'):
            return render_template('login.html')    
        else:
            if request.method=='POST':
                rows=int(request.form['amoutRows'])
                ingredientsData=requestIngredients(ingredients,rows)
                generalInfoData=multRequest(generalInfoItems)
                preparationProcess=request.form['preparationProcess']
                print("notas de preparacion")
                print(preparationProcess,generalInfoData,ingredientsData)
                db=dbInteracion(DBNAME)
                db.connect(LOGINTABLE)
        return render_template("add_recipe.html")
    @app.route(WEBPAGE+"resetes.html", methods=['GET','POST'])
    def publicResipes():
        return render_template("public_recipes.html")
    @app.route(WEBPAGE+"login.html", methods=['GET', 'POST'])
    def login():
        try:
            usr=request.form["username"]
            pwd=request.form["password"]
            protectpwd=enPassowrdStrHex(pwd)
            db=dbInteracion(DBNAME)
            db.connect(LOGINTABLE)
            if db.findUser(usr) and db.findPassword(protectpwd)  :
                session["loged"]=True
                session["user"]=usr
                return redirect("/resetes.html")
            else:
                flash("Contraseña invalida!")
            return resetes.resetes()
        except:
            if request.method=='POST':
                usr=request.form["username"]
                pwd=request.form["password"]
                protectpwd=enPassowrdStrHex(pwd)
                db=dbInteracion(DBNAME)
                db.connect(LOGINTABLE)
                print(usr,protectpwd)
                if db.findUser(usr) and db.findPassword(protectpwd)  :
                    session["loged"]=True
                    session["user"]=usr
                    return redirect("/resetes.html")
                else:
                    flash("Contraseña invalida!")
            return render_template('login.html')    
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
                    except db.userError():
                        return "Usuario invalido , por favor intente con otro usuario y clave"		
        return render_template("register.html")
if __name__=='__main__':
    app.run(debug=True,host="0.0.0.0",port=9600)