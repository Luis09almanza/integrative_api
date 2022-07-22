from http import client
import json
import time
import serial

# Creacion de un objeto de la clase HHTPConnetion
_conn = client.HTTPConnection('localhost', port=5000)

# Creacion de un objeto de la clase Sensor
ser = serial.Serial('COM5', 9600, timeout=1)

h = {'Content-type': 'application/json'}



while True:
    raw_data = ser.readline()
    data = str(raw_data)
        
    value = data[2:5]
    value_string = value.replace("\\", '')
    data2 = value_string
    json_data = json.dumps(str(data2))

    _conn.request('POST', '/devices', json_data, headers=h)
    _conn.close()
    
    print(value_string)
    time.sleep(2)
        