from ciarc.melvin.api import MelvinApi
from ciarc.melvin.defs import *
from typing import NoReturn
from time import sleep
from curses import window
import curses
from typing import List


class KeysNamespace: R = ord('r'); A = ord('a'); I = ord('i'); C = ord('c')


class ApiFacade:
  def __init__(self, api: MelvinApi):
    self.__api: MelvinApi = api

  def sim_speedup(self, addend: int = 1):
    old_speed = self.__api.get_telemetry().sim_speed
    return self.__api.set_simulation(sim_speed=old_speed+addend)

  def sim_slowdown(self, addend: int = 1):
    old_speed = self.__api.get_telemetry().sim_speed
    return self.__api.set_simulation(sim_speed=old_speed-addend)
  
  def shoot_and_display(self):
    self.__api.get_image().show()


class ApiDash:
  def __init__(self, api: MelvinApi, screen: window):
    self.__api: MelvinApi = api
    self.__screen: window = screen
    self.__events: List[str] = list()
  
  def telemetry_monitor(self):
    telem_str = str(self.__api.get_telemetry())
    self.__screen.addstr(telem_str)
  
  def print_instructions(self):
    self.__screen.addstr(
      "Press 'a'/'c' to transition, respectively, to acquisition or charge mode\n" +
      "Press 'i' to acquire an image\n" +
      "Press 'r to reset Melvin\n" +
      "Press key up or key down to speedup or slowdown the simulation\n\n")

  def print_events(self):
    self.__screen.addstr(f"Events log: {self.__events}\n\n")
    
  def keys_listener(self):
    pressed_key = self.__screen.getch()
    is_key_pressed = True
    event = ""

    match pressed_key:
      case KeysNamespace.A: self.__api.control(StateControl(state=MelvinState.ACQUISITION))
      case KeysNamespace.C: self.__api.control(StateControl(state=MelvinState.CHARGE))
      case KeysNamespace.I: ApiFacade(self.__api).shoot_and_display()
      case KeysNamespace.R: self.__api.reset()
      case curses.KEY_UP: ApiFacade(self.__api).sim_speedup(); event = "speedup"
      case curses.KEY_DOWN: ApiFacade(self.__api).sim_slowdown(); event = "slowdown"
      case _: is_key_pressed = False
    
    if is_key_pressed:
      self.__events.append(chr(pressed_key) if 33 <= pressed_key <= 126 else event)
    
    while self.__screen.getch() != -1: pass
    
  def interactive_superloop(self, instructions_banner: bool = True) -> NoReturn:
    self.__screen.nodelay(True)

    while True:
      self.keys_listener()
      self.__screen.clear()
      if instructions_banner: self.print_instructions()
      self.print_events()
      self.telemetry_monitor()
      self.__screen.refresh()
      sleep(0.1)
