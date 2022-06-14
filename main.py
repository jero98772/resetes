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
ingredients=["amout","amoutUnit","ingredient","price","notes"]
WEBPAGE="/"
dbitems=["title"]+generalInfoItems+ingredients+["preparationProcess"]+["user"]+["rows"]
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
                #preparationProcess=request.form['preparationProcess']
                preparationProcess=request.form['preparationProcess'].replace("\t"," ").replace("\r"," ").replace("\n","<br>")
                generalInfoData=multRequest(generalInfoItems)
                ingredientsData=requestIngredients(ingredients,rows)
                db.addRestes(dbitems,[title]+generalInfoData+ingredientsData+[preparationProcess]+[session["user"]]+[rows])
        return render_template("add_recipe.html")
    @app.route(WEBPAGE+"login_.html", methods=['GET', 'POST'])
    def loginInterface():
        #ok
        if not session.get('loged'):
            return redirect("login.html")
        else:
            return "<center><h1>Ya estas logeado</h1></center><br><a href="+WEBPAGE+"profile/"+session["user"]+">tu perfil</a>"
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
    @app.route(WEBPAGE+"register.html", methods=['GET','POST'])
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
    @app.route(WEBPAGE+"actualisar/<string:id>", methods=['GET','POST'])
    def doUpdate(id):
        if request.method=='POST':
            db=dbInteracion(DBNAME)
            db.connect(TABLE)
            if session.get("user")==db.authChange(id):
                rows=int(request.form['amoutRows'])
                title=request.form['title']
                preparationProcess=request.form['preparationProcess'].replace("\t"," ").replace("\r"," ").replace("\n","<br>")
                generalInfoData=multRequest(generalInfoItems)
                ingredientsData=requestIngredients(ingredients,rows+1)
                #debugshit(ingredientsData)
                sentence=setUpdate(dbitems,[title]+generalInfoData+ingredientsData+[preparationProcess]+[session["user"]]+[str(rows)])
                db.update(sentence,id)
        return redirect(WEBPAGE)
#finish cheking
    @app.route(WEBPAGE+"editar/<string:id>", methods=['POST', 'GET'])
    def update(id):
        #ok
        msjError=""
        db=dbInteracion(DBNAME)
        db.connect(TABLE)
        rows=db.getDataWhere(id,"id")
        if session.get("user")!=db.authChange(id):
            msjError="Nesitas auteticacion para editar,con el usuario que escribio la receta."
        #debugshit(rows[0])
        return render_template("update.html",data=rows[0],error=msjError)
    @app.route(WEBPAGE+"eliminar/<string:id>", methods=['GET','POST'])
    def delete(id):
        db=dbInteracion(DBNAME)
        db.connect(TABLE)
        if session.get("user")==db.authChange(id):
            db.deleteWhere(id)
            flash("Delete success")
        elif session.get("user")=="" :
             return render_template_string("{% extends  'template.html'%}{% block content %}<center><br><br><br><br><h1><div class='required'><p><strong>Error:</strong>Nesitas auteticacion para eliminar.</div><br><br><a href='/login.html'>autenticarse</a></h1></center>{% endblock%}")
        else:
             #redirect(WEBPAGE+"login.html")
            return render_template_string("{% extends  'template.html'%}{% block content %}<center><br><br><br><br><h1><div class='required'><p><strong>Error:</strong>Nesitas auteticacion con el usuario que escribio la receta.</div></h1></center>{% endblock%}")
        return redirect(WEBPAGE)
    
    @app.route(WEBPAGE+"profile.html", methods=['GET','POST'])
    def userProfile():
        if session['loged']:
            return redirect(WEBPAGE+"profile/"+session["user"])
        else:
            return render_template_string("{% extends  'template.html'%}{% block content %}<center><br><br><br><br><h1><div class='required'><p><strong>Error:</strong>Nesitas auteticacion.</div></h1></center>{% endblock%}")
    @app.route(WEBPAGE+"profile/<string:user>", methods=['GET','POST'])
    def profile(user):
        db=dbInteracion(DBNAME)
        db.connect(TABLE)
        data=db.getDataWhere("user","'"+user+"'")
        return render_template("profile.html",data=data)
#add manifest
#add voice resetes
if __name__=='__main__':
    app.run(debug=True,host="0.0.0.0",port=9600)