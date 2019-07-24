#! -*- coding: utf-8 -*-
from MessageParser import MessageParser
from Sentence import Sentence
from Word import Word
import math
import random


class TextAnalyzer:
    """ A text Analyzer """
    parser = MessageParser()


    def extractTopics(self, text_list, threshold=0.5):
        """ Return a list of Words which seems to be the current topic """
        if not text_list:return []
        #Make pseudo sentences from the text_list
        pCandidates=[]
        for message in text_list:
            pSentence=self.parser.parseSentence(message)
            if not pSentence:return []
            #pick out only the Candidates from the pseudo words
            candidates = [x for x in pSentence if x['main_type'] in [u'名詞']]
            #print 'candidates:%s' % candidates
            #pCandidates is a list of pseudo words which are candidates of the topic
            if candidates:pCandidates.extend(candidates)
            #print 'pCandidates:%s' % pCandidates
        #Next we make a dictionary of occurences of this particular candidates
        #Convert the pseudo words to real words
        true_candidates = Sentence()
        true_candidates.pseudo2real(pCandidates)
        #print 'true_candidates:%s' % true_candidates.words
        #make a dictionary {word_id:occurence}
        sample_words={}
        for w in true_candidates:
            if sample_words.has_key(int(w.id)):
                sample_words[int(w.id)]+=1
            else:
                sample_words[int(w.id)]=1
        
        if len(sample_words)<1:return []
        #print 'sample_words:%s' % sample_words

        #We make the actual occurences from the database
        base_words={}
        for word_id in sample_words.keys():
            base_words[word_id]=Word.get(word_id).occurence
            

        sample_count=0
        for k,v in sample_words.iteritems():
            sample_count+=v
        
        base_count = 0
        for k,v in base_words.iteritems():
            base_count+=v
            
        scores={}
        for w in sample_words.keys():
            scores[w]=self.score(float(sample_words[w]), float(sample_count), float(base_words[w]), float(base_count))
            
        items = [(v, k) for k, v in scores.items()]
        items.sort()
        items.reverse()             # so largest is first
        candidate_keywords = [x[1] for x in items if x[0] > threshold]
        #Fallback - if no topics are found, we choose a random noun
        # Yucky, but makes Juna more talkative.
        if (not candidate_keywords) and (candidates):
            choice = [candidates[int(random.random()*len(candidates))]]
            s = Sentence()
            s.pseudo2real(choice)
            candidate_keywords=[s[0].id]
        return candidate_keywords

    def score(self, sample_occurence, sample_count, base_occurence, base_count):
        """Scoring for relavance """

        if base_count==sample_count:return None
        #print 'score_vars::s_occ:%d s_count:%d b_occ:%d b_count:%d' % (sample_occurence, sample_count, base_occurence, base_count)
        return math.tanh(sample_occurence/sample_count*200) -5*math.tanh((base_occurence-sample_occurence)/(base_count-sample_count)*200)

