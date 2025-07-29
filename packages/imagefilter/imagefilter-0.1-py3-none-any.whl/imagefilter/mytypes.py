from dataclasses import dataclass
import math

@dataclass
class Parameter:
    bright: float
    contrast: float
    saturation: float

    def is_default(self) -> bool:
        return  math.isclose(self.bright, 1.0) and math.isclose(self.contrast, 1.0) and math.isclose(self.saturation, 1.0)
