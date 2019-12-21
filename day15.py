import sys
import math

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

class Point:
  def __init__(self, x, y):
    self.x, self.y = x, y

  def __str__(self):
    return '({}, {})'.format(self.x, self.y)

  def __add__(self, o):
    return Point(self.x + o.x, self.y + o.y)

  def __sub__(self, o):
    return Point(self.x - o.x, self.y - o.y)

  def getTuple(self):
    return (self.x, self.y)

north = Point(0, 1)
south = Point(0, -1)
west = Point(-1, 0)
east = Point(1, 0)
directions = [north, south, west, east]

class Node:
  def __init__(self, location):
    self.neighbours = [None, None, None, None]
    self.kind = '?' # unexplored
    self.location = location

  def __str__(self):
    return '{} {}'.format(self.kind, self.location)

  def generate(self):
    for i in range(4):
      self.neighbours[i] = Node(self.location + directions[i])
      self.neighbours[i].neighbours[i + (-1 if i % 2 else 1)] = self

def getReturnInput(i):
  if i == 0: return 2 # south
  if i == 1: return 1 # north
  if i == 2: return 4 # east
  if i == 3: return 3 # west

visited = {}

def build(node, returnInput):
  node.generate()
  # print('Visiting {}'.format(node))
  visited[node.location.getTuple()] = node.kind
  for i in range(4):
    neighbour = node.neighbours[i]
    if neighbour.location.getTuple() in visited: continue
    computer.run(i + 1)
    status = computer.output[0]
    if status != 0:
      neighbour.kind = '.' if status == 1 else 'x'
      build(neighbour, getReturnInput(i))
      nodes.append(neighbour)
  computer.run(returnInput)

program = [int(x) for x in sys.stdin.readline().split(',')]
computer = IntcodeComputer(program)

start = Node(Point(0, 0))
start.kind = '.'
nodes = [start]

build(start, None)

n = len(nodes)
# print(n)
dist = [[math.inf for i in range(n)] for j in range(n)]
goalIdx = None

for i in range(n):
  if nodes[i].kind == 'x': goalIdx = i
  for j in range(n):
    if i == j:
      dist[i][j] = 0
    else:
      diff = nodes[i].location - nodes[j].location
      if (diff.x == 0 and abs(diff.y) == 1) or (abs(diff.x) == 1 and diff.y == 0):
        dist[i][j] = 1

for k in range(n):
  for i in range(n):
    for j in range(n):
      if dist[i][j] > dist[i][k] + dist[k][j]:
        dist[i][j] = dist[i][k] + dist[k][j]

print(dist[0][goalIdx])
print(max(dist[goalIdx]))