from itertools import izip
import math

# Used to map sequence elements to their coordinate in the substitution matrix
b2i = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

# Substitution matrix
sub = [
    #    A    C  G   T
    [10, -5, 0, -5],  # A
    [-5, 10, -5, 0],  # C
    [0, -5, 10, -5],  # G
    [-5, 0, -5, 10]  # T
]
# Gap penalty
d = -4

class Alignment:
    def __init__(self, s1, s2):
        # Since sequences are indexed from 1 ... and strings are indexed from 0
        # ... spaces are added to realign the sequence indexes with the string
        # indices.
        self.s1 = " " + s1
        self.s2 = " " + s2
        # maxI is associated with s1
        # maxJ is associated with s2
        self.maxI = len(s1)
        self.maxJ = len(s2)
        self.globalMatrix = self._GlobalAlignMatrix()
        self.localMatrix = self._LocalAlignMatrix()

    def _LocalAlignMatrix(self):
        # j is row number, i is column number
        matrix = [[0 for x in range(len(self.s1))]
                  for y in range(len(self.s2))]
        # Fill first horizontal row
        for k in range(0, self.maxI + 1):
            matrix[0][k] = 0
        # Fill first vertical column
        for k in range(0, self.maxJ + 1):
            matrix[k][0] = 0
        # Iterate column by column and fill cells
        for z in range(1, self.maxI + 1):
            for k in range(1, self.maxJ + 1):
                matrix[k][z] = max(
                    [matrix[k - 1][z - 1] +
                     sub[b2i[self.s1[z]]][b2i[self.s2[k]]],
                     matrix[k - 1][z] + d, matrix[k][z - 1] + d, 0])
        return matrix

    # Matrix method, most efficient
    def _GlobalAlignMatrix(self):
        j, i = self.maxJ, self.maxI
        # j is row number (s2), i is column number (s1)
        matrix = [[0 for x in range(len(self.s1))]
                  for y in range(len(self.s2))]
        # Fill first horizontal row
        for k in range(0, i + 1):
            matrix[0][k] = k * d
        # Fill first vertical column
        for k in range(0, j + 1):
            matrix[k][0] = k * d
        # Iterate column by column and fill cells
        for z in range(1, i + 1):
            for k in range(1, j + 1):
                matrix[k][z] = max(
                    [matrix[k - 1][z - 1] +
                     sub[b2i[self.s1[z]]][b2i[self.s2[k]]],
                     matrix[k - 1][z] + d, matrix[k][z - 1] + d])
        return matrix

    def GlobalTraceback(self):
        s1Aligned = ""
        s2Aligned = ""
        # Start at the lower right corner and see which of the three adjacent
        # matrix cells yield the score in the current cell by applying the
        # recursive conditions. Move to the correct cell and repeat until
        # (i,  j) = (0, 0)
        matrix = self.globalMatrix
        i, j = self.maxI, self.maxJ
        while i > 0 and j > 0:
            if matrix[j][i] == matrix[j - 1][i - 1] + sub[b2i[self.s1[i]]][b2i[
                    self.s2[j]]]:
                s1Aligned += self.s1[i]
                s2Aligned += self.s2[j]
                j -= 1
                i -= 1
            elif matrix[j][i] == matrix[j][i - 1] + d:
                s1Aligned += self.s1[i]
                s2Aligned += " "
                i -= 1
            elif matrix[j][i] == matrix[j - 1][i] + d:
                s1Aligned += " "
                s2Aligned += self.s2[j]
                j -= 1
        # Matrix edge reached. Put all remaining characters in the non
        # exhausted string against spaces.
        while i > 0:
            s1Aligned += self.s1[i]
            i -= 1
        while j > 0:
            s2Aligned += self.s2[j]
            j -= 1
        # The strings were built in reverse order.
        return (s1Aligned[::-1], s2Aligned[::-1])

    def LocalTraceback(self):
        # Find the position of largest value
        # Highest i positions in row order
        maxColumns = [row.index(max(row)) for row in self.localMatrix]
        # Map rows to the highest value they contain
        maxRows = map(max, self.localMatrix)
        # maximum j is the index of the row with highest maximum value
        j = maxRows.index(max(maxRows))
        # Get the i of the maximum value in the row corresponding to maximum j
        i = maxColumns[j]
        return self._LocalTraceback(i, j)

    def _LocalTraceback(self, i, j):
        # Local traceback is exactly the same as global traceback except that
        # we begin at the highest value and stop at the first 0 value instead
        # of starting at (i, j) = (maxI, maxJ) and continuing to (i, j) = (0,
        # 0).
        matrix = self.localMatrix
        s1Aligned = ""
        s2Aligned = ""
        # Trace from the highest value (i, j) to a 0 value
        # See explanation from GlobalTraceback.
        while matrix[j][i] != 0:
            if matrix[j][i] == matrix[j - 1][i - 1] + sub[b2i[self.s1[i]]][b2i[
                    self.s2[j]]]:
                s1Aligned += self.s1[i]
                s2Aligned += self.s2[j]
                j -= 1
                i -= 1
            elif matrix[j][i] == matrix[j][i - 1] + d:
                s1Aligned += self.s1[i]
                s2Aligned += " "
                i -= 1
            elif matrix[j][i] == matrix[j - 1][i] + d:
                s1Aligned += " "
                s2Aligned += self.s2[j]
                j -= 1
        return (s1Aligned[::-1], s2Aligned[::-1])

    def EndGapTraceback(self):
        # Find the highest vertical or horizontal value on last column or row.
        # Values in last row
        lastRow = self.localMatrix[self.maxJ]
        # Values in last column
        lastColumn = [r[self.maxI] for r in self.localMatrix]
        # Find the maximum value on the last row and last column
        lastRowMax = max(lastRow)
        lastColumnMax = max(lastColumn)
        i, j = 0, 0
        # Use the largest value as origin of traceback
        if lastRowMax > lastColumnMax:
            i, j = lastRow.index(lastRowMax), self.maxJ
        else:
            i, j = self.maxI, lastColumn.index(lastColumnMax)
        return self._LocalTraceback(i, j)

    def EndGapAlignScore(self):
        # Concatenate last row with last column and return the maximum
        return max(self.localMatrix[self.maxJ] + [r[self.maxI]
                                                  for r in self.localMatrix])

    def GetGlobalAlignScore(self):
        return self.globalMatrix[j][i]

    def GetLocalAlignScore(self):
        # Flatten list and return maximum value in matrix
        return max([i for row in self.localMatrix for i in row])

# Local alignment function. Recursive method
def LocalAlignScore(i, j, s1, s2):
    # Base cases
    if i == 0 or j == 0:
        return 0
    # Maximization list of all the recursive paths
    return max([LocalAlign(i - 1, j - 1) + sub[b2i[s1[i]]][b2i[s2[j]]],
                LocalAlign(i, j - 1, s1, s2) + d,
                LocalAlign(i - 1, j, s1, s2) + d])

# Recursive method, not the most efficient
def GlobalAlignScore(i, j, s1, s2):
    # This condition prevents infinite recursion. This happens because the
    # corner cases of V(0, j) and V(i, 0) are not properly handled in the
    # maximizing list
    if j != 0 and i == 0:
        return GlobalAlign(i, j - 1, s1, s2) + d
    elif i != 0 and j == 0:
        return GlobalAlign(i - 1, j, s1, s2) + d
    # Base case.
    if i == 0 and j == 0:
        return 0
    # Maximization list of all the recursive paths
    return max(
        [GlobalAlign(i - 1, j - 1, s1, s2) + sub[b2i[s1[i]]][b2i[s2[j]]],
         GlobalAlign(i, j - 1, s1, s2) + d, GlobalAlign(i - 1, j, s1, s2) + d])

# E(C_m) = n^2 * p^m
# Calculates the expected number of m length common substrings for two random
# strings of length n, alphabet size z for which p = 1 / z
def ExpectedNumberOfSubstr(n, p, m):
    return math.pow(n, 2) * math.pow(p, m)

# r <= 2log_z(n) where r is max m for which E(C_m) >= 1
def MaxCommonSubstrLength(n, z):
    return 2*math.log(n, z)

def MinimumCommonSubseq(n, z):
    return float(n) / float(z)

def FindGlobalAlignScore(s1, s2):
    return GlobalAlign(len(s1), len(s2), " " + s1, " " + s2)

# Creates visual visualization of V(i, j) values for all pairs of V(i, j)
def CreateMatrix(seq1, seq2):
    matrix = [['a' for x in range(len(seq1))] for y in range(len(seq2))]
    for n in range(len(seq2)):
        for m in range(len(seq1)):
            matrix[n][m] = GlobalAlign(m, n, seq1, seq2)
    return matri

# Basic pretty printing function
def PrintMatrix(m):
    for row in m:
        print row
