from ciarc.melvin.api import MelvinApi, build_uri
from signal import signal, SIGINT
from sys import exit
from ciarc.odometry.model import predict_position_discrete_time, predict_position
from time import sleep
import numpy as np

ENDPOINT_IP = "10.100.50.1"
ENDPOINT_PORT = 33000
SAMPLES = 10

def main():
  api = MelvinApi(build_uri(ENDPOINT_IP, ENDPOINT_PORT))

  start_telem = api.get_telemetry()

  for _ in range(SAMPLES):
    telem = api.get_telemetry()
    predicted_coord = predict_position(start_telem, telem.time)
    predicted_coord_discrete = predict_position_discrete_time(start_telem, telem.time)
    print(f"Continous vs discrete: {np.linalg.norm(telem.coord-predicted_coord)} {np.linalg.norm(telem.coord-predicted_coord_discrete)}")
    

if __name__ == "__main__":
  signal(SIGINT, lambda sig, frame: exit(0))
  main()