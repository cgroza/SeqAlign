from alignment import *
from ultm import *
from binarytree import pprint

def doTests():
    # Test sequences
    T1 = "GAATC"
    T2 = "CATAC"

    print "S1: " + T1
    print "S2: " + T2

    # Alignment
    a = Alignment(T1, T2)

    # Global alignment test
    print "Global alignment: " + str(a.GlobalTraceback())
    # Local alignment test
    print "Local alignment: " + str(a.LocalTraceback())
    # End gap alignment tests
    print "End gap alignment: " + str(a.EndGapTraceback())

    print "\n Ultramtric Tree Test:"
    print test_matrix
    pprint(make_tree(test_matrix))

    return a
