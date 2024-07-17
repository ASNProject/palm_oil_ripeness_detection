import tkinter as tk
import cv2
from PIL import Image, ImageTk
from tkinter import Scale
import numpy as np
from utils.telegram_bot import send_message
from utils.classify_maturity import classify_maturity


class CameraApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Palm Oil Detection")
        self.window.geometry("860x420")

        # Membuka kamera menggunakan OpenCV
        self.cap = cv2.VideoCapture(0)

        # Membuat label untuk menampilkan gambar dari kamera
        self.label = tk.Label(window)
        self.label.place(x=20, y=20)

        # Label untuk menampilkan gambar yang di capture
        self.captured_label = tk.Label(window)
        self.captured_label.place(x=435, y=20)

        # Button untuk mengambil gambar dari kamera
        self.capture_btn = tk.Button(window, text="Capture", command=self.capture_image)
        self.capture_btn.place(x=435, y=260)

        # Hue trackbar
        self.hue_scale = Scale(window, from_=0, to=179, orient=tk.HORIZONTAL, command=self.update_hue_label)
        self.hue_scale.place(x=20, y=280)
        self.label_hue = tk.Label(window, text="LH: 0")
        self.label_hue.place(x=20, y=260)

        # Saturation trackbar
        self.saturation_scale = Scale(window, from_=0, to=255, orient=tk.HORIZONTAL,
                                      command=self.update_saturation_label)
        self.saturation_scale.place(x=145, y=280)
        self.label_saturation = tk.Label(window, text="LS: 0")
        self.label_saturation.place(x=145, y=260)

        # Value trackbar
        self.value_scale = Scale(window, from_=0, to=255, orient=tk.HORIZONTAL, command=self.update_value_label)
        self.value_scale.place(x=270, y=280)
        self.label_value = tk.Label(window, text="LV: 0")
        self.label_value.place(x=270, y=260)

        # Upper Hue trackbar
        self.upper_hue_var = tk.IntVar(value=179)
        self.upper_hue_scale = Scale(window, from_=0, to=179, orient=tk.HORIZONTAL, variable=self.upper_hue_var,
                                     command=self.upper_update_hue_label)
        self.upper_hue_scale.place(x=20, y=350)
        self.upper_label_hue = tk.Label(window, text="UH: 0")
        self.upper_label_hue.place(x=20, y=330)

        # Upper Saturation trackbar
        self.upper_saturation_var = tk.IntVar(value=255)
        self.upper_saturation_scale = Scale(window, from_=0, to=255, orient=tk.HORIZONTAL,
                                            variable=self.upper_saturation_var,
                                            command=self.upper_update_saturation_label)
        self.upper_saturation_scale.place(x=145, y=350)
        self.upper_label_saturation = tk.Label(window, text="US: 0")
        self.upper_label_saturation.place(x=145, y=330)

        # Upper Value trackbar
        self.upper_value_var = tk.IntVar(value=255)
        self.upper_value_scale = Scale(window, from_=0, to=255, orient=tk.HORIZONTAL, variable=self.upper_value_var,
                                       command=self.upper_update_value_label)
        self.upper_value_scale.place(x=270, y=350)
        self.upper_label_value = tk.Label(window, text="UV: 0")
        self.upper_label_value.place(x=270, y=330)

        # Hasil Klasifikasi
        self.classify_maturity = tk.Label(window, text="Hasil Klasifikasi: ", font=("Helvetica", 20))
        self.classify_maturity.place(x=450, y=350)

        # Mulai proses pembacaan gambar dari kamera
        self.show_frame()

    def show_frame(self):
        _, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Konversi dari BGR ke RGB

        # Resize frame agar sesuai dengan ukuran label
        height, width, channels = frame.shape
        ratio = height / width
        new_width = 400
        new_height = int(new_width * ratio)
        frame = cv2.resize(frame, (new_width, new_height))

        # Ambil nilai dari slider HSV
        lower_hue = self.hue_scale.get()
        lower_saturation = self.saturation_scale.get()
        lower_value = self.value_scale.get()
        upper_hue = self.upper_hue_scale.get()
        upper_saturation = self.upper_saturation_scale.get()
        upper_value = self.upper_value_scale.get()

        # Konversi frame ke HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        # Buat lower dan upper nilai HSV
        lower_color = np.array([lower_hue, lower_saturation, lower_value])
        upper_color = np.array([upper_hue, upper_saturation, upper_value])

        # Buat mask menggunakan inRange
        mask = cv2.inRange(hsv_frame, lower_color, upper_color)

        # Gabungkan frame asli dengan mask
        result_frame = cv2.bitwise_and(frame, frame, mask=mask)

        # Tampilkan frame hasil di label menggunakan PIL
        img = Image.fromarray(result_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)

        # Simpan frame yang sudah di-adjust saat tombol "Capture" ditekan
        self.result_frame = result_frame

        # Perbarui frame setiap 10 milidetik (100 fps)
        self.label.after(10, self.show_frame)

    def capture_image(self):
        # Simpan gambar yang sudah di-adjust
        if hasattr(self, 'result_frame'):
            captured_img = Image.fromarray(self.result_frame)
            captured_img.save("captured_image.png")  # Simpan gambar dengan nama captured_image.png
            captured_imgtk = ImageTk.PhotoImage(image=captured_img)
            self.captured_label.imgtk = captured_imgtk
            self.captured_label.configure(image=captured_imgtk)

            result_classification = classify_maturity(self.hue_scale.get(), self.saturation_scale.get(),
                                                      self.value_scale.get())

            if result_classification == "belum_matang":
                result = "Belum Matang"
            elif result_classification == "setengah_matang":
                result = "Setengah Matang"
            elif result_classification == "matang":
                result = "Matang"
            else:
                result = "Tidak Terdeteksi"

            self.classify_maturity.config(text=f"Hasil Klasifikasi: {result}")

            # Program Kirim telegram
            send_message(result)

    def update_hue_label(self, value):
        self.label_hue.config(text=f"LH: {value}")
        return value

    def update_saturation_label(self, value):
        self.label_saturation.config(text=f"LS: {value}")
        return value

    def update_value_label(self, value):
        self.label_value.config(text=f"LV: {value}")
        return value

    def upper_update_hue_label(self, value):
        self.upper_label_hue.config(text=f"UH: {value}")
        return value

    def upper_update_saturation_label(self, value):
        self.upper_label_saturation.config(text=f"US: {value}")
        return value

    def upper_update_value_label(self, value):
        self.upper_label_value.config(text=f"UV: {value}")
        return value


if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()

# Jangan lupa untuk melepaskan kamera setelah selesai
cv2.destroyAllWindows()
