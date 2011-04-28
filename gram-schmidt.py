#! /usr/bin/python
import sys
import copy
from matrix import Matrix
from math import sqrt

def gramschmidt(basis):
  ret = "\\begin{align*}\n"
  orthogonalbasis = []
  for i,x in enumerate(basis):
    ret += "  v_" + str(i+1) + " &= x_" + str(i+1)
    v = copy.copy(x)
    for j in range(len(orthogonalbasis)):
      v1 = "v_"+str(j+1)
      ret += " - \\frac{x_"+str(i+1)+"\cdot "+v1+"}{"+v1+"\cdot "+v1+"}"+v1
      v2 = orthogonalbasis[j]
      proj = x.cdot(v2) / v2.cdot(v2)
      v -= v2 * proj
    orthogonalbasis.append(v)
    ret += " = " + v.toString({'nobar':True,'compact':True}) + " \\\\\n"
  ret += "\\end{align*}\n"
  ret += "$\left\{" + ",".join(x.toString({'nobar':True,'compact':True}) for x in orthogonalbasis) + "\\right\}$ is therefore an orthogonal basis for $W$"

  ret += ", so \n\\begin{align*}\n"
  ret += "\\left\{" + ",".join("u_{"+str(i+1)+"}" for i in range(len(orthogonalbasis))) + "\\right\} \n"
  ret += "&= \\left\{" + ",".join("\\frac{1}{\|v_{"+str(i+1)+"}\|}v_{"+str(i+1)+"}" for i in range(len(orthogonalbasis))) + "\\right\} \\\\\n"
  ret += "&= \\left\{" + ",".join("\\frac{1}{\\sqrt{"+ str(v.cdot(v)) +"}}" + v.toString({'nobar':True,'compact':True}) for v in orthogonalbasis) + "\\right\} \\\\\n"
  ret += "&= \\left\{\\right\}\n"
  ret += "\\end{align*} is an orthonormal basis."
  return ret

if __name__ == "__main__":
  r = input()
  basis = []
  for i in range(r):
    basis.append(Matrix([ [x] for x in raw_input().split()]))

  print gramschmidt(basis)
