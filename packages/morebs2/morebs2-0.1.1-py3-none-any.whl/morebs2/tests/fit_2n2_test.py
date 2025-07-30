from morebs2 import fit_2n2
import numpy as np

import unittest

'''
python -m morebs2.tests.fit_2n2_test  
'''
class TestFit22Class(unittest.TestCase):

    def test__Exp2Fit22__inverse(self):
        # case 1
        lf22 = fit_2n2.Exp2Fit22(np.array([[60.,80.],[30.,12.]]),direction=[1,0])
        (x1,y1) = (40,lf22.f(40))
        (x2,y2) = (lf22.g(y1),y1) 
        assert(x1 == x2 and y1 == y2)

        (x1,y1) = (30,lf22.f(30))
        (x2,y2) = (lf22.g(y1),y1) 
        assert(x1 == x2 and y1 == y2)

        (x1,y1) = (60,lf22.f(60))
        (x2,y2) = (lf22.g(y1),y1) 
        assert(x1 == x2 and y1 == y2)

    def test__LogFit22__inverse(self):
        lf22 = fit_2n2.LogFit22(np.array([[60.,80.],[30.,12.]]),direction=[1,0])
        (x1,y1) = (40,lf22.f(40))
        (x2,y2) = (lf22.g(y1),y1) 
        assert(x1 == x2 and y1 == y2)

        (x1,y1) = (30,lf22.f(30))
        (x2,y2) = (lf22.g(y1),y1) 
        assert(x1 == x2 and y1 == y2)

        (x1,y1) = (60,lf22.f(60))
        (x2,y2) = (lf22.g(y1),y1) 
        assert(x1 == x2 and y1 == y2), "got {} want {}".format((x1,x2),(y1,y2))

if __name__ == '__main__':
    unittest.main()