# ejercicios/__init__.py
# -------------------------------
# Requierements
# -------------------------------
from .curl_bicep import CurlBicep
from .sentadilla import Sentadilla
from .flexion import Flexion
from .quad_extension import QuadExtension
from .press_militar import PressMilitar
from .crunch_abdominal import CrunchAbdominal
from .tricep_dip import TricepDip
from .elevacion_lateral import ElevacionLateral
from .base import Ejercicio
# -------------------------------
# Helpers
# -------------------------------
__all__ = [
    "CurlBicep", "Sentadilla", "Flexion", "QuadExtension", "PressMilitar",
    "CrunchAbdominal", "TricepDip", "ElevacionLateral", "Ejercicio"
]
