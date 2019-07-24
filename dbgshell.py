#!/usr/bin/python
# -*- coding: utf-8 -*-
from config import DB_URI
from sqlobject import *
import code

"""Debug Shell to access the site"""
connection = connectionForURI(DB_URI)
sqlhub.processConnection = connection

code.interact(banner='Juna Debug Shell')

