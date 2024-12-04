from numpy.typing import NDArray
from datetime import timedelta, datetime
from ciarc.melvin.defs import Telemetry
import numpy as np

def motion_model(start_coord: NDArray, velocity: NDArray, delta_sec: float):
  return start_coord + velocity * delta_sec

def discretize_time(time_sec: float, freq_hz: int) -> float:
  sim_quanta: float = 1/freq_hz
  under_sec = np.modf(time_sec)[0]
  quanta_idx = under_sec // sim_quanta
  return int(time_sec) + quanta_idx * sim_quanta

def predict_position(telemetry: Telemetry, time: datetime|float = datetime.now()):
  if issubclass(type(time), datetime):
    diff_time = (time - telemetry.time).total_seconds()
  else:
    diff_time = time - telemetry.active_time
  
  return np.round(motion_model(
    telemetry.coord,
    telemetry.vel,
    diff_time
  ))

def predict_position_discrete_time(telemetry: Telemetry, time: datetime|float = datetime.now(), sim_freq_hz: int = 2):
  ref_time = telemetry.active_time
  
  if issubclass(type(time), datetime):
    time = time.timestamp()
    ref_time = telemetry.time.timestamp()
  
  return np.round(motion_model(
    telemetry.coord,
    telemetry.vel,
    discretize_time(time, sim_freq_hz) - discretize_time(ref_time, sim_freq_hz)
  ))