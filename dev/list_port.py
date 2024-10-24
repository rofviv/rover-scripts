import serial.tools.list_ports

def listar_puertos():
    puertos = list(serial.tools.list_ports.comports())
    if len(puertos) == 0:
        print("No se han encontrado puertos.")
    else:
        for puerto in puertos:
            print(f"Puerto: {puerto.device} - Descripción: {puerto.description}")

listar_puertos()
