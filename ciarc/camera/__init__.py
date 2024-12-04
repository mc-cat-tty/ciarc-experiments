from dataclasses import namedtuple
from numpy.typing import NDArray

@namedtuple
class CameraROI:
  center: NDArray
  width: int
  height: int