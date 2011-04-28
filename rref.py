#! /usr/bin/python
import sys
import copy
from matrix import Matrix

def solve(matrix,options):
  print "\\begin{align*}"
  print matrix

  # First, find the pivot
  row = 0;
  x,y = matrix.findPivot(row)
  while(row < len(matrix) and not (x==None and y==None)):
    matrix.swap(x,row)
    print "% Found pivot at (",x,",",y,")."
    if (x==row):
      print "% no need to swap" 
    else:
      print "% Swapping rows",x,"and",row 
      print "&\\sim",matrix,"\\\\"

    if (matrix[row][y].inverse() == 1):
      print "% no need to scale"
    else:
      print "% Scaling row",row,"by",matrix[row][y].inverse()
      matrix.row(row).scale(matrix[row][y].inverse())
      print "&\\sim",matrix,"\\\\"

    print "% Reducing other rows"
    for i in range(row+1,len(matrix)):
      matrix.row(i).reduce(matrix.row(row).scaled(matrix[i][y]))
      print "%",i
    print "&\\sim",matrix,"\\\\"
    row += 1
    x,y = matrix.findPivot(row)

  # Now that we're in REF, Reduce!
  row = 1
  x,y = matrix.findPivot(row)
  while(row < len(matrix) and not (x==None and y==None)):
    print "% Pivot at",x,",",y
    for i in range(x,0,-1):
      print "%",i-1
      matrix.row(i-1).reduce(matrix.row(x).scaled(matrix[i-1][y]))
    print "&\\sim",matrix,"\\\\"
    row += 1
    x,y = matrix.findPivot(row)

  print "\\end{align*}"
  return

def usage():
  print """DO IT RIGHT"""

if __name__ == "__main__":
  import getopt
  try:                                
    opts, args = getopt.getopt(sys.argv[1:], "r:v", ["rows=","verbose"]) 
  except getopt.GetoptError:           
    usage()                          
    sys.exit(2)

  r = 0
  options = {};

  for opt,arg in opts:
    if opt in ("-r","--rows"):
      r = int(arg)
    if opt in ("-v","--verbose"):
      options['verbose'] = True

  if r == 0:
    r = input()

  matrix = []
  for i in range( r ):
    matrix.append(raw_input().split())

  solve(Matrix(matrix),options)
