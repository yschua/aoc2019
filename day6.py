import sys

orbit = {}

for line in sys.stdin.readlines():
  obj = line.strip().split(')')
  orbit[obj[1]] = obj[0]

def explore(obj):
  return 0 if obj == 'COM' else explore(orbit[obj]) + 1

print(sum([explore(obj) for obj in orbit]))

youPath = {}
sanPath = {}

def explorePath(obj, path, dist):
  if obj == 'COM': return path
  path[orbit[obj]] = dist
  return explorePath(orbit[obj], path, dist + 1)

youPath = explorePath(orbit['YOU'], youPath, 1)
sanPath = explorePath(orbit['SAN'], sanPath, 1)

minDist = None

for obj in youPath:
  if obj in sanPath:
    dist = youPath[obj] + sanPath[obj]
    if minDist is None: minDist = dist
    minDist = min(minDist, dist)

print(minDist)