import cv2

# Inisialisasi objek kamera USB
cap = cv2.VideoCapture(0)  # Nomor 0 menunjukkan kamera pertama yang terdeteksi

# Periksa apakah kamera terbuka dengan benar
if not cap.isOpened():
    print("Kamera tidak dapat diakses")
else:
    while True:
        # Baca frame dari kamera
        ret, frame = cap.read()

        # Jika berhasil membaca frame
        if ret:
            # Tampilkan frame
            cv2.imshow("Kamera USB", frame)

            # Tekan tombol 'q' untuk keluar dari aplikasi
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Tidak dapat membaca frame dari kamera")
            break

# Setelah selesai, lepaskan kamera dan tutup jendela tampilan
cap.release()
cv2.destroyAllWindows()


