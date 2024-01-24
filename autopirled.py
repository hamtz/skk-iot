import wiringpi
import time
from wiringpi import GPIO

# Inisialisasi WiringPi
wiringpi.wiringPiSetup()

# Tentukan pin sensor PIR
pir_pin = 2
led_pin = 6

# Setel pin sebagai input
wiringpi.pinMode(pir_pin, GPIO.INPUT)
wiringpi.pinMode(led_pin, GPIO.OUTPUT)


try:
    while True:
        # Baca nilai dari sensor PIR
        pir_value = wiringpi.digitalRead(pir_pin)
        

        # Tampilkan nilai sensor PIR
        print("Nilai PIR:", pir_value)
        if( pir_value == 1):
             wiringpi.digitalWrite(led_pin,GPIO.HIGH)

        else:
            wiringpi.digitalWrite(led_pin,GPIO.LOW)


        # Tunggu sebentar sebelum membaca kembali
        time.sleep(2)

except KeyboardInterrupt:
    # Tangkap penekanan tombol Ctrl+C untuk keluar dari program dengan aman
    print("Program dihentikan oleh pengguna.")

