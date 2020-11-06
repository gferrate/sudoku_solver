import pprint


class NoZerosLeftException(Exception):
    pass


class SudokuSolver:

    def __init__(self, filename):
        self.sudoku = self.read_sudoku(filename)
        self.printer = pprint.PrettyPrinter(indent=4)

    @staticmethod
    def read_sudoku(filename):
        sudoku = []
        with open(filename) as f:
            for line in f:
                line = list(map(int, line.strip(' \n').split(' ')))
                sudoku.append(line)
        return sudoku

    def get_square(self, i, j):
        i = i // 3
        j = j // 3
        sq = []
        for c in range(3):
            sq.extend(self.sudoku[i*3+c][j*3:j*3+3])
        return sq

    def get_next_zero(self, i, j):
        for y in range(i, 9):
            for x in range(j, 9):
                if self.sudoku[y][x] == 0:
                    return y, x
        if i == 0 and j == 0:
            raise NoZerosLeftException()
        return self.get_next_zero(0, 0)

    def check_row(self, i, val):
        return val not in self.sudoku[i]

    def check_col(self, j, val):
        return val not in [row[j] for row in self.sudoku]

    def check_square(self, i, j, val):
        sq = self.get_square(i, j)
        return val not in sq

    def check_if_valid(self, i, j, val):
        if (self.check_row(i, val) and
                self.check_col(j, val) and
                self.check_square(i, j, val)):
            return True
        return False

    def print_sudoku(self):
        self.printer.pprint(self.sudoku)

    def solve(self, i=0, j=0):
        try:
            i, j = self.get_next_zero(i, j)
        except NoZerosLeftException:
            return True
        for elm in range(1, 10):
            val = self.check_if_valid(i, j, elm)
            if val:
                self.sudoku[i][j] = elm
                if self.solve(i, j):
                    return True
                self.sudoku[i][j] = 0
        return False


def main():
    filename = 'examples/sudoku_1.txt'
    ss = SudokuSolver(filename)
    print('Sudoku:')
    ss.print_sudoku()
    ss.solve()
    print('Solution:')
    ss.print_sudoku()


if __name__ == '__main__':
    main()

