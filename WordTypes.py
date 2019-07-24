from sqlobject import SQLObject, UnicodeCol

class WordTypes(SQLObject):
    """Base class for word types"""
    name = UnicodeCol(alternateID=True)


class MainType(WordTypes):
    """ The Main Type of the word """


class SubType(WordTypes):
    """ The Subt Type of the word """


