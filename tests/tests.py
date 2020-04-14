"""
tests.py

Script for collecting test/analytical
data on synchronous algorithms.

Kat Cannon-MacMartin | Marlboro College
guthrie@marlboro.edu
"""

import sys
import os

def generate_paths(logfile=None):
    paths_dict = {}
    paths_dict['test'] = os.path.dirname(os.path.realpath(__file__))
    paths_dict['hs'] = paths_dict['test'] + '/../hs/hs.py'
    paths_dict['lcr'] = paths_dict['test'] + '/../lcr/lcr.py'
    if logfile != None: paths_dict['log'] = logfile
    else: paths_dict['log'] = paths_dict['test'] + '/log'
    return paths_dict

def echo_write(fpath, write_string):
    write_string = "'" + write_string + "'"
    return os.system("echo " + write_string + " >> " + fpath)

def main(bottom, top, reps=10):
    bottom = int(bottom)
    top = int(top)
    reps = int(reps)
    paths = generate_paths()

    if os.path.isfile(paths['log']):
        print "Deleting previous log file, hope you saved it!"
        os.system("rm " + paths['log'])
    
    for p_count in xrange(bottom, top):
        echo_write(paths['log'], "--" + str(p_count))
        for alg in ['lcr', 'hs']:
            print "*** Starting " + alg + " with " + str(p_count) + " processes... ***"
            for i in xrange(reps):
                cmnd = "python " + paths[alg] + " -p " + str(p_count) + " >> " + paths['log']
                print cmnd
                os.system(cmnd)
                echo_write(paths['log'], "")
    return 0
            
if __name__ == "__main__":
    if len(sys.argv) > 2:
        if len(sys.argv) > 3:
            main(sys.argv[1], sys.argv[2], sys.argv[3])
        else:
            main(sys.argv[1], sys.argv[2])
    else:
        print "Error: Not enough arguments."
        sys.exit(1)
