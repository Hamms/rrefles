import copy

def gcd(x,y):
  while(y!=0):
    x,y = y,x%y
  return x

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

  def __float__(self):
    return float(self.num)/float(self.den)
    
  def __copy__(self):
    return Fraction( self.num, self.den )

  def __deepcopy__(self,memo=None):
    return Fraction( copy.deepcopy(self.num), copy.deepcopy(self.den) )

