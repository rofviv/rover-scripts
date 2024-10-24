import pyrealsense2 as rs
import numpy as np
import cv2

# Configurar el pipeline de RealSense
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)

# Iniciar la transmisión
profile = pipeline.start(config)

# Obtener el sensor de profundidad
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

# Crear un filtro de colormap
colorizer = rs.colorizer()
colorizer.set_option(rs.option.visual_preset, 1)  # Configurar el preset

try:
    while True:
        # Obtener frames
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue

        # Aplicar colormap a la imagen de profundidad
        depth_colormap = np.asanyarray(colorizer.colorize(depth_frame).get_data())

        # Mostrar la imagen de profundidad con colormap
        cv2.imshow('RealSense Depth', depth_colormap)

        # Salir si se presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    pipeline.stop()
    cv2.destroyAllWindows()
