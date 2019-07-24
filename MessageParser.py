#! -*- coding: utf-8 -*-

import sys
import re
import chasen
from Preprocessor import Preprocessor
from config import MY_NAMES

class MessageParser:
    my_name = re.compile('|'.join(MY_NAMES))

    def __init__(self):
        self.cha=chasen
        self.pp = Preprocessor()
        self.cha.setformat('%m,%y,%M,%Y,%U(%P1),%BB|$|')


    def parseLine(self, message, clean=True):
        """ Parse a given line via chasen.
            If clean is True, does the preporcessing of message
        """

        pMessage=''
        if clean:
            pMessage=self.pp.clean(message)
        else:
             pMessage = message
        if pMessage:
            #print 'pmessage:%s' % pMessage
            pl = self.cha.sparse(pMessage.encode('euc-jp')).strip()
            return unicode(pl, 'euc-jp')
        else:
            print 'message is empty:' + message
            return None


    def parseSentence(self, message, clean=True):
        """ Return a list of pseudo words(=setence) from a string """
        myNameFlag, message = self.checkForMe(message)
        words = self.parseLine(message, clean)
        if words:
            sentence=[]
            for word in words.split('|$|'):
                if word:
                    keywords = ['appeared_name',
                                'appeared_reading',
                                'base_name',
                                'base_reading',
                                'main_type',
                                'sub_type']
                    pseudo_word = generateDict(keywords, word.split(','))
                    sentence.append(pseudo_word)
            return self.doMergers(myNameFlag, sentence)
        else:
            return None


    def checkForMe(self, message):
        """Checks if my name is in the term """
        name_flag = False
        is_name = self.my_name.search(message)
        if is_name:
            message = re.sub(self.my_name, u'私', message)
            name_flag = True
        return name_flag, message

    def merge(self, part, first, second=None):
        """Merge words of a part depending on it's lex class
        """
        if len(part) == 1:return part
        new_part = []
        merged_flag=False
        if not second: second = first

        for i, word in enumerate(part):
            if word['main_type'] == first:
                #Check to see if the nextword
                if i < len(part)-1:
                    if part[i+1]['main_type'] == second:
                        new_word = self.joinWords(word, part[i+1])
                        part[i+1]=new_word
                        part.pop(i)
                        return self.merge(part, first, second)
        #printWords(part)
        return part


    def joinWords(self, word1, word2):
        """Return a pseudo word joining the given 2"""
        new_word = {}
        new_word['appeared_name'] = ''.join([word1['appeared_name'], word2['appeared_name']])
        new_word['appeared_reading'] = ''.join([word1['appeared_reading'], word2['appeared_reading']])
        new_word['base_name'] = ''.join([word1['base_name'], word2['base_name']])
        new_word['base_reading'] = ''.join([word1['base_reading'], word2['base_reading']])
        new_word['main_type'] = word2['main_type']
        new_word['sub_type'] = word2['sub_type']
        return new_word
            
        
    def doMergers(self, myNameFlag, sentence):
        """Do some post processing functions on the sentence
           Required to workaround some of the chasen limitations
        """
        jyoshi_idx = [sentence.index(x) for x in sentence if x['main_type'] == u'助詞']
        #Append the last letter too
        jyoshi_idx.append(len(sentence)-1)

        parts = []
        w_part = []
        for i, word in enumerate(sentence):
            if i in jyoshi_idx:
                parts.append(w_part)
                parts.append([word])
                w_part=[]
            else:
                if myNameFlag == True and word['appeared_name'] == u'私':
                    word['appeared_name'] = u'じゅな'
                    word['appared_reading'] = u'じゅな'
                    word['base_name'] = u'じゅな'
                    word['base_reading'] = u'じゅな'
                w_part.append(word)
        
        # We need to iterate thro the parts, and merge nonus.
        # This is because a combo noun is quite different meaning wise 
        # from a regular noun
        for p in parts:
            p = self.merge(p, u'名詞')
            p = self.merge(p, u'未知語')
            p = self.merge(p, u'記号')
        
       #Finally we merge them all to a new pseudo sentence
        n_sentence = []
        for p in parts:
            for w in p:
                n_sentence.append(w)
        return n_sentence


def generateDict(keywords, values):
    """ Return a dictionary from 2 iterators.
        keywords and values must have equal lengths.
        Should probably go into my Utils Library
    """

    if len(keywords) != len(values):
        print ' '.join(values)
        raise ValueError('keywords and vaules must be the same length!\nkw:%s\nv:%s' % (keywords, values))
    dict={}
    for k,v in map(None, keywords, values):
        dict[k]=v
    return dict

def printWords(words):
    for w in words:
        print '%s:%s[%s]' % (w['appeared_name'], w['main_type'], w['sub_type'])
