#!/usr/bin/python
import threading

class Event(object):
    event = ''
    action = None

    def __init__(self, event, action):
        self.event = event
        self.action = action


class EventDispatcher(object):
    """"Event Dispatcher"""
    def __init__(self, targets=None, nonBlocking=True):
        if not targets or targets is None:
            self._targets = []
        else:
            self._targets = targets
        self._nonBlocking = nonBlocking

    def __iadd__(self, target):
        self._targets.append(target)
        return self

    def __isub__(self, target):
        self._targets.remove(target)
        return self

    def isNonBlocking(self):
        return self._nonBlocking
    nonBlocking = property(isNonBlocking)

    def __call__(self, msg, *listArgs, **kwArgs):
        def invokeTargets():
            for target in [x.action for x in self._targets if x.event == msg]:
                target(*listArgs, **kwArgs)
        if self.nonBlocking:
            threading.Timer(0, invokeTargets).start()
        else:
            invokeTargets()


