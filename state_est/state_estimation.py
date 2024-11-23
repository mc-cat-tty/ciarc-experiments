from ciarc.melvin.api import MelvinApi, build_uri
from ciarc.melvin.tools import ApiTools

ENDPOINT_IP = "10.100.50.1"
ENDPOINT_PORT = 33000

def main():
  api = MelvinApi(build_uri(ENDPOINT_IP, ENDPOINT_PORT))
  tools = ApiTools(api)
  tools.telemetry_monitor()

if __name__ == "__main__":
  main()