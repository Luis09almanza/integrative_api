from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask_cors import CORS


app = Flask('__main__')

app.config['MONGO_URI'] = 'mongodb://localhost/integradoraTest'
mongo = PyMongo(app)
CORS(app)


userCollection = mongo.db.users
devicesCollection = mongo.db.devices

''' ######################## RECIBIR LAS NOTAS DEL DISPOSITIVO ✅###########################'''    
@app.route('/devices', methods=['POST'])
def save_device():
    device = request.json
    
    if device:
        devicesCollection.insert_one({
            "value":device
        })
        
        print(device)
        return device
    else:
        not_found()
 
 
''' ######################## OBTENER LAS NOTAS ✅###########################'''
@app.route('/devices', methods=['GET'])
def getValues():
    values = []
    
    for doc in devicesCollection.find():
        values.append({
            'values': doc['value']
        })
    return jsonify(values)
    
    
''' ############################# CREAR EL USUARIO ✅ ####################################'''
@app.route('/users', methods=['POST'])
def create_user():
    name = request.json['name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    isActive = request.json['isActive']
    created_at = datetime.now()
    
    # devices = request.json['device']
    
    if name and last_name and email and password and isActive:
        encrypted_pass = generate_password_hash(password)
        id = userCollection.insert_one({
            'name':name,
            'last_name':last_name,
            'email':email,
            'password':encrypted_pass,
            'is_active': isActive,
            'created_at': created_at
        })
        
        return jsonify((str(ObjectId(id.inserted_id))))
    else:
        not_found()



''' ############################# BORRAR USUARIOS ✅ ####################################'''       
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    userCollection.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'User Deleted Successfully'})
    response.status_code = 200
    return response



''' ############################# OBTENER USUARIOS POR ID ✅ ####################################'''    
@app.route('/users/<id>', methods=['GET'])
def getUser(id):
    user = userCollection.find_one({'_id': ObjectId(id)})
    print(user)
    
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'last_name': user['last_name'],
        'email': user['email'],
        'password': user['password'],
        'is_active':user['is_active'],
        'created_at':user['created_at']
    })
    
    
    
''' ############################# MODIFICAR USUARIOS POR ID ✅ ####################################''' 
@app.route('/users/<_id>', methods=['PUT'])
def update_user(_id):
    name = request.json['name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    isActive = request.json['isActive']

    if name and last_name and email and password and isActive and _id:
        encrypted_pass = generate_password_hash(password)
        userCollection.update_one(
            {'_id': ObjectId(_id)},
            {"$set":{
                'name':name,
                'last_name':last_name,
                'email':email,
                'password':encrypted_pass,
                'is_active': isActive,
            }}
        )
        
        response = jsonify({'message': 'User Updated'})
        response.status_code = 200
        return response
    else:
        return not_found



# Para que de error 404
@app.errorhandler(404)
def not_found(error=None):
    
    response = jsonify({
        'message': 'Resource Not Found: ' + request.url,
        'status':404
    })
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True)