#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
resetes - 2021 - por jero98772
resetes - 2021 - by jero98772
"""
from flask import request
from hashlib import  sha256
import base64
def multRequest(items):	
    values = []
    for item in items:		
        item = str(request.form.get(item))
        values.append(item)
    return values
def requestIngredients(items,amount): 
    values=[]
    for item in items:      
        tmpArray=[]
        if amount==1:
            for i in range(1,amount+1):
                #print(item,request.form.get(item+str(i)))
                tmpArray.append(request.form.get(item+str(i)))
        else:
            for i in range(1,amount):
                #print(item,request.form.get(item+str(i)))
                tmpArray.append(request.form.get(item+str(i)))
            #debugshit(tmpArray)
        values.append(str(tmpArray)[1:-1])
    return values
def enPassowrdStrHex(password):
    password = str(password)
    hashPassowrd = str(sha256(password.encode('utf-8')).hexdigest())
    return hashPassowrd
def enPassowrdHash(password):
    password = str(password)
    hashPassowrd = sha256(password.encode("utf-8")).digest()
    return hashPassowrd
def generatePassword():
    genPassowrd = ""
    for i in range(0,16):
        if len(genPassowrd) >= 16 and len(genPassowrd)-len(hexStr) <= 16:
            num=rnd.randint(0,9999)
            if 32>num>126:
                char=chr(num)
                genPassowrd+=char
            else:
                hexStr=str(hex(hexStr))
                genPassowrd+=hexStr
        else:
            break
    return enPassowrdStrHex(genPassowrd)
def setUpdate(dataname, data):
    sentence=dataname[0]+"="+'"'+data[0]+'"'
    for i,ii in zip(dataname[1:],data[1:]):
        sentence+=','+i+"="+'"'+ii+'"'
    return sentence
def debugshit(arr):
    for i in arr:
        print([str(i).replace(" ","-")])