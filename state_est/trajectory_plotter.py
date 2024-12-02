from ciarc.melvin.api import MelvinApi, build_uri
from ciarc.odometry.model import predict_position_discrete_time, predict_position
from signal import signal, SIGINT
from sys import exit
import numpy as np
import seaborn as sb
import matplotlib.pyplot as pl


ENDPOINT_IP = "10.100.50.1"
ENDPOINT_PORT = 33000
SAMPLES = 100


def main():
  api = MelvinApi(build_uri(ENDPOINT_IP, ENDPOINT_PORT))

  samples_telem = [api.get_telemetry() for _ in range(SAMPLES)]

  pl.show()

if __name__ == "__main__":
  signal(SIGINT, lambda sig, frame: exit(0))
  main()
