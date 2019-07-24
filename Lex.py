from MultipleOccurence import MultipleOccurence
from sqlobject import UnicodeCol

class Lex(MultipleOccurence):
    """ The Lex Object
        This is a lex-log
    """
    entry = UnicodeCol(alternateID=True)

