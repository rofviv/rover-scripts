from pymavlink import mavutil

def send_rc_override(channel, value, host='10.13.13.4', port=14551):
    """
    Envía un comando de sobreescritura de RC a MAVProxy usando pymavlink.
    
    :param channel: Canal de RC que quieres controlar (1-8).
    :param value: Valor de sobreescritura en microsegundos (1000-2000).
    :param host: La dirección IP del MAVProxy.
    :param port: El puerto UDP en el que MAVProxy está escuchando.
    """
    # Conéctate al puerto UDP especificado
    master = mavutil.mavlink_connection(f'udp:{host}:{port}')
    
    # Espera hasta que el sistema esté disponible
    master.wait_heartbeat()
    print("Conectado al sistema con ID:", master.target_system)
    
    # Envía el comando de sobreescritura de RC
    master.mav.rc_channels_override_send(
        master.target_system,
        master.target_component,
        0,  # Canal 1 (específico de tu caso)
        0,  # Canal 2
        value if channel == 3 else 0,  # Canal 3
        0,  # Canal 4
        0,  # Canal 5
        0,  # Canal 6
        0,  # Canal 7
        0   # Canal 8
    )

    print(f"Comando RC {channel} {value} enviado")

if __name__ == "__main__":
    channel = 3  # Canal que deseas controlar
    value = 1000  # Valor que deseas enviar
    send_rc_override(channel, value)

# NO MUEVE TODO EL SERVO, REVISAR