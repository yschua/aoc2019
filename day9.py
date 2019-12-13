import sys

class IntcodeComputer:
  def __init__(self, program, inp):
    self.m = dict(zip(range(len(program)), program))
    self.i = 0
    self.end = False
    self.output = 0
    self.relBase = 0
    self.run(inp)

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

  def run(self, inp):
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
        self.output = self.get(1)
        print(self.output)
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

program = [int(x) for x in sys.stdin.readline().split(',')]
IntcodeComputer(program, 2)