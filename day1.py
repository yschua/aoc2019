import sys
import math

def calcFuel(module):
  total = 0
  while True:
    module = math.floor(module / 3) - 2
    if module <= 0:
      break
    total += module
  return total

total = 0
for line in sys.stdin:
  total += calcFuel(int(line))

print(total)