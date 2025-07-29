# ejercicios/base.py
# -------------------------------
# Requierements
# -------------------------------
from abc import ABC
from trackerfit.utils.angulos import calcular_angulo_landmarks

# -------------------------------
# Helpers
# -------------------------------

class Ejercicio(ABC):
    """
    Clase base para ejercicios. Define la lógica general de conteo de repeticiones
    basada en el análisis de ángulos entre tres landmarks clave.
    """
    def __init__(self, angulo_min, angulo_max, puntos):
        """
        Inicializa un ejercicio con umbrales y puntos clave.

        Args:
            angulo_min (float): Ángulo mínimo esperado (posición contraída).
            angulo_max (float): Ángulo máximo esperado (posición extendida).
            puntos (tuple): IDs de 3 landmarks (id1, id2, id3) en orden.
        """
        self.reps = 0
        self.arriba = False
        self.abajo = False
        self.angulo_min = angulo_min
        self.angulo_max = angulo_max
        self.id1, self.id2, self.id3 = puntos
        self.umbral_validacion = 90 # Valor por defecto, en las subclases se sobrescribe

    def actualizar(self, puntos_detectados):
        """
        Actualiza el estado del ejercicio con los puntos detectados.

        Returns:
            tuple: (ángulo actual, repeticiones acumuladas)
        """
        if not all(k in puntos_detectados for k in [self.id1, self.id2, self.id3]):
            return None, self.reps

        # Frame a frame iremos calculando el ángulo que forman los puntos clave del ejercicio,buscando detectar transiciones.
        angulo = calcular_angulo_landmarks(puntos_detectados, self.id1, self.id2, self.id3)
        self.detectar_transicion(angulo) # Si se detectara una transición entre arriba y abajo, se agregaría una repetición.
        
        return angulo, self.reps

    def detectar_transicion(self, angulo):
        """
        Detecta si ha habido una transición válida (subida y bajada) para contar una repetición.
        """
        if angulo >= self.angulo_max:
            self.arriba = True
        if self.arriba and not self.abajo and angulo <= self.angulo_min:
            self.abajo = True
        if self.arriba and self.abajo and angulo >= self.angulo_max:
            self.reps += 1 # Cuando detectamos que ya ha subido y bajado añadimos una repetición
            self.arriba = False
            self.abajo = False

    def reset(self):
        """Reinicia el conteo de repeticiones."""
        self.reps = 0
        self.arriba = False
        self.abajo = False

    def get_reps(self):
        """Devuelve el número actual de repeticiones."""
        return self.reps
