#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import math

class BBox:
    def __init__(self, minx, miny, maxx, maxy):
        self.minx = float(minx)
        self.miny = float(miny)
        self.maxx = float(maxx)
        self.maxy = float(maxy)

    def __repr__(self):
        return 'BBox(%s,%s,%s,%s)' % (self.minx,self.miny,self.maxx,self.maxy)

    def __eq__(self, other):
        if (self.minx == other.minx and
            self.miny == other.miny and
            self.maxx == other.maxx and
            self.maxy == other.maxy):
            return True
        return False

    def width(self):
        return self.maxx - self.minx

    def height(self):
        return self.maxy - self.miny

    def contains(self, x, y):
        if (self.minx <= x and self.maxx >= x and
            self.miny <= y and self.maxy >=y):
            return True
        return False

    def create_quads(self):
        newWidth = self.width()/2
        newHeight = self.height()/2
        quad0 = BBox(self.minx, self.miny + newHeight, self.minx + newWidth, self.maxy)
        quad1 = BBox(self.minx + newWidth, self.maxy - newHeight, self.minx + (2*newWidth), self.maxy)
        quad2 = BBox(self.minx, self.maxy - (2*newHeight), self.minx + newWidth, self.maxy - newHeight)
        quad3 = BBox(self.minx + newWidth, self.maxy - (2*newHeight),  self.minx + (2*newWidth), self.maxy - newHeight)
        return [quad0, quad1, quad2, quad3]

        

class QuadTree:
    def __init__(self,bbox,levels):
        self.bbox = bbox
        self.levels = int(levels)

    def __repr__(self):
        return 'QuadTree(%s,%s)' % (self.bbox,self.levels)

    def resolution(self):
        #assuming quadtree contains box which is a square
        return self.bbox.width() / math.pow(2, self.levels)

    #creates the morton key space for a point inside the bbox
    def xy_to_morton(self, x, y):
        res = '0'
        if not self.bbox.contains(x, y):
           return ''
        curQuads = self.bbox.create_quads()
        for i in range(1, self.levels):
            for j in range(4):
                if curQuads[j].contains(x, y):
                    res += str(j)
                    curQuads = curQuads[j].create_quads()
                    break
        return res



_gbox = BBox(420000,30000,900000,510000)
_gqt = QuadTree(_gbox, 20)

class TestBBox(unittest.TestCase):

    def test_contains(self):
        box = _gbox
        self.assertTrue(box.contains(600000,200000))
        self.assertFalse(box.contains(950000,200000))
        self.assertFalse(box.contains(419999,200000))
        self.assertFalse(box.contains(600000,899999))
        self.assertFalse(box.contains(600000,510001))
        self.assertEqual(480000, box.width())
        self.assertEqual(480000, box.height())

    def test_equality(self):
        self.assertEqual(BBox(420000,30000,900000,510000), _gbox)
        self.assertNotEqual(BBox(420001,30000,900000,510000), _gbox)
        self.assertNotEqual(BBox(420000,30001,900000,510000), _gbox)
        self.assertNotEqual(BBox(420000,30000,900001,510000), _gbox)
        self.assertNotEqual(BBox(420000,30000,900000,510001), _gbox)

    def test_createQuads(self):
        box = _gbox.create_quads()
        self.assertEqual(BBox(420000,270000,660000,510000), box[0])
        self.assertEqual(BBox(660000,270000,900000,510000), box[1])
        self.assertEqual(BBox(420000,30000,660000,270000), box[2])
        self.assertEqual(BBox(660000,30000,900000,270000), box[3])

class TestQuadTree(unittest.TestCase):

    def test_resolution(self):
        self.assertEqual(0.45, math.floor(_gqt.resolution()*100)/100)

    def test_xy_to_morton(self):
        self.assertEqual('', _gqt.xy_to_morton(600000,899999))
        teststring = '0' * _gqt.levels
        self.assertEqual(teststring, _gqt.xy_to_morton(420000.3, 509999.7))
        teststring = '0' + ('1' * (_gqt.levels-1))
        self.assertEqual(teststring, _gqt.xy_to_morton(899999.8, 509999.9))
        teststring = '0' + ('2' * (_gqt.levels-1))
        self.assertEqual(teststring, _gqt.xy_to_morton(420000.3, 30000.4))
        teststring = '0' + ('3' * (_gqt.levels-1))
        self.assertEqual(teststring, _gqt.xy_to_morton(899999.8, 30000.4))
        

if __name__ == "__main__":
    unittest.main()
    
