import sys

class IntcodeComputer:
  def __init__(self, program):
    self.m = dict(zip(range(len(program)), program))
    self.i = 0
    self.end = False
    self.output = []
    self.relBase = 0
    # self.run(inp)

  def idx(self, n):
    mode = self.paramModes[-n] if n <= len(self.paramModes) else 0
    if mode == 0:   return self.m[self.i + n]                # position
    elif mode == 1: return self.i + n                        # immediate
    elif mode == 2: return self.m[self.i + n] + self.relBase # relative

  def set(self, n, val):
    self.m[self.idx(n)] = val

  def get(self, n):
    idx = self.idx(n)
    return self.m[idx] if idx in self.m else 0

  def setParamModes(self):
    self.paramModes = [int(x) for x in str(self.m[self.i] // 100)]

  def run(self, inp):
    self.output = []
    while True:
      op = self.m[self.i] % 100
      self.setParamModes()
      if op == 99:
        # terminate
        self.end = True
        break
      elif op == 1:
        # add
        self.set(3, self.get(1) + self.get(2))
        self.i += 4
      elif op == 2:
        # multiply
        self.set(3, self.get(1) * self.get(2))
        self.i += 4
      elif op == 3:
        # input
        if inp is None: break
        self.set(1, inp)
        inp = None
        self.i += 2
      elif op == 4:
        # output
        self.output.append(self.get(1))
        self.i += 2
      elif op == 5:
        # jump if true
        self.i = self.get(2) if self.get(1) != 0 else self.i + 3
      elif op == 6:
        # jump if false
        self.i = self.get(2) if self.get(1) == 0 else self.i + 3
      elif op == 7:
        # less than
        self.set(3, int(self.get(1) < self.get(2)))
        self.i += 4
      elif op == 8:
        # equals
        self.set(3, int(self.get(1) == self.get(2)))
        self.i += 4
      elif op == 9:
        # relative base offset
        self.relBase += self.get(1)
        self.i += 2

program = [int(x) for x in sys.stdin.readline().split(',')]

# 0 if black, 1 if white
# output 0 to black, 1 to white
# output 0 to left, 1 to right, move forward

grid = {}
pos = (0, 0)
dir = 'up'
robot = IntcodeComputer(program)
color = 1

def move(pos, dir, turnRight):
  if dir == 'up':
    return (pos[0] + (1 if turnRight else -1), pos[1]), 'right' if turnRight else 'left'
  elif dir == 'down':
    return (pos[0] + (-1 if turnRight else 1), pos[1]), 'left' if turnRight else 'right'
  elif dir == 'right':
    return (pos[0], pos[1] + (-1 if turnRight else 1)), 'down' if turnRight else 'up'
  else:
    return (pos[0], pos[1] + (1 if turnRight else -1)), 'up' if turnRight else 'down'

def getColor(pos):
  return 0 if pos not in grid else grid[pos]

while not robot.end:
  robot.run(color)
  if len(robot.output) > 0:
    paint, turnRight = robot.output
    grid[pos] = paint
    pos, dir = move(pos, dir, turnRight)
    color = getColor(pos)

print(len(grid))

xmin = min(grid.keys(), key=lambda x: x[0])[0]
xmax = max(grid.keys(), key=lambda x: x[0])[0]
ymin = min(grid.keys(), key=lambda x: x[1])[1]
ymax = max(grid.keys(), key=lambda x: x[1])[1]

for y in range(ymax, ymin - 1, -1):
  for x in range(xmin, xmax + 1):
    print('#' if getColor((x,y)) else ' ', end='')
  print()
