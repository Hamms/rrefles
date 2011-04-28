from variable import *
from fraction import *
from row import *

class Matrix:
  def __init__(self,rows):
    self.rows = []
    for x in rows:
      list = []
      for y in x:
        if isinstance(y,str):
          try:
            y = int(y)
          except:
            y = Variable(y)
        if isinstance(y,int):
          y = Fraction(y)
        list.append(y)
      self.rows.append(Row(list))

  def findPivot(self,start_row = 0):
    for x in range(len(self.rows[0])):
      for y in range(len(self.rows)):
        if y>=start_row and not self.rows[y][x] == 0 and not isinstance(self.rows[y][x],Variable):
          return (y,x)
    return (None,None)

  def transpose(self):
    that = []
    for j in range(len(self[0])):
      row = []
      for i in range(len(self)):
        row.append(self[i][j])
      that.append(row)
    return Matrix(that)

  def swap(self,one,two):
    if not one == two:
      self.rows[one], self.rows[two] = copy.copy(self.rows[two]),copy.copy(self.rows[one])

  def set(self,index,row):
    self.rows[index] = row

  def row(self,index):
    return self.rows[index]

  def cdot(self,other):
    sum = Fraction(0)
    for i in range(len(self)):
      sum += self[i][0] * other[i][0]
    return sum

  def __len__(self):
    return len(self.rows)

  def __getitem__(self,index):
    return self.rows[index]

  def __div__(self,other):
    if isinstance(other,int) or isinstance(other,Fraction):
      return self * (1/other)
    else:
      TypeError("cannot divide a Matrix by a " + type(other))
  def __mul__(self,other):
    if isinstance(other,int) or isinstance(other,Fraction):
      this = []
      for i in range(len(self)):
        row = []
        for j in range(len(self[i])):
          row.append(self[i][j] * other)
        this.append(row)
      return Matrix(this)
    elif isinstance(other,Matrix):
      if len(self[0]) == len(other):
        this = []
        for i in range(len(self)):
          row = []
          for j in range(len(other[0])):
            val = Fraction(0)
            for x in range(len(other)):
              val += self[i][x] * other[x][j]
            row.append(val)
          this.append(row)
        return Matrix(this)
      else:
        TypeError("cannot multiply a " + str(len(self)) + "x" + str(len(self[0])) + "matrix by a " + str(len(other)) + str(len(other[0])) + "matrix")
    else:
      TypeError("cannot multiply a Matrix and a " + str(type(other)))
  
  def __add__(self,other):
    this = []
    for i in range(len(self)):
      row = []
      for j in range(len(self[i])):
        try:
          row.append( self[i][j] + other[i][j] )
        except:
          TypeError("cannot add a " + str(len(self)) + "x" + str(len(self[0])) + "matrix and a " + str(len(other)) + str(len(other[0])) + "matrix")
      this.append(row)
    return Matrix(this)

  def __sub__(self,other):
    return self + (other*-1)

  def toString(self,options={}):
    for opt in ["nobar","compact"]:
      if opt not in options:
        options[opt] = True
    ret = "\left[ \\begin{array}{"
    for _ in range(len(self.rows[0])-1):
      ret += "r "
    if not options['nobar']:
      ret += "| "
    ret += "r}"
    if not options['compact']:
      ret += "\n"
    for r in self.rows:
      ret += str(r) + " \\\\"
      if not options['compact']:
        ret += "\n"
    ret += "\end{array} \\right]"
    return ret

  def __str__(self):
    return self.toString({'nobar':False,'compact':False})
    

