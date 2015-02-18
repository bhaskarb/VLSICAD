import unittest
import logging 

class Cube:
    def __init__(self, n):
        self.n = n
        self.prod = None
        self.logger = logging.getLogger("Cube")
        self.logger.debug("Cube Constructor: %d" %self.n)

    def SetVar(self, i, val):
        self.logger.debug("Cube: SetVar: %d, %d" %(i, val))
        assert i >= 0 and i < self.n
        assert val > 0 and val <=3 
        if self.prod == None:
            self.prod = [3]*self.n
        self.prod[i] = val

    def GetVar(self, i):
        assert i >= 0 and i < self.n
        return self.prod[i]

    def IsTrue(self):
        if(self.prod == None):
            return False
        for prod in self.prod:
            if (prod != 3):
                return False
        return True

    def IsFalse(self):
        return (self.prod == None)

    def CoFactor(self, idx, isPos):
        value = 2
        if isPos:
            value = 1
        if(self.prod[idx] != value and self.prod[idx] != 3):
            return None
        cube = Cube(self.n)
        cube.prod = []
        for i in range(self.n):
            if i != idx:
                cube.prod.append(self.prod[i])
            else:
                cube.prod.append(3)
        return cube

    def Print(self):
        if self.IsFalse():
            return "0"
        if self.IsTrue():
            return "1"
        val = ""
        for i in range(self.n):
            prod = self.prod[i]
            if prod == 1:
                val = val + "x" + str(i + 1)
            elif prod == 2:
                val = val + "x" + str(i + 1) +"'"
        return val

    def Report(self):
        if self.IsFalse():
            return "0"
        if self.IsTrue():
            return "1"
        val = ""
        ndc = 0
        for i in range(self.n):
            prod = self.prod[i]
            if prod == 1:
                val = val + " " + str(i + 1)
            elif prod == 2:
                val = val + " -" + str(i + 1) 
            elif prod == 3:
                ndc += 1
        val = str(self.n - ndc) + val + "\n"
        return val

class CubeTest(unittest.TestCase):
    def setUp(self):
        self.c0 = Cube(4)
        self.c1 = Cube(4)
        self.c1.SetVar(0, 3)
        self.c = Cube(6)
        self.c.SetVar(1, 1)
        self.c.SetVar(3, 1)
        self.c.SetVar(4, 2)

    def test_tautology(self):
        self.assertTrue(self.c1.IsTrue())
        self.assertFalse(self.c0.IsTrue())
        self.assertFalse(self.c.IsTrue())

    def test_false(self):
        self.assertFalse(self.c1.IsFalse())
        self.assertTrue(self.c0.IsFalse())
        self.assertFalse(self.c.IsFalse())

    def test_print(self):
        self.assertEqual(self.c.Print(), "x2x4x5'")

    def test_report(self):
        self.assertEqual(self.c.Report(), "3 2 4 -5\n")

if __name__ == "__main__":
    logger = logging.getLogger("Cube")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("debug.log")
    logger.addHandler(fh)

    unittest.main()
        
