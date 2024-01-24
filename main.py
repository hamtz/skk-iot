import cv2
import os
from flask import Flask, render_template, send_from_directory, Response, request, redirect, url_for
# from wiringpi import wiringpi, GPIO

app = Flask(__name__, static_folder='assets', template_folder='templates')

cap = cv2.VideoCapture(1)
cap.set(3, 360)
cap.set(4, 240)

# Inisialisasi WiringPi
# wiringpi.wiringPiSetup()
# led_pin = 10
# wiringpi.pinMode(led_pin, GPIO.OUTPUT)

# wiringpi.digitalWrite(led_pin, GPIO.HIGH)


def generate_frames():
    if not cap.isOpened():
        print("Kamera tidak dapat diakses")
    else:
        while True:
            success, frame = cap.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#
# def get_image_list():
#     image_path = 'assets/captured'
#     image_list = [filename for filename in os.listdir(
#         image_path) if filename.endswith('.jpg')]
#     return image_list


def get_image_list():
    image_path = 'assets/captured'
    image_list = [filename for filename in os.listdir(image_path) if filename.endswith('.jpg')]
    sorted_image_list = sorted(image_list)
    return sorted_image_list

# Contoh penggunaan
sorted_images = get_image_list()
for image in sorted_images:
    print(image)


@app.route('/')
def index():
    captured_folder = 'assets/captured'
    # Menghitung jumlah file gambar dalam folder captured
    image_count = len([f for f in os.listdir(captured_folder)
                      if f.endswith(('.jpg', '.jpeg', '.png'))])
    return render_template('index.html', image_count=image_count)


@app.route('/list-deteksi')
def deteksi():
    images = get_image_list()
    # Menambahkan nomor urutan (start=1)
    enumerated_images = list(enumerate(images, start=0))
    return render_template('list-deteksi.html', images=enumerated_images)


@app.route('/zoom_image/<image_name>')
def zoom_image(image_name):
    image_path = os.path.join('captured', image_name).replace(os.path.sep, '/')
    return render_template('zoom_image.html', image_name=image_name, image_path=image_path)


@app.route('/delete_image', methods=['POST'])
def delete_image():
    image_to_delete = request.form['image_to_delete']

    # Implementasi logika delete gambar di sini
    image_path = os.path.join('assets/captured', image_to_delete)
    if os.path.exists(image_path):
        os.remove(image_path)
        print(f"Gambar {image_to_delete} berhasil dihapus.")
    else:
        print(f"Gambar {image_to_delete} tidak ditemukan.")

    return redirect(url_for('deteksi'))


@app.route('/start_camera', methods=['POST'])
def start_camera():
    global cap
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
        cap.set(4, 240)
    return redirect(url_for('index'))


@app.route('/stop_camera', methods=['POST'])
def stop_camera():
    global cap
    if cap.isOpened():
        cap.release()
    return redirect(url_for('index'))


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
