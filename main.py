import cv2
import numpy as np
from utils.classify_maturity import classify_maturity
from utils.telegram_bot import send_message
import asyncio


async def main():
    while True:
        # Read image
        image = cv2.imread('assets/images/kelapa_sawit.jpg')

        # Mengonversi gambar dari RGB (default OpenCV) ke HSV
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Menampilkan gambar HSV
        cv2.imshow('HSV Image', hsv_image)

        # Ekstraksi nilai H, S, dan V
        hue, saturation, value = cv2.split(hsv_image)

        # Menampilkan histogram dari nilai hue (Jika ingin menampilkan histogram hilangkan comment program dibawah)
        # hist = cv2.calcHist([hue], [0], None, [256], [0, 256])
        # plt.plot(hist)
        # plt.title('Hostogram of Hue')
        # plt.xlabel('Hue Value')
        # plt.ylabel('Frequency')
        # plt.show()

        # Ambil nilai rata-rata dari Hue untuk klasifikasi
        average_hue = np.mean(hue)
        maturity = classify_maturity(average_hue)
        print(f'Tingkat kematangan: {maturity}')

        # Kirim pesan ke telegram
        await send_message(f'Tingkat kematangan: {maturity}')

        # Tunggu input dari pengguna
        print("Tekan tombol apa saja untuk mengulagi atau 'q' untuk keluar dari program")
        key = cv2.waitKey(0)
        if key == ord('q'):
            break

    # Menutup program
    cv2.destroyAllWindows()


if __name__ == '__main__':
    asyncio.run(main())
