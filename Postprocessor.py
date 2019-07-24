#! -*- coding: utf-8 -*-
import sys
import re

class Postprocessor:
    """Postprocessiong functions"""

    def postProcess(self, msg):
        regexp = {u'。*$':u'',
                  u'ません$':u'ませんね',
                  u'のだろう\?$':u'んだろうねぇ',
                  u'だろう\?$':u'だろうね?',
                  u'([ういるどか])なー$':u'\\1なぁ',
                  u'([よいどか])ねー$':u'\\1ねぇ',
                  u'([だよ])な$':u'\\1ね',
                  u'ない$':u'ないよ',
                  u'だけか$':u'だけだよ',
                  u'いか$':u'いかな',
                  u'したい$':u'したいね',
                  u'ろう!$':u'ろうよ!',
                  u'ろう$':u'ろうね',
                  u'うか$':u'うかな',
                  u'がいい$':u'がいいよ',
                  u'いかん(.+)$':u'いけない\\1',
                  u'きた$':u'きたよ',
                  u'けど$':u'けどね',}
        for expression in regexp.keys():
            #print expression.encode('utf-8')
            #print regexp[expression].encode('utf-8')
            msg = re.sub(expression, regexp[expression], msg)
        
        return msg
    
