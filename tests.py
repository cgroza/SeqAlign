from alignment import *

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
