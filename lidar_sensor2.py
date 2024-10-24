from flask import Flask, jsonify, render_template
from rplidar import RPLidar
import os
import time
import threading

app = Flask(__name__)

# Variables globales para los datos del LiDAR
lidar_data = {'left': 0, 'right': 0, 'front': 0}

# Set Correct Com/USB port
port_com_lidar = os.getenv('PORT_COM_LIDAR', 'COM10')
lidar = RPLidar(port_com_lidar, 256000)

def lidar_scanner():
    global lidar_data
    print("starting spinning .......\n")
    time.sleep(5)
    print("scanning started")

    try:
        for scan in lidar.iter_scans():
            for (_, angle, distance) in scan:
                # Detectar objetos en diferentes lados
                if (angle > 350.0 and angle < 359.9 and distance < 400):
                    lidar_data['front'] = distance
                    print("Frontal detectado")

                if (angle > 90.0 and angle < 91.0 and distance < 400):
                    lidar_data['left'] = distance
                    print("Izquierda detectada")

                if (angle > 270.0 and angle < 271.0 and distance < 400):
                    lidar_data['right'] = distance
                    print("Derecha detectada")

    except KeyboardInterrupt:
        print('Stopping.')

    finally:
        lidar.stop()
        lidar.stop_motor()
        lidar.disconnect()

# Endpoint para servir la página HTML
@app.route('/')
def index():
    return render_template('lidar_heatmap.html')

# Endpoint para enviar los datos del LiDAR al cliente
@app.route('/lidar-data')
def get_lidar_data():
    return jsonify(lidar_data)

if __name__ == "__main__":
    # Iniciar la lectura del LiDAR en un hilo separado
    lidar_thread = threading.Thread(target=lidar_scanner)
    lidar_thread.daemon = True
    lidar_thread.start()

    # Iniciar el servidor Flask
    app.run(debug=True)
