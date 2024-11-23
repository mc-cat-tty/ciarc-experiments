from ciarc.melvin.api import MelvinApi
from typing import NoReturn
from time import sleep

class ApiTools:
  def __init__(self, api: MelvinApi):
    self.__api: MelvinApi = api
  
  def telemetry_monitor(self) -> NoReturn:
    while True:
      print(self.__api.get_telemetry())
      sleep(0.5)