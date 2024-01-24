import cv2
import os
import time

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

        # Tunggu 5 detik sebelum mengambil gambar berikutnya
        time.sleep(5)

    # Tutup koneksi ke webcam
    cap.release()

# Folder tempat menyimpan gambar
output_folder = "assets/captured"

# Pastikan folder output ada atau buat folder jika belum ada
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Panggil fungsi untuk mengambil dan menyimpan gambar
capture_and_save_image(output_folder)

