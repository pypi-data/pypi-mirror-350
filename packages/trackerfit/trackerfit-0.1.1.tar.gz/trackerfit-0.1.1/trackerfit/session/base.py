# session/base.py
# -------------------------------
# Requierements
# -------------------------------

from abc import ABC, abstractmethod
from typing import Optional

# -------------------------------
# Helpers
# -------------------------------

class BaseSession(ABC):
    @abstractmethod
    def start(self, nombre_ejercicio: str, fuente: Optional[str] = None):
        """
        Inicia la sesión (cámara o vídeo).

        Args:
            nombre_ejercicio (str): Nombre del ejercicio a contar.
            fuente (Optional[str]): Fuente de entrada. Puede ser None para cámara o path para vídeo.
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Detiene la sesión y libera recursos.
        """
        pass

    @abstractmethod
    def get_repeticiones(self) -> int:
        """
        Devuelve el número actual de repeticiones contadas.
        """
        pass