from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from flask_cors import CORS


app = Flask('__main__')

app.config['MONGO_URI'] = 'mongodb://localhost/integradoraTest'
mongo = PyMongo(app)
CORS(app)


userCollection = mongo.db.users
devicesCollection = mongo.db.devices

  
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
 
 
@app.route('/devices', methods=['GET'])
def getValues():
    values = []
    
    for doc in devicesCollection.find():
        values.append({
            'values': doc['value']
        })
    return jsonify(values)
    
    
@app.route('/lastnote', methods=['GET'])
def getLastNote():
    
    values = []
    contador = 0
    
    for doc in devicesCollection.find():
        values.append({
            'values': doc['value']
        })
        
        contador += 1
      
    return jsonify(values[contador-1])

    
    
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
        id = userCollection.insert_one({
            'name':name,
            'last_name':last_name,
            'email':email,
            'password':password,
            'is_active': isActive,
            'created_at': created_at
        })
        
        return jsonify((str(ObjectId(id.inserted_id))))
    else:
        not_found()


  
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
    
    

@app.route('/users/login', methods=['POST'])
def validateUser():
    email = request.json['email']
    password = request.json['password']
    
    if email and password:
        validate = userCollection.find_one(
            {
                "email":email,
                "password": password
            }
        ) 
        
        print(validate)
        if validate == None:
            response = jsonify(False)
            return response
        else:
            return jsonify({
            '_id': str(ObjectId(validate['_id'])),
            'name': validate['name'],
            'last_name': validate['last_name'],
            'email': validate['email'],
            'password': validate['password'],
            'is_active':validate['is_active'],
            'created_at':validate['created_at']
        })
            
    else:
        not_found()

    
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