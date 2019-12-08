import sys

image = sys.stdin.readline().strip()
width = 25
height = 6
size = width * height
goodLayer = None
lowestZero = 0
layers = []

for i in range(0, len(image), size):
  layer = [int(x) for x in image[i:i+size]]
  layers.append(layer)
  zero = layer.count(0)
  if goodLayer is None or zero < lowestZero:
    goodLayer = layer
    lowestZero = zero

print(goodLayer.count(1) * goodLayer.count(2))

decoded = ""

def getPixel(i):
  for layer in layers:
    if layer[i] != 2:
      return layer[i]

for i in range(0, size):
  if i % width == 0: decoded += '\n'
  decoded += 'O' if getPixel(i) else ' '

print(decoded)