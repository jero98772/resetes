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
        item = request.form.get(item)
        try:
            item = int(item)
        except:	
            item = str(item)
        values.append(item)
    return values
def requestIngredients(items,amount): 
    values=[]
    ii=0
    for item in items:      
        tmpArray=[]
        for i in range(0,amount):
            tmpArray.append(request.form.get(item+str(i)))
        values.append(str(tmpArray))
    return values
def enPassowrdStrHex(password):
    password = str(password)
    hashPassowrd = str(sha256(password.encode('utf-8')).hexdigest())
    return hashPassowrd
