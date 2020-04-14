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

"""
Below are some utility functions for
dealing with Enumerator classes.
"""

def ev(enumerator):
    return enumerator.value

def en(enumerator):
    return enumerator.name

def otherv(benumerator):
    return (benumerator.value - 1) % 2
