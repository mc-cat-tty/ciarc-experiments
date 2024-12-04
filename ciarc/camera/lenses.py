from enum import Enum
import numpy as np
from numpy.typing import ArrayLike
from collections import namedtuple

class CameraAngle(Enum):
  NARROW = "narrow"
  NORMAL = "normal"
  WIDE = "wide"

  def get_size(self) -> ArrayLike:
    match self:
      case self.NARROW:
        return np.asarray((600, 600))
      case self.NORMAL:
        return np.asarray((800, 800))
      case self.WIDE:
        return np.asarray((1000, 1000))

