from flask import Flask,request,make_response, jsonify
from pymongo import MongoClient

PORT = 3200
HOST = '0.0.0.0'

app = Flask(__name__)
uri = "mongodb+srv://admin:mesillas1@reto.so2nkgk.mongodb.net/?retryWrites=true&w=majority"


@app.route('/altausuario', methods=['POST'])
def create_user():

    req = request.get_json()

    if 'nombre' in req and 'usuario' in req and 'contrasena' in req:

        nombre = request.json["nombre"]
        usuario = request.json["usuario"]
        contrasena = request.json["contrasena"]
        client = MongoClient(uri)
        db = client.gettingStarted
        microservicios = db.microservicios

        existe = microservicios.find_one({"usuario":usuario})

        if existe:
            
            res = make_response(jsonify({"error":"El usuario ya existe"}),400)
            client.close
            return res
        else:    
            microservicios.insert_one({"nombre":nombre,"usuario":usuario,"contrasena":contrasena})
    

        res = make_response(jsonify({"mensaje":"El usuario se registro de manera correcta"}),200)
        client.close
        return res

    else:
        res = make_response(jsonify({"error":"Faltan datos en request"}),400)
        client.close
        return res



@app.route('/usuario', methods=['POST'])
def consulta_usuario():

    req = request.get_json()

    if 'usuario' in req and 'contrasena' in req:

        usuario = request.json["usuario"]
        contrasena = request.json["contrasena"]
        client = MongoClient(uri)
        db = client.gettingStarted
        microservicios = db.microservicios

        existe = microservicios.find_one({"usuario":usuario})
    
        if existe and usuario == existe["usuario"] and contrasena == existe["contrasena"]:

            res = make_response(jsonify({"nombre":existe["nombre"],"usuario":existe["usuario"]}),400)
            client.close
            return res
           
         
        else:    

            res = make_response(jsonify({"error":"El usuario o contraseña incorrectos"}),400)
            client.close
            return res
        
    else:
        res = make_response(jsonify({"error":"Faltan datos en request"}),400)
        client.close
        return res      




@app.route('/loginusuario', methods=['POST'])

def login_usuario():

    req = request.get_json()

    if 'usuario' in req and 'contrasena' in req:

        usuario = request.json["usuario"]
        contrasena = request.json["contrasena"]
        client = MongoClient(uri)
        db = client.gettingStarted
        microservicios = db.microservicios

        existe = microservicios.find_one({"usuario":usuario})
    
        if existe and usuario == existe["usuario"] and contrasena == existe["contrasena"]:

            access_token = create_access_token(identity=existe["usuario"])
            return make_response(jsonify({ "token": access_token}) ,200)   
            
        else:    

            res = make_response(jsonify({"error":"El usuario o contraseña incorrecto"}),400)
            return res
        
    else:
        res = make_response(jsonify({"error":"Faltan datos en request"}),400)
        return res   
   


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)

