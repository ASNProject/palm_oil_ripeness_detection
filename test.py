import json
import time

import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from utils.telegram_bot import send_message


class CameraApp:
    def __init__(self, window):
        self.hsv_ranges = None
        self.window = window
        self.window.title("Color Detection")
        self.window.geometry("1280x480")  # Menyesuaikan ukuran window untuk dua kamera

        # Membuka dua kamera
        self.cap1 = cv2.VideoCapture(0)
        self.cap2 = cv2.VideoCapture(0)  # Ganti dengan indeks kamera kedua jika perlu

        # Label untuk menampilkan video dari kedua kamera
        self.label1 = tk.Label(window)
        self.label1.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.label2 = tk.Label(window)
        self.label2.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Ukuran maksimum untuk gambar
        self.max_width = 640
        self.max_height = 480

        # Status deteksi
        self.detected_status = {
            'Sawit Matang': {'detected': False, 'last_sent': 0},
            'Sawit Belum Matang': {'detected': False, 'last_sent': 0},
            'Sawit Setengah Matang': {'detected': False, 'last_sent': 0}
        }
        self.send_interval = 10  # Interval dalam detik untuk mengirim pesan ulang

        # Mulai proses pembacaan gambar dari kamera
        self.show_frame()

    def show_frame(self):
        # Baca frame dari kedua kamera
        ret1, frame1 = self.cap1.read()
        ret2, frame2 = self.cap2.read()

        if ret1:
            # Proses dan tampilkan frame dari kamera 1
            frame1 = self.process_frame(frame1)
            img1 = self.convert_to_tk_image(frame1)
            self.label1.imgtk = img1
            self.label1.configure(image=img1)

        if ret2:
            # Proses dan tampilkan frame dari kamera 2
            frame2 = self.hsv_process(frame2)
            img2 = self.convert_to_tk_image(frame2)
            self.label2.imgtk = img2
            self.label2.configure(image=img2)

        # Panggil fungsi ini lagi setelah 10 milidetik
        self.label1.after(10, self.show_frame)

    def process_frame(self, frame):
        # Memuat rentang HSV dari file JSON
        file_path = 'hsv_data.json'
        hsv_ranges = self.load_hsv_ranges_from_json(file_path)

        # Definisi rentang warna dalam ruang HSV
        lower_ripe = np.array([hsv_ranges["matang"]["LH"], hsv_ranges["matang"]["LS"], hsv_ranges["matang"]["LV"]])
        upper_ripe = np.array([hsv_ranges["matang"]["UH"], hsv_ranges["matang"]["US"], hsv_ranges["matang"]["UV"]])
        lower_unripe = np.array(
            [hsv_ranges["belum_matang"]["LH"], hsv_ranges["belum_matang"]["LS"], hsv_ranges["belum_matang"]["LV"]])
        upper_unripe = np.array(
            [hsv_ranges["belum_matang"]["UH"], hsv_ranges["belum_matang"]["US"], hsv_ranges["belum_matang"]["UV"]])
        lower_half_ripe = np.array([hsv_ranges["setengah_matang"]["LH"], hsv_ranges["setengah_matang"]["LS"],
                                    hsv_ranges["setengah_matang"]["LV"]])
        upper_half_ripe = np.array([hsv_ranges["setengah_matang"]["UH"], hsv_ranges["setengah_matang"]["US"],
                                    hsv_ranges["setengah_matang"]["UV"]])

        # Deteksi warna
        ripe_mask = self.detect_color(frame, lower_ripe, upper_ripe)
        unripe_mask = self.detect_color(frame, lower_unripe, upper_unripe)
        half_ripe_mask = self.detect_color(frame, lower_half_ripe, upper_half_ripe)

        # Temukan kontur terbesar untuk setiap warna
        largest_ripe_contour = self.find_largest_contour(ripe_mask)
        largest_unripe_contour = self.find_largest_contour(unripe_mask)
        largest_half_ripe_contour = self.find_largest_contour(half_ripe_mask)

        # Tentukan kontur terbesar di antara semua warna
        largest_contour = None
        color_name = ''
        color_box = (0, 0, 0)

        if largest_ripe_contour is not None and (
                largest_contour is None or cv2.contourArea(largest_ripe_contour) > cv2.contourArea(largest_contour)):
            largest_contour = largest_ripe_contour
            color_name = 'Sawit Matang'
            color_box = (0, 0, 255)

        if largest_unripe_contour is not None and (
                largest_contour is None or cv2.contourArea(largest_unripe_contour) > cv2.contourArea(largest_contour)):
            largest_contour = largest_unripe_contour
            color_name = 'Sawit Belum Matang'
            color_box = (0, 255, 0)

        if largest_half_ripe_contour is not None and (
                largest_contour is None or cv2.contourArea(largest_half_ripe_contour) > cv2.contourArea(
            largest_contour)):
            largest_contour = largest_half_ripe_contour
            color_name = 'Sawit Setengah Matang'
            color_box = (255, 0, 0)

        # Gambar kotak di sekitar kontur terbesar yang ditemukan
        if largest_contour is not None:
            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color_box, 2)
            cv2.putText(frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color_box, 2)

            # Kirim pesan hanya jika belum pernah mengirim pesan untuk warna ini atau jika interval sudah berlalu
            current_time = time.time()
            if (not self.detected_status[color_name]['detected'] or
                    (current_time - self.detected_status[color_name]['last_sent']) > self.send_interval):
                send_message(color_name)
                self.detected_status[color_name]['detected'] = True
                self.detected_status[color_name]['last_sent'] = current_time

        else:
            # Reset status deteksi jika tidak ada kontur yang terdeteksi
            for key in self.detected_status:
                self.detected_status[key]['detected'] = False

        return frame

    def hsv_process(self, frame):

        # Memuat rentang HSV dari file JSON
        file_path = 'hsv_data.json'
        hsv_ranges = self.load_hsv_ranges_from_json(file_path)

        # Definisi rentang warna dalam ruang HSV
        lower_ripe = np.array([hsv_ranges["matang"]["LH"], hsv_ranges["matang"]["LS"], hsv_ranges["matang"]["LV"]])
        upper_ripe = np.array([hsv_ranges["matang"]["UH"], hsv_ranges["matang"]["US"], hsv_ranges["matang"]["UV"]])
        lower_unripe = np.array(
            [hsv_ranges["belum_matang"]["LH"], hsv_ranges["belum_matang"]["LS"], hsv_ranges["belum_matang"]["LV"]])
        upper_unripe = np.array(
            [hsv_ranges["belum_matang"]["UH"], hsv_ranges["belum_matang"]["US"], hsv_ranges["belum_matang"]["UV"]])
        lower_half_ripe = np.array([hsv_ranges["setengah_matang"]["LH"], hsv_ranges["setengah_matang"]["LS"],
                                    hsv_ranges["setengah_matang"]["LV"]])
        upper_half_ripe = np.array([hsv_ranges["setengah_matang"]["UH"], hsv_ranges["setengah_matang"]["US"],
                                    hsv_ranges["setengah_matang"]["UV"]])

        # Deteksi warna
        ripe_mask = self.detect_color(frame, lower_ripe, upper_ripe)
        unripe_mask = self.detect_color(frame, lower_unripe, upper_unripe)
        half_ripe_mask = self.detect_color(frame, lower_half_ripe, upper_half_ripe)

        # Menampilkan hasil deteksi
        ripe_result = cv2.bitwise_and(frame, frame, mask=ripe_mask)
        unripe_result = cv2.bitwise_and(frame, frame, mask=unripe_mask)
        half_ripe_result = cv2.bitwise_and(frame, frame, mask=half_ripe_mask)

        # Gabungkan hasil deteksi
        combined_result = cv2.addWeighted(ripe_result, 1.0, unripe_result, 1.0, 0)
        combined_result = cv2.addWeighted(combined_result, 1.0, half_ripe_result, 1.0, 0)

        return combined_result

    def convert_to_tk_image(self, frame):
        # Convert frame to ImageTk format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img.thumbnail((self.max_width, self.max_height), Image.LANCZOS)
        return ImageTk.PhotoImage(image=img)

    def detect_color(self, frame, lower_bound, upper_bound):
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
        return mask

    def find_largest_contour(self, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest_contour) > 500:  # Filter out small contours
                return largest_contour
        return None

    def load_hsv_ranges_from_json(self, file_path):
        with open(file_path, 'r') as file:
            hsv_ranges = json.load(file)
        return hsv_ranges


if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
