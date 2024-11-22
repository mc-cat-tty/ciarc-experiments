from ciarc.melvin.api import ApiWrapper
from typing import NoReturn
from time import sleep

class ApiUtils:
  def __init__(self, api: ApiWrapper):
    self.__api: ApiWrapper = api
  
  def telemetry_monitor_(self) -> NoReturn:
    while True:
      print(self.__api.get_telemetry())
      sleep(0.5)