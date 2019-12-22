import sys

baseInp = [int(x) for x in sys.stdin.readline().strip()]
pattern = [0, 1, 0, -1]

def fft(inp, n):
  total = 0
  i = n - 1
  while i < len(inp):
    p = pattern[(i + 1) // n % 4]
    if p != 0:
      for x in range(n):
        total += inp[i] * p
        i += 1
        if i >= len(inp): break
    else:
      i += n
  return abs(total) % 10

phases = 100
inp = baseInp

for phase in range(phases):
  nextInp = []
  for i in range(len(inp)):
    nextInp.append(fft(inp, i + 1))
  inp = nextInp

for x in inp[:8]: print(x, end='')
print()

inp = baseInp * 10000
offset = int(''.join([str(x) for x in inp[:7]]).lstrip('0'))

inp = reversed(inp[offset:])

for phase in range(phases):
  nextInp = []
  total = 0
  for x in inp:
    total += x
    nextInp.append(total % 10)
  inp = nextInp

for x in reversed(inp[-8:]): print(x, end='')
