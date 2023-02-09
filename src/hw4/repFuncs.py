from helpers import *
from pretty import pretty
from dataClass import DATA
import copy

# I had to move these to their own file because of circular dependencies

def repCols(cols):
  # Combines the columns titles of the input file and reformats them
  cols = copy.deepcopy(cols)
  for i in range(len(cols)):
    col = cols[i]
    col[len(col) - 1] = str(col[0]) + ":" + str(col[len(col) - 1])
    for j in range(1, len(col)):
      col[j-1] = col[j]
    col.pop(len(col) - 1)
  cols = insert(cols, kap(cols[0], lambda k,v: ("Num" + str(k), None)))
  cols[0][len(cols[0]) - 1] = "thingX"
  return DATA(cols)

def repRows(t, rows):
  # Adds the row descriptions to their place based on the input file
  rows = copy.deepcopy(rows)
  for j, s in last(rows).items():
    rows[0][j] = str(rows[0][j]) + ":" + str(s)
  rows.pop(len(rows) - 1)
  for n in range(len(rows)):
    row = rows[n]
    if n == 0:
      row[len(row)] = "thingX"
    else:
      u = t["rows"][(len(t["rows"]) - 1) - n + 1]
      row[len(row)] = last(u)
  return DATA(rows)

def repPlace(data):
  # Makes and displays the grid
  n = 20
  g = {}

  for i in range(n + 1):
    g[i] = {}
    for j in range(n + 1):
      g[i][j] = " "
  maxy = 0
  print("")
  for r, row in data.rows.items():
    c = chr(65 + r)
    print(c, last(row.cells))
    x = int(row.x * n)
    y = int(row.y * n)
    maxy = max(maxy, y + 1)
    g[y][x] = c
  print("")
  for y in range(maxy):
    pretty(g[y])

def repgrid(sFile):
  # Does everything tested above
  t = dofile(sFile)
  rows = repRows(t, transpose(t["cols"]))
  cols = repCols(t["cols"])
  show(rows.cluster())
  show(cols.cluster())
  repPlace(rows)


