#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
resetes - 2021 - por jero98772
resetes - 2021 - by jero98772
"""
import sqlite3
class dbInteracion():
	def __init__(self,dbName):
		self.dbName = str(dbName)
	def connect(self,tableName):
		self.tableName = str(tableName)
		self.connecting = sqlite3.connect(self.dbName)
		self.cursor = self.connecting.cursor()
		return self.cursor
	def userAvailable(self,user,pwd,item="usr"):
		dbcomand =  "SELECT * FROM {0} WHERE {1} =  '{2}' ".format(self.tableName,item,user)
		self.cursor.execute(dbcomand)
		users = self.cursor.fetchall()
		print(users)
		if (user in users) and (pwd in users):
			return False
		else:
			return True
	def userError(self):
		return sqlite3.OperationalError
	def saveUser(self,usr,pwd):
		insertUser = "INSERT INTO {0}(usr, pwd) VALUES( ?, ? );".format(self.tableName)
		self.cursor.execute(insertUser,(usr,pwd))
		self.cursor.connection.commit()
	def createUser(self,usr,salt="resetes"):
		dbcomand='CREATE TABLE "{0}{1}" ("id"	INTEGER,"typeFood"	TEXT,"amoutPersons"	INTEGER,"origin"	TEXT,"amouts"	TEXT,"amoutUnits"	TEXT,"ingredients"	TEXT,"notes"	TEXT,PRIMARY KEY("id" AUTOINCREMENT));'
		self.cursor.execute(dbcomand)
		self.cursor.connection.commit()
	def findUser(self,user):
		userTuple = (user,)
		dbcomand =  "SELECT usr FROM {0} Where usr =  ? ".format(self.tableName)
		self.cursor.execute(dbcomand,userTuple)
		userDb = self.cursor.fetchall()
		try:
			if userDb[0] == userTuple :
				return True
			else :
				return False
		except:
			return False
	def findPassword(self,password):
		passwordTulple = (password,)
		dbcomand =  "SELECT pwd FROM {0} WHERE pwd =  ? ".format(self.tableName)
		self.cursor.execute(dbcomand,passwordTulple)
		passwordHash = self.cursor.fetchall()
		try:
			if  passwordHash[0] == passwordTulple:
				return True
			else :
				return False
		except:
			return False
	
	def addGas(self,dbItems,data ):
		dbcomand = str("INSERT INTO {0} {1}  VALUES {2} ;".format(self.tableName,tuple(dbItems),tuple(data)))
		self.cursor.execute(dbcomand)
		self.cursor.connection.commit()
	def getDataGasWhere(self,row,equals):
		dbcomand = " SELECT * FROM {0} WHERE {1} = {2} ;".format(self.tableName,row,equals)
		self.cursor.row_factory = lambda cursor, row: list(row[1:])
		self.cursor.execute(dbcomand)
		alldata = self.cursor.fetchall()
		return alldata
		self.cursor.row_factory = sqlite3.Row
	def getDataGas(self):
		dbcomand = " SELECT * FROM {0} ;".format(self.tableName)
		self.cursor.row_factory = lambda cursor, row: list(row[1:])
		self.cursor.execute(dbcomand)
		alldata = self.cursor.fetchall()
		return alldata
		self.cursor.row_factory = sqlite3.Row
	def update(self,updateSentence, id):
		dbcomand = str("UPDATE {0} SET {1} WHERE item_id = {2}; ".format((self.tableName),updateSentence,id))
		self.cursor.execute(dbcomand)
		self.cursor.connection.commit()
	def closeDB(self):
		self.cursor.close()
