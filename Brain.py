#! -*- coding: utf-8 -*-

from config import DB_URI, DEBUG
from MessageParser import MessageParser
from Postprocessor import Postprocessor
from Sentence import Sentence
from Markov import Markov, MarkovLex
from Lex import Lex
from Word import Word
from Log import Log
from sqlobject import *
import math
import random
from lib.Event import Event

#Database Connection
connection = connectionForURI(DB_URI)
sqlhub.processConnection = connection

class Brain:
    def __init__(self, dispatcher):
        """ Juna's brain. Handles messages and tries to make a reply.
        """
        self.dispatcher = dispatcher
        #Callbacks
        self.dispatcher += Event('rcv', self.learn)
        self.dispatcher += Event('speak_request', self.getMessageString)

        self.parser = MessageParser()
        self.postprocessor = Postprocessor()
        self.DEBUG=DEBUG
        
    def learn(self, message, speaker=''):
        """ The learning Mechanism
            At the moment, it doesn't really learn per se
            It only adds stuff to the database
        """
        # We take the message and convert it to a pseudo sentence
        pseudo_sentence = self.parser.parseSentence(message)
        if not pseudo_sentence:
            return None
        #Convert the pseudo sentence to a real sentence object
        sentence = Sentence()
        sentence.pseudo2real(pseudo_sentence, increment=True)
        #add the lex entry
        lex_string = sentence.lexString()
        try:
            lex = Lex.byEntry(lex_string)
        except SQLObjectNotFound:
            lex = Lex(increment=True, entry=lex_string)

        #add the log entry
        log_string = sentence.logString()
        Log(entry = log_string, lex = lex.id)

        #Finally, the marcov table
        sentence.createMarkovChains(increment=True)
        
 
    def getMessageString(self, message_queue, my_queue, topic_queue):
        """This is the main algo to speak"""
        markov_candidates=[]
        if topic_queue:
            #Make Marg Chains from the keywords and covert them to Senteces
            for keyword in topic_queue:
                marg_chain = self.generateMargChain(keyword)
                if marg_chain:
                    sentence = Sentence()
                    sentence.createFromIDs(marg_chain)
                    markov_candidates.append(sentence)
            
        if markov_candidates:
            #Filter out things we spoke/heard recently.
            mc = [x.readable() for x in markov_candidates]
            mc = list(set(mc) - (set(message_queue) | set(my_queue)))
            #mc is list of real text, so we convert it back to our Sentence object
            if mc:
                final_candidates=[]
                for c in mc:
                    s = Sentence()
                    s.pseudo2real(self.parser.parseSentence(c))
                    final_candidates.append(s)
                #Do the grammar check
                best_choice = self.checkGrammar(final_candidates)
                #Postprocess the output
                final_output = self.postprocessor.postProcess(best_choice.readable())
                self.debug('final_output:%s' % final_output)
                #Dispatch the final output
                self.dispatcher('speak', final_output)


    def checkGrammar(self, choice_list):
        """Uses the MarkovLex chain to pick the sentence with highest grammatical probablility
           TODO refactor this part and the one below.
        """
        if len(choice_list) == 1: return choice_list[0]
        scores = []
        for choice in choice_list:
            if len(choice)<3:
                scores.append(5.0)
            else:
                #We run it thro the markov check
                anchor = Word.byAppeared_name('EOS')
                copy = choice[:]
                copy.append(anchor)
                scores.append(self._generateScore(copy))
        #We take the best scoring sentence
        print scores
        return choice_list[scores.index(max(scores))]


    def _generateScore(self, sentence, score=[], position=0):
        """Score the Sentence using the markov chain"""
        (first, second, third) = [sentence[position + 0].main_type.id,
                                  sentence[position + 1].main_type.id,
                                  sentence[position + 2].main_type.id]

        tm = MarkovLex.select(AND(MarkovLex.q.first_lexID == first,
                                  MarkovLex.q.second_lexID == second,
                                  MarkovLex.q.third_lexID == third))
        if not tm:return 0
        this_mlex=list(tm)[0]

        mlex = MarkovLex.select(AND(MarkovLex.q.first_lexID == first,
                                    MarkovLex.q.second_lexID == second))
        mlex_hits = list(mlex)
        total_occurences = reduce(lambda x, y:x+y, [x.occurence for x in mlex_hits])
        prob = float(float(this_mlex.occurence) / float(total_occurences))
        score.append(prob)
        if third != 1:
            #We continue the chain
            position += 1
            return self._generateScore(sentence, score=score, position=position)
        else:
            #We are done so we return the average score
            return reduce(lambda x, y:x+y, score) / float(len(score))


    def generateMargChain(self, key_word):
        """Return a Margarine Chain as Sentence
           Inspired by the Open Source project Margarine
           which uses a similar concept to the Markov Chain.
           MargChains go both ways, starting from the keyword
        """
        if not key_word:return None
        base_margs = Markov.select(Markov.q.second_wordID == key_word)
        base_margs = list(base_margs)
        if not base_margs:return None

        #base is random for now!!
        base = base_margs[int(random.random()*len(base_margs))]
        # Create the forward chain (keyword -> end)
        first_word = base.first_word.id
        second_word = base.second_word.id
        third_word = base.third_word.id
        
        second_half = [base.second_word.id]
        while third_word !=1 and len(second_half) < 12:
            #Loop until it hits EOF = id(1)
            second_half.append(third_word)
            #swap things forward
            first_word = second_word
            second_word = third_word
            #self.debug('first_word:%s second_word:%s' % (first_word, second_word))
            hits = Markov.select(AND(Markov.q.first_wordID == first_word, Markov.q.second_wordID == second_word))
            hits=list(hits)
            choice = hits[int(random.random()*len(hits))]
            #choice = self.pickBestChoice(hits)
            second_word = choice.second_word.id
            third_word = choice.third_word.id
        # Next the reverese chain keyword -> start
        first_half=[]
        first_word = base.first_word.id
        second_word = base.second_word.id
        while first_word !=1:
            first_half.append(first_word)
            hits = Markov.select(AND(Markov.q.second_wordID == first_word, Markov.q.third_wordID == second_word))
            hits = list(hits)
            choice = hits[int(random.random()*len(hits))]
            first_word = choice.first_word.id
            second_word= choice.second_word.id
        #Merge the halves together
        first_half.reverse()
        first_half.extend(second_half)
        #self.debug('first_half:%s' % first_half)
        return first_half
        
    def pickBestChoice(self, choice_list):
        """Return the most grammatically sound choice from the list
           TODO refactor me
        """
        if len(choice_list) == 1: return choice_list[0]
        probabilities = []
        for choice in choice_list:
            (first, second, third) = [choice.first_word.main_type.id, 
                                      choice.second_word.main_type.id,
                                      choice.third_word.main_type.id]
            tm = MarkovLex.select(AND(MarkovLex.q.first_lexID == first,
                                      MarkovLex.q.second_lexID == second,
                                      MarkovLex.q.third_lexID == third))
            this_mlex=list(tm)[0]

            mlex = MarkovLex.select(AND(MarkovLex.q.first_lexID == first,
                                        MarkovLex.q.second_lexID == second))
            mlex_hits = list(mlex)
            total_occurences = reduce(lambda x, y:x+y, [x.occurence for x in mlex_hits])
            #self.debug('my occurences:%d' % this_mlex.occurence)
            #self.debug('total_occurences:%d' % total_occurences)
            prob = float(float(this_mlex.occurence) / float(total_occurences))
            #self.debug('prob:%f' % prob)
            probabilities.append(prob)
        if probabilities: 
            best_choice = probabilities.index(max(probabilities))
            return choice_list[best_choice]
        else:
            return ''
            
   
    def debug(self, debug_string):
        """Output debug string
        """
        if self.DEBUG==1:print debug_string
        return None

