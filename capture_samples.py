import os
import cv2
import numpy as np
from mediapipe.python.solutions.holistic import Holistic
from helpers import create_folder, draw_keypoints, mediapipe_detection, save_frames, there_hand
from constants import FONT, FONT_POS, FONT_SIZE, FRAME_ACTIONS_PATH, ROOT_PATH
import tkinter as tk
from tkinter import ttk
import threading

class CaptureSamplesApp:
    def __init__(self, root):
        self.root = root
        self.create_ui()

    def create_ui(self):
        self.root.title("Capture Samples")
        
        self.label_instruction = tk.Label(self.root, text="Ingrese el nombre de la palabra u oración:")
        self.label_instruction.pack(pady=(10, 5))

        self.word_name_entry = tk.Entry(self.root)
        self.word_name_entry.pack(pady=5)

        self.capture_button = tk.Button(self.root, text="Comenzar Captura", command=self.start_capture)
        self.capture_button.pack(pady=5)

        self.quit_button = tk.Button(self.root, text="Salir", command=self.quit)
        self.quit_button.pack(pady=5)

        self.label_status = tk.Label(self.root, text="", fg="green")
        self.label_status.pack(pady=(5, 10))

    def start_capture(self):
        word_name = self.word_name_entry.get()
        if word_name:
            self.label_status.config(text="Capturando muestras...", fg="blue")
            threading.Thread(target=self.capture_samples_thread, args=(word_name,), daemon=True).start()
        else:
            self.label_status.config(text="¡Por favor ingrese un nombre de palabra!", fg="red")

    def quit(self):
        self.root.destroy()

    def capture_samples_thread(self, word_name):
        word_path = os.path.join(ROOT_PATH, FRAME_ACTIONS_PATH, word_name)
        capture_samples(word_path)
        self.label_status.config(text="¡Muestras capturadas con éxito!", fg="green")

def capture_samples(path, margin_frame=2, min_cant_frames=5):
    create_folder(path)
    
    cant_sample_exist = len(os.listdir(path))
    count_sample = 0
    count_frame = 0
    frames = []
    
    with Holistic() as holistic_model:
        video = cv2.VideoCapture(0)
        
        while video.isOpened():
            _, frame = video.read()
            image, results = mediapipe_detection(frame, holistic_model)
            
            if there_hand(results):
                count_frame += 1
                if count_frame > margin_frame: 
                    cv2.putText(image, 'Capturando...', FONT_POS, FONT, FONT_SIZE, (255, 50, 0))
                    frames.append(np.asarray(frame))
                
            else:
                if len(frames) > min_cant_frames + margin_frame:
                    frames = frames[:-margin_frame]
                    output_folder = os.path.join(path, f"sample_{cant_sample_exist + count_sample + 1}")
                    create_folder(output_folder)
                    save_frames(frames, output_folder)
                    count_sample += 1
                
                frames = []
                count_frame = 0
                cv2.putText(image, 'Listo para capturar...', FONT_POS, FONT, FONT_SIZE, (0,220, 100))
                
            draw_keypoints(image, results)
            cv2.imshow(f'Toma de muestras para "{os.path.basename(path)}"', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        video.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = CaptureSamplesApp(root)
    root.mainloop()
