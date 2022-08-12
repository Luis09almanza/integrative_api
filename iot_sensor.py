from http import client
import json
import time
import serial

# Creacion de un objeto de la clase HHTPConnetion
_conn = client.HTTPConnection('localhost', port=5000)

# Creacion de un objeto de la clase Sensor
ser = serial.Serial('COM9', 115200, timeout=1)

h = {'Content-type': 'application/json'}

notes = ['DO', 'RE', 'MI', 'FA', 'SOL', 'LA', 'SI']
    
last_note = ""

while True:
    raw_data = ser.readline()
    data = str(raw_data)
      
    #Selecciona una parte del string  
    value = data[2:5]
    
    #quita caracteres
    value_string = value.replace("r", '')
    value_string2 = value_string.replace("\\",'')
    
    #el string sin filtros
    finally_data = value_string2

    #Si los datos de los sensores estan dentro del array entonces..
    if finally_data in notes:
        
        if finally_data != last_note:
            last_note = finally_data
            print("Nota ingresada: " + last_note)
            
            json_data = json.dumps(str(last_note))
            _conn.request('POST', '/devices', json_data, headers=h)
            _conn.close()