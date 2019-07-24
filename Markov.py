from MultipleOccurence import MultipleOccurence
from sqlobject import ForeignKey, sqlbuilder

class MarkovBase(MultipleOccurence):
    """ Base class for Markov chain-like objects"""
    class sqlmeta:
        defaultOrder = '-occurence'


class Markov(MarkovBase):
    """ Markov Chains for words """
    first_word  = ForeignKey('Word')
    second_word = ForeignKey('Word')
    third_word  = ForeignKey('Word')


class MarkovLex(MarkovBase):
    """ Markov Chains for lexicons """
    first_lex  = ForeignKey('MainType')
    second_lex = ForeignKey('MainType')
    third_lex  = ForeignKey('MainType')


