from Word import Word
from Markov import Markov, MarkovLex
from WordTypes import MainType, SubType
from sqlobject import *

class Sentence:
    """ A Sentence is basically a list of Words.
        A real sentence is a list of Word objects.
    """
    words=[]

    def pseudo2real(self, pseudo_words, increment=False):
        """ Convert a pseudo sentence to a real sentence.
            If increment is True, we update the occurence
        """
        #Word._connection.debug=True
        self.words=[]
        for pword in pseudo_words:
            try:
                real_word = Word.byAppeared_name(pword['appeared_name'].encode('utf-8'))
                #Do we increment?
                if increment: real_word.increment()
            except SQLObjectNotFound:
                #We don't have the word yet
                try:
                    main_type = MainType.byName(pword['main_type'].encode('utf-8'))
                except SQLObjectNotFound:
                    main_type = MainType(name = pword['main_type'])
                try:
                    sub_type = SubType.byName(pword['sub_type'].encode('utf-8'))
                except SQLObjectNotFound:
                    sub_type = SubType(name = pword['sub_type'])

                # We create a new word object
                real_word = Word(appeared_name = pword['appeared_name'],
                                 appeared_reading = pword['appeared_reading'],
                                 base_name = pword['base_name'],
                                 base_reading = pword['base_reading'],
                                 main_type = main_type.id,
                                 sub_type = sub_type.id)
            self.words.append(real_word)
                
    def lexString(self):
        """Return the lex string for this sentence
        """
        if self.words:
            lex_string = '|'.join([x.wordType() for x in self.words])
        else:
            raise ValueError('no words?:%s' % self.words)
        return lex_string
    
    def logString(self):
        """Return the log string for this sentence
        """
        if self.words:
            return '|'.join([str(x.id) for x in self.words])
        else:
            return None

    def readable(self):
        """ Return a unicode string of the sentence
        """
        if self.words:
            return ''.join([x.appeared_name for x in self.words])
        else:
            return None

    def _markovify(self):
        """ Add anchors to the sentence
            Make a triplets of words ready for insertion
        """
        anchor = Word.byAppeared_name('EOS')
        mc = self.words[:]
        mc.append(anchor)
        mc.insert(0, anchor)
        markov_table =[]
        for i in range(2, len(mc)):
            markov_table.append([mc[i-2], mc[i-1], mc[i]])
        return markov_table

    def createMarkovChains(self, increment=False):
        """ Generate Markov Chains and store it in the database """
        mt = self._markovify()
        for entry in mt:
            (first, second, third) = [x.id for x in entry]
            #Frist the markov chain
            mw =  Markov.select(AND(Markov.q.first_wordID == first,
                                    Markov.q.second_wordID == second,
                                    Markov.q.third_wordID == third))
            markov = list(mw)
            if markov and increment == True:
                markov[0].increment()
            else:
                Markov(first_word=first,
                       second_word=second,
                       third_word=third)
            #Next the Markov Lex chain 
            (first, second, third) = [x.main_type.id for x in entry]
            ml =  MarkovLex.select(AND(MarkovLex.q.first_lexID == first,
                                       MarkovLex.q.second_lexID == second,
                                       MarkovLex.q.third_lexID == third))
            markovlex = list(ml)
            if markovlex and increment == True:
                markovlex[0].increment()
            else:
                MarkovLex(first_lex=first,
                          second_lex=second,
                          third_lex=third)

    def createFromIDs(self, id_list):
        """Genereate a sentence from a list of word ids"""
        self.words = []
        for id in id_list:
            self.words.append(Word.get(id))
 
    def __len__(self):
        """ The length of a sentence is how many words it has
        """
        return len(self.words)

    def __iter__(self):
        """ A Sentence should be iterable.
            So we can say 'for words in Sentence:'
        """
        return self.words.__iter__()

    def __getitem__(self, x):
        """ sentence[x] should return the word at index[x]"""
        return self.words[x]

    def insert(self, position, word):
        """ Insert a word at the given position """
        self.words.insert(position, word)

    def append(self, word):
        """ Append a word at the end of the sentence """
        self.words.append(word)

