#!/usr/bin/env python2

"""
hs.py
"""

from src.ring import *

def protocol(node):
    recsent = [0, 0]
    while node.status == Status.UNKNOWN:
        for direc in [mq.PLUS, mq.MINUS]:
            recsent[1] += node.sendm(direc)
        recsent[0] += node.rec()
        
    for final in [mq.PLUS, mq.MINUS]:
        recsent[1] += node.sendm(final)
    node.ret[node.u] = (node.status, recsent, node.phase)
    return node.status

def main(low, high):
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
    leader_index = None

    random.shuffle(ring)
    for i in range(n):
        qs.append([mp.Queue(), mp.Queue()])
        nodes.append(Node(ring[i], qs[i], None, retdict))
    for i in range(n):
        nodes[i].oq = [qs[(i + 1) % n][1], qs[(i - 1) % n][0]]
        procs.append(mp.Process(target=protocol, args=(nodes[i],)))
    for i in range(n):
        procs[i].start()
    for i in range(n):
        procs[i].join()
        if retdict[ring[i]][0] == Status.LEADER:
            leader_index = i
        
    print "Ring structure:"
    print "------------------------------------"
    for j in range(n):
        i = (j + leader_index) % n
        print "   Node", ring[i]
        print "  ", retdict[ring[i]][0].name
        print "   (rec, sent):", retdict[ring[i]][1]
        print "   phase:", retdict[ring[i]][2]
        print "------------------------------------"

if __name__=="__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1], sys.argv[1])
    elif len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        main(0, 0)
