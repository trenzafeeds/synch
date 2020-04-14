"""
header.py
Just managing the import
statements for other code.
"""

import multiprocessing as mp
from enum import Enum
import random
import copy
import sys

# Also some utility functions below

def ev(enumerator):
    return enumerator.value

def en(enumerator):
    return enumerator.name

def otherv(benumerator):
    return (benumerator.value - 1) % 2
