import copy

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

