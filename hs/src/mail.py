"""
mail.py
Enumerators and a class definition
for inter-process messaging.

Kat Cannon-MacMartin
"""

from header import *

# Enumerators

# Message flag
class mf(Enum):
    IN = 0           # Inbound message
    OUT = 1          # Outbound message
    L_DECLARE = 3    # Special message type for ending
                     # the algorithm and declaring a leader

# Flag to differentiate
# message queue directions
class mq(Enum):     
    PLUS = 0
    MINUS = 1

    
# Message class
class Message:
    def __init__(self, uid, flag, hopc=1):
        self.uid = uid    # UID of sender
        self.flag = flag  # mf enumerator
        self.hopc = hopc  # Hop count (decreased each send)
