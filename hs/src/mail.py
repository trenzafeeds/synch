"""
mail.py
For facilitation the messaging
of the HS algorithm.

Kat Cannon-MacMartin
"""

from header import *

# Message Flags
class mf(Enum):
    IN = 0
    OUT = 1
    L_DECLARE = 3

# Message queues
class mq(Enum):
    PLUS = 0
    MINUS = 1
    
class Message:

    def __init__(self, uid, flag, hopc=1):
        self.uid = uid
        self.flag = flag
        self.hopc = hopc
