"""
lcr.py
Toy version of the LCR 
algorithm in Python

Kat Cannon-MacMartin | Marlboro College
guthrie@marlboro.edu

Usage:
lcr creates a collection of processes
with unique UIDs, and arranges them randomly in
a ring structure. The processes then work to elect
a leader based on the LCR protocol. Upon completion
of the algorithm, the program prints some information
about the processes, arranged in the order in which they
appear in the ring.

The program can be invoked with zero, one, or two arguments.
With zero arguments:
> python lcr.py
The program will create 6 processes with UIDs 1 through 6

With one argument:
> python lcr.py x
The program will create x processes with UIDs 1 through x

With two arguments:
> python lcr.py x y
The program creates (y - x) processes, in a similar
manner to the python range() function, with 
UIDs x through (y - 1)
"""

import multiprocessing as mp
from enum import Enum
import random
import copy
import sys

class Status(Enum):
    UNKNOWN = 0
    LEADER = 1
    NOTLEADER = 2

class Message:

    def __init__(self, val):
        self.mtype = None
        self.val = val
        if val == 0: self.mtype = "finish"
        else: self.mtype = "update"

class Node:

    def __init__(self, uid, iq, oq, ret):
        self.send = Message(uid)
        self.status = Status(0)
        self.u = uid
        self.oq = oq
        self.iq = iq
        self.ret = ret

    def rec(self, message):
        self.send = None
        if message.mtype == "finish":
            self.send = Message(0)
            self.status = Status(2)
            return 0
        else:
            if message.val > self.u: self.send = Message(message.val)
            elif message.val == self.u:
                self.send = Message(0)
                self.status = Status(1)
                return 0
            else: pass
            return 1

def protocol(node):
    recsent = [0, 0]
    while node.status == Status.UNKNOWN:
        if node.send != None:
            recsent[1] += 1
            node.oq.put(node.send)
            node.send = None
        if not node.iq.empty():
            recsent[0] += 1
            if not node.rec(node.iq.get()):
                recsent[1] += 1
                node.oq.put(node.send)

    node.ret[node.u] = [node.status, recsent]
    return node.status

def main(low, high, py_out=False):
    low = int(low)
    high = int(high)
    if low == high:
        if low == 0: low = 1; high = 7
        else: low = 1; high += 1
    manager = mp.Manager()
    uids = list(range(low, high))
    ring = copy.deepcopy(uids)
    n = len(uids)
    qs = []
    procs = []
    nodes = []
    retdict = manager.dict()

    random.shuffle(ring)
    for i in range(n):
        qs.append(mp.Queue())
        nodes.append(Node(ring[i], qs[i], None, retdict))
    for i in range(n):
        nodes[i].oq = qs[(i + 1) % n]
        procs.append(mp.Process(target=protocol, args=(nodes[i],)))
    for i in range(n):
        procs[i].start()
    for i in range(n):
        procs[i].join()
        if retdict[ring[i]][0] == Status.LEADER:
            leader_index = i

    if py_out:
        mutable_dict = copy.deepcopy(retdict)
        for proc in uids:
            mutable_dict[proc][0] = mutable_dict[proc][0].value
        sys.stdout.write(str(mutable_dict))
        sys.stdout.flush()
    else:
        print "Ring structure:"
        for j in range(n):
            i = (j + leader_index) % n
            print "   ", ring[i], "--"
            print "   ", retdict[ring[i]][0]
            print "   (rec, sent):", retdict[ring[i]][1]
            print "|"

if __name__=="__main__":
    py_out = False
    ao = 0          # ao short for Argument Offset
    if len(sys.argv) > 1:
        try: int(argv[1])
        except:
            if sys.argv[1] in ["-p", "--python"]:
                py_out = True
                ao = 1
            else:
                print "Error: invalid argument:", argv[1]
        if len(sys.argv) == 2 + ao:
            main(sys.argv[1 + ao], sys.argv[1 + ao], py_out)
        elif len(sys.argv) == 3 + ao:
            main(sys.argv[1 + ao], sys.argv[2 + ao], py_out)
        else:
            main(0, 0, py_out)
    else:
        main(0, 0, py_out)
