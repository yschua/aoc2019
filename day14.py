import sys
import math

class Chemical:
  def __init__(self, chemStr):
    amt, name = chemStr.split(' ')
    self.name = name
    self.amt = int(amt)
    self.depth = 0

  def __str__(self):
    return '{} {} {}'.format(self.amt, self.name, self.depth)

class Reaction:
  def __init__(self, outChem, inChems):
    self.outChem = outChem
    self.inChems = inChems

  def __str__(self):
    s = '{} = '.format(self.outChem)
    for chem in self.inChems: s += str(chem) + ', '
    return s

reactions = {}
bucket = {'ORE': 0}

for line in sys.stdin.readlines():
  inputs, output = line.strip().split(' => ')
  outChem = Chemical(output)
  inChems = [Chemical(x) for x in inputs.split(', ')]
  reactions[outChem.name] = Reaction(outChem, inChems)
  bucket[outChem.name] = 0

def getDepth(name):
  if name == 'ORE': return 0
  maxDepth = 0
  for chem in reactions[name].inChems:
    chem.depth = getDepth(chem.name) + 1
    maxDepth = max(maxDepth, chem.depth)
  return maxDepth

getDepth('FUEL')

# greedy
for k, reaction in reactions.items():
  reaction.inChems = sorted(reaction.inChems, key=lambda x: -x.depth)

def takeFromBucket(name, amt):
  if name == 'FUEL': return amt

  bucket[name] -= amt
  if bucket[name] >= 0:
    return 0
  else:
    ret = abs(bucket[name])
    bucket[name] = 0
    return ret

ores = 0

def doot(name, outChemAmtNeeded):
  global ores

  if name == 'ORE':
    bucket['ORE'] += outChemAmtNeeded
    ores += outChemAmtNeeded
    return

  reaction = reactions[name]

  outChem = reaction.outChem
  outChemAmtNeeded = takeFromBucket(outChem.name, outChemAmtNeeded)
  n = math.ceil(outChemAmtNeeded / outChem.amt)

  if n == 0: return

  for inChem in reaction.inChems:
    inChemAmtNeeded = n * inChem.amt
    inChemAmtNeeded = takeFromBucket(inChem.name, inChemAmtNeeded)

    doot(inChem.name, inChemAmtNeeded)

    if takeFromBucket(inChem.name, inChemAmtNeeded) != 0:
      raise NotEnoughChemicals # should not ever occur

  # add to bucket
  bucket[outChem.name] += n * outChem.amt

doot('FUEL', 1)
print(ores)

oresPerFuel = ores
maxOres = 1000000000000

while True:
  remOres = maxOres - ores
  fuelAmt = remOres // oresPerFuel
  # print('{} = {} // {}'.format(fuelAmt, remOres, oresPerFuel))
  if remOres < oresPerFuel: break
  doot('FUEL', fuelAmt)

# squeeze out some last drops
while ores < maxOres:
  doot('FUEL', 1)

print(bucket['FUEL'] - 1)