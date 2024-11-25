from ciarc.melvin.api import MelvinApi, build_uri
from ciarc.odometry.model import predict_position_discrete_time, predict_position
from signal import signal, SIGINT
from sys import exit
import numpy as np
import seaborn as sb
import matplotlib.pyplot as pl
import pandas as pd
from functools import partial
from operator import attrgetter

ENDPOINT_IP = "10.100.50.1"
ENDPOINT_PORT = 33000
SAMPLES = 100


def process_data(start_telem, samples_telem, use_active_time: bool):
  """
  :param use_active_time: Use active_time if True, use time otherwise
  """
  
  _pred_coord_continuous_fn = partial(predict_position, start_telem)
  _pred_coord_discrete_fn = partial(predict_position_discrete_time, start_telem)
  
  sample_times = list(map(attrgetter("active_time" if use_active_time else "time"), samples_telem))
  _coord_ground_truth = list(map(attrgetter("coord"), samples_telem))
  _predictions_continous = list(map(_pred_coord_continuous_fn, sample_times))
  _predictions_discrete = list(map(_pred_coord_discrete_fn, sample_times))
  predictions_continous_error = np.linalg.norm(np.array(_predictions_continous) - np.array(_coord_ground_truth), axis=1).tolist()
  predictions_discrete_error = np.linalg.norm(np.array(_predictions_discrete) - np.array(_coord_ground_truth), axis=1).tolist()

  return sample_times, predictions_continous_error, predictions_discrete_error


def plot_data(sample_times, predictions_continous_error, predictions_discrete_error, ax, x_label):
  y_label = "error"

  plot_data = pd.DataFrame({
    x_label: sample_times * 2,
    y_label: predictions_continous_error + predictions_discrete_error,
    "type": ["continous"] * len(sample_times) + ["dicrete"] * len(sample_times),
  })

  sb.set_theme(style="whitegrid")
  sb.lineplot(
		data=plot_data,
		palette="rocket_r",
		hue="type",
		linewidth=2,
		x=x_label,
		y=y_label,
    ax=ax
	)


def main():
  api = MelvinApi(build_uri(ENDPOINT_IP, ENDPOINT_PORT))

  # Collect data
  start_telem = api.get_telemetry()
  samples_telem = [api.get_telemetry() for _ in range(SAMPLES)]

  fig, ax = pl.subplots(1, 2, sharey=True)

  plot_data(*process_data(start_telem, samples_telem, True), ax[0], "active_time")
  plot_data(*process_data(start_telem, samples_telem, False), ax[1], "time")

  pl.show()

    

if __name__ == "__main__":
  signal(SIGINT, lambda sig, frame: exit(0))
  main()