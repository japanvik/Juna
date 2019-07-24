#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, string

"""
zen2han.py
Converts Zenkaku characters to Hankaku.
Reads from stdin *must be utf-8*
"""

# Zenkaku characters
zenkaku = [u"ａ", u"ｂ", u"ｃ", u"ｄ", u"ｅ", u"ｆ", u"ｇ", u"ｈ", u"ｉ",
           u"ｊ", u"ｋ", u"ｌ", u"ｍ", u"ｎ", u"ｏ", u"ｐ", u"ｑ", u"ｒ",
           u"ｓ", u"ｔ", u"ｕ", u"ｖ", u"ｗ", u"ｘ", u"ｙ", u"ｚ",
           u"Ａ", u"Ｂ", u"Ｃ", u"Ｄ", u"Ｅ", u"Ｆ", u"Ｇ", u"Ｈ", u"Ｉ",
           u"Ｊ", u"Ｋ", u"Ｌ", u"Ｍ", u"Ｎ", u"Ｏ", u"Ｐ", u"Ｑ", u"Ｒ",
           u"Ｓ", u"Ｔ", u"Ｕ", u"Ｖ", u"Ｗ", u"Ｘ", u"Ｙ", u"Ｚ",
           u"！", u"”", u"＃", u"＄", u"％", u"＆", u"’", u"（", u"）",
           u"＊", u"＋", u"，", u"−", u"．", u"／", u"：", u"；", u"＜",
           u"＝", u"＞", u"？", u"＠", u"［", u"￥", u"］", u"＾", u"＿",
           u"‘", u"｛", u"｜", u"｝", u"　", u"０", u"１", u"２", 
           u"３", u"４", u"５", u"６", u"７", u"８", u"９"]

hankaku = [u"a", u"b", u"c", u"d", u"e", u"f", u"g", u"h", u"i",
           u"j", u"k", u"l", u"m", u"n", u"o", u"p", u"q", u"r",
           u"s", u"t", u"u", u"v", u"w", u"x", u"y", u"z",
           u"A", u"B", u"C", u"D", u"E", u"F", u"G", u"H", u"I",
           u"J", u"K", u"L", u"M", u"N", u"O", u"P", u"Q", u"R",
           u"S", u"T", u"U", u"V", u"W", u"X", u"Y", u"Z",
           u"!", u'"', u"#", u"$", u"%", u"&", u"'", u"(", u")",
           u"*", u"+", u",", u"-", u".", u"/", u":", u";", u"<",
           u"=", u">", u"?", u"@", u"[", u"\\", u"]", u"^", u"_",
           u"`", u"{", u"|", u"}", u" ", u"0", u"1", u"2", 
           u"3", u"4", u"5", u"6", u"7", u"8", u"9"]


def convert(text):
    global z2h_map
    output = ''
    for letter in text.strip():
        if z2h_map.has_key(letter):
            output += z2h_map[letter]
        else:
            output += letter
    return output.lower()

#We make a dictionary to map the 2 sets
z2h_map={}
for i in range(len(zenkaku)):
    z2h_map[zenkaku[i]] = hankaku[i]

#Now we read from stdin, and convert the letters as we go
"""
for line in sys.stdin.readlines():
    try: 
        print convert(line)
    except UnicodeEncodeError:
        pass
"""
