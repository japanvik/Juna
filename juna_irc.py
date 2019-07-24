#!/usr/bin/python
#! -*- coding: utf-8 -*-

from lib.testbot import TestBot
from Brain import Brain

class Juna(TestBot):
    def __init__(self, channel, nickname, server, port=6667):
        self.brain = Brain()
        self.message_que=[]
        self.my_que=[]
        self.topic_que=[]
        TestBot.__init__(self, channel, nickname, server, port)


        
    def on_pubmsg(self, c, e):
        incoming_message = unicode(e.arguments()[0], 'utf-8')
        sentence = self.brain.learn(incoming_message)
        if sentence:self.message_que.append(incoming_message)
        if len(self.message_que) > 10:self.message_que.pop(0)
        self.speak(c)
        """
        print '---pubq---'
        for pubq in self.message_que:print pubq
        print '---myq---'
        for myq in self.my_que:print myq
        """
        return

    def speak(self,c):
        """Speak something!
        """
        final_output=self.brain.getMessageString(self.message_que, self.my_que, self.topic_que)
        if final_output:
            c.privmsg(self.channel, final_output[0].encode('utf-8'))
            message_que=final_output[1]
            my_que=final_output[2]
            topic_que=final_output[3]

        
def main():
    channel='#Test'
    nickname='Juna'
    server='mail'
    port=6667
    juna = Juna(channel, nickname, server, port)
    juna.start()

if __name__ == "__main__":
    main()
