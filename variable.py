import copy
from fraction import *

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


