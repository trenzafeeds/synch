"""
ring.py
For organizing the ring structure
of the HS algorithm.

Kat Cannon-MacMartin
"""

from mail import *

class Status(Enum):
    UNKNOWN = 0
    LEADER = 1
    NOTLEADER = 2

class Node:

    def __init__(self, uid, iq, oq, ret):
        self.u = uid
        self.send = [Message(self.u, mf.OUT, 1),\
                     Message(self.u, mf.OUT, 1)]
        self.status = Status.UNKNOWN
        self.iq = iq
        self.oq = oq
        self.phase = 0
        self.phase_counter = 0
        self.ret = ret

    # Returns 1 for message sent, 0 for none sent
    def sendm(self, direction):
        if self.send[ev(direction)] != None:
            self.oq[ev(direction)].put(self.send[ev(direction)])
            self.send[ev(direction)] = None
            return 1
        else:
            return 0

    def process_m(self, message, fromdirec):
        if message.flag == mf.L_DECLARE:
            self.status = Status.NOTLEADER
            for outdir in [mq.PLUS, mq.MINUS]:
                self.send[ev(outdir)] =\
                Message(message.uid, mf.L_DECLARE, -1)
            return -1
        elif message.flag == mf.OUT:
            if message.uid > self.u:
                if message.hopc > 1:
                    self.send[otherv(fromdirec)] =\
                    Message(message.uid, mf.OUT, message.hopc - 1)
                elif message.hopc == 1:
                    self.send[ev(fromdirec)] =\
                    Message(message.uid, mf.IN)
            elif message.uid == self.u:
                self.status = Status.LEADER
                for outdir in [mq.PLUS, mq.MINUS]:
                    self.send[ev(outdir)] =\
                    Message(self.u, mf.L_DECLARE, -1)
                return -1
        else:
            if message.uid != self.u:
                self.send[otherv(fromdirec)] =\
                Message(message.uid, mf.IN)
            else:
                return 0
        return 1

    def rec(self):
        rec_count = 0
        for direction in [mq.PLUS, mq.MINUS]:
            if not self.iq[ev(direction)].empty():
                currentm = self.iq[ev(direction)].get()
                rec_count += 1
                if not self.process_m(currentm, direction):
                    self.phase_counter += 1
                elif self.status != Status.UNKNOWN:
                    return rec_count
                    
        if self.phase_counter == 2:
            self.phase_counter = 0
            self.phase += 1
            for outdir in [mq.PLUS, mq.MINUS]:
                self.send[ev(outdir)] =\
                Message(self.u, mf.OUT, 2**self.phase)

        return rec_count
            
