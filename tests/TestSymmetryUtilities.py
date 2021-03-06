##############################################################################
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

"""Unit tests for SymmetryUtilities.py
"""

# version
__id__ = '$Id: TestSymmetryUtilities.py 2896 2009-03-16 05:45:06Z juhas $'

import os
import sys
import unittest

import numpy
from danse.ins.matter.SpaceGroups import GetSpaceGroup
from danse.ins.matter.SymmetryUtilities import *
from danse.ins.matter.SymmetryUtilities import _Position2Tuple

# useful variables
thisfile = locals().get('__file__', 'TestSymmetryUtilities.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
testdata_dir = os.path.join(tests_dir, 'testdata')

##############################################################################
class TestRoutines(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_isSpaceGroupLatPar(self):
        """check isSpaceGroupLatPar()
        """
        triclinic = GetSpaceGroup("P1")
        monoclinic = GetSpaceGroup("P2")
        orthorhombic = GetSpaceGroup("P222")
        tetragonal = GetSpaceGroup("P4")
        trigonal = GetSpaceGroup("P3")
        hexagonal = GetSpaceGroup("P6")
        cubic = GetSpaceGroup("P23")
        self.failUnless(isSpaceGroupLatPar(triclinic, 1, 2, 3, 40, 50, 60))
        self.failIf(isSpaceGroupLatPar(monoclinic, 1, 2, 3, 40, 50, 60))
        self.failUnless(isSpaceGroupLatPar(monoclinic, 1, 2, 3, 90, 50, 90))
        self.failIf(isSpaceGroupLatPar(orthorhombic, 1, 2, 3, 90, 50, 90))
        self.failUnless(isSpaceGroupLatPar(orthorhombic, 1, 2, 3, 90, 90, 90))
        self.failIf(isSpaceGroupLatPar(tetragonal, 1, 2, 3, 90, 90, 90))
        self.failUnless(isSpaceGroupLatPar(tetragonal, 2, 2, 3, 90, 90, 90))
        self.failIf(isSpaceGroupLatPar(trigonal, 2, 2, 3, 90, 90, 90))
        self.failUnless(isSpaceGroupLatPar(trigonal, 2, 2, 2, 80, 80, 80))
        self.failIf(isSpaceGroupLatPar(hexagonal, 2, 2, 2, 80, 80, 80))
        self.failUnless(isSpaceGroupLatPar(hexagonal, 2, 2, 3, 90, 90, 120))
        self.failIf(isSpaceGroupLatPar(cubic, 2, 2, 3, 90, 90, 120))
        self.failUnless(isSpaceGroupLatPar(cubic, 3, 3, 3, 90, 90, 90))
        return

    def test_expandPosition(self):
        """check expandPosition()
        """
        # ok again Ni example
        fcc = GetSpaceGroup(225)
        pos,pops,pmult = expandPosition(fcc, [0,0,0])
        self.failUnless(numpy.all(pos[0] == 0.0))
        self.assertEqual(4, len(pos))
        self.assertEqual(192, sum([len(l) for l in pops]))
        self.assertEqual(4, pmult)
        return

    def test_pruneFormulaDictionary(self):
        """check pruneFormulaDictionary()
        """
        fmdict = {"x" : "3*y-0.17", "y" : '0', "z" : "0.13"}
        pruned = pruneFormulaDictionary(fmdict)
        self.assertEqual({"x" : "3*y-0.17"}, pruned)
        return

    def test_isconstantFormula(self):
        """check isconstantFormula()
        """
        self.failIf(isconstantFormula('x-y+z'))
        self.failUnless(isconstantFormula('6.023e23'))
        self.failUnless(isconstantFormula('22/7'))
        self.failUnless(isconstantFormula('- 22/7'))
        self.failUnless(isconstantFormula('+13/ 9'))
        return

# End of class TestRoutines

##############################################################################
class Test_Position2Tuple(unittest.TestCase):

    def setUp(self):
        self.eps = 1.0e-4
        self.pos2tuple = _Position2Tuple(self.eps)
        return

    def tearDown(self):
        del self.pos2tuple
        return

    def test___init__(self):
        """check _Position2Tuple.__init__()
        """
        self.assertNotEqual(0.0, self.pos2tuple.eps)
        self.pos2tuple = _Position2Tuple(1.0/sys.maxint/2)
        self.assertEqual(0.0, self.pos2tuple.eps)
        return

    def test___call__(self):
        """check _Position2Tuple.__call__()
        """
        pos2tuple = self.pos2tuple
        positions = numpy.zeros((100,3), dtype=float)
        positions[:,0] = numpy.arange(100)/100.0*pos2tuple.eps + 0.1
        positions = positions - numpy.floor(positions)
        # pos2tuple should generate at most 2 distinct tuples
        alltuples = dict.fromkeys([pos2tuple(xyz) for xyz in positions])
        self.failIf(len(alltuples) > 2)
        return

# End of class Test_Position2Tuple

##############################################################################
class TestGeneratorSite(unittest.TestCase):

    generators = {}

    def setUp(self):
        x, y, z = 0.07, 0.11, 0.13
        self.x, self.y, self.z = x, y, z
        if TestGeneratorSite.generators:
            self.__dict__.update(TestGeneratorSite.generators)
            return
        sg117 = GetSpaceGroup(117)
        sg143 = GetSpaceGroup(143)
        sg164 = GetSpaceGroup(164)
        sg227 = GetSpaceGroup(227)
        g117c = GeneratorSite(sg117, [0, 0.5, 0])
        g117h = GeneratorSite(sg117, [x, x+0.5, 0.5])
        g143a = GeneratorSite(sg143, [0, 0, z])
        g143b = GeneratorSite(sg143, [1./3, 2./3, z])
        g143c = GeneratorSite(sg143, [2./3, 1./3, z])
        g143d = GeneratorSite(sg143, [x, y, z])
        g164e = GeneratorSite(sg164, (0.5, 0, 0))
        g164f = GeneratorSite(sg164, (0.5, 0, 0.5))
        g164g = GeneratorSite(sg164, (x, 0, 0))
        g164h = GeneratorSite(sg164, (x, 0, 0.5))
        g227a = GeneratorSite(sg227, [0, 0, 0])
        g227c = GeneratorSite(sg227, 3*[1./8])
        g227oa = GeneratorSite(sg227, 3*[1./8], sgoffset=3*[1./8])
        g227oc = GeneratorSite(sg227, [0, 0, 0], sgoffset=3*[1./8])
        TestGeneratorSite.generators = {
                'g117c' : g117c,  'g117h' : g117h,
                'g143a' : g143a,  'g143b' : g143b,
                'g143c' : g143c,  'g143d' : g143d,
                'g164e' : g164e,  'g164f' : g164f,
                'g164g' : g164g,  'g164h' : g164h,
                'g227a' : g227a,  'g227c' : g227c,
                'g227oa' : g227oa,  'g227oc' : g227oc
        }
        self.__dict__.update(TestGeneratorSite.generators)
        return

    def tearDown(self):
        return

    def test___init__(self):
        """check GeneratorSite.__init__()
        """
        # check multiplicities
        self.assertEqual(2,  self.g117c.multiplicity)
        self.assertEqual(4,  self.g117h.multiplicity)
        self.assertEqual(1,  self.g143a.multiplicity)
        self.assertEqual(1,  self.g143b.multiplicity)
        self.assertEqual(1,  self.g143c.multiplicity)
        self.assertEqual(3,  self.g143d.multiplicity)
        self.assertEqual(3,  self.g164e.multiplicity)
        self.assertEqual(3,  self.g164f.multiplicity)
        self.assertEqual(6,  self.g164g.multiplicity)
        self.assertEqual(6,  self.g164h.multiplicity)
        self.assertEqual(8,  self.g227a.multiplicity)
        self.assertEqual(16, self.g227c.multiplicity)
        self.assertEqual(8,  self.g227oa.multiplicity)
        self.assertEqual(16, self.g227oc.multiplicity)
        return

    def test_positionFormula(self):
        """check GeneratorSite.positionFormula()
        """
        import re
        # 117c
        self.assertEqual([], self.g117c.pparameters)
        self.assertEqual([("x", self.x)], self.g117h.pparameters)
        # 143c
        pfm143c = self.g143c.positionFormula(self.g143c.xyz)
        places = 12
        self.assertEqual("+2/3", pfm143c["x"])
        self.assertEqual("+1/3", pfm143c["y"])
        self.assertEqual("z", pfm143c["z"])
        # 143d
        x, y, z = self.x, self.y, self.z
        pfm143d = self.g143d.positionFormula([-x+y, -x, z])
        self.assertEqual("-x+y", pfm143d["x"].replace(' ',''))
        self.assertEqual("-x+1", pfm143d["y"].replace(' ',''))
        self.failUnless(re.match("[+]?z", pfm143d["z"].strip()))
        # 227a
        self.assertEqual([], self.g227a.pparameters)
        self.assertEqual([], self.g227oa.pparameters)
        # 227c
        self.assertEqual([], self.g227c.pparameters)
        self.assertEqual([], self.g227oc.pparameters)
        return

    def test_UFormula(self):
        """check GeneratorSite.UFormula()
        """
        # Ref: Willis and Pryor, Thermal Vibrations in Crystallography,
        # Cambridge University Press 1975, p. 104-110
        smbl = ('A', 'B', 'C', 'D', 'E', 'F')
        norule = { 'U11':'A', 'U22':'B', 'U33':'C',
                   'U12':'D', 'U13':'E', 'U23':'F' }
        rule05 = { 'U11':'A', 'U22':'A', 'U33':'C',
                   'U12':'D', 'U13':'0', 'U23':'0' }
        rule07 = { 'U11':'A', 'U22':'A', 'U33':'C',
                   'U12':'D', 'U13':'E', 'U23':'-E' }
        rule15 = { 'U11':'A', 'U22':'B', 'U33':'C',
                   'U12':'0.5*B', 'U13':'0.5*E', 'U23':'E' }
        rule16 = { 'U11':'A', 'U22':'A', 'U33':'C',
                   'U12':'0.5*A', 'U13':'0', 'U23':'0' }
        rule17 = { 'U11':'A', 'U22':'A', 'U33':'A',
                   'U12':'0', 'U13':'0', 'U23':'0' }
        rule18 = { 'U11':'A', 'U22':'A', 'U33':'A',
                   'U12':'D', 'U13':'D', 'U23':'D' }
        ufm = self.g117c.UFormula(self.g117c.xyz, smbl)
        self.assertEqual(rule05, ufm)
        ufm = self.g117h.UFormula(self.g117h.xyz, smbl)
        self.assertEqual(rule07, ufm)
        ufm = self.g143a.UFormula(self.g143a.xyz, smbl)
        self.assertEqual(rule16, ufm)
        ufm = self.g143b.UFormula(self.g143b.xyz, smbl)
        self.assertEqual(rule16, ufm)
        ufm = self.g143c.UFormula(self.g143c.xyz, smbl)
        self.assertEqual(rule16, ufm)
        ufm = self.g143d.UFormula(self.g143d.xyz, smbl)
        self.assertEqual(norule, ufm)
        ufm = self.g164e.UFormula(self.g164e.xyz, smbl)
        self.assertEqual(rule15, ufm)
        ufm = self.g164f.UFormula(self.g164f.xyz, smbl)
        self.assertEqual(rule15, ufm)
        ufm = self.g164g.UFormula(self.g164g.xyz, smbl)
        self.assertEqual(rule15, ufm)
        ufm = self.g164h.UFormula(self.g164h.xyz, smbl)
        self.assertEqual(rule15, ufm)
        ufm = self.g227a.UFormula(self.g227a.xyz, smbl)
        self.assertEqual(rule17, ufm)
        ufm = self.g227c.UFormula(self.g227c.xyz, smbl)
        self.assertEqual(rule18, ufm)
        ufm = self.g227oa.UFormula(self.g227oa.xyz, smbl)
        self.assertEqual(rule17, ufm)
        ufm = self.g227oc.UFormula(self.g227oc.xyz, smbl)
        self.assertEqual(rule18, ufm)
        return

    def test__findUParameters(self):
        """check GeneratorSite._findUParameters()
        """
        # by default all Uparameters equal zero, this would fail for NaNs
        for gen in TestGeneratorSite.generators.values():
            for usym, uval in gen.Uparameters:
                self.assertEqual(0.0, uval)
        # special test for g117h
        Uij = numpy.array([[1, 3, 4], [3, 1, -4], [4, -4, 2]])
        sg117 = GetSpaceGroup(117)
        g117h = GeneratorSite(sg117, self.g117h.xyz, Uij)
        upd = dict(g117h.Uparameters)
        self.assertEqual(1, upd['U11'])
        self.assertEqual(2, upd['U33'])
        self.assertEqual(3, upd['U12'])
        self.assertEqual(4, upd['U13'])
        return

    def test_eqIndex(self):
        """check GeneratorSite.eqIndex()
        """
        self.assertEqual(13, self.g227oc.eqIndex(self.g227oc.eqxyz[13]))
        return

# End of class TestGeneratorSite

##############################################################################
class TestSymmetryConstraints(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test___init__(self):
        """check SymmetryConstraints.__init__()
        """
        sg225 = GetSpaceGroup(225)
        # initialize from nested lists and arrays from ExpandAsymmetricUnit
        eau = ExpandAsymmetricUnit(sg225, [[0, 0, 0]])
        sc0 = SymmetryConstraints(sg225, eau.expandedpos)
        self.assertEqual(1, len(sc0.coremap))
        # initialize from list of arrays of coordinates
        poslistarrays = [xyz for xyz in sc0.positions]
        sc1 = SymmetryConstraints(sg225, poslistarrays)
        self.assertEqual(1, len(sc1.coremap))
        # initialize from list of lists of coordinates
        poslistlist = [list(xyz) for xyz in poslistarrays]
        sc2 = SymmetryConstraints(sg225, poslistlist)
        self.assertEqual(1, len(sc2.coremap))
        # initialize from nx3 array
        posarray = numpy.array(poslistlist)
        sc3 = SymmetryConstraints(sg225, posarray)
        self.assertEqual(1, len(sc3.coremap))
        # finally initialize from a single coordinate
        sc4 = SymmetryConstraints(sg225, [0, 0, 0])
        self.assertEqual(1, len(sc4.coremap))
        return

    def test_corepos(self):
        """test_corepos - find positions in the asymmetric unit.
        """
        sg225 = GetSpaceGroup(225)
        corepos = [[0, 0, 0], [0.1, 0.13, 0.17]]
        eau = ExpandAsymmetricUnit(sg225, corepos)
        sc = SymmetryConstraints(sg225, eau.expandedpos)
        self.assertEqual(2, len(sc.corepos))
        self.failUnless(numpy.all(corepos[0] == sc.corepos[0]))
        self.failUnless(numpy.all(corepos[1] == sc.corepos[1]))
        self.assertEqual(2, len(sc.coremap))
        mapped_count = sum([len(idcs) for idcs in sc.coremap.values()])
        self.assertEqual(len(sc.positions), mapped_count)
        self.failUnless(sc.coremap[0] == range(4))
        self.failUnless(sc.coremap[4] == range(4, 4+192))
        return

#   def test__findConstraints(self):
#       """check SymmetryConstraints._findConstraints()
#       """
#       return
#
#   def test_posparSymbols(self):
#       """check SymmetryConstraints.posparSymbols()
#       """
#       return
#
#   def test_posparValues(self):
#       """check SymmetryConstraints.posparValues()
#       """
#       return
#
#   def test_positionFormulas(self):
#       """check SymmetryConstraints.positionFormulas()
#       """
#       return
#
#   def test_positionFormulasPruned(self):
#       """check SymmetryConstraints.positionFormulasPruned()
#       """
#       return
#
    def test_UparSymbols(self):
        """check SymmetryConstraints.UparSymbols()
        """
        sg1 = GetSpaceGroup(1)
        sg225 = GetSpaceGroup(225)
        pos = [[0, 0, 0]]
        Uijs = numpy.zeros((1, 3, 3))
        sc1 = SymmetryConstraints(sg1, pos, Uijs)
        self.assertEqual(6, len(sc1.UparSymbols()))
        sc225 = SymmetryConstraints(sg225, pos, Uijs)
        self.assertEqual(['U110'], sc225.UparSymbols())
        return

    def test_UparValues(self):
        """check SymmetryConstraints.UparValues()
        """
        places = 12
        sg1 = GetSpaceGroup(1)
        sg225 = GetSpaceGroup(225)
        pos = [[0, 0, 0]]
        Uijs = [[[0.1, 0.4, 0.5],
                 [0.4, 0.2, 0.6],
                 [0.5, 0.6, 0.3]]]
        sc1 = SymmetryConstraints(sg1, pos, Uijs)
        duv = 0.1 * numpy.arange(1, 7) - sc1.UparValues()
        self.assertAlmostEqual(0, max(numpy.fabs(duv)), places)
        sc225 = SymmetryConstraints(sg225, pos, Uijs)
        self.assertEqual(1, len(sc225.UparValues()))
        self.assertAlmostEqual(0.2, sc225.UparValues()[0], places)
        return

#   def test_UFormulas(self):
#       """check SymmetryConstraints.UFormulas()
#       """
#       return
#
#   def test_UFormulasPruned(self):
#       """check SymmetryConstraints.UFormulasPruned()
#       """
#       return

# End of class TestSymmetryConstraints

if __name__ == '__main__':
    unittest.main()

# End of file
