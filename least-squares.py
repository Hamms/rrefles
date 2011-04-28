#! /usr/bin/python
from matrix import Matrix
from variable import Variable

def leastsquares(A,b):
  ret = "\\begin{align*}\n"
  Atrans = A.transpose()
  ret += "  A^TA &= " + Atrans.toString() + A.toString() + " = " + (Atrans*A).toString() + " \\\\\n"
  ret += "  A^Tb &= " + Atrans.toString() + b.toString() + " = " + (Atrans*b).toString() + " \\\\\n"
  ret += "\\end{align*}\n"
  ret += "Then the equation $A^TAx = A^Tb$ becomes $$" + (Atrans*A).toString()
  ret += Matrix([ [Variable("x_"+str(i+1))] for i in range(len(Atrans))]).toString()
  ret += "=" + (Atrans*b).toString() + "$$\n"
  ret += "Then to solve $A^TAx = A^Tb$ as \\begin{align*}\n"
  ret += "  \hat{x} \n  &= \left(A^TA\\right)^{-1}A^Tb \\\\\n"
  ret += "\\end{align*}"
  return ret

if __name__ == "__main__":

  A = []
  r = raw_input()
  while(r):
    A.append(r.split())
    r = raw_input()
  A = Matrix(A)

  b = Matrix( [ [x] for x in raw_input().split() ])

  print leastsquares(A,b)
