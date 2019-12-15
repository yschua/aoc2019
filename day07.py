import sys
import itertools

class Amplifier:
  def __init__(self, program, phase):
    self.m = program
    self.pm = []
    self.i = 0
    self.end = False
    self.output = 0
    self.run(phase)

  def idx(self, n):
    mode = self.pm[-n] if n <= len(self.pm) else 0
    return self.m[self.i + n] if mode == 0 else self.i + n

  def set(self, n, val):
    self.m[self.idx(n)] = val

  def get(self, n):
    return self.m[self.idx(n)]

  def run(self, inp):
    while True:
      op = self.m[self.i] % 100
      self.pm = [int(x) for x in str(self.m[self.i] // 100)]
      if op == 99:
        self.end = True
        break
      elif op == 1:
        self.set(3, self.get(1) + self.get(2))
        self.i += 4
      elif op == 2:
        self.set(3, self.get(1) * self.get(2))
        self.i += 4
      elif op == 3:
        if inp is None: break
        self.set(1, inp)
        inp = None
        self.i += 2
      elif op == 4:
        self.output = self.get(1)
        self.i += 2
      elif op == 5:
        self.i = self.get(2) if self.get(1) != 0 else self.i + 3
      elif op == 6:
        self.i = self.get(2) if self.get(1) == 0 else self.i + 3
      elif op == 7:
        self.set(3, int(self.get(1) < self.get(2)))
        self.i += 4
      elif op == 8:
        self.set(3, int(self.get(1) == self.get(2)))
        self.i += 4

baseProgram = [int(x) for x in sys.stdin.readline().split(',')]

def getSignal(amplifiers):
  signal = 0
  while not amplifiers[-1].end:
    for amplifier in amplifiers:
      amplifier.run(signal)
      signal = amplifier.output
  return signal

def getMaxSignal(phaseSequences):
  maxSignal = 0
  for phaseSequence in itertools.permutations(phaseSequences):
    amplifiers = [Amplifier(baseProgram, phase) for phase in phaseSequence]
    maxSignal = max(maxSignal, getSignal(amplifiers))
  return maxSignal

print(getMaxSignal([0, 1, 2, 3, 4]))
print(getMaxSignal([5, 6, 7, 8, 9]))