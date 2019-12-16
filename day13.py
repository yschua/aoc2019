import sys
import enum
import math
import time

class IntcodeComputer:
  def __init__(self, program):
    self.m = dict(zip(range(len(program)), program))
    self.i = 0
    self.end = False
    self.output = []
    self.relBase = 0

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

  def run(self, inp=None):
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

class Tile(enum.Enum):
  empty = 0
  wall = 1
  block = 2
  paddle = 3
  ball = 4

  def __str__(self):
    if self == Tile.empty: return ' '
    if self == Tile.wall: return '#'
    if self == Tile.block: return 'x'
    if self == Tile.paddle: return '_'
    if self == Tile.ball: return 'o'

program = [int(x) for x in sys.stdin.readline().split(',')]
computer = IntcodeComputer(program)
computer.m[0] = 2

screen = {}
xmax, ymax = 0, 0
score = 0

def update(output):
  global xmax, ymax, score
  i = 0
  while i < len(output):
    x, y, tileId = [x for x in output[i:i+3]]
    xmax = max(xmax, x)
    ymax = max(ymax, y)
    if (x, y) == (-1, 0): score = tileId
    else: screen[(x, y)] = Tile(tileId)
    i += 3

def getNextInput():
  ball, paddle = None, None
  for k, v in screen.items():
    if v == Tile.ball: ball = k
    if v == Tile.paddle: paddle = k
    if ball and paddle:
      diff = ball[0] - paddle[0]
      return 0 if diff == 0 else math.copysign(1, diff)
  return 0

def draw():
  for i in range(30): print()
  print(score)
  for y in range(ymax + 1):
    for x in range(xmax + 1):
      print(str(screen[(x, y)]), end='')
    print()

while not computer.end:
  computer.run(getNextInput())
  update(computer.output)
  draw()
  time.sleep(0.04)
