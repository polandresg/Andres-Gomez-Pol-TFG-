import cv2
import numpy as np
import subprocess
import threading
from ultralytics import YOLO

# CONFIGURACIÓN 
url_camara_1 = 'rtsp://admin:sartisarti@192.168.1.12:554/stream1'
url_camara_2 = 'rtsp://admin:sartisarti@192.168.1.13:554/stream1'

FPS = "30"        # Target fps para ffmpeg
VBR = "6000k"
QUAL = "ultrafast"
YOUTUBE_URL = "rtmp://a.rtmp.youtube.com/live2/"
KEY = "rzrm-rsbr-hybk-tu36-3szx"

out_w, out_h = 1920, 1080
final_width, final_height = out_w , out_h
yolo_w, yolo_h = 960, 540

REPETICIONES = 2  # Número de veces que se manda el mismo frame

model = YOLO('nano.pt')

# FUNCION PARA GENERAR REMAPEOS 
def generar_mapas(cx, cy, r, out_w, out_h):
    theta = np.linspace(-np.pi / 2, np.pi / 2, out_w)
    phi = np.linspace(-np.pi / 2, np.pi / 2, out_h)
    theta, phi = np.meshgrid(theta, phi)

    x = np.cos(phi) * np.sin(theta)
    y = np.sin(phi)
    z = np.cos(phi) * np.cos(theta)

    angle = np.arccos(z)
    radius = angle / (np.pi / 2) * r

    denom = np.sqrt(x**2 + y**2) + 1e-8
    x_img = cx + radius * (x / denom)
    y_img = cy + radius * (y / denom)

    return x_img.astype(np.float32), y_img.astype(np.float32)

# CAPTURA DE LAS CÁMARAS 
captura_1 = cv2.VideoCapture(url_camara_1)
captura_2 = cv2.VideoCapture(url_camara_2)

ret1, frame1 = captura_1.read()
ret2, frame2 = captura_2.read()
assert ret1 and ret2, "No se pudo leer de las cámaras."

H1, W1 = frame1.shape[:2]
map_x1, map_y1 = generar_mapas(W1 // 2 + 35, H1 // 2 - 15, int(H1 * 0.48), out_w, out_h)

H2, W2 = frame2.shape[:2]
map_x2, map_y2 = generar_mapas(W2 // 2 + 30, H2 // 2 + 15, int(H2 * 0.48), out_w, out_h)

frame_flat1 = None
frame_flat2 = None

def captura_hilo(captura, map_x, map_y, update_func):
    while True:
        ret, frame = captura.read()
        if ret:
            remap = cv2.remap(frame, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
            update_func(remap)

def set_frame1(f): global frame_flat1; frame_flat1 = f
def set_frame2(f): global frame_flat2; frame_flat2 = f

threading.Thread(target=captura_hilo, args=(captura_1, map_x1, map_y1, set_frame1), daemon=True).start()
threading.Thread(target=captura_hilo, args=(captura_2, map_x2, map_y2, set_frame2), daemon=True).start()

# CONFIGURACIÓN DE FFmpeg 
command = [
    "ffmpeg", "-hide_banner",
    "-f", "rawvideo", "-pixel_format", "bgr24", "-video_size", f"{final_width}x{final_height}",
    "-framerate", FPS, "-i", "-",
    "-f", "lavfi", "-i", "anullsrc=sample_rate=44100:channel_layout=mono",
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "-profile:v", "high", "-level", "4.1",
    "-vf", "fifo", "-preset", QUAL,
    "-b:v", VBR, "-maxrate", VBR, "-bufsize", "10000k",
    "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
    "-f", "flv", f"{YOUTUBE_URL}{KEY}"
]
ffmpeg_process = subprocess.Popen(command, stdin=subprocess.PIPE)

# BUCLE PRINCIPAL 
while True:
    if frame_flat1 is None or frame_flat2 is None:
        continue

    combined = np.hstack((frame_flat1, frame_flat2))

    # YOLO en pequeño
    small_combined = cv2.resize(combined, (yolo_w * 2, yolo_h))
    results = model.predict(source=small_combined, stream=False, verbose=False)
    annotated_small = results[0].plot()

    # Escalado de imágen de nuevo 
    annotated_final = cv2.resize(annotated_small, (final_width, final_height))

    # Enviar el mismo frame 4 veces
    for _ in range(4):
        ffmpeg_process.stdin.write(annotated_final.tobytes())
