# Aturan untuk klasifikasi kematangan berdasarkan nilai Hue
def classify_maturity(hue_value):
    if hue_value < 30:
        return 'Matang'
    elif 30 <= hue_value < 60:
        return 'Setengah Matang'
    else:
        return 'Mentah'
