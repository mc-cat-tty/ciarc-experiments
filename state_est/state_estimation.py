from ciarc.melvin.api import MelvinApi, build_uri
from ciarc.odometry.model import predict_position_discrete_time, predict_position
from signal import signal, SIGINT
from sys import exit
import numpy as np
import seaborn as sb
import matplotlib.pyplot as pl
import pandas as pd
from functools import partial
from operator import attrgetter, sub

ENDPOINT_IP = "10.100.50.1"
ENDPOINT_PORT = 33000
SAMPLES = 50

def main():
  api = MelvinApi(build_uri(ENDPOINT_IP, ENDPOINT_PORT))

  start_telem = api.get_telemetry()
  samples_telem = [api.get_telemetry() for _ in range(SAMPLES)]
  
  _pred_coord_continuous_fn = partial(predict_position, start_telem)
  _pred_coord_discrete_fn = partial(predict_position_discrete_time, start_telem)
  
  sample_times = list(map(attrgetter("time"), samples_telem))
  _coord_ground_truth = list(map(attrgetter("coord"), samples_telem))
  _predictions_continous = list(map(_pred_coord_continuous_fn, sample_times))
  _predictions_discrete = list(map(_pred_coord_discrete_fn, sample_times))
  predictions_continous_error = np.linalg.norm(np.array(_predictions_continous) - np.array(_coord_ground_truth), axis=1).tolist()
  predictions_discrete_error = np.linalg.norm(np.array(_predictions_discrete) - np.array(_coord_ground_truth), axis=1).tolist()

  plot_data = pd.DataFrame({
    "times": sample_times * 2,
    "error": predictions_continous_error + predictions_discrete_error,
    "type": ["continous"] * len(sample_times) + ["dicrete"] * len(sample_times),
  })

  sb.set_theme(style="whitegrid")
  sb.lineplot(
		data=plot_data,
		palette="rocket_r",
		hue="type",
		linewidth=2,
		x="times",
		y="error"
	)
  sb.despine()
  pl.show()

  # print(f"Continous vs discrete: {np.linalg.norm(telem.coord-predicted_coord)} {np.linalg.norm(telem.coord-predicted_coord_discrete)}")
    

if __name__ == "__main__":
  signal(SIGINT, lambda sig, frame: exit(0))
  main()