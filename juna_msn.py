#! -*- coding: utf-8 -*-
import sys
import time
import select
import threading
from lib import msnlib, msncb
from config import MSN_NICK
from lib.Event import Event

class JunaMsn(threading.Thread):

    """
    MSN implementation for Juna
    """

    def __init__(self, email, pwd, dispatcher):
        """
        Initialize function
        Login and set the initial state.
        """
        threading.Thread.__init__(self)
        msnlib.debug=debug
        msncb.debug=debug
        self.m = msnlib.msnd()
        self.m.cb = msncb.cb()
        self.m.encoding='utf-8'
        self.m.email = email
        self.m.pwd = pwd
        self.message = ''
        self.last_recvd_from=''
        self.m.cb.msg=self.cb_msg
        #Event stuff
        self.dispatcher = dispatcher
        #register callbacks
        self.dispatcher += Event('speak', self.send)

        print 'Logging in...'
        self.m.login()
        print 'Syncing...'
        self.m.sync()
        time.sleep(10)
        print 'Changing Status'
        self.m.change_status('online')
        # Change nick accordingly
        my_nick = MSN_NICK.encode('utf-8')
        if self.m.nick != msnlib.nickquote(my_nick):
            #my nick has changed, so update it
            print 'Changing nick to %s' % my_nick
            self.m.change_nick(my_nick)

    def send(self, msg):
        """Send a message"""
        #r = self.m.sendmsg(self.last_recvd_from, msg.encode('utf-8'))
        r = self.m.sendmsg('wockywock@msn.com', msg.encode('utf-8'))

    def run(self):
        """
        The main loop
        """
        while 1:
            fds = self.m.pollable()
            infd = fds[0]
            outfd = fds[1]
            #infd.append(sys.stdin)
            try:
                fds = select.select(infd, outfd, [], None)
            except KeyboardInterrupt:
                self.quit()
            for i in fds[0] + fds[1]:       # see msnlib.msnd.pollable.__doc__
                 self.m.read(i)


    def quit(self):
        try:
            self.m.disconnect()
        except:
            pass
        print "Exit"
        sys.exit(0)

    def cb_msg(self, md, type, tid, params, sbd):
        t = tid.split(' ')
        email = t[0]
        # parse
        lines = params.split('\n')
        headers = {}
        eoh = 0
        for i in lines:
            # end of headers
            if i == '\r': break
            tv = i.split(':', 1)
            type = tv[0]
            value = tv[1].strip()
            headers[type] = value
            eoh += 1
        eoh +=1

        # Ignore everythin which is not a message
        if headers['Content-Type'] in ['text/x-msmsgsinitialemailnotification; charset=UTF-8', 'text/x-msmsgscontrol', 'text/x-clientcaps']:
            pass
        else:
            # Messages are all UTF-8 in msn
            self.message = unicode(''.join([x.strip() for x in lines[eoh:]]), 'utf-8')
            self.last_recvd_from = email
            #Call the dispatcher with a rcv message
            #print 'msn:msg:%s' % self.message.encode('utf-8')
            self.dispatcher('rcv', self.message, self.last_recvd_from)
        
        msncb.cb_msg(md, type, tid, params, sbd)

def debug(s):
    pass

def main():
    msn = JunaMsn()

if __name__ == "__main__":
    main()

