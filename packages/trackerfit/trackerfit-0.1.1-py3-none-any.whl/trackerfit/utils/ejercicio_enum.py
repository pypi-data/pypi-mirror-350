# utils/ejercicio_enum.py
# -------------------------------
# Requierements
# -------------------------------
from enum import Enum

# -------------------------------
# Helpers
# -------------------------------

class EjercicioId(str, Enum):
    CURL_BICEP = "curl_bicep"
    SENTADILLA = "sentadilla"
    FLEXION = "flexion"
    PRESS_MILITAR = "press_militar"
    QUAD_EXTENSION = "quad_extension"
    CRUNCH_ABDOMINAL = "crunch_abdominal"
    TRICEP_DIP = "tricep_dip"
    ELEVACION_LATERAL = "elevacion_lateral"
