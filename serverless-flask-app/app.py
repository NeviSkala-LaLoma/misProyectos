import json
import sqlite3
from types import NoneType
from flask import Flask, jsonify, make_response

app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def hello_from_root(event, context):    
    
    body = json.dumps(event["body"])  
    
    #Almaceno los inputs ingresados por el usuario
    
    #Realizo la conexión por la BD
    with sqlite3.connect("../bd/basedatos.db") as con:
        # for producto in body.values():
        cur = con.cursor()
        cur.execute("INSERT INTO productos (producto) VALUES (?)",[body])
        con.commit
    
    response = {
        "message" : "Producto guardado con exito!",
        "status" : 1
    }

    response = {"statusCode": 200, "body": json.dumps(response)}
        
    return response


@app.route("/hello", methods=["POST","GET"])
def hello(event, context):
    body = json.dumps(event["body"])

    #Realizo la conexión por la BD
    try:   
        with sqlite3.connect("../bd/basedatos.db") as con:
            cur = con.cursor()
            cur.execute(f"SELECT producto FROM productos WHERE idproducto = {body}")
            row = cur.fetchone()
           
            if type(row) == NoneType:
                mensaje = {
                    "message": "Registro no encontrado",
                    "status" : 0
                }    
                
                status = 500
                
            else:                                     
                mensaje = {
                        "message" : "Se encontró el registro con exito!",
                        "status" : 1,
                        "data": row[0][1:-1]   
                    }
                
                status = 200   
            
    except Exception as err:
        mensaje = {
            "message": str(err),
            "status" : 0
        }
        
        status = 500
    
    response = {"statusCode": status, "body": json.dumps(mensaje)}
        
    return response