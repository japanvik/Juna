from config import DB_URI
from sqlobject import *

from WordTypes import MainType, SubType
from Word import Word
from Lex import Lex
from Log import Log
from Markov import Markov, MarkovLex

#Database Connection
connection = connectionForURI(DB_URI)
sqlhub.processConnection = connection

#Database Generator
MainType.createTable()
SubType.createTable()
Word.createTable()
Lex.createTable()
Log.createTable()
Markov.createTable()
MarkovLex.createTable()

#Insert default data
#The End Of Sentence
SubType(name='EOS')
MainType(name='EOS')
Word(appeared_name='EOS', appeared_reading='EOS', base_name='EOS', base_reading='EOS', main_type = 1, sub_type = 1)

