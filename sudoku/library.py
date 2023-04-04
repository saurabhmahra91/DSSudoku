import random
import math


class Sudoku:
    def __init__(self, N, K):
        self.N = N
        self.K = K
        # Compute square root of N
        SRNd = math.sqrt(N)
        self.SRN = int(SRNd)
        self.mat = [[0 for _ in range(N)] for _ in range(N)]

    def fillValues(self):
        # Fill the diagonal of SRN x SRN matrices
        self.fillDiagonal()

        # Fill remaining blocks
        self.fillRemaining(0, self.SRN)

        # Remove Randomly K digits to make game
        self.removeKDigits()

    def fillDiagonal(self):
        for i in range(0, self.N, self.SRN):
            self.fillBox(i, i)

    def unUsedInBox(self, rowStart, colStart, num):
        for i in range(self.SRN):
            for j in range(self.SRN):
                if self.mat[rowStart + i][colStart + j] == num:
                    return False
        return True

    def fillBox(self, row, col):
        num = 0
        for i in range(self.SRN):
            for j in range(self.SRN):
                while True:
                    num = self.randomGenerator(self.N)
                    if self.unUsedInBox(row, col, num):
                        break
                self.mat[row + i][col + j] = num

    def randomGenerator(self, num):
        return math.floor(random.random() * num + 1)

    def checkIfSafe(self, i, j, num):
        return (self.unUsedInRow(i, num) and self.unUsedInCol(j, num) and self.unUsedInBox(i - i % self.SRN, j - j % self.SRN, num))

    def unUsedInRow(self, i, num):
        for j in range(self.N):
            if self.mat[i][j] == num:
                return False
        return True

    def unUsedInCol(self, j, num):
        for i in range(self.N):
            if self.mat[i][j] == num:
                return False
        return True

    def fillRemaining(self, i, j):
        # Check if we have reached the end of the matrix
        if i == self.N - 1 and j == self.N:
            return True

        # Move to the next row if we have reached the end of the current row
        if j == self.N:
            i += 1
            j = 0

        # Skip cells that are already filled
        if self.mat[i][j] != 0:
            return self.fillRemaining(i, j + 1)

        # Try filling the current cell with a valid value
        for num in range(1, self.N + 1):
            if self.checkIfSafe(i, j, num):
                self.mat[i][j] = num
                if self.fillRemaining(i, j + 1):
                    return True
                self.mat[i][j] = 0

        # No valid value was found, so backtrack
        return False

    def removeKDigits(self):
        count = self.K

        while (count != 0):
            i = self.randomGenerator(self.N) - 1
            j = self.randomGenerator(self.N) - 1
            if (self.mat[i][j] != 0):
                count -= 1
                self.mat[i][j] = 0

        return

    def printSudoku(self):
        for i in range(self.N):
            for j in range(self.N):
                print(self.mat[i][j], end=" ")
            print()

    def flatList(self):
        return [cell for row in self.mat for cell in row]



def makeMatrix(string_array):
    char_array = list(string_array)
    array = list(map(int, char_array))

    mtx = []
    
    for i in range(9):
        row = []
        for j in range(9):
            row.append(array[9*i+j])
        mtx.append(row)
    return mtx

def isValidSudoku(array):
    mtx = makeMatrix(array)
    possiblities = set([1, 2, 3, 4, 5, 6, 7, 8, 9])

    # rows check
    for i in range(9):
        if set(mtx[i]) != possiblities:
            return False
    print("row check success")

    # column check
    for i in range(9):
        col = []
        for j in range(9):
            col.append(mtx[j][i])

        if set(col) != possiblities:
            return False
    print("column check success")

    # 3v3 grid check
    filled = []
    for i in range(3):
        for j in range(3):
            filled.append(mtx[i][j])
    if set(filled) != possiblities:
        return False
    
    filled = []
    for i in range(3):
        for j in range(3, 6):
            filled.append(mtx[i][j])
    if set(filled) != possiblities:
        return False
    
    filled = []
    for i in range(3):
        for j in range(6, 9):
            filled.append(mtx[i][j])
    if set(filled) != possiblities:
        return False
    
    filled = []
    for i in range(3, 6):
        for j in range(3):
            filled.append(mtx[i][j])
    if set(filled) != possiblities:
        return False
    
    filled = []
    for i in range(3, 6):
        for j in range(3, 6):
            filled.append(mtx[i][j])
    if set(filled) != possiblities:
        return False
    
    filled = []
    for i in range(3, 6):
        for j in range(6, 9):
            filled.append(mtx[i][j])
    if set(filled) != possiblities:
        return False

    filled = []
    for i in range(6, 9):
        for j in range(3):
            filled.append(mtx[i][j])
    if set(filled) != possiblities:
        return False
    
    filled = []
    for i in range(6, 9):
        for j in range(3, 6):
            filled.append(mtx[i][j])
    if set(filled) != possiblities:
        return False
    
    filled = []
    for i in range(6, 9):
        for j in range(6, 9):
            filled.append(mtx[i][j])
    if set(filled) != possiblities:
        return False
    
    print("subgrid check success")
    return True


def isOriginalSudoku(values, cells):
    for cell in cells:
        row = cell.row
        col = cell.col
        filled_value = values[9*(row-1)+(col-1)]
        print("row=", row)
        print("col=", col)
        print("filled=", filled_value)
        print("expected=", cell.value)
        if cell.value is not None and str(cell.value) != filled_value.strip():
            return False
    
    return True


# N = 9
# K = 40
# sudoku = Sudoku(N, K)
# sudoku.fillValues()
# # sudoku.printSudoku()
# print(sudoku.mat)
# print(sudoku.flatList())
# print( 2 or None)