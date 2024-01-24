import cv2
import os
import time
import wiringpi
from wiringpi import GPIO

# Inisialisasi WiringPi
wiringpi.wiringPiSetup()

# Tentukan pin sensor PIR dan LED
pir_pin = 2
led_pin = 6

# Setel pin sebagai input dan output
wiringpi.pinMode(pir_pin, GPIO.INPUT)
wiringpi.pinMode(led_pin, GPIO.OUTPUT)

# Fungsi untuk mengambil dan menyimpan gambar
def capture_and_save_image(output_folder):
    # Buka koneksi ke webcam (USB)
    cap = cv2.VideoCapture(0)

    # Pastikan koneksi berhasil dibuka
    if not cap.isOpened():
        print("Error: Gagal membuka koneksi ke webcam.")
        return

    # Loop untuk mengambil gambar setiap 5 detik
    while True:
        # Baca nilai dari sensor PIR
        pir_value = wiringpi.digitalRead(pir_pin)

        # Tampilkan nilai sensor PIR
        print("Nilai PIR:", pir_value)

        if pir_value == 1:
            # Hidupkan LED
            wiringpi.digitalWrite(led_pin, GPIO.HIGH)

            # Baca frame dari webcam
            ret, frame = cap.read()

            # Periksa apakah pembacaan frame berhasil
            if not ret:
                print("Error: Gagal membaca frame.")
                break

            # Tentukan nama file dengan timestamp
            timestamp = time.strftime("%Y%m%d%H%M%S")
            file_name = f"{timestamp}.jpg"
            file_path = os.path.join(output_folder, file_name)

            # Simpan frame sebagai gambar
            cv2.imwrite(file_path, frame)

            print(f"Gambar disimpan: {file_path}")

            # Matikan LED setelah gambar disimpan
            wiringpi.digitalWrite(led_pin, GPIO.LOW)
          

        # Tunggu 2 detik sebelum membaca kembali
        time.sleep(2)

    # Tutup koneksi ke webcam
    cap.release()

# Folder tempat menyimpan gambar
output_folder = "captured"

# Pastikan folder output ada atau buat folder jika belum ada
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Panggil fungsi untuk mengambil dan menyimpan gambar
capture_and_save_image(output_folder)

