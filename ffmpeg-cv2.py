import cv2
import subprocess
import numpy as np

# Parameter koneksi RTMP
rtmp_url = "rtmp://yourserver/live/streamkey"

# Resolusi video
width = 640
height = 480
fps = 30

# Inisialisasi capture video
cap = cv2.VideoCapture(0)  # Ganti dengan indeks kamera Anda atau path perangkat

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cap.set(cv2.CAP_PROP_FPS, fps)

# Periksa apakah kamera berhasil dibuka
if not cap.isOpened():
    print("Tidak dapat membuka kamera")
    exit()

# Perintah FFmpeg untuk streaming
ffmpeg_command = [
    'ffmpeg',
    '-y',
    '-f', 'rawvideo',
    '-vcodec','rawvideo',
    '-pix_fmt', 'bgr24',
    '-s', '{}x{}'.format(width, height),
    '-r', str(fps),
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'veryfast',
    '-f', 'flv',
    rtmp_url
]

# Inisialisasi proses FFmpeg
process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Gagal mendapatkan frame dari kamera")
            break

        # Pemrosesan citra (contoh: Canny Edge Detection)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Tampilkan frame yang diproses (opsional)
        cv2.imshow('Processed Frame', edges_colored)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Tulis frame yang diproses ke stdin FFmpeg
        process.stdin.write(edges_colored.tobytes())

except KeyboardInterrupt:
    print("Streaming dihentikan oleh pengguna")

finally:
    cap.release()
    process.stdin.close()
    process.wait()
    cv2.destroyAllWindows()
