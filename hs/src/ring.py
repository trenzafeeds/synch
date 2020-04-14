
"""
ring.py
Definition of the Node class, which
defines the functions executed by
each individual process.

Kat Cannon-MacMartin
"""

from mail import *

# Flag for each process to internally store
# leader information.
class Status(Enum):
    UNKNOWN = 0
    LEADER = 1
    NOTLEADER = 2

class Node:

    def __init__(self, uid, iq, oq, ret):
        self.u = uid                               # Process UID
        self.send = [Message(self.u, mf.OUT, 1), Message(self.u, mf.OUT, 1)]
                                                   # send array has two entries corresponding
                                                   # to [direction +, direction -]. It is
                                                   # initialized with first-round messages for
                                                   # each direction.
        self.status = Status.UNKNOWN               # Internal leader information
        self.iq = iq                               # iq array has two entries, both of them in-bound
                                                   # message queues, with [direction +, direction -]
        self.oq = oq                               # oq array is similar to iq, but for out-bound
        self.phase = 0                             # current internal phase of the HS algorithm
        self.phase_counter = 0                     # counts recieved messages that meet the qualifications
                                                   # to trigger a change of phase. 
        self.ret = ret                             # ret is actually an inter-process shared dictionary used
                                                   # to record analytical data for each node in the format:
                                                   # ret[UID] = (final status,
                                                   #             [messages recieved, messages sent],
                                                   #             final phase)


    def sendm(self, direction):
        """
        Node.sendm(int direction)

        Places the message currently stored in Node.send[direction]
        in the message queue stored in Node.oq[direction], then
        clears the sent message from Node.send.
        
        Returns: 1 if message was sent 
                 0 if no message was sent.
        """
        if self.send[ev(direction)] != None:
            self.oq[ev(direction)].put(self.send[ev(direction)])
            self.send[ev(direction)] = None
            return 1
        else:
            return 0

    def process_m(self, message, fromdirec):
        """
        Node.process_m(Message message, int fromdirec)
        
        Uses information from message and fromdirec to
        take some combination of the following actions:
         - place messages in Node.oq
         - propogate information upwards to trigger changes in
           Node.phase_counter and Node.phase
         - update Node.status
        process_m uses the exact protocol for the HS
        algorithm provided on Page 33 of Lynch's
        Distributed Algorithms.

        Returns: -1 if Node.status was updated
                  0 if the message was inbound with
                    uid equal to the uid of Node
                  1 for all other successful executions
        """
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
        """
        Node.rec()
        
        Handles incoming messages one level higher than process_m.
        Executes process_m on one message from each direction in
        iq (if available). Then, using the recieved return values,
        updates Node.phase if required and handles creating the
        outbound messages corresponding to the new phase. Also
        propogates data on the number of recieved messages upwards
        for storage.

        Returns: rec_count variable containing number of messages
                           recieved (min 0, max 2).
        """
        rec_count = 0
        for direction in [mq.PLUS, mq.MINUS]:
            if not self.iq[ev(direction)].empty():
                currentm = self.iq[ev(direction)].get()
                rec_count += 1
                if not self.process_m(currentm, direction):   # When Node recieves one of
                    self.phase_counter += 1                   # its own message inbound 
                elif self.status != Status.UNKNOWN:
                    return rec_count
                    
        if self.phase_counter == 2:                           # After recieving two of its
            self.phase_counter = 0                            # own messages inbound, Node.phase
            self.phase += 1                                   # is updated and new outbound messages
            for outdir in [mq.PLUS, mq.MINUS]:                # with a longer trajectory (higher
                                                              # starting hopc value) are sent
                self.send[ev(outdir)] = Message(self.u, mf.OUT, 2**self.phase)

        return rec_count
            
