from flask import Flask, Response, render_template_string
import cv2

app = Flask(__name__)

# Cambia el índice de la cámara a la cámara virtual de OBS (puede ser 0, 1, etc.)
camera = cv2.VideoCapture(0)  # Cambia a 1 si 0 no funciona

def generate_frame():
    while True:
        # Captura el frame
        success, frame = camera.read()
        if not success:
            break
        # Codifica el frame como JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # Envía el frame como un flujo de bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template_string('''
    <html>
        <head>
            <title>Cámara Virtual de OBS</title>
            <style>
                body { display: flex; flex-direction: column; align-items: center; height: 100vh; margin: 0; background: black; }
                img { max-width: 100%; height: auto; }
                button { margin-top: 20px; padding: 10px; background-color: white; color: black; border: none; cursor: pointer; }
                button:hover { background-color: gray; }
            </style>
        </head>
        <body>
            <h1 style="color: white;">Transmisión de la Cámara Virtual de OBS</h1>
            <img id="video" src="/video" onclick="toggleFullScreen()">
            <button onclick="toggleFullScreen()">Pantalla Completa</button>
            <script>
                function toggleFullScreen() {
                    const img = document.getElementById('video');
                    if (img.requestFullscreen) {
                        img.requestFullscreen();
                    } else if (img.mozRequestFullScreen) { // Firefox
                        img.mozRequestFullScreen();
                    } else if (img.webkitRequestFullscreen) { // Chrome, Safari y Opera
                        img.webkitRequestFullscreen();
                    } else if (img.msRequestFullscreen) { // IE/Edge
                        img.msRequestFullscreen();
                    }
                }
            </script>
        </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
