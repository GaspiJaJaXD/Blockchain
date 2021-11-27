# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 22:56:33 2021

@author: gaspa
"""

# Modulo 1 - Create a Blockchain 
# Flask==0.12.2: pip install Flask==0.12.2
# CLiente HTTP Postman: https://www.getpostman.com/ 

# Importar las Librerias
import datetime # para poder utilizar tiempo
import hashlib
import json 
from flask import Flask, jsonify

# Parte 1 - Crear la Cadena de BLoques
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = "0" )
        
        
    def create_block(self, proof, previous_hash):
        block = {"index" : len(self.chain)+1,
                 "timestamp" : str(datetime.datetime.now()),
                 "proof" : proof, 
                 "previous_hash" : previous_hash }
        
        self.chain.append(block)
        return block


# Parte 2 - Minado de un Bloque de la Cadenab