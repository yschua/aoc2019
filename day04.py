count = 0

for i in range(387638, 919123):
  s = [int(x) for x in str(i)]
  if sorted(s) == s and 2 in dict( (x, s.count(x)) for x in set(s) ).values():
    count += 1

print(count)