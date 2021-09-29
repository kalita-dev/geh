import os
os.system('pip install tqdm')
import numpy as np
from tqdm import tqdm
import itertools


def next_check(st, s):
  # print('check', st, s)
  if st not in new: 
    # print('not in')
    return False
  for i in new[st]:
    # print('in nef', i)
    if i in s: 
      # print('i in s')
      return True
    global ss
    ss.add(i)
    if next_check(i, s.union({i})): 
      return True

  return False

def get_ans():    
    cols = [0 for _ in range(ndots)]
    todo = set(range(ndots)).difference(new1.keys())
    todoc = { _: len(new1[_]) for _ in new1 }

    while True:
      curr = next(iter(todo))
      if curr in new1:
        mc = 0
        for i in new1[curr]:
          mc = max(cols[i], mc)
        cols[curr] = mc + 1
      else:
        cols[curr] = 0
      if curr in new:
        for i in new[curr]:
          todoc[i] -= 1
          if not todoc[i]: todo.add(i)
        
      todo.remove(curr)
      if not len(todo): break

    return len(np.unique(cols))

def check_cycles():
  global ss
  ss = set()
  for i in new:
    # print('init', i)
    if i in ss: continue
    # {0: {1, 2}, 3: {1}, 5: {1, 4, 7}, 4: {0}, 2: {3, 6}, 7: {3, 6}, 6: {4}}
    if next_check(i, {i}): return True
  return False



n = int(input('Enter n: '))
ndots = 2**n
if n > 4: 
  print('The number is too large, it will be calculating for a lifetime.')
  exit()

edges = []
for g in range(ndots):
  for s in range(n):
    new = g ^ (1 << s)
    # print(bin(g), bin(new))
    if new > g:
      edges.append((g,new))


# print(edges)
# print(len(edges))

numbers = set()
# print(bin(2**(len(edges))-1))
for mask in tqdm(range(2**(len(edges))), position=0, leave=True):
  # print('mask', bin(mask))
  new1 = [ edges[_] if ((1 << _) & mask) else ( (edges[_][1], edges[_][0]) ) for _ in range(len(edges)) ]
  new = {}
  for i in new1:
    if i[0] not in new: new[i[0]] = set()
    new[i[0]].add(i[1])

  new1 = None
  if check_cycles():
    continue
    print('mask', bin(mask))
    print(new)
  # print(new)

  new1 = new
  new = {}
  for i in new1:
    for j in new1[i]:
      if j not in new: new[j] = set()
      new[j].add(i)

  numbers.add(get_ans())
  # if len(numbers) == ndots-1: break


print('\nPossible number of colors:', numbers)
