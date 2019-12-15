# velocity <- gravity. +1/-1 to pull axis closer
# position <- velocity. offset position by velocity
# total = potential * kinetic
# potential = sum of abs(position)
# kinetic = sum of abs(velocity)

import sys
import math

class Moon():
  def __init__(self, pos):
    self.x = pos[0]
    self.y = pos[1]
    self.z = pos[2]
    self.vx = 0
    self.vy = 0
    self.vz = 0

  def __str__(self):
    return 'pos={},{},{} vel={},{},{}'.format(self.x, self.y, self.z, self.vx, self.vy, self.vz)

  def updateVelocity(self, moon):
    dx = moon.x - self.x
    dy = moon.y - self.y
    dz = moon.z - self.z
    if dx: self.vx += int(math.copysign(1, dx))
    if dy: self.vy += int(math.copysign(1, dy))
    if dz: self.vz += int(math.copysign(1, dz))

  def updatePosition(self):
    self.x += self.vx
    self.y += self.vy
    self.z += self.vz

  def getEnergy(self):
    potential = abs(self.x) + abs(self.y) + abs(self.z)
    kinetic = abs(self.vx) + abs(self.vy) + abs(self.vz)
    return potential * kinetic

moons = []

for line in sys.stdin.readlines():
  moons.append(Moon([int(x[2:]) for x in line.strip('<').strip('>\n').split(', ')]))

n = len(moons)

def getTotalEnergy(steps):
  for step in range(steps):
    for i in range(n):
      for j in range(n):
        if i != j: moons[i].updateVelocity(moons[j])
    for moon in moons:
      moon.updatePosition()
      # print(moon)
  # print()

  energy = sum([m.getEnergy() for m in moons])
  return energy

# print(getTotalEnergy(1000))

class States:
  def __init__(self):
    self.savedStates = {}
    self.repeating = False
    self.period = None

  def stateName(vals):
    return '{} {} {} {}'.format(*vals)

  def saveState(self, step, vals):
    if self.period: return
    state = States.stateName(vals)
    if state in self.savedStates:
      if self.repeating: self.period = step - 1
      else: self.repeating = True
    else:
      self.savedStates[state] = None
      self.repeating = False

def simulateStep(): getTotalEnergy(1)

def getPeriods():
  step = 0
  xStates, yStates, zStates = States(), States(), States()
  while not xStates.period or not yStates.period or not zStates.period:
    simulateStep()
    xStates.saveState(step, [(m.x, m.vx) for m in moons])
    yStates.saveState(step, [(m.y, m.vy) for m in moons])
    zStates.saveState(step, [(m.z, m.vz) for m in moons])
    step += 1
  return (xStates.period, yStates.period, zStates.period)

p = getPeriods()
print(p)

def lcm(a, b):
  return a * b // math.gcd(a, b)

print(lcm(lcm(p[0], p[1]), p[2]))
