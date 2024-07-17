import json

import cv2
import numpy as np
from utils.classify_maturity import classify_maturity
from utils.telegram_bot import send_message
import asyncio


async def main():
    def nothing(x):
        pass

    # Load gambar
    image = cv2.imread('../assets/images/belum_matang.jpg')

    # Konversi ke HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Buat jendela untuk trackbar
    cv2.namedWindow('Trackbars')

    # Buat trackbar untuk mengatur nilai HSV
    cv2.createTrackbar('LH', 'Trackbars', 0, 179, nothing)  # Lower Hue
    cv2.createTrackbar('LS', 'Trackbars', 0, 255, nothing)  # Lower Saturation
    cv2.createTrackbar('LV', 'Trackbars', 0, 255, nothing)  # Lower Value
    cv2.createTrackbar('UH', 'Trackbars', 179, 179, nothing)  # Upper Hue
    cv2.createTrackbar('US', 'Trackbars', 255, 255, nothing)  # Upper Saturation
    cv2.createTrackbar('UV', 'Trackbars', 255, 255, nothing)  # Upper Value

    while True:
        # Baca nilai trackbar
        lh = cv2.getTrackbarPos('LH', 'Trackbars')
        ls = cv2.getTrackbarPos('LS', 'Trackbars')
        lv = cv2.getTrackbarPos('LV', 'Trackbars')
        uh = cv2.getTrackbarPos('UH', 'Trackbars')
        us = cv2.getTrackbarPos('US', 'Trackbars')
        uv = cv2.getTrackbarPos('UV', 'Trackbars')
        # Definisikan rentang warna berdasarkan nilai trackbar
        lower_color = np.array([lh, ls, lv])
        upper_color = np.array([uh, us, uv])

        # Buat masker berdasarkan rentang warna
        mask = cv2.inRange(hsv_image, lower_color, upper_color)

        # Terapkan masker ke gambar asli
        result = cv2.bitwise_and(image, image, mask=mask)

        # Tampilkan hasil
        cv2.imshow('Result', result)

        # Tunggu input dari pengguna
        print("Tekan s untuk klasifikasi")
        key = cv2.waitKey(1)
        if key == ord('s'):
            palm_oil_value = classify_maturity(lh, ls, lv)
            await send_message(f'Tingkat kematangan: {palm_oil_value}')

        elif key == ord('q'):
            break

    # Menutup program
    cv2.destroyAllWindows()


if __name__ == '__main__':
    asyncio.run(main())
