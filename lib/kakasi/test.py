#!/usr/bin/python
#! -*- coding: euc-jp -*-
import pykakasi
arg = ['-w']
pykakasi.init(arg)
input = '��������ŷ�ʤꡣ'
output = pykakasi.execute(input)
print unicode(output, 'euc_jp').encode('utf-8')

