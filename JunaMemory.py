#! -*- coding: utf-8 -*-
from lib.Event import Event
from TextAnalyzer import TextAnalyzer
from Log import Log
from Sentence import Sentence
from sqlobject import *
from config import DB_URI

#Database Connection
connection = connectionForURI(DB_URI)
sqlhub.processConnection = connection

class JunaMemory(object):
    """Stores the various queues for Juna """
    topics = []
    recent_logs = []
    recent_spoken = []

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.dispatcher += Event('rcv', self.rSentence)
        self.dispatcher += Event('send', self.sSentence)

        self.analyzer = TextAnalyzer()

    def rSentence(self, msg, dummy):
        """Somebody talked"""
        if msg:
            self.recent_logs.append(msg)
            #FIFO style queue
            if len(self.recent_logs)>10:self.recent_logs.pop(0)

            #update the topic queue = extractTopics + relatedWords of the first topic word
            topic_cands = self.analyzer.extractTopics(self.recent_logs)
            if topic_cands:
                related_words=self.analyzer.extractTopics(self.getRelatedLogs(topic_cands[0]))
                self.topics = list(set(topic_cands) | set(related_words) | set(self.topics)) #Union
                #Truncate topics to max 8 words
                self.topics = self.topics[:8]
            #Notify the event dispatcher
            self.dispatcher('speak_request', self.recent_logs, self.recent_spoken, self.topics)


    def sSentence(self, msg):
        """I talked!"""
        self.recent_spoken.append(msg)
        if len(self.recent_spoken)>20:self.recent_spoken.pop(0)
        #Notify the dispatcher
        self.dispatcher('log', self.recent_spoken)


    def getRelatedLogs(self, word_id):
        """Return a list of logs based on the word_id
        """
        if not word_id:return []
        big_log=[]
        all_matching_logs = Log.select("Log.entry LIKE '%%\|%s\|%%' OR Log.entry LIKE '%%\|%s' OR Log.entry LIKE '%s\|%%'" % tuple([str(word_id)]*3))
        if all_matching_logs:
            for log in list(all_matching_logs):
                rows = Log.select(id > log.id)[:4]
                if rows:
                    for row in list(rows):
                        big_log.append(row.entry)

        readable_logs=[]
        for log in big_log:
            sentence = Sentence()
            sentence.createFromIDs(log.split('|'))
            readable_logs.append(sentence.readable())
        return readable_logs

