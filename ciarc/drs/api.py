import requests as rq
from typing import Callable

def build_uri(hostname: str, port: str|int) -> str:
  return f"http://{hostname}:{port}"

class ApiWrapper:
  def __init__(self, endpoint_uri: str):
    self.__uri = endpoint_uri
  
  @staticmethod
  def __api_getter(path: str):
    def decorator(f: Callable):

      def wrapper(self):
        res = rq.get(self.__uri+path)
        if not res.ok:
          raise RuntimeError(f"[GetError] {res.status_code} {res.reason}: {res.json()['detail']}")
        return f(self, res)
      
      return wrapper
    return decorator
  
  @__api_getter("/image")
  def get_image(self, res):
    return res

  def get_telemetry():
    pass

  def control():
    pass

