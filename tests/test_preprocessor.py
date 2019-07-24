#!/usr/bin/python
#! -*- coding: utf-8 -*-
import unittest
import sys
sys.path.append('/home/vkumar/Desktop/Documents/codage/nlp/Juna/')


from Preprocessor import Preprocessor

class TestPreprocessor(unittest.TestCase):

    def setUp(self):
        self.pp = Preprocessor()

    def testPreporcessNull(self):
        #Null String should return none
        result = self.pp.clean('')
        self.assertEquals(result, None)

    def testPreporcessOneHiragana(self):
        #One hiragana should return None
        result = self.pp.clean(u'あw(^^)w')
        self.assertEquals(result, None)

    def testPreporcessZenkaku(self):
        #Zenkaku stuff should be converted and cleaned
        result = self.pp.clean(u'全角です１２３ｗｗ')
        self.assertEquals(result, u'全角です123')

    def testPreprocessNakano(self):
        #Test to see if the Preprocessing work as intended
        test_string = u'私の名前は中野ですwwww>あふぉ(^^)o'
        result = self.pp.clean(test_string)
        expected = u'私の名前は中野です'
        self.assertEquals(result, expected)

if __name__ == '__main__':
    unittest.main()

