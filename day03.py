import sys

wire1 = sys.stdin.readline().strip().split(',')
wire2 = sys.stdin.readline().strip().split(',')

grid = {}
x, y = 0, 0

actions = {'R': (1, 0), 'L': (-1, 0)}

def visit(x, y, firstWire):
  coord = (x, y)
  if firstWire:
    grid[coord] = False
  else:
    if grid.get(coord) is not None:
      grid[coord] = True

def doMove(x, y, action, dist, firstWire):
  for i in range(0, dist):
    if action == 'R':
      x += 1
    elif action == 'L':
      x -= 1
    elif action == 'U':
      y += 1
    elif action == 'D':
      y -= 1
    visit(x, y, firstWire)
  return x, y

def drawPath(wire, firstWire):
  x, y = 0, 0
  for move in wire:
    action = move[0]
    dist = int(move[1:])
    x, y = doMove(x, y, action, dist, firstWire)

drawPath(wire1, True)
drawPath(wire2, False)

# print(grid)

shortest = None
intersections = []

for coord, intersect in grid.items():
  if intersect:
    intersections.append(coord)
    # print(coord)
    dist = abs(coord[0]) + abs(coord[1])
    if shortest is None:
      shortest = dist
    else:
      shortest = min(shortest, dist)

# print(shortest)

print(intersections)

def calcSteps(coord, wire):
  x, y = 0, 0
  steps = 0
  for move in wire:
    action = move[0]
    dist = int(move[1:])
    for i in range(0, dist):
      if action == 'R':
        x += 1
      elif action == 'L':
        x -= 1
      elif action == 'U':
        y += 1
      elif action == 'D':
        y -= 1
      steps += 1

      if (x, y) == coord:
        return steps

minSteps = None

for coord in intersections:
  steps = calcSteps(coord, wire1) + calcSteps(coord, wire2)
  # print(steps)
  if minSteps is None:
    minSteps = steps
  else:
    minSteps = min(minSteps, steps)

print(minSteps)
