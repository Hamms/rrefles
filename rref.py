#! /usr/bin/python
import sys
import copy

class Fraction:
  def __init__(self,num,den=1):
    g = gcd(int(num),int(den))
    g = 1 if g==0 else g
    self.num = int(num)/g
    self.den = int(den)/g

  def inverse(self):
    if self.num == 0:
      return Fraction(0,1)
    else:
      return Fraction(self.den,self.num)

  def invert(self):
    if not self.num == 0:
      self.num, self.den = self.den, self.num

  def __eq__(self,other):
    if isinstance(other,int):
      return self.den == 1 and self.num == other
    else:
      return (self.num == other.num and self.den == other.den)

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    if (self.den == 1):
      return str(self.num)
    else:
      return "\\frac{"+str(self.num)+"}{"+str(self.den)+"}"

  def __add__(self,other):
    if isinstance(other,int):
      return Fraction( self.num + other*self.den, self.den )
    else:
      return Fraction( (self.num*other.den + other.num*self.den), self.den*other.den ) 

  def __sub__(self,other):
    return self.__add__( other*-1 )
    #return Fraction( (self.num*other.den - other.num*self.den), self.den*other.den ) 

  def __mul__(self,other):
    if isinstance(other,int):
      return Fraction( self.num * other, self.den )
    else:
      return Fraction( self.num*other.num, self.den*other.den )

  def __div__(self,other):
    if isinstance(other,int):
      return self.__mul__(Fraction(1,other))
    else:
      return self.__mul__(other.inverse())

  def __cmp__(self,other):
    if (isinstance(other,int)):
      other = Fraction(other)
    if ( self.num*other.den < other.num*self.den ):
      return -1
    elif ( self.num*other.den > other.num*self.den ):
      return 1
    else:
      return 0
    
  def __copy__(self):
    return Fraction( self.num, self.den )

  def __deepcopy__(self,memo=None):
    return Fraction( copy.deepcopy(self.num), copy.deepcopy(self.den) )

class Variable:
  def __init__(self,vars,scalars=[1]):
    if isinstance(vars,Variable):
      self.vars = copy.deepcopy(vars.vars)
    else:
      if isinstance(vars,str):
        vars = [vars]
      if isinstance(scalars,int):
        scalars = [scalars]

      self.vars = {}
      for s,v in zip(scalars,vars):
        self.vars[v] = Fraction(s)

  def __copy__(self):
    print "COPYING",self
    ret = Variable(copy.copy(self.vars.keys()), copy.copy(self.vars.values()))
    print "RESULT IS",ret
    return ret

  def __deepcopy(self):
    print "DEEPCOPYING",self
    ret = Variable(copy.deepcopy(self.vars.keys()), copy.deepcopy(self.vars.values()))
    print "RESULT IS",ret
    return ret
      
  def __add__(self,other):
    ret = Variable(self)
    for var in other.vars.keys():
      if var in ret.vars.keys():
        ret.vars[var] += other.vars[var]
      else:
        ret.vars[var] = other.vars[var]
    return ret
      
  def __sub__(self,other):
    ret = Variable(self)
    for var in other.vars.keys():
      if var in ret.vars.keys():
        ret.vars[var] -= other.vars[var]
      else:
        ret.vars[var] = other.vars[var]
    return ret

  def __mul__(self,other):
    ret = Variable(self)
    for v in ret.vars.keys():
      ret.vars[v] *= other
    return ret

  def __div__(self,other):
    ret = Variable(self)
    for var in ret.vars.values():
      var /= other
    return ret

  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    for v in self.vars.keys():
      if self.vars[v] == 0:
        del self.vars[v]

    if self.vars[self.vars.keys()[0]] == 1:
      ret = self.vars.keys()[0]
    else:
      ret = str(self.vars[self.vars.keys()[0]]) + self.vars.keys()[0]

    for v in self.vars.keys()[1:]:
      if (self.vars[v] == 1):
        ret += "+" + v
      else:
        ret += "+" + str(self.vars[v]) + v
    return ret

class Row:
  def __init__(self,list):
    self.list = copy.deepcopy(list)

  def toList(self):
    return copy.deepcopy(self.list)

  def scale(self,const):
    self.list = [x*const for x in self.list]

  def scaled(self,const):
    return Row([x*const for x in self.list])

  def reduce(self,other):
    for i in range(len(self.list)):
      self.list[i] -= other.list[i]

  def __str__(self):
    ret = ""
    for x in self.list[:-1]:
      ret += str(x) + " & "
    ret += str(self.list[-1])
    return ret

  def __add__(self,other):
    if isinstance(other,list):
      l = other
    else:
      l = other.list
    ret = []
    for x,y in zip(self.list,l):
      ret.append(x+y)
    return ret

  def __sub__(self,other):
    return self.__add__(other.scaled(-1))

  def __len__(self):
    return len(self.list)

  def __getitem__(self,index):
    return self.list[index]

  def __copy__(self):
    return Row(copy.copy(self.list))

  def __deepcopy(self):
    return Row(copy.deepcopy(self.list))

class Matrix:
  def __init__(self,rows):
    self.rows = []
    for x in rows:
      list = []
      for y in x:
        try:
          list.append(Fraction(int(y)))
        except:
          list.append(Variable(y))
      self.rows.append(Row(list))

  def findPivot(self,start_row = 0):
    for x in range(len(self.rows[0])):
      for y in range(len(self.rows)):
        if y>=start_row and not self.rows[y][x] == 0 and not isinstance(self.rows[y][x],Variable):
          return (y,x)
    return (None,None)

  def swap(self,one,two):
    if not one == two:
      self.rows[one], self.rows[two] = copy.copy(self.rows[two]),copy.copy(self.rows[one])

  def set(self,index,row):
    self.rows[index] = row

  def row(self,index):
    return self.rows[index]

  def __len__(self):
    return len(self.rows)

  def __getitem__(self,index):
    return self.rows[index]

  def __str__(self):
    ret = "\left( \\begin{array}{"
    for _ in range(len(self.rows[0])-1):
      ret += "c "
      #TODO: add option for '|'
    ret = ret + "| c}\n"
    for r in self.rows:
      ret += str(r) + " \\\\\n"
    ret += "\end{array} \\right)"
    return ret
    
def gcd(x,y):
  while(y!=0):
    x,y = y,x%y
  return x

def solve(matrix):
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
      print "&\\rightarrow",matrix,"\\\\"

    if (matrix[row][y].inverse() == 1):
      print "% no need to scale"
    else:
      print "% Scaling row",row,"by",matrix[row][y].inverse()
      matrix.row(row).scale(matrix[row][y].inverse())
      print "&\\rightarrow",matrix,"\\\\"

    print "% Reducing other rows"
    for i in range(row+1,len(matrix)):
      matrix.row(i).reduce(matrix.row(row).scaled(matrix[i][y]))
      print "%",i
    print "&\\rightarrow",matrix,"\\\\"
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
    print "&\\rightarrow",matrix,"\\\\"
    row += 1
    x,y = matrix.findPivot(row)

  print "\\end{align*}"
  return

def usage():
  print """DO IT RIGHT"""

if __name__ == "__main__":
  import getopt
  try:                                
    opts, args = getopt.getopt(sys.argv[1:], "r:", ["rows="]) 
  except getopt.GetoptError:           
    usage()                          
    sys.exit(2)

  r = 0

  for opt,arg in opts:
    if opt in ("-r","--rows"):
      r = int(arg)

  if r == 0:
    r = input()

  matrix = []
  for i in range( r ):
    matrix.append(raw_input().split())

  solve(Matrix(matrix))
