# inp = [1,9,10,3,2,3,11,0,99,30,40,50]

def compute(noun, verb, memory):
  memory[1] = noun
  memory[2] = verb
  for i in range(0, len(memory), 4):
    opcode = memory[i]
    if opcode == 99:
      break
    elif opcode == 1:
      memory[memory[i+3]] = memory[memory[i+1]] + memory[memory[i+2]]
    elif opcode == 2:
      memory[memory[i+3]] = memory[memory[i+1]] * memory[memory[i+2]]
  return memory[0]

inp = [1,12,2,3,1,1,2,3,1,3,4,3,1,5,0,3,2,9,1,19,1,19,5,23,1,23,6,27,2,9,27,31,1,5,31,35,1,35,10,39,1,39,10,43,2,43,9,47,1,6,47,51,2,51,6,55,1,5,55,59,2,59,10,63,1,9,63,67,1,9,67,71,2,71,6,75,1,5,75,79,1,5,79,83,1,9,83,87,2,87,10,91,2,10,91,95,1,95,9,99,2,99,9,103,2,10,103,107,2,9,107,111,1,111,5,115,1,115,2,119,1,119,6,0,99,2,0,14,0]

for noun in range(0, 99):
  for verb in range(0, 99):
    if compute(noun, verb, inp.copy()) == 19690720:
      print(100 * noun + verb)
