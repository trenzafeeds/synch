"""
analysis.py

Reads and graphs data from tests.py.

Kat Cannon-MacMartin | Marlboro College
guthrie@marlboro.edu
"""

import sys
import os
import ast

class Data:
    
    def __init__(self):
        self.inf = {}
        self.cnt = None
        self.alg = None

    def new_count(self, inline):
        count = int(inline)
        self.inf[count] = {}
        self.cnt = count
        return 0
        
    def new_alg(self, inline):
        if self.cnt:
            self.inf[self.cnt][inline] = []
            self.alg = inline
        else:     
            print "Unexpected error!"
            sys.exit(1)
        return 0

    def new_result(self, inline):
        if self.cnt and self.alg:
            dict_string = inline.rstrip()
            self.inf[self.cnt][self.alg]\
                .append(ast.literal_eval(dict_string))
        else:
            print "Unexpected error!"
            sys.exit(1)
        return 0

    def process_line(self, raw_line):
        if raw_line[0:2] == "--":
            self.new_count(raw_line[2:])
        elif raw_line[0:2] == "..":
            self.new_alg(raw_line[2:].rstrip())
        else:
            self.new_result(raw_line)
        return 0

    
        
def main(infile):
    if infile == None:
        infile = os.path.dirname(os.path.realpath(__file__)) + "/log"

    log = open(infile, "r")
    data = Data()
    
    line = log.readline()
    while line:
        data.process_line(line)
        line = log.readline()

    return 0
        
if __name__=="__main__":
    if len(sys.argv) > 1:
        if os.path.exists(argv[1]):
            main(argv[1])
        else:
            print "Error: invalid log file provided as argument."
            sys.exit(1)
    else:
        main(None)
