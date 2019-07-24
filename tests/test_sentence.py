#!/usr/bin/python
#! -*- coding: utf-8 -*-
import unittest
import sys
sys.path.append('/home/vkumar/Desktop/Documents/codage/nlp/Juna/')

from Brain import Brain
from Word import Word
from Sentence import Sentence
from Markov import Markov, MarkovLex
from MessageParser import MessageParser

class TestSentence(unittest.TestCase):
    """ Test to make sure the brain's learining algo works """

    def testWordOccurence(self):
        #Test to see if we learned our words correctly
        word = Word.byAppeared_name('名前')
        self.assertEquals(word.occurence, 3)

    def testMarkovChainDuplicates(self):
        # We should only have 1 instance where second word = 名前
        word = Word.byAppeared_name('名前')
        hits = Markov.select(Markov.q.second_wordID == word.id)
        check = list(hits)
        self.assertEquals(len(check), 1)

    def testMarkovChainOccurence(self):
        # We should have 3 for occurence where second word = 名前
        word = Word.byAppeared_name('名前')
        hits = Markov.select(Markov.q.second_wordID == word.id)
        check = list(hits)[0]
        self.assertEquals(check.occurence, 3)

    def testMarkovLexDuplicates(self):
        # We should only have 3 instance where second word = 名前
        word = Word.byAppeared_name('名前')
        hits = MarkovLex.select(MarkovLex.q.second_lexID == word.main_type.id)
        check = list(hits)
        self.assertEquals(len(check), 3)

    def testMarkovLexOccurence(self):
        # We should have 3 for occurence where second word = 名前
        word = Word.byAppeared_name('名前')
        hits = MarkovLex.select(MarkovLex.q.second_lexID == word.main_type.id)
        check = list(hits)[0]
        self.assertEquals(check.occurence, 3)


if __name__ == '__main__':
    brain = Brain()
    phrase = [u'私の名前は中野です', u'私の名前は中野です', u'私の名前は中野です']
    for p in range(len(phrase)):
        #We learn the phrase 3 times
        print 'pase:%d' % p
        brain.learn(phrase[p])
    unittest.main()

