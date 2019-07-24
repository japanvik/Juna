#!/usr/bin/python
#! -*- coding: utf-8 -*-
from juna_msn import JunaMsn
from JunaMemory import JunaMemory
from Brain import Brain
from config import MSN_ID, MSN_PW
from lib.Event import Event, EventDispatcher

class Juna:
    def __init__(self):
        self.dispatcher = EventDispatcher()
        self.memory = JunaMemory(self.dispatcher)
        self.brain = Brain(self.dispatcher)
        self.msn = JunaMsn(MSN_ID, MSN_PW, self.dispatcher)
        self.msn.start()
        self.msn.join()

juna = Juna()

