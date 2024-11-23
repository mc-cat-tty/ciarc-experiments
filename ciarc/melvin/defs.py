from __future__ import annotations
from enum import Enum
from dataclasses import dataclass, fields, asdict, field
from operator import attrgetter
from datetime import datetime
from numpy.typing import ArrayLike
import numpy as np

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
class Energy:
  current_batt: float
  max_batt: float
  fuel: float

  def get_battery_percentage(self):
    return self.current_batt / self.max_batt

@dataclass
class Telemetry:
  time: datetime
  state: MelvinState
  cam_angle: CameraAngle
  energy: Energy
  sim_speed: int
  coord: ArrayLike = field(default_factory=np.ndarray)  # (x, y)
  vel: ArrayLike = field(default_factory=np.ndarray)  # (vx, vy)

  def __init__(
    self,
    state: str, angle: str, simulation_speed: int,
    width_x: int, height_y: int, vx: float, vy: float,
    battery: float, max_battery: float, fuel: float,
    timestamp: str, *args, **kwargs
  ):
    self.time = datetime.fromisoformat(timestamp)
    self.state = MelvinState(state)
    self.cam_angle = CameraAngle(angle)
    self.energy = Energy(battery, max_battery, fuel)
    self.sim_speed = simulation_speed
    self.coord = np.asarray((width_x, height_y))
    self.vel = np.asarray((vx, vy))
    
  def __str__(self):
    return f"x{self.sim_speed} [{self.state} {self.time:%d/%m/%Y %H:%M:%S}]: coord={self.coord} vel={self.vel} | {self.energy} | {self.cam_angle}"


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

  def asdict(self) -> dict:
    def factory(attributes):
      _attributes = map(
        lambda ele: (ele[0], ele[1].value) if issubclass(type(ele[1]), Enum) else (ele[0], ele[1]),
        attributes
      )
      return dict(_attributes)

    return asdict(self, dict_factory=factory)

  @staticmethod
  def from_telemetry(telemetry: Telemetry) -> StateControl:
    return StateControl(
      float(telemetry.vel[0]),
      float(telemetry.vel[1]),
      telemetry.cam_angle,
      telemetry.state
    )
  
  