from sqlobject import SQLObject, IntCol

class MultipleOccurence(SQLObject):
    """ Base class for objects with an occurence column """

    occurence = IntCol(default=1)

    def _init(self, id, increment=False, connection=None, selectResults=None, *args, **kw):
        """Constructor override to get occurence updates"""
        SQLObject._init(self, id, connection=None, selectResults=None, *args, **kw)
        if increment:self.increment()

    def increment(self):
        """ Increments the occurence """
        self.occurence += 1
