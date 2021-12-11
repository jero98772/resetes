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
TABLESALT="publicResipes"
app=Flask(__name__)
app.secret_key = str(enPassowrdHash(generatePassword()))
generalInfoItems=["typeFood","amoutPersons","origin"]
ingredients=["amout","amoutUnit","ingredient","notes"]
class resetes():
    WEBPAGE = "/"
    @app.route(WEBPAGE)
    def resetes():
        #ok,but i need add info and clear html file 
        return render_template("resetes.html")
    @app.route(WEBPAGE+"addResetes.html", methods=['GET','POST'])
    def addResipe():
        if not session.get('loged'):
            return redirect("login.html")    
        else:
            db=dbInteracion(DBNAME)
            db.connect(TABLESALT)
            if request.method=='POST':
                rows=int(request.form['amoutRows'])
                title=request.form['title']
                preparationProcess=request.form['preparationProcess']
                generalInfoData=multRequest(generalInfoItems)
                ingredientsData=requestIngredients(ingredients,rows)
                print("\n",ingredients,rows,"\n")
                preparationProcess=request.form['preparationProcess']
                print("titulo",title)
                print("notas de preparacion",preparationProcess)
                print("general info",generalInfoData)
                print("ingredient",ingredientsData)
                db.addRestes(["title"]+generalInfoItems+ingredients+["preparationProcess"],[title]+generalInfoData+ingredientsData+[preparationProcess])
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
if __name__=='__main__':
    app.run(debug=True,host="0.0.0.0",port=9600)