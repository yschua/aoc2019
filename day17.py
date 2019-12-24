import sys
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

class Point:
  def __init__(self, x, y):
    self.x, self.y = x, y

  def __str__(self):
    return str(self.getTuple())

  def __add__(self, o):
    return Point(self.x + o.x, self.y + o.y)

  def __sub__(self, o):
    return Point(self.x - o.x, self.y - o.y)

  def __eq__(self, o):
    return self.x == o.x and self.y == o.y

  def getTuple(self):
    return (self.x, self.y)

program = [int(x) for x in sys.stdin.readline().split(',')]
computer = IntcodeComputer(program)
computer.run()

grid = []
row = []

for code in computer.output:
  if code != 10:
    row.append(chr(code))
  else:
    grid.append(row)
    row = []
  # print(chr(code), end='')

grid = grid[:-1]
ymax = len(grid)
xmax = len(grid[0])

def get(x, y):
  if x < 0 or x >= xmax or y < 0 or y >= ymax: return None
  return grid[y][x]

def isIntersection(x, y):
  return get(x+1,y) == '#' and get(x-1,y) == '#' and get(x,y+1) == '#' and get(x,y-1) == '#'

total = 0
for y in range(ymax):
  for x in range(xmax):
    if get(x, y) == '^': start = Point(x, y)
    if get(x, y) != '#': continue
    if isIntersection(x, y): total += x * y
print(total)
# print(start)

def turn(direction, move):
  left = (move == 'L')
  if direction == '^': return Point(-1,0) if left else Point(1,0)
  elif direction == 'v': return Point(1,0) if left else Point(-1,0)
  elif direction == '>': return Point(0,-1) if left else Point(0,1)
  elif direction == '<': return Point(0,1) if left else Point(0,-1)

def getDirection(point):
  if point == Point(0,-1): return '^'
  elif point == Point(0,1): return 'v'
  elif point == Point(1,0): return '>'
  elif point == Point(-1,0): return '<'

def forward(direction):
  if direction == '^': return Point(0,-1)
  elif direction == 'v': return Point(0,1)
  elif direction == '>': return Point(1,0)
  elif direction == '<': return Point(-1,0)

def getPt(point):
  return get(point.x, point.y)

baseSeq = []

count = 0
current = start
direction = '^'

i = 0
while True:
  if getPt(current + forward(direction)) == '#':
    current += forward(direction)
    count += 1
  else:
    if count:
      baseSeq.append(str(count))
      count = 0
    if getPt(current + turn(direction, 'L')) == '#':
      baseSeq.append('L')
      direction = getDirection(turn(direction, 'L'))
    elif getPt(current + turn(direction, 'R')) == '#':
      baseSeq.append('R')
      direction = getDirection(turn(direction, 'R'))
    else:
      break
  i += 1

baseSeqStr = ','.join(baseSeq)
print(baseSeqStr)

def getSubstring(seq, n):
  subStr = ''
  for item in seq:
    itemStr = str(item)
    if len(subStr) + len(itemStr) > n: break
    subStr += itemStr + ','
  return subStr[:-1]

def getOccurrence(subStr, seqStrs):
  if subStr == '': return 0
  count = 0
  for seqStr in seqStrs:
    i = seqStr.find(subStr)
    while i >= 0:
      count += 1
      seqStr = removeSubstring(subStr, seqStr, 1).replace(',,', ',')
      # print(seqStr)
      i = seqStr.find(subStr)
  return count

def findBest(seqStrs):
  maxLength = 0
  bestSubstr = None
  seq = seqStrs[0].split(',')
  for subStr in [getSubstring(seq, x) for x in range(1, 21)]:
    length = getOccurrence(subStr, seqStrs) * len(subStr)
    if length > maxLength:
      bestSubstr = subStr
      maxLength = length
  return bestSubstr

def record(subStr, funcName):
  moveStrs[funcName] = subStr
  offset = 0
  while True:
    i = baseSeqStr.find(subStr, offset)
    if i == -1: return
    mainRoutine[i] = funcName
    offset = i + 1

def removeSubstring(subStr, seqStr, count=-1):
  return seqStr.replace(subStr, '', count).strip(',')

mainRoutine = {}
moveStrs = {}

seqStrs = [baseSeqStr]
for function in ['A', 'B', 'C']:
  subStr = findBest(seqStrs)
  record(subStr, function)
  newStrs = []
  for seqStr in seqStrs:
    newStrs += removeSubstring(subStr, seqStr).split(',,')
  seqStrs = list(filter(None, newStrs))

mainStr = ','.join([mainRoutine[x] for x in sorted(mainRoutine.keys())])
print(mainRoutine)
print(mainStr)
print(moveStrs)
if len(seqStrs) > 0: raise ValueError

computer = IntcodeComputer(program)
computer.m[0] = 2

def feedInput(inpStr):
  for c in inpStr:
    computer.run(ord(c))
  computer.run(10)

feedInput(mainStr)
feedInput(moveStrs['A'])
feedInput(moveStrs['B'])
feedInput(moveStrs['C'])

# feedInput('y')
# px = 0
# for code in computer.output:
#   print(chr(code), end='')
#   px = (px + 1) % ((ymax + 1) * xmax)
#   if px == 0: time.sleep(0.5)

feedInput('n')
print(computer.output[-1])
