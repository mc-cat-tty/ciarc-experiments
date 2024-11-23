import requests as rq
from typing import Callable
from ciarc.melvin.defs import *
from dataclasses import asdict

def build_uri(hostname: str, port: str|int) -> str:
  return f"http://{hostname}:{port}"

class ApiError(Exception):
  def __init__(self, response):
    super().__init__(f"[GetError] {response.status_code} {response.reason}: {response.json()['detail']}")

def api_getter(path: str = None):
  def decorator(f: Callable):

    def wrapper(self, *args, **kwargs):
      _path = path if path else self.get_get_path()

      try: api_wrapper = args[0]
      except: api_wrapper = self

      uri = api_wrapper.get_uri()
      res = rq.get(uri+_path)

      if not res.ok: raise ApiError(res)
      return f(self, res.json(), *args, **kwargs)
    
    return wrapper
  return decorator


class State:
  def __init__(self, get_path: str, put_path: str):
    self.__get_path = get_path
    self.__put_path = put_path
  
  def get_get_path(self):
    return self.__get_path
  
  def get_put_path(self):
    return self.__put_path
  
  @api_getter()
  def __get__(self, res, obj, objtype=None):
    return res

  def __set__(self, obj, control: StateControl):
    current_state = self.__get__(obj, type(obj))
    current_state = StateControl.from_telemetry(Telemetry(**current_state)).asdict()
    _control = control.asdict()

    changed_vals = filter(lambda ele: ele[1] is not None, _control.items())
    current_state.update(changed_vals)

    res = rq.put(obj.get_uri() + self.__put_path, json=current_state)
    if not res.ok: raise ApiError(res)
    return res.status_code


class MelvinApi:
  __melvin_state = State("/observation", "/control")

  def __init__(self, endpoint_uri: str):
    self.__uri = endpoint_uri
  
  def get_uri(self):
    return self.__uri
  
  @api_getter("/image")
  def get_image(self, res):
    return res
  
  @api_getter("/reset")
  def reset(self, _):
    return None

  def get_telemetry(self) -> Telemetry:
    return Telemetry(**self.__melvin_state)

  def control(self, state_control: StateControl):
    """
    Leave state_control's fields empty to keep their current values
    """
    self.__melvin_state = state_control

  def set_simulation(self, sim_speed: int, network_sim: bool = False):
    payload = {"is_network_simulation": network_sim, "user_speed_multiplier": sim_speed}
    res = rq.put(self.__uri + "/simulation", params=payload)
    return res
  