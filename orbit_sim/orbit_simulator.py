from ciarc.map.grid import MapGrid


def main():
  map = MapGrid().set_scale_factor(10)

  x = []
  y = []
  colors = []
  visited = []

  V_X, V_Y = LENS_W, SIZE_H

  P0 = np.asarray((0, 0))
  v = np.asarray((V_X, V_Y)) * 1/10
  # v = v / np.min(v)
  print(v)

  print(f"Velocities ratio: {v[0]/v[1]}")
  print(f"Map aspect ratio: {SIZE_W/SIZE_H}")
  print(f"K = {(v[0]/v[1]) * SIZE_H/SIZE_W}")
  print(f"Tx, Ty: {(SIZE_W*36)/v[0]}, {(SIZE_H*18)/v[1]}")
  p = P0

  it = 0
  IT_SAFEGUARD = SIZE_W * 1e3

  while it < IT_SAFEGUARD and (not any(np.all(ele == np.round(p)) for ele in visited) or np.all(np.round(p) == visited[-1])):
    if len(visited) <= 0 or not np.all(np.round(p) == visited[-1]):
      visited.append(np.round(p))
      colors.append(np.asarray((0, 1, 1)) * it)
    p = (p + v) % SIZE
    it += 1

  p = np.round(p)
  print(visited)

  colors = np.asarray(colors)
  colors = colors / colors[-1]

  if it == IT_SAFEGUARD: print("Safeguard parameter hit")
  else: print(f"{p} reincountered")
  
  map.add_visited_area()
  
  map.plot()


if __name__ == "__main__":
  main()