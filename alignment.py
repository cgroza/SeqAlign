from itertools import izip
# Test sequences
T1 = "GAATC"
T2 = "CATAC"

# Used to map sequence elements to their coordinate in the substitution matrix
b2i = {'A' : 0, 'C' : 1, 'G' : 2, 'T' : 3}

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

# Local alignment function. Recursive method
def LocalAlign(i, j, s1, s2):
    # Base cases
    if i == 0 or j == 0:
        return 0
    # Maximization list of all the recursive paths
    return max([LocalAlign(i - 1, j - 1, s1, s2) + sub[b2i[s1[i]]][b2i[s2[j]]],
                LocalAlign(i, j - 1, s1, s2) + d,
                LocalAlign(i - 1, j, s1, s2) + d])

def LocalAlignMatrix(i, j, s1, s2):
    # j is row number, i is column number
    matrix = [[0 for x in range(len(s1))] for y in range(len(s2))]
    # Fill first horizontal row
    for k in range(0, i + 1):
        matrix[0][k] = 0
    # Fill first vertical column
    for k in range(0, j + 1):
        matrix[k][0] = 0
    # Iterate column by column and fill cells
    for z in range(1, i + 1):
        for k in range(1, j + 1):
            matrix[k][z] = max ([matrix[k - 1][z - 1] + sub[b2i[s1[z]]][b2i[s2[k]]],
                                 matrix[k - 1][z] + d,
                                 matrix[k][z - 1] + d])
    return matrix

# Recursive method, not the most efficient
def GlobalAlign(i, j, s1, s2):
    # This condition prevents infinite recursion. This happens because the
    # corner cases of V(0, j) and V(i, 0) are not properly handled in the
    # maximizing list
    if j != 0 and i == 0:
        return GlobalAlign(i, j -1, s1, s2) + d
    elif i != 0 and j == 0:
        return GlobalAlign(i - 1, j, s1, s2) + d
    # Base case.
    if i == 0 and j == 0:
        return 0
    # Maximization list of all the recursive paths
    return max([GlobalAlign(i - 1, j - 1, s1, s2) + sub[b2i[s1[i]]][b2i[s2[j]]],
                GlobalAlign(i, j - 1, s1, s2) + d,
                GlobalAlign(i - 1, j, s1, s2) + d])

# Matrix method, most efficient
def GlobalAlignMatrix(i, j, s1, s2):
    # j is row number (s2), i is column number (s1)
    matrix = [[0 for x in range(len(s1))] for y in range(len(s2))]
    # Fill first horizontal row
    for k in range(0, i + 1):
        matrix[0][k] = k * d
    # Fill first vertical column
    for k in range(0, j + 1):
        matrix[k][0] = k * d
    # Iterate column by column and fill cells
    for z in range(1, i + 1):
        for k in range(1, j + 1):
            matrix[k][z] = max ([matrix[k - 1][z - 1] + sub[b2i[s1[z]]][b2i[s2[k]]],
                                 matrix[k - 1][z] + d,
                                 matrix[k][z - 1] + d])
    return matrix

def GlobalTraceBack(i, j, s1, s2, matrix):
    s1Aligned = ""
    s2Aligned = ""
    while i > 0 and j > 0:
       if matrix[j][i] == matrix[j - 1][i - 1] + sub[b2i[s1[i]]][b2i[s2[j]]]:
           s1Aligned += s1[i]
           s2Aligned += s2[j]
           j -= 1;
           i -= 1;
       elif matrix[j][i] == matrix[j][i - 1] + d:
           s1Aligned += s1[i]
           s2Aligned += " "
           i -= 1
       elif matrix[j][i] == matrix[j - 1][i] + d:
           s1Aligned += " "
           s2Aligned += s2[j]
           j -= 1
    while i > 0:
        s1Aligned += s1[i]
        i -= 1
    while j > 0:
        s2Aligned += s2[j]
        j -= 1
    return (s1Aligned[::-1], s2Aligned[::-1])


# Creates visual visualization of V(i, j) values for all pairs of V(i, j)
def CreateMatrix(seq1, seq2):
    matrix = [['a' for x in range(len(seq1))] for y in range(len(seq2))]
    for n in range(len(seq2)):
        for m in range(len(seq1)):
            matrix[n][m] = GlobalAlign(m, n, seq1, seq2)
    return matrix

# Basic pretty printing function
def PrintMatrix(m):
    for row in m:
        print row

# Sanitizes the input

# Since sequences are indexed from 1 ... and strings are indexed from 0
# ... spaces are added to realign the sequence indexes with the string
# indices.
def FindGlobalAlignScore(s1, s2):
    return GlobalAlign(len(s1), len(s2), " " + s1, " " + s2)

def FindGlobalAlignMatrixScore(s1, s2):
    i = len(s1)
    j = len(s2)
    return GlobalAlignMatrix(i, j, " " + s1, " " + s2)[j][i]

def FindBestAlignment(s1, s2):
    i = len(s1)
    j = len(s2)
    s1_ = " " + s1
    s2_ = " " + s2
    m = GlobalAlignMatrix(i, j, s1_, s2_)
    return GlobalTraceBack(i, j, s1_, s2_, m)

def FindLocalAlignScore(s1, s2):
    return LocalAlign(len(s1), len(s2), " " + s1, " " + s2)

def FindLocalAlignMatrixScore(s1, s2):
    # Flatten list and return maximum value in matrix
    return max([i for row in LocalAlignMatrix(len(s1), len(s2), " " + s1, " " + s2) for i in row])

print FindBestAlignment(T1, T2)
