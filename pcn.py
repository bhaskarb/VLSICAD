import cube
import unittest
import logging 

import sys 

class PCN:
    def __init__(self, nv = 0):
        self.nv = nv;
        self.pos = []

    def AddCube(self, cube):
        assert self.nv > 0
        self.pos.append(cube)

    def GetCube(self, i):
        assert i >= 0 and i < len(self.pos)
        val = self.pos[i]
        return val

    def IsTrue(self):
        for prod in self.pos:
            if prod.IsTrue():
                return True
        return False

    def IsFalse(self):
        if len(self.pos) == 0:
            return True;
        for prod in self.pos:
            if prod.IsFalse() == False:
                return False
        return True

    def Print(self):
        val = None 
        for prod in self.pos:
            if val == None:
                val = prod.Print()
            else:
                val = val + " + " + prod.Print()
        return val

    def Report(self, fname):
        with open(fname, "w") as wf:
            wf.write("%d\n" %self.nv)
            if(self.IsTrue()):
                wf.write("1\n0")
            elif self.IsFalse():
                wf.write("0\n")
            else:
                wf.write("%d\n" %len(self.pos))
                for prod in self.pos:
                    wf.write(prod.Report())

    def ReadFromFile(self,fname):
        with open(fname, "r") as rf:
            lines = rf.readlines()
        self.nv = int(lines[0])
        np = int(lines[1])
        logger.info("num Var = %d, num products = %s" %(self.nv, np))
        for i in range(np):
            line = lines[i + 2]
            val = str.split(line) 
            cu = cube.Cube(self.nv)
            for j in range(1, len(val)):
                i = int(val[j]) 
                value = 1
                if(i < 0):
                    value = 2
                    i = -i
                i = i - 1
                cu.SetVar(i, value)
            self.AddCube(cu)

def CoFactor(pcn, idx, isPos):
    cofactor = PCN(pcn.nv)
    for pos in pcn.pos:
        cofcube = pos.CoFactor(idx, isPos)
        if cofcube != None:
            cofactor.AddCube(cofcube)
    return cofactor

def ComplementSimplePCN(pcn):
    pcnnew = PCN(pcn.nv)
    cu = pcn.pos[0]
    for i in range(cu.n):
        val = cu.prod[i]
        if(val == 1):
            ncu = cube.Cube(pcn.nv)
            ncu.SetVar(i, 2)
            pcnnew.AddCube(ncu)
        elif(val == 2):
            ncu = cube.Cube(pcn.nv)
            ncu.SetVar(i, 1)
            pcnnew.AddCube(ncu)
    return pcnnew

def pcnIsSimple(pcn):
    if(pcn.IsTrue()):  #F=1, F'=0
        pcn0 = PCN()
        logger.debug("PCN is simple: %s, complement is %s" %(pcn.Print(), pcn0.Print()))
        return (True, pcn0) 
    if(pcn.IsFalse()): #F=0, F'=1
        pcn1 = PCN(pcn.nv)
        cu = cube.Cube(pcn.nv)
        cu.SetVar(1, 3)
        pcn1.AddCube(cu)
        logger.debug("PCN is simple: %s, complement is %s" %(pcn.Print(), pcn1.Print()))
        return (True, pcn1)
    if(len(pcn.pos) == 1): #F = xyz, F' = x' + y' + z'
        pcnnew = ComplementSimplePCN(pcn)
        logger.debug("PCN is simple: %s, complement is %s" %(pcn.Print(), pcnnew.Print()))
        return (True, pcnnew)
    return (False, None)

def compare_binate(x, y):
    if(x[1] == y[1]):
        if(x[2] == y[2]):
            return x[0] - y[0]
        return x[2] - y[2]
    return y[1] - x[1]

def compare_unate(x, y):
    if(x[1] == y[1]):
        return x[0] - y[0]
    return y[1] - x[1]

def findMostBinateVariable(pcn):
    truelist = [0]*pcn.nv
    falselist = [0]*pcn.nv
    onelist = [0]*pcn.nv
    for i in range(len(pcn.pos)):
        pos = pcn.pos[i]
        for j in range(len(pos.prod)):
            val = pos.prod[j]
            if(val == 1):
                truelist[j] += 1
            elif val == 2:
                falselist[j] += 1
    binate = []
    unate = []
    for i in range(pcn.nv):
        if(truelist[i] > 0 and falselist[i] > 0): #binate
            binate.append((i, truelist[i] + falselist[i], abs(truelist[i] - falselist[i])))
        elif((truelist[i] == 0  and falselist[i] > 0) or (falselist[i] == 0 and truelist[i] > 0)): #unate
            unate.append((i, truelist[i] + falselist[i]))
    logger.debug("Binate list: %s\n Unate List %s\n" %(str(binate), str(unate)))
    if len(binate) > 0:
        binate.sort(cmp=compare_binate)
        return binate[0][0]
    unate.sort(cmp=compare_unate)
    return unate[0][0]

def OrPCN(pcn1, pcn2):
    pcn = PCN()
    pcn.nv = max(pcn1.nv, pcn2.nv)
    for pos in pcn1.pos:
        pcn.pos.append(pos)
    for pos in pcn2.pos:
        pcn.pos.append(pos)
    return pcn

def AndVarPCN(pcn, idx, isPos):
    value = 2
    if isPos:
        value = 1
    for pos in pcn.pos:
        assert pos.GetVar(idx) == 3
        pos.SetVar(idx, value)
    return pcn


def ComplementURP(pcn):
    logger.debug("----Complementing %s" %pcn.Print())
    (simple, val) = pcnIsSimple(pcn)
    if simple == True:
        return val
    binate = findMostBinateVariable(pcn)
    logger.debug("Index selected for confactoring: x%d" %(binate + 1))
    poscofactor = CoFactor(pcn, binate, True)
    logger.debug("Positive Cofactor: %s" %(poscofactor.Print()))
    negcofactor = CoFactor(pcn, binate, False)
    logger.debug("Negative Cofactor: %s" %(negcofactor.Print()))
    pospcncomp = ComplementURP(poscofactor)
    logger.debug("F(x)': %s" %(pospcncomp.Print()))
    negpcncomp = ComplementURP(negcofactor)
    logger.debug("F(x')': %s" %(negpcncomp.Print()))
    xpospcn = AndVarPCN(pospcncomp, binate, True)
    logger.debug("xF(x)': %s" %(xpospcn.Print()))
    xpnegpcn = AndVarPCN(negpcncomp, binate, False)
    logger.debug("x'F(x')': %s" %(xpnegpcn.Print()))
    orpcn = OrPCN(xpospcn, xpnegpcn)
    logger.debug("----F': %s" %orpcn.Print())
    return orpcn

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        print "Usage python pcn.py filename"
        sys.exit(1)
    fname = sys.argv[1]
    logger = logging.getLogger("PCN URP Complement")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("debug.log")
    logger.addHandler(fh)

    pcn = PCN();
    pcn.ReadFromFile(fname)
    print pcn.Print()
    outname = fname + ".orig"
    pcn.Report(outname)
    comppcn = ComplementURP(pcn)
    print comppcn.Print()
    newname = fname.replace(".pcn", "_comp.pcn")
    comppcn.Report(newname)
