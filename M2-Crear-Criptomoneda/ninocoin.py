# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 09:06:47 2021

@author: gaspa
"""
# Modulo  - Create a Criptomoneda 
# Flask==0.12.2: pip install Flask==0.12.2
# CLiente HTTP Postman: https://www.getpostman.com/ 
# request==2.25.1: pip install requests==2.25.1 -> libreria de peticiones de python

# Importar las Librerias
import datetime # para poder utilizar tiempo
import hashlib
import json 
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse


# Parte 1 - Crear la Cadena de BLoques
class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = "0" )
        self.nodes = set()
        
        
    def create_block(self, proof, previous_hash):
        block = {"index" : len(self.chain)+1,
                 "timestamp" : str(datetime.datetime.now()),
                 "proof" : proof, 
                 "previous_hash" : previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys= True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1 
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_proof = previous_block["proof"]
            proof = block["proof"]
            operation = proof**2 - previous_proof**2
            hash_operation = hashlib.sha256(str(operation).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender, 
                                  'reciever': receiver,
                                  'amount' : amount})
        previous_block = self.previous_block()
        return previous_block['index'] + 1   

    def add_node(self, address):
        parsed_url = urlparse(address)
        node = parsed_url.netloc
        self.nodes.add(node)
        
        
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
          
# Parte 2 - Minado de un Bloque de la Cadena

# Crear una Aplicación Web, basada en Flask 
app = Flask(__name__)
# si se obtiene un Error 500 el ejecutar, actualziar Flask , reiniciar spyder y ejecutar la siguiente linea  
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Crear una Blockchain 
blockchain = Blockchain()

#Minar un nuevo Bloque 
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : 'felicidades por minar el Bloque!!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']}
    return jsonify(response), 200 

# Obtener la Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200 

# Tarea 
@app.route('/is_valid', methods=['GET'])
def is_valid():
    chain = blockchain.chain
    if blockchain.is_chain_valid(chain) == True:
        response = {'message': 'la cadena es correcta'}
    else:
        response = {'message': 'la cadena no es valida'}
    
    return jsonify(response), 200
         
# Parte 3 - Descentralizar la Cadena de Bloques
    

# Ejecutar la app
app.run(host= '0.0.0.0', port= 5000)
