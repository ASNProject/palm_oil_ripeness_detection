import json


# Fungsi callback trackbar (tidak melakukan apa-apa)
def nothing(x):
    pass


# Fungsi untuk memuat data rentang HSV dari file JSON
def load_hsv_ranges_from_json(file_path):
    with open(file_path, 'r') as f:
        hsv_ranges = json.load(f)
    return hsv_ranges


# Memuat rentang HSV dari file JSON
file_path = 'hsv_data.json'
hsv_ranges = load_hsv_ranges_from_json(file_path)


def classify_color_with_json_data(hsv, hsv_ranges):
    # Fungsi untuk memeriksa apakah HSV berada dalam rentang tertentu
    def check_in_range(hsv, hsv_range):
        if hsv_range["LH"] <= hsv[0] <= hsv_range["UH"] and \
                hsv_range["LS"] <= hsv[1] <= hsv_range["US"] and \
                hsv_range["LV"] <= hsv[2] <= hsv_range["UV"]:
            return True
        return False

    # Periksa data baru terhadap masing-masing rentang yang dimuat dari JSON
    for category, range_data in hsv_ranges.items():
        if check_in_range(hsv, range_data):
            return category

    return "tidak diketahui"  # Jika data tidak cocok dengan semua kategori


def classify_maturity(h, s, v):
    data_baru = (h, s, v)
    print(f'Data Baru {data_baru}')

    hasil_klasifikasi = classify_color_with_json_data(data_baru, hsv_ranges)

    return hasil_klasifikasi
