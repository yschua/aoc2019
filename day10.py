import sys
import math

grid = {}

for y, line in enumerate(sys.stdin.readlines()):
  for x, obj in enumerate(line.strip()):
    grid[(x,y)] = obj

# print(grid)

def count(stationLoc):
  asteroids = 0
  for loc, obj in grid.items():
    if loc == stationLoc or obj == '.': continue
    if canSee(loc, stationLoc): asteroids += 1
  # print(str(stationLoc) + str(asteroids))
  return asteroids

def minus(a, b):
  return (a[0]-b[0], a[1]-b[1])

def plus(a, b):
  return (a[0]+b[0], a[1]+b[1])

def canSee(loc, stationLoc):
  diff = minus(loc, stationLoc)
  diff = minDiff(diff)
  while True:
    loc = minus(loc, diff)
    if loc == stationLoc: return True
    if grid[loc] == '#': return False

def minDiff(d):
  gcd = math.gcd(d[0], d[1])
  return (d[0]/gcd, d[1]/gcd)

# print(minDiff((12, 4)))
# print(canSee((4,3), (1,0)))

maxAsteroids = 0
bestLoc = None
for loc, obj in grid.items():
  if obj == '.': continue
  if count(loc) > maxAsteroids: maxAsteroids, bestLoc = count(loc), loc

print(maxAsteroids)

destroyed = []

for loc, obj in grid.items():
  if loc == bestLoc or obj == '.': continue
  if canSee(loc, bestLoc):
    destroyed.append(minus(loc, bestLoc))
# print(destroyed)

def calcAngle(loc):
  x, y = loc[0], loc[1]
  if x == 0: return 0 if y < 0 else 180
  if y == 0: return 90 if x > 0 else 270

  if x > 0 and y < 0:
    return math.degrees(math.atan(abs(x)/abs(y)))
  elif x > 0 and y > 0:
    return 90 + math.degrees(math.atan(abs(y)/abs(x)))
  elif x < 0 and y > 0:
    return 180 + math.degrees(math.atan(abs(x)/abs(y)))
  else:
    return 270 + math.degrees(math.atan(abs(y)/abs(x)))

# for d in destroyed:
#   print('{} {}'.format(calcAngle(d), d))

destroyed = sorted(destroyed, key=lambda x: calcAngle(x))
# print(destroyed)
destroyed = [plus(x, bestLoc) for x in destroyed]

# print(destroyed[199])

x, y = destroyed[199]
print(x * 100 + y)