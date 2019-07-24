from sqlobject import SQLObject, UnicodeCol, ForeignKey
from MultipleOccurence import MultipleOccurence

class Word(MultipleOccurence):
    """
    The Word Object
    """
    appeared_name    = UnicodeCol(alternateID=True)
    appeared_reading = UnicodeCol()
    base_name        = UnicodeCol()
    base_reading     = UnicodeCol()
    main_type        = ForeignKey('MainType')
    sub_type         = ForeignKey('SubType')

    def wordType(self):
        """Return 'main_type.sub_type' as string """
        word_type = '.'.join([str(self.main_type.id), str(self.sub_type.id)])
        return word_type

