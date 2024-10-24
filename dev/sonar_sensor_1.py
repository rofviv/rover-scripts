import serial
import time


arduino = serial.Serial(port='COM7', baudrate=9600, timeout=1)

# Función para leer los datos del sensor
def leer_sensor():
    try:
        while True:
            if arduino.in_waiting > 0:
                linea = arduino.readline().decode('utf-8').strip()
                try:
                    # Procesamos los datos del sensor
                    datos = linea.split(',')
                    sensor = int(datos[0])
                    distancia = float(datos[1])

                    print(f'sensor: {sensor} distancia: {distancia}')
                    
                except (IndexError, ValueError):
                    print("Error al procesar los datos del sensor")
            time.sleep(0.1)  # Ciclo continuo con un pequeño delay de 100ms para detectar cambios
    except Exception as e:
        print(f"Error en la lectura del sensor: {e}")
    finally:
        arduino.close()

# Ejecución principal
try:
    leer_sensor()
except KeyboardInterrupt:
    print("Programa detenido por el usuario")
finally:
    if arduino.is_open:
        arduino.close()
