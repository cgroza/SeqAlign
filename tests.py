from alignment import *

# Test sequences
T1 = "GAATC"
T2 = "CATAC"

# Alignment

a = Alignment(T1, T2)

# Global alignment test
print a.GlobalTraceback()
# Local alignment test
print a.LocalTraceback()
