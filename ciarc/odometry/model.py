from numpy.typing import ArrayLike
from datetime import timedelta, datetime
from ciarc.melvin.defs import Telemetry
import numpy as np

def motion_model(start_coord: ArrayLike, velocity: ArrayLike, delta_sec: float):
  return start_coord + velocity * delta_sec

def discretize_time(time_sec: float, freq_hz: int) -> float:
  sim_quanta: float = 1/freq_hz
  under_sec = np.modf(time_sec)[0]
  quanta_idx = int(under_sec / sim_quanta)
  return int(time_sec) + quanta_idx * sim_quanta

def predict_position(telemetry: Telemetry, time: datetime = datetime.now(), sim_freq_hz: int = 2):
  return motion_model(
    telemetry.coord,
    telemetry.vel,
    (time - telemetry.time).total_seconds()
  )

def predict_position_discrete_time(telemetry: Telemetry, time: datetime = datetime.now(), sim_freq_hz: int = 2):
  return motion_model(
    telemetry.coord,
    telemetry.vel,
    discretize_time(time.timestamp(), sim_freq_hz) - discretize_time(telemetry.time.timestamp(), sim_freq_hz)
  )