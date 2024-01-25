import cv2
import wiringpi
import time
from wiringpi import GPIO
import os  # Tambahkan ini untuk mengimpor modul os
from pyfcm import FCMNotification


# Inisialisasi WiringPi
wiringpi.wiringPiSetup()

# Tentukan pin sensor PIR
pir_pin = 2
led_pin = 6

# Setel pin sebagai input
wiringpi.pinMode(pir_pin, GPIO.INPUT)
wiringpi.pinMode(led_pin, GPIO.OUTPUT)


# Ganti dengan kunci server Firebase Anda
push_service = FCMNotification(api_key="AIzaSyBKoixbI0LyS93C1mQ2ZA_Slz3BEXN9Xqw")

# Token perangkat Android
registration_id = "fcp4YhjjSEmJQjh2nuVwNS:APA91bEOZoquLFRGEfPhs0IWT3YU4xlONepWo-q4EQlvpLlwEQw82t4TmgUj-Upz1gBzDegkb8RKm_7ml9sJV5xsyma3QbXbZyc8nIz3hDbKIk1J32T5et0EBAPFsmRGh19lJkZS6p66"


# @app.route('/pushnotif')
def pushnotif():
    # Kirim pesan
    message_title = "Peringatan!"
    message_body = "Gerakan Terdeteksi"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
    print(result)

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
            pushnotif()

        else:
            wiringpi.digitalWrite(led_pin, GPIO.LOW)

        # Tunggu sebentar sebelum membaca kembali
        time.sleep(2)

except KeyboardInterrupt:
    # Tangkap penekanan tombol Ctrl+C untuk keluar dari program dengan aman
    print("Program dihentikan oleh pengguna.")
