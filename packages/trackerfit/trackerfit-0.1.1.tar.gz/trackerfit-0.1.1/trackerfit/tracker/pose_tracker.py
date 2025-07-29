# tracker/pose_tracker.py
# -------------------------------
# Requierements
# -------------------------------

import cv2
import mediapipe as mp

# -------------------------------
# Helpers
# -------------------------------

class PoseTracker:

    ''' Configuración inicial: Inicializo el modelo de pose de Mediapipe con mis parámetros 
        - static_image_mode --> Para gestionar si capturamos vídeo en tiempo real o no
        - model_complexity --> Nivel de precisión que usaremos (1=preciso y lento, 2=aceptable y rápido)-
        - min_detection_confidence --> Confianza mínima para detectar
        - min_tracking_confidence --> Confianza mínima para seguir el movimiento
    '''
    def __init__(self, static_image_mode=False, model_complexity=1,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.pose = mp.solutions.pose.Pose(
            static_image_mode = static_image_mode,
            model_complexity = model_complexity,
            min_detection_confidence = min_detection_confidence,
            min_tracking_confidence = min_tracking_confidence
        )
        
        self.drawing_utils = mp.solutions.drawing_utils # Para dibujar puntos y líneas
        self.drawing_styles = mp.solutions.drawing_styles # Para obtener los colores y estilos por defecto
        self.pose_connections = mp.solutions.pose.POSE_CONNECTIONS # Cómo se conectan los puntos del cuerpo
    
    ''' Detección de landmarks
    Convierte el frame de BGR (formato de OpenCV) a RGB (formato de MediaPipe) y luego
    lo pasa por el modelo para obtener los landmarks (puntos del cuerpo)'''
    def procesar(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)
        return results # Results contiene toda la información de la pose
    
    
    ''' Dibuja la pose (Esqueleto)
    Es decir, dibujo los landmarks y las conexiones entre ellos para mostrar
    visualmente la pose en pantalla'''
    def dibuja_landmarks(self, frame, results):
        if(results.pose_landmarks):
            self.drawing_utils.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.pose_connections,
                self.drawing_styles.get_default_pose_landmarks_style()
            )
        return frame

    def dibujar_triangulo_con_angulo(self,frame, puntos, id1, id2, id3, angulo, umbral_validacion):
        """
        Dibuja un triángulo entre tres landmarks y muestra el ángulo.
        Cambia de color (rojo/verde) según si supera el umbral de validación.
        """
        p1 = puntos[id1]["x"], puntos[id1]["y"]
        p2 = puntos[id2]["x"], puntos[id2]["y"]
        p3 = puntos[id3]["x"], puntos[id3]["y"]

        # Color según validación del ángulo
        color = (0, 255, 0) if angulo < umbral_validacion else (0, 0, 255)  # verde o rojo

        # Dibujar líneas del triángulo
        cv2.line(frame, p1, p2, color, 2)
        cv2.line(frame, p2, p3, color, 2)
        cv2.line(frame, p3, p1, color, 2)

        # Mostrar valor del ángulo
        cv2.putText(frame, f"{int(angulo)}", p2, cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    
    ''' Extraemos las coordenadas de los landmarks
    Convierto los landmarks a coordenadas reales en píxeles según el tamaño del frame (alto,ancho),
    ya que los landmarks están en coordenadas normalizadas (0,1)'''
    def extraer_landmarks(self, results, frame_shape):
        height, width, _ = frame_shape
        puntos = {}
        
        if(results.pose_landmarks):
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                puntos[idx] = {
                    'x': int(landmark.x * width),
                    'y': int(landmark.y * height),
                    'z': landmark.z,
                    #'visibilidad': landmark.visibility
                }
        return puntos
    
    
    
        