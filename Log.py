from sqlobject import SQLObject, StringCol, DateTimeCol, ForeignKey, sqlbuilder
from datetime import datetime

class Log(SQLObject):
    """ The log object
        Stores a list of word id's
    """
    entry      = StringCol()
    lex        = ForeignKey('Lex')
    entry_date = DateTimeCol(default=sqlbuilder.func.NOW())

    class sqlmeta:
        defaultOrder = 'entry_date'

    def wordList(self):
        """Return a list of word_ids for this log"""
        return self.entry.split('|')


"""
    def _init(self, id, *args, **kw):
        Constructor overrride to update dates
        self.entry_date = datetime.now()
        SQLObject._init(self, id, *args, **kw)
"""
