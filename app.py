import cv2
import wiringpi
import time
from wiringpi import GPIO
import os  # Tambahkan ini untuk mengimpor modul os
from pyfcm import FCMNotification
import firebase_admin
from firebase_admin import credentials, messaging

import FCMManager as fcm


firebaseConfig = {
  apiKey: "AIzaSyAQSVQguhdTQ-N7gQKE2juIG1jpBmQOQts",
  authDomain: "siskam-df66d.firebaseapp.com",
  databaseURL: "https://siskam-df66d-default-rtdb.firebaseio.com",
  projectId: "siskam-df66d",
  storageBucket: "siskam-df66d.appspot.com",
  messagingSenderId: "473723424795",
  appId: "1:473723424795:web:f026c68141cc6fdf3de8be",
  measurementId: "G-E25RBCKH3J"
};

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
db = firebase.database()

# tokens = ["eGvKDO6wRieOXj_TlOF7ub:APA91bHmyDIcaC_UPXV21rjEFSzoq19OY3aB473ebDh8ORxb6gy5dCFCSCh8qqf8YqzhWxSFA2fsv2t2lIlBoLY2ckVQ-ey0CYDhGc9vkssy7NuRHkeEfdxnTSsT4sS6LSv8_NEcmzPY"]

# Mendapatkan referensi ke database tokens
tokens_ref = firebase_admin.db.reference("tokens")

# Mendapatkan semua token dari database
tokens_snapshot = tokens_ref.get()
tokens_list = [token for token in tokens_snapshot.values()] if tokens_snapshot else []

# Inisialisasi WiringPi
wiringpi.wiringPiSetup()

# Tentukan pin sensor PIR
pir_pin = 2
led_pin = 6

# Setel pin sebagai input
wiringpi.pinMode(pir_pin, GPIO.INPUT)
wiringpi.pinMode(led_pin, GPIO.OUTPUT)


# # Ganti dengan kunci server Firebase Anda
# push_service = FCMNotification(api_key="AIzaSyBKoixbI0LyS93C1mQ2ZA_Slz3BEXN9Xqw")
#
# # Token perangkat Android
# registration_id = "eGvKDO6wRieOXj_TlOF7ub:APA91bHmyDIcaC_UPXV21rjEFSzoq19OY3aB473ebDh8ORxb6gy5dCFCSCh8qqf8YqzhWxSFA2fsv2t2lIlBoLY2ckVQ-ey0CYDhGc9vkssy7NuRHkeEfdxnTSsT4sS6LSv8_NEcmzPY"


# @app.route('/pushnotif')
# def pushnotif():
#     # Kirim pesan
#     message_title = "Peringatan!"
#     message_body = "Gerakan Terdeteksi"
#     result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
#     print(result)



def capture_image():
    # Inisialisasi objek VideoCapture dengan indeks kamera. Biasanya, kamera internal memiliki indeks 0.
    cap = cv2.VideoCapture(0)

    # Periksa apakah kamera terbuka dengan benar
    if not cap.isOpened():
        print("Kamera tidak dapat diakses.")
        return

    # Baca frame dari kamera
    ret, frame = cap.read()

    # Periksa apakah operasi pembacaan berjalan dengan benar
    if not ret:
        print("Gagal membaca frame.")
        cap.release()
        return

    # Dapatkan timestamp saat ini sebagai string
    timestamp = time.strftime("%Y%m%d%H%M%S")

    # Tentukan jalur folder untuk menyimpan gambar
    folder_path = "captured"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Buat nama file dengan timestamp di dalam folder "captured"
    file_name = os.path.join(folder_path, f"image_{timestamp}.jpg")

    # Simpan frame sebagai gambar dengan nama file timestamp
    cv2.imwrite(file_name, frame)

    # Tutup kamera
    cap.release()

    # Tampilkan informasi penyimpanan gambar
    print(f"Gambar berhasil disimpan: {file_name}")


try:
    while True:
        # Baca nilai dari sensor PIR
        pir_value = wiringpi.digitalRead(pir_pin)

        # Tampilkan nilai sensor PIR
        print("Nilai PIR:", pir_value)
        if (pir_value == 1):
            wiringpi.digitalWrite(led_pin, GPIO.HIGH)
            capture_image()
            fcm.pushNotif(tokens_list)

        else:
            wiringpi.digitalWrite(led_pin, GPIO.LOW)

        # Tunggu sebentar sebelum membaca kembali
        time.sleep(2)

except KeyboardInterrupt:
    # Tangkap penekanan tombol Ctrl+C untuk keluar dari program dengan aman
    print("Program dihentikan oleh pengguna.")
