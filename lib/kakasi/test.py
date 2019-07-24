#!/usr/bin/python
#! -*- coding: euc-jp -*-
import pykakasi
arg = ['-w']
pykakasi.init(arg)
input = '本日は晴天なり。'
output = pykakasi.execute(input)
print unicode(output, 'euc_jp').encode('utf-8')

