import os
import pyvisa as visa
import time
import requests

# TODO: SET IP STATIC ARDUINO
base_ip_relay_env = os.getenv('BASE_IP_RELAY', '0.0.0.0')
base_url_patio_env = os.getenv('BASE_URL_PATIO', 'https://www.patio-driver.patiodelivery2.com')
token_patio_env = os.getenv('TOKEN_PATIO', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDQsInVzZXJuYW1lIjoic2NAdGVzdC5jb20iLCJpYXQiOjE3MjE3NjY5NjgsImV4cCI6MTc1MzMwMjk2OH0.UrIetzHOSBcTlMdeOD_TRyj4eLIHMdzx-SxZXSfwQM4')

baseUrlRover = f"http://{base_ip_relay_env}"
baseUrlPatio = base_url_patio_env
# TODO: GET TOKEN ROVER APP
tokenPatio = token_patio_env

print("Starting nextion script...")
ports = visa.ResourceManager()
print(ports.list_resources())

# TODO: SET INPUT CORRECT (CHECK CONSOLE)
while True:
  try:
    serialPort = ports.open_resource('ASRL8::INSTR')
    serialPort.baud_rate = 9600
    print("NEXTION Connection successfully!")
    break
  except:
    print(f"Error al conectar al puerto serie:. Reintentando en 5 segundos...")
    time.sleep(5)

def openDoorOne():
  # requests.get(baseUrlRover+'/first-lock?value=1')
  requests.get(baseUrlRover+'/relay8')
  serialPort.write_raw(b'textComplete.txt="Opening door number one"')
  serialPort.write_raw(b'\xff\xff\xff')
  serialPort.write_raw(b'buttonComplete.txt="Close 1"')
  serialPort.write_raw(b'\xff\xff\xff')
  
def openDoorTwo():
  # requests.get(baseUrlRover+'/second-lock?value=1')
  requests.get(baseUrlRover+'/relay5')
  serialPort.write_raw(b'textComplete.txt="Door number two open, open the door"')
  serialPort.write_raw(b'\xff\xff\xff')
  serialPort.write_raw(b'buttonComplete.txt="Close 2"')
  serialPort.write_raw(b'\xff\xff\xff')
  

def findOrderByPassword(password):
  try:
    url = baseUrlPatio+"/api/orders/" + password
    headers = {
      'accept': 'application/json',
      'Authorization': 'Bearer '+tokenPatio
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()

        sms_status_value = data["data"]["sms_status"]
        
        if (sms_status_value == 0 or sms_status_value == 1):
          openDoorOne()
        elif (sms_status_value == 2):
          openDoorTwo()
        else:
          serialPort.write_raw(b'textComplete.txt="Something went wrong, try again"')
          serialPort.write_raw(b'\xff\xff\xff')
        
    else:
        print(f"Error en la solicitud. Código de estado: {response.status_code}")
        serialPort.write_raw(b'textComplete.txt="Incorrect password, try again"')
        serialPort.write_raw(b'\xff\xff\xff')

  except requests.exceptions.RequestException as e:
    serialPort.write_raw(b'textComplete.txt="Something went wrong, try again"')
    serialPort.write_raw(b'\xff\xff\xff')
    print(f"Error en la solicitud: {e}")
    

def verifyPassword(password):
  if password == "":
    serialPort.write_raw(b'textComplete.txt="Password is empty, try again"')
    serialPort.write_raw(b'\xff\xff\xff')
  else:
    serialPort.write_raw(b'textComplete.txt="Checking password..."')
    serialPort.write_raw(b'\xff\xff\xff')
    time.sleep(2)
    findOrderByPassword(password)

while(True):
  if(serialPort.bytes_in_buffer>0):
    data = serialPort.read_bytes(serialPort.bytes_in_buffer).decode('utf-8', errors='ignore')
    print(data)
    if "enter" in data:
      password = data.replace('enter', '')
      verifyPassword(password)
    elif data == "Close 1":
      # requests.get(baseUrlRover+'/first-lock?value=0')
      requests.get(baseUrlRover+'/relay8')
    elif data == "Close 2":
      # requests.get(baseUrlRover+'/second-lock?value=0')
      requests.get(baseUrlRover+'/relay5')
  time.sleep(2)