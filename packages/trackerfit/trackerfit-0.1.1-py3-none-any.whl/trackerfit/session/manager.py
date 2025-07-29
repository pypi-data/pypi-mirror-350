# session/manager.py
# -------------------------------
# Requierements
# -------------------------------

from typing import Optional
from datetime import datetime

from trackerfit.session.base import BaseSession
from trackerfit.session.camera import CameraSession
from trackerfit.session.video import VideoSession
from trackerfit.utils.tipo_entrada_enum import TipoEntrada

# -------------------------------
# Helpers
# -------------------------------

class SessionManager:
    """
    Clase que gestiona el ciclo de vida de una sesión de ejercicio:
    inicialización, ejecución, finalización y generación de resumen.
    """
    def __init__(self):
        self.session: Optional[BaseSession] = None
        self.tipo: Optional[str] = None
        self.fuente: Optional[str] = None
        self.nombre_ejercicio: Optional[str] = None
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.historial_temporal = []

    def iniciar_sesion(self, tipo: TipoEntrada, nombre_ejercicio: str, fuente: Optional[str] = None, lado: str = "derecho"):
        """
        Inicia una nueva sesión de ejercicio.
        Puede ser desde cámara o desde un vídeo pregrabado.

        Args:
            tipo (TipoEntrada): Tipo de entrada (CAMARA o VIDEO).
            nombre_ejercicio (str): ID del ejercicio a realizar.
            fuente (str, opcional): Ruta del vídeo si se usa entrada por vídeo.
            lado (str): Lado del cuerpo ('derecho' o 'izquierdo').
        """
        if self.session is not None:
            raise RuntimeError("Ya hay una sesión activa.")

        if tipo == TipoEntrada.CAMARA:
            self.session = CameraSession()
            self.session.start(nombre_ejercicio, lado)
        elif tipo == TipoEntrada.VIDEO:
            if not fuente:
                raise ValueError("Se requiere fuente de vídeo para una sesión tipo 'video'")
            self.session = VideoSession()
            self.session.start(nombre_ejercicio, fuente, lado)
        else:
            raise ValueError(f"Tipo de sesión desconocido: {tipo}")

        self.tipo = tipo
        self.fuente = fuente
        self.nombre_ejercicio = nombre_ejercicio
        self.start_time = datetime.now()

    def detener_sesion(self):
        """
        Detiene la sesión en curso (si existe) y guarda el historial de frames.
        """
        if self.session:
            self.session.stop()
            self.end_time = datetime.now()
            self.historial_temporal = self.session.historial_frames
            self.session = None

    def obtener_repeticiones(self) -> int:
        """
        Devuelve el número de repeticiones detectadas hasta el momento.

        Returns:
            int: total de repeticiones contadas
        """
        if self.session:
            return self.session.get_repeticiones()
        return 0

    def generar_resumen(self, reps: int) -> dict:
        """
        Genera un resumen de la sesión, incluyendo tiempo, repeticiones y detalles frame a frame.

        Args:
            reps (int): Número total de repeticiones contadas

        Returns:
            dict: resumen estructurado de la sesión
        """
        if not self.start_time or not self.end_time:
            return {}

        duracion = self.end_time - self.start_time

        return {
            "ejercicio": self.nombre_ejercicio,
            "tipo_entrada": self.tipo,
            "repeticiones": reps,
            "inicio": self.start_time.isoformat(),
            "fin": self.end_time.isoformat(),
            "duracion_segundos": int(duracion.total_seconds()),
            "duracion_formateada": str(duracion),
            "detalles_frame_a_frame": self.historial_temporal
        }

    def sesion_activa(self) -> bool:
        """
        Indica si hay una sesión en curso.

        Returns:
            bool: True si la sesión está activa, False en caso contrario.
        """
        return self.session is not None