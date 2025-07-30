from morebs2 import numerical_generator
import numpy as np
from collections import OrderedDict

import unittest

'''
python -m morebs2.tests.numerical_generator_test  
'''
class TestNumericalGeneratorClass(unittest.TestCase):

    def test_CycleMap__random_map(self):
        vr = numerical_generator.CycleMap.random_cycle_map(5)
        ##print("VR")
        ##print(vr)

        f = numerical_generator.CycleMap.is_valid_map(vr)
        ##print("F: ", f)
        assert f, "random cycle map is not cycle"

        q = OrderedDict()
        x = [(3,1),(1,3),(2,4),(4,2)]
        for k,v in x:
            q[k] = v

        f2 = numerical_generator.CycleMap.is_valid_map(q)
        ##print("F2: ", f2)
        assert not f2, "non-cyclic map"
        return

    def test__generate_possible_binary_sequences(self):
        g = numerical_generator.generate_possible_binary_sequences(5, [])
        g = list(g)
        assert len(g) == 2 ** 5, "incorrect generation"

        # uncomment for viewing
        '''
        for g_ in g:
            print(g_)
        '''

    def test__random_npoint_from_point_in_bounds(self):

        bounds = np.array([[-100,100.0],\
                        [-100,100.0],\
                        [-100,100.0],\
                        [-100,100.0],\
                        [-100,100.0],\
                        [-100,100.0]])
        r = 200.0

        # case point on >= 1 of the bound extremes
        p1 = np.array([-100,100,-99,80,95.0,-100])
        for i in range(100):
            p2 = numerical_generator.random_npoint_from_point_in_bounds(bounds,p1,r)
            assert type(p2) != type(None)
        return

    def test__random_npoint_from_point(self):
        r = 200.0

        # case point on >= 1 of the bound extremes
        p1 = np.array([-100,100,-99,80,95.0,-100])
        for i in range(100):
            p2 = numerical_generator.random_npoint_from_point(p1,r)
            assert type(p2) != type(None)
        return

    def test__CycleMap__next(self): 
        cm = numerical_generator.CycleMap(5)
        d = OrderedDict({10:13,13:74,74:21,21:16,16:10})
        cm.set_map(d)
        q = set() 

        for i in range(10): 
            q_ = next(cm) 
            q |= {q_}
        assert len(q) == 5 

        cm = numerical_generator.CycleMap(7)
        f = numerical_generator.CycleMap.random_cycle_map(7)
        cm.set_map(f) 
        q = set()
        for i in range(10): 
            q_ = next(cm) 
            q |= {q_}
        assert len(q) == 7

    def test__prg_seqsort_ties(self): 
        prg0 = numerical_generator.prg__constant(5)
        prg4 = numerical_generator.prg__n_ary_alternator(s0=3,s1=25,start=1) 
        R2 = ["3","52432","cat","DGO","bingo","ROGUE", "rauchu", "NOBODIES","12,55","32","43,10,13","12"] 
        Q = [(40,r) for r in R2] 
        vf = lambda x: x[1] 
        rq = numerical_generator.prg_seqsort_ties(Q,prg4,vf) 

        assert rq == [(40, '12'), (40, '12,55'), (40, '3'), \
            (40, '32'), (40, '43,10,13'), (40, '52432'), \
            (40, 'DGO'), (40, 'NOBODIES'), (40, 'ROGUE'), \
            (40, 'bingo'), (40, 'cat'), (40, 'rauchu')]

        Q2 = [(prg4(),r) for r in R2] 
        Q2.extend([(prg4(),r) for r in R2]) 
        Q2.extend([(prg4(),r) for r in R2]) 

        vf2 = lambda x: x[0] 
        rq2 = numerical_generator.prg_seqsort_ties(Q2,prg4,vf2) 
        rq3 = numerical_generator.prg_seqsort_ties(Q2,prg0,vf2) 

        assert rq2 == [(3, '32'), (3, 'NOBODIES'), \
            (4, '43,10,13'), (4, '12,55'), (5, '12'), \
            (5, '32'), (6, '3'), (6, '43,10,13'), \
            (7, '52432'), (7, '12'), (8, 'cat'), \
            (9, 'DGO'), (10, 'bingo'), (11, 'ROGUE'), \
            (12, 'rauchu'), (13, 'NOBODIES'), (14, '12,55'), \
            (15, '32'), (16, '3'), (16, '43,10,13'), \
            (17, '52432'), (17, '12'), (18, 'cat'), (18, '3'), \
            (19, 'DGO'), (19, '52432'), (20, 'bingo'), (20, 'cat'), \
            (21, 'ROGUE'), (21, 'DGO'), (22, 'rauchu'), \
            (22, 'bingo'), (23, 'NOBODIES'), (23, 'ROGUE'), \
            (24, '12,55'), (24, 'rauchu')]

        assert rq3 == [(3, 'NOBODIES'), (3, '32'), (4, '12,55'), \
            (4, '43,10,13'), (5, '32'), (5, '12'), (6, '43,10,13'), \
            (6, '3'), (7, '12'), (7, '52432'), (8, 'cat'), (9, 'DGO'), \
            (10, 'bingo'), (11, 'ROGUE'), (12, 'rauchu'), \
            (13, 'NOBODIES'), (14, '12,55'), (15, '32'), \
            (16, '43,10,13'), (16, '3'), (17, '12'), (17, '52432'), \
            (18, '3'), (18, 'cat'), (19, '52432'), (19, 'DGO'), \
            (20, 'cat'), (20, 'bingo'), (21, 'DGO'), (21, 'ROGUE'), \
            (22, 'bingo'), (22, 'rauchu'), (23, 'ROGUE'), (23, 'NOBODIES'), \
            (24, 'rauchu'), (24, '12,55')]



if __name__ == '__main__':
    unittest.main()
