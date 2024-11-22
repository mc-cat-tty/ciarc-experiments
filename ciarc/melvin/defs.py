from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, fields
from operator import attrgetter

class CameraAngle(Enum):
  NARROW = "narrow"
  NORMAL = "normal"
  WIDE = "wide"

class MelvinState(Enum):
  DEPLOYMENT = "deployment"
  ACQUISITION = "acquisition"
  CHARGE = "charge"
  COMMUNICATION = "communication"
  SAFE = "safe"
  TRANSITION = "transition"

@dataclass(frozen=True)
class StateControl:
  vel_x: int = None
  vel_y: int = None
  camera_angle: CameraAngle = None
  state: MelvinState = None

  def get_attributes(self) -> list:
    return list(
      map(attrgetter('name'), fields(self))
    )
  
  @staticmethod
  def map_key(in_key: str) -> str:
    match in_key:
      case "angle": return "camera_angle"
      case "vx": return "vel_x"
      case "vy": return "vel_y"
      case "state": return "state"
      case _: return None

  @staticmethod
  def from_telemetry(telemetry: dict) -> StateControl:
    _telem = map(
      lambda ele: (StateControl.map_key(ele[0]), ele[1]),
      telemetry.items()
    )

    _telem = dict(
      filter(
        lambda k: k[0] is not None,
        _telem
      )
    )

    return StateControl(**_telem)
  
  