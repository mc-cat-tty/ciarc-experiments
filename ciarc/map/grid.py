from __future__ import annotations
import numpy as np
from numpy.typing import ArrayLike, NDArray
from ciarc.camera import CameraROI
from typing import List
import matplotlib.pyplot as pl
from operator import itemgetter


class MapGrid:
  SIZE: NDArray = np.asarray((21600, 10800))
  SIZE_W, SIZE_H = SIZE

  def __init__(self):
    self.scale_factor: float = 1.0

    self.visited_pxs: List[NDArray] = list()
    self.covered_rois: List[CameraROI] = list()

    self.color_pxs: List[pl.Color] = list()
    self.color_rois: List[pl.Color] = list()


  def get_size(self) -> NDArray:
    return self.SIZE/self.scale_factor
  
  def set_scale_factor(self, scale_factor: float) -> MapGrid:
    self.scale_factor = scale_factor
    return self

  def add_visited_area(self, coord: ArrayLike, size: ArrayLike, color: pl.Color = (255, 255, 255)) -> MapGrid:
    coord = np.round(np.asarray(coord))
    size = np.round(np.asarray(size))
    
    self.visited_pxs.append(
      CameraROI(
        coord = coord,
        width = size[0],
        height = size[1]
      )
    )

    self.color_rois.append(color)

    return self

  def add_visited_pixel(self, coord: ArrayLike, color: pl.Color = (255, 255, 255)) -> MapGrid:
    coord = np.asarray(coord)
    self.visited_pxs.append(np.round(coord))
    self.color_pxs.append(color)
    return self
  
  def plot(self, ax: pl.Axes):
    def get_coord_from_list_factory(pos: int):
      return lambda l: [*map(itemgetter(pos), l)]

    x_getter = get_coord_from_list_factory(0)
    y_getter = get_coord_from_list_factory(1)
    boxes = [pl.Rectangle((r.coord[0], r.coord[1]), r.width, r.height, color=c) for r, c in zip(self.covered_rois, self.color_rois)]

    ax.scatter(x_getter(self.visited_pxs), y_getter(self.visited_pxs), c=self.color_pxs)
    [ax.add_patch(p) for p in boxes]

    size = self.get_size()
    ax.xlim((0, size[1]-1))
    ax.ylim((0, size[0]-1))

    ax.grid(True)
    ax.show()