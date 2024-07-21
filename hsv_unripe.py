import cv2
import numpy as np
import json
import os


# Fungsi callback trackbar (tidak melakukan apa-apa)
def nothing(x):
    pass


# Nama file untuk menyimpan data JSON
output_file = 'hsv_data.json'


# Fungsi untuk membaca data JSON dari file
def read_json(file):
    if os.path.exists(file):
        with open(file, 'r') as json_file:
            return json.load(json_file)
    else:
        return {}


# Baca data JSON dari file
data = read_json(output_file)

# Jika tidak ada data matang, inisialisasi dengan data kosong
if 'matang' not in data:
    data['matang'] = {"LH": 0, "LS": 0, "LV": 0, "UH": 0, "US": 0, "UV": 0}

# Jika tidak ada data setengah_matang, inisialisasi dengan data kosong
if 'setengah_matang' not in data:
    data['setengah_matang'] = {"LH": 0, "LS": 0, "LV": 0, "UH": 0, "US": 0, "UV": 0}

# Jika tidak ada data belum_matang, inisialisasi dengan data kosong
if 'belum_matang' not in data:
    data['belum_matang'] = {"LH": 0, "LS": 0, "LV": 0, "UH": 0, "US": 0, "UV": 0}

# Baca gambar (UBAH SESUAI KEBUTUHAN)
image = cv2.imread('assets/images/hijau.jpg')

# Konversi gambar dari BGR ke HSV
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

    # Hitung rata-rata nilai HSV dari area terdeteksi
    mean_hsv = cv2.mean(hsv_image, mask=mask)

    # Perbarui data dengan nilai rata-rata HSV
    data['belum_matang']["LH"] = lh
    data['belum_matang']["LS"] = ls
    data['belum_matang']["LV"] = lv
    data['belum_matang']["UH"] = uh
    data['belum_matang']["US"] = us
    data['belum_matang']["UV"] = uv

    # Tampilkan gambar asli dan hasil
    # cv2.imshow('Original Image', image)
    cv2.imshow('Masked Image', result)

    # Cetak data JSON di terminal
    print(json.dumps(data, indent=4))

    # Tunggu sampai tombol 'ESC' ditekan, kemudian tutup jendela
    key = cv2.waitKey(1)
    if key == 27:  # ESC key
        break

# Simpan data JSON ke file
with open(output_file, 'w') as json_file:
    json.dump(data, json_file, indent=4)

print(f"Data HSV diperbarui dan disimpan ke file: {output_file}")

cv2.destroyAllWindows()
