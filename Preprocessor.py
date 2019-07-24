#! -*- coding: utf-8 -*-
import re
from lib import zen2han

class Preprocessor:
    """ Preprocess functions for cleaning text up
    """
    
    def clean(self, text):
        """ Return cleaned up text from a given unicode text
        """
        #Clean wierd hankaku zenkaku stuff
        text = zen2han.convert(text)
        #Check to see if we can reject it already
        text = self._checkReject(text)
        if not text:return None
        
        #Do some early replacements
        text = self._earlyReplacements(text)

        #Do the recurse cleanage
        text = self._recurseClean(text)
        
        # Check for reject again
        if text : text = self._checkReject(text)
        return text


    def _earlyReplacements(self, text):
        """Cleans the text up from strange characters"""
        return re.sub(u'，', u'、', text)


    def _recurseClean(self, text):
        """ Loop thro the criteria until no further cleaning occur
        """
        dirty = False
        regs = [u'^(.+?)[＜＞<>].+$',
                 '^(.+?)[A-Za-z]+$',
                 '^(.+?)\(.+\)+$']
        result = self._matchReg(text, regs)
        if result:
            dirty=True
            text = result.group(1)
            return self._recurseClean(text)
        else:
            return text


    def _checkReject(self, text):
        """ See if the string is viable to be checked at all
        """
        regs=['^\n'
              '^.$',                                                  #Only one letter
             u'^[ぁ-んァ-ンー]$',                                     #Only one hiragana
             u'^[ぁ-んー][ぁ-んー]$',                                 #Only 2 Hiraganas
             u'^[-.\/+*:;,~_|&\'"`()0-9a-zA-Z]+$',                    #Only symbols numbers, and alphabet
              '^[,]',                                                 #Starts with wierd stuff
             u'^[（◆￣＿\-)）」・〕】』ーをんぁぃぅぇぉゃゅょっ]',
             u'^[ーヲンァィゥェォャュョッヶヵ]',]
        result = self._matchReg(text, regs)
        if result: return None
        return text


    def _matchReg(self, text, reg_list):
        """ loops thro the reg_list and see if the text matches
        """
        for reg in reg_list:
            match = re.compile(reg).match(text)
            if match: return match
        return None


