#!/usr/bin/env python2

"""
hs.py

Defines logistical functions for executing
the HS algorithm and serves as the top-level
executable script.

Kat Cannon-MacMartin | Marlboro College
guthrie@marlboro.edu

Usage:
lcr creates a collection of processes
with unique UIDs, and arranges them randomly in
a ring structure. The processes then work to elect
a leader based on the HS protocol. Upon completion
of the algorithm, the program prints some information
about the processes, arranged in the order in which they
appear in the ring.

The program can be invoked with zero, one, or two arguments.
With zero arguments:
> python hs.py
The program will create 6 processes with UIDs 1 through 6

With one argument:
> python hs.py x
The program will create x processes with UIDs 1 through x

With two arguments:
> python hs.py x y
The program creates (y - x) processes, in a similar
manner to the python range() function, with 
UIDs x through (y - 1)
"""

from src.ring import *

def protocol(node):
    """
    protocol(Node node)
    
    The absolute top-level function for each individual
    process in the HS algorithm. protocol loops as long
    as the process does not know its own leader status,
    executing the node's internal recieve and send message
    functions and recording total recieved/sent messages.

    Returns: node.status variable of the Status enumerator type.
                         At this point in the algorithm possible
                         values are Status.LEADER or Status.NOTLEADER
    """
    recsent = [0, 0]
    while node.status == Status.UNKNOWN:
        for direc in [mq.PLUS, mq.MINUS]:
            recsent[1] += node.sendm(direc)
        recsent[0] += node.rec()
        
    for final in [mq.PLUS, mq.MINUS]:        # After the node exits the while loop
        recsent[1] += node.sendm(final)      # of the main algorithm, the queued L_DECLARE
                                             # messages are sent before it finishes
    node.ret[node.u] = [node.status, recsent, node.phase]  # Analytical information is stored in the
                                                           # inter-process shared dictionary
    return node.status

def main(low, high, py_out=False):
    low = int(low)                       # low is the smallest UID
    high = int(high)                     # high is the greatest UID + 1
    if low == high:                      # if low and high were not both provided by the user
        if low == 0: low = 1; high = 7   # if neither were provided, default to UIDS 1 through 6
        else: low = 1; high += 1         # if only one value was provided, use that as the max UID
    n = high - low
    manager = mp.Manager()
    uids = list(range(low, high))
    ring = copy.deepcopy(uids)
    qs = []
    procs = []
    nodes = []
    retdict = manager.dict()
    leader_index = None

    # Shuffles the order of the ring so process will not be
    # arrenged in order of UID
    random.shuffle(ring)

    # This block creates and correctly links the message queues
    # for each process
    for i in range(n):
        qs.append([mp.Queue(), mp.Queue()])
        nodes.append(Node(ring[i], qs[i], None, retdict))
    for i in range(n):
        nodes[i].oq = [qs[(i + 1) % n][1], qs[(i - 1) % n][0]]
        procs.append(mp.Process(target=protocol, args=(nodes[i],)))

    # Starts and joins all processes
    for i in range(n):
        procs[i].start()
    for i in range(n):
        procs[i].join()
        if retdict[ring[i]][0] == Status.LEADER:
            leader_index = i

    if py_out:
        mutable_dict = copy.deepcopy(retdict)
        for proc in uids:
            mutable_dict[proc][0] = ev(mutable_dict[proc][0])
        sys.stdout.write(str(mutable_dict))
        sys.stdout.flush()
    else:
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
