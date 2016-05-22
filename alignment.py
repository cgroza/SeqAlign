# Test sequences
T1 = "GAATC"
T2 = "CATAC"

# Used to map sequence elements to their coordinate in the substitution matrix
baseToInt = {'A' : 0, 'C' : 1, 'G' : 2, 'T' : 3}

# Substitution matrix
sub = [
#    A    C  G   T
    [10, -5, 0, -5], # A
    [-5, 10, -5, 0], # C
    [0, -5, 10, -5], # G
    [-5, 0, -5, 10]  # T
]
# Gap penalty
d = -4

# Recursive method, not the most efficient
def V(i, j, s1, s2):
    # This condition prevents infinite recursion. This happens because the
    # corner cases of V(0, j) and V(i, 0) are not properly handled in the
    # maximizing list
    if j != 0 and i == 0:
        return V(i, j -1, s1, s2) + d
    elif i != 0 and j == 0:
        return V(i - 1, j, s1, s2) + d
    # Base case.
    if i == 0 and j == 0:
        return 0;
    # Maximization list of all the recursive paths
    return max([V(i - 1, j - 1, s1, s2) + sub[baseToInt[s1[i]]][baseToInt[s2[j]]],
                V(i, j - 1, s1, s2) + d,
                V(i - 1, j, s1, s2) + d])

# Matrix method, most efficient
def F(i, j, s1, s2):
    pass

# Creates visual visualization of V(i, j) values for all pairs of V(i, j)
def CreateMatrix(seq1, seq2):
    matrix = [['a' for x in range(len(seq1))] for y in range(len(seq2))]
    for n in range(len(seq2)):
        for m in range(len(seq1)):
            matrix[n][m] = V(m, n, seq1, seq2)
    return matrix

# Basic pretty printing function
def PrintMatrix(m):
    for row in m:
        print row

# Sanitizes the input
def FindMaxV(s1, s2):
    # Since sequences are indexed from 1 ... and strings are indexed from 0
    # ... spaces are added to realign the sequence indexes with the string
    # indices.
    return V(len(s1), len(s2), " " + s1, " " + s2)
