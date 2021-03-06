##############################################################################
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
##############################################################################

"""Unit tests for Structure.Parsers module.
"""

__id__ = "$Id: TestParsers.py 2825 2009-03-09 04:33:12Z juhas $"

import unittest
import os
import re

from danse.ins.matter import Structure, StructureFormatError
from danse.ins.matter import Lattice
from danse.ins.matter import Atom

# useful variables
thisfile = locals().get('__file__', 'TestParsers.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
testdata_dir = os.path.join(tests_dir, 'testdata')

def datafile(filename):
    """prepend testdata_dir to filename
    """
    return os.path.join(testdata_dir, filename)

def assertListAlmostEqual(self, l1, l2, places=None):
    """wrapper for list comparison"""
    if places is None: places = self.places
    self.assertEqual(len(l1), len(l2))
    for i in range(len(l1)):
        self.assertAlmostEqual(l1[i], l2[i], places)

##############################################################################
class TestP_xyz(unittest.TestCase):
    """test Parser for xyz file format"""

    def setUp(self):
        self.stru = Structure()
        self.format = 'xyz'
        import tempfile
        handle, self.tmpname = tempfile.mkstemp()
        os.close(handle)

    def tearDown(self):
        import os
        os.remove(self.tmpname)

    def test_read_xyz_si(self):
        """check reading of normal xyz file"""
        stru = self.stru
        #stru.read(datafile('bucky.xyz'), self.format)
        stru.read(datafile('si64.init.xyz'), self.format)
        print stru.lattice
        s_els = [a.symbol for a in stru]
        #self.assertEqual(stru.description, 'bucky-ball')
        #self.assertEqual(s_els, 60*['C'])

    def test_read_xyz(self):
        """check reading of normal xyz file"""
        stru = self.stru
        stru.read(datafile('bucky.xyz'), self.format)
        s_els = [a.symbol for a in stru]
        self.assertEqual(stru.description, 'bucky-ball')
        self.assertEqual(s_els, 60*['C'])

    def test_read_xyz_bad(self):
        """check exceptions when reading invalid xyz file"""
        stru = self.stru
        self.assertRaises(StructureFormatError, stru.read,
                datafile('bucky-bad1.xyz'), self.format )
        self.assertRaises(StructureFormatError, stru.read,
                datafile('bucky-bad2.xyz'), self.format )
        self.assertRaises(StructureFormatError, stru.read,
                datafile('bucky-plain.xyz'), self.format )
        self.assertRaises(StructureFormatError, stru.read,
                datafile('hexagon-raw.xy'), self.format )

    def test_writeStr_xyz(self):
        """check string representation of normal xyz file"""
        stru = self.stru
        stru.description = "test of writeStr"
        stru.lattice = Lattice(1.0, 2.0, 3.0, 90.0, 90.0, 90.0)
        stru[:] = [
            Atom('H', [1., 1., 1.]),
            Atom('Cl', [3., 2., 1.])
        ]
        s1 = stru.writeStr(self.format)
        s1 = re.sub('[ \t]+', ' ', s1)
        s0 = "2\n%s\nH 1 2 3\nCl 3 4 3\n" % stru.description
        self.assertEqual(s1, s0)
        
    def test_writeStr_xyz_Supercell(self):
        at1 = Atom('Al', [0.0, 0.0, 0.0])
        at2 = Atom('Al', [0.0, 0.5, 0.5])
        at3 = Atom('Al', [0.5, 0.0, 0.5])
        at4 = Atom('Al', [0.5, 0.5, 0.0])
        self.stru4 = Structure( [ at1, at2, at3, at4], 
                        lattice=Lattice(4.05, 4.05, 4.05, 90, 90, 90),
                        sgid = 225 )
        from danse.ins.matter.expansion import supercell
        al_333 = supercell(self.stru4, (3, 3, 3))
        s1 = al_333.writeStr(self.format)
        #print s1
#        s1 = re.sub('[ \t]+', ' ', s1)
#        s0 = "2\n%s\nH 1 2 3\nCl 3 4 3\n" % stru.description
#        self.assertEqual(s1, s0)

    def test_write_xyz(self):
        """check writing of normal xyz file"""
        stru = self.stru
        stru.description = "test of writeStr"
        stru.lattice = Lattice(1.0, 2.0, 3.0, 90.0, 90.0, 90.0)
        stru[:] = [
            Atom('H', [1., 1., 1.]),
            Atom('Cl', [3., 2., 1.])
        ]
        stru.write(self.tmpname, self.format)
        f_s = open(self.tmpname).read()
        f_s = re.sub('[ \t]+', ' ', f_s)
        s_s = "2\n%s\nH 1 2 3\nCl 3 4 3\n" % stru.description
        self.assertEqual(f_s, s_s)

# End of TestP_xyz

##############################################################################
class TestP_forces(unittest.TestCase):
    """test Parser for forces file (three column ascii"""

    def setUp(self):
        self.stru = Structure()
        self.format = 'forces'
        import tempfile
        handle, self.tmpname = tempfile.mkstemp()
        os.close(handle)

    def tearDown(self):
        import os
        os.remove(self.tmpname)

    def test_read_forces(self):
        """check reading of forces file"""
        stru = self.stru
        stru.read(datafile('bucky.xyz'))
        s_els = [a.symbol for a in stru]
        self.assertEqual(stru.description, 'bucky-ball')
        self.assertEqual(s_els, 60*['C'])

#    def test_write_forces(self):
#        """check writing of normal xyz file"""
#        stru = self.stru
#        stru.description = "test of writeStr"
#        stru.lattice = Lattice(1.0, 2.0, 3.0, 90.0, 90.0, 90.0)
#        stru[:] = [
#            Atom('H', [1., 1., 1.]),
#            Atom('Cl', [3., 2., 1.])
#        ]
#        stru.write(self.tmpname, self.format)
#        f_s = open(self.tmpname).read()
#        f_s = re.sub('[ \t]+', ' ', f_s)
#        s_s = "2\n%s\nH 1 2 3\nCl 3 4 3\n" % stru.description
#        self.assertEqual(f_s, s_s)

# End of TestP_forces

##############################################################################
class TestP_rawxyz(unittest.TestCase):
    """test Parser for rawxyz file format"""

    def setUp(self):
        self.stru = Structure()
        self.format = "rawxyz"

    def test_read_plainxyz(self):
        """check reading of a plain xyz file"""
        stru = self.stru
        stru.read(datafile('bucky-plain.xyz'), self.format)
        s_els = [a.symbol for a in stru]
        #print 'description',stru.description
        self.assertEqual(stru.description, 'C60 in Lattice()')
        self.assertEqual(s_els, 60*['C'])

    def test_read_plainxyz_bad(self):
        """check exceptions when reading invalid plain xyz file"""
        stru = self.stru
        self.assertRaises(StructureFormatError, stru.read,
                datafile('bucky-plain-bad.xyz'), self.format)

    def test_read_rawxyz(self):
        """check reading of raw xyz file"""
        stru = self.stru
        stru.read(datafile('bucky-raw.xyz'), self.format)
        s_els = [a.symbol for a in stru]
        #stru.description = stru.generateDescription()
        #print 'description',stru.description
        self.assertEqual(stru.description, '60 in Lattice()')
        self.assertEqual(s_els, 60*[''])
        stru.read(datafile('hexagon-raw.xyz'), self.format)
        zs = [a.xyz[-1] for a in stru]
        self.assertEqual(zs, 6*[0.0])

    def test_read_rawxyz_bad(self):
        """check exceptions when reading unsupported xy file"""
        stru = self.stru
        self.assertRaises(StructureFormatError, stru.read,
                datafile('hexagon-raw-bad.xyz'), self.format)
        self.assertRaises(StructureFormatError, stru.read,
                datafile('hexagon-raw.xy'), self.format)

    def test_writeStr_rawxyz(self):
        """check writing of normal xyz file"""
        stru = self.stru
        stru.description = "test of writeStr"
        stru.lattice = Lattice(1.0, 2.0, 3.0, 90.0, 90.0, 90.0)
        # plain version
        stru[:] = [ Atom('H', [1., 1., 1.]) ]
        s1 = stru.writeStr(self.format)
        s1 = re.sub('[ \t]+', ' ', s1)
        s0 = "H 1 2 3\n"
        # brutal raw version
#        stru[0].symbol = ""
#        s1 = stru.writeStr(self.format)
#        s0 = "1 2 3\n"
#        self.assertEqual(s1, s0)

# End of TestP_rawxyz

##############################################################################
class TestP_pdb(unittest.TestCase):
    """test Parser for PDB file format"""

    def setUp(self):
        self.stru = Structure()
        self.format = "pdb"
        self.places = 3

    def assertListAlmostEqual(self, l1, l2, places=None):
        """wrapper for list comparison"""
        if places is None: places = self.places
        self.assertEqual(len(l1), len(l2))
        for i in range(len(l1)):
            self.assertAlmostEqual(l1[i], l2[i], places)

    def test_read_pdb_arginine(self):
        """check reading of arginine PDB file"""
        stru = self.stru
        stru.read(datafile('arginine.pdb'), self.format)
        f_els = [ "N", "C", "C", "O", "C", "C", "C", "N", "C", "N", "N", "H",
            "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H", "H",
            "O", "H" ]
        s_els = [a.symbol for a in stru]
        self.assertEqual(s_els, f_els)
        s_lat = [ stru.lattice.a, stru.lattice.b, stru.lattice.c,
            stru.lattice.alpha, stru.lattice.beta, stru.lattice.gamma ]
        f_lat = [1.0, 1.0, 1.0, 90.0, 90.0, 90.0]
        self.assertEqual(s_lat, f_lat)
        a0 = stru[0]
        self.assertListAlmostEqual(a0.xyz, [0.735, 2.219, 1.389])

    def test_rwStr_pdb_CdSe(self):
        """check conversion to PDB file format"""
        stru = self.stru
        stru.read(datafile('CdSe_bulk.stru'), 'pdffit')
        #print stru.description
        s = stru.writeStr(self.format)
        # all lines should be 80 characters long
        linelens = [ len(l) for l in s.split('\n') if l != "" ]
        self.assertEqual(linelens, len(linelens)*[80])
        # now clean and re-read structure
        stru = Structure()
        stru.readStr(s, self.format)
        #print stru.description
        s_els = [a.symbol for a in stru]
        f_els = ['Cd', 'Cd', 'Se', 'Se']
        self.assertEqual(s_els, f_els)
        s_lat = [ stru.lattice.a, stru.lattice.b, stru.lattice.c,
            stru.lattice.alpha, stru.lattice.beta, stru.lattice.gamma ]
        f_lat = [ 4.235204,  4.235204,  6.906027, 90.0, 90.0, 120.0 ]
        self.assertListAlmostEqual(s_lat, f_lat)
        a0 = stru[0]
        s_Uii = [ a0.U[i,i] for i in range(3) ]
        f_Uii = [ 0.01303035, 0.01303035, 0.01401959 ]
        self.assertListAlmostEqual(s_Uii, f_Uii)
        s_sigUii = [ a0.sigU[i,i] for i in range(3) ]
        f_sigUii = [ 0.00011127, 0.00011127, 0.00019575 ]
        self.assertListAlmostEqual(s_sigUii, f_sigUii)
        s_title = stru.description
        f_title = "Cell structure file of CdSe #186"
        self.assertEqual(s_title, f_title)

# End of TestP_pdb

##############################################################################
class TestP_xcfg(unittest.TestCase):
    """test Parser for XCFG file format"""

    def setUp(self):
        self.stru = Structure()
        self.format = "xcfg"
        self.places = 6

    def assertListAlmostEqual(self, l1, l2, places=None):
        """wrapper for list comparison"""
        if places is None: places = self.places
        self.assertEqual(len(l1), len(l2))
        for i in range(len(l1)):
            self.assertAlmostEqual(l1[i], l2[i], places)

    def test_read_xcfg(self):
        """check reading of BubbleRaft XCFG file"""
        stru = self.stru
        stru.read(datafile('BubbleRaftShort.xcfg'), self.format)
        f_els = 500* [ "Ar" ]
        s_els = [a.symbol for a in stru]
        self.assertEqual(s_els, f_els)
        self.assertAlmostEqual(stru.distance(82, 357), 47.5627, 3)
        s_lat = [ stru.lattice.a, stru.lattice.b, stru.lattice.c,
            stru.lattice.alpha, stru.lattice.beta, stru.lattice.gamma ]
        f_lat = [127.5, 119.5, 3.0, 90.0, 90.0, 90.0]
        self.assertListAlmostEqual(s_lat, f_lat)

    def test_rwStr_xcfg_CdSe(self):
        """check conversion to XCFG file format"""
        stru = self.stru
        stru.read(datafile('CdSe_bulk.stru'), 'pdffit')
        s = stru.writeStr(self.format)
        stru = Structure()
        stru.readStr(s, self.format)
        s_els = [a.symbol for a in stru]
        f_els = ['Cd', 'Cd', 'Se', 'Se']
        self.assertEqual(s_els, f_els)
        s_lat = [ stru.lattice.a, stru.lattice.b, stru.lattice.c,
            stru.lattice.alpha, stru.lattice.beta, stru.lattice.gamma ]
        f_lat = [ 4.235204,  4.235204,  6.906027, 90.0, 90.0, 120.0 ]
        self.assertListAlmostEqual(s_lat, f_lat)
        a0 = stru[0]
        s_Uii = [ a0.U[i,i] for i in range(3) ]
        f_Uii = [ 0.01303035, 0.01303035, 0.01401959 ]
        self.assertListAlmostEqual(s_Uii, f_Uii)

# End of TestP_xcfg
##############################################################################
#class TestP_bratoms(unittest.TestCase):
#    """test Parser for Bruce Ravel's atoms file format"""
#
#    def setUp(self):
#        self.stru = Structure()
#        self.format = "bratoms"
#        self.places = 6
#
#    def test_writeStr_cif(self):
#        """check conversion to CIF string"""
#        stru = self.stru
#        stru.read(datafile('GaAs.inp'), 'bratoms')
#        s_s = stru.writeStr(self.format)
#
#    def test_read_bratoms_bad(self):
#        """check exceptions when reading invalid bratoms file"""
#        badfiles = [
#                'LiCl-bad.cif',
#                'PbTe.cif',
#                'arginine.pdb',
#                'ZnSb_RT_Q28X_VM_20_fxiso.rstr',
#                'Ni-bad.stru',
#                'Ni-discus.stru',
#                'Ni.stru',
#                'BubbleRaftShort.xcfg',
#                'bucky-bad1.xyz',
#                'bucky-bad2.xyz',
#                'bucky-plain-bad.xyz',
#                'bucky-plain.xyz',
#                'bucky-raw.xyz',
#                'bucky.xyz',
#                'hexagon-raw-bad.xyz',
#                'hexagon-raw.xyz',
#        ]
#        for ft in badfiles:
#            ff = datafile(ft)
#            self.assertRaises(StructureFormatError,
#                    self.stru.read, ff, format=self.format)
#        return

# End of TestP_bratoms


if __name__ == '__main__':
    unittest.main()

# End of file
