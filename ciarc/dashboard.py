from ciarc.melvin.api import MelvinApi, build_uri
from ciarc.melvin.tools import ApiDash
from curses import wrapper
from signal import signal, SIGINT
from sys import exit

ENDPOINT_IP = "10.100.50.1"
ENDPOINT_PORT = 33000

def main(screen):
  api = MelvinApi(build_uri(ENDPOINT_IP, ENDPOINT_PORT))
  tools = ApiDash(api, screen)
  tools.interactive_superloop()


if __name__ == "__main__":
  signal(SIGINT, lambda sig, frame: exit(0))
  wrapper(main)