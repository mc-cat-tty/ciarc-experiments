import requests as rq
from typing import Callable

def build_uri(hostname: str, port: str|int) -> str:
  return f"http://{hostname}:{port}"

class ApiError(Exception):
  def __init__(self, response):
    super().__init__(f"[GetError] {response.status_code} {response.reason}: {response.json()['detail']}")

class State:
  def __init__(self, get_path: str):
    self.__get_path = get_path
  
  def __get__(self, obj, objtype=None):
    return rq.get(obj._ApiWrapper__uri + self.__get_path)

class ApiWrapper:
  __melvin_state = State("/observation")

  def __init__(self, endpoint_uri: str):
    self.__uri = endpoint_uri
  
  @staticmethod
  def __api_getter(path: str):
    def decorator(f: Callable):

      def wrapper(self):
        res = rq.get(self.__uri+path)
        if not res.ok:
          raise ApiError(res)
        return f(self, res.json())
      
      return wrapper
    return decorator
  
  @__api_getter("/image")
  def get_image(self, res):
    print(res)
    return res

  def get_telemetry(self):
    return self.__melvin_state

  def set_control(self):
    pass

