# session/camera_session.py
# -------------------------------
# Requierements
# -------------------------------
import ctypes
import threading
import cv2
from typing import Optional
import time

from trackerfit.tracker.pose_tracker import PoseTracker
from trackerfit.factory import get_ejercicio
from trackerfit.session.base import BaseSession

# -------------------------------
# Helpers
# -------------------------------

def get_screen_height():
    return ctypes.windll.user32.GetSystemMetrics(1)  # Altura de pantalla

class CameraSession(BaseSession):
    def __init__(self):
        self.pose_tracker = PoseTracker()
        self.contador = None
        self.repeticiones = 0
        self.running = False
        self.thread = None
        self.cap = None
        self.historial_frames = []

    def start(self, nombre_ejercicio: str, lado: str = "derecho"):
        if self.running:
            return
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Camara no se pudo abrir")
            raise RuntimeError("No se pudo abrir la cámara")

        self.contador = get_ejercicio(nombre_ejercicio,lado)

        self.repeticiones = 0
        self.running = True
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def loop(self):
        """
        Bucle principal que procesa el vídeo y actualiza el estado del ejercicio Frame a Frame
        """
        pantalla_alto = ctypes.windll.user32.GetSystemMetrics(1)
        nuevo_alto = pantalla_alto - 120

        # Crear ventana antes del bucle
        cv2.namedWindow("Camara - Seguimiento de Ejercicio", cv2.WINDOW_NORMAL)
        cv2.moveWindow("Camara - Seguimiento de Ejercicio", 100, 100)

        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            results = self.pose_tracker.procesar(frame)
            puntos = self.pose_tracker.extraer_landmarks(results, frame.shape)

            if puntos and self.contador:
                angulo, reps = self.contador.actualizar(puntos)
                
                #Dibujo del triángulo representativo del ángulo
                umbral = self.contador.umbral_validacion
                self.pose_tracker.dibujar_triangulo_con_angulo(
                    frame, puntos,
                    self.contador.id1,
                    self.contador.id2,
                    self.contador.id3,
                    angulo,
                    umbral
                )
                
                self.repeticiones = reps
                timestamp = time.time()
                estado = "activo" if self.contador.arriba or self.contador.abajo else "reposo"
                # Guardar detalles del frame actual para el resumen final
                # Incluye timestamp, valor del ángulo, estado del movimiento, repeticiones y coordenadas de landmarks
                self.historial_frames.append({
                    "timestamp": timestamp,
                    "angulo": angulo,
                    "repeticiones": self.repeticiones,
                    "estado": estado,
                    "landmarks": puntos
                })

            if results:
                frame = self.pose_tracker.dibuja_landmarks(frame, results)
                alto_original, ancho_original = frame.shape[:2]
                ratio = nuevo_alto / alto_original
                nuevo_ancho = int(ancho_original * ratio)
                frame = cv2.resize(frame, (nuevo_ancho, nuevo_alto))
                cv2.imshow("Cámara - Seguimiento de Ejercicio", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                self.running = False

        self._cleanup()



    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self._cleanup()

    def _cleanup(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()  # Cierra la ventana al finalizar


    def get_repeticiones(self) -> int:
        return self.repeticiones
