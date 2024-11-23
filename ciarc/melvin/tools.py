from ciarc.melvin.api import MelvinApi
from typing import NoReturn
from time import sleep
from curses import window

class ApiTools:
  def __init__(self, api: MelvinApi, screen: window):
    self.__api: MelvinApi = api
    self.__screen: window = screen
  
  def telemetry_monitor(self) -> NoReturn:
    while True:
      self.__screen.clear()
      telem_str = str(self.__api.get_telemetry())
      self.__screen.addstr(telem_str)
      self.__screen.refresh()
      sleep(0.5)