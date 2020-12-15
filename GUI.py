import pygame
from vision import *
from backtracking import *
from copy import deepcopy

IMG_CELL_DARK = pygame.image.load('assets/cell_dark.png')
IMG_CELL_LIGHT = pygame.image.load('assets/cell_light.png')
IMG_CELL_SEL_RED = pygame.image.load('assets/cell_selected.png')
IMG_CELL_INCORRECT = pygame.image.load('assets/cell_incorrect.png')


class Cell:
    def __init__(self, x, y, value, window, image):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 65, 65)
        self.value = value
        self.window = window
        self.image = image
        self.selected = False
        self.board_solved = []

    def draw(self):
        # Draws a cell on the board
        self.window.blit(self.image, (self.x, self.y))

    def display(self, value, x, y, offset):
        # Displays a number in the cell
        font = pygame.font.Font('assets/Montserrat-Medium.ttf', 45)
        text = font.render(str(value), True, (215, 215, 208))
        w, h = text.get_size()
        self.window.blit(text, ((offset-w)//2 + x, (offset-h)//2 + y))  # Centralises text inside of a cell

    def isClicked(self, mouse_pos):
        # Checks if cell was clicked
        # noinspection PyArgumentList
        if self.rect.collidepoint(mouse_pos):
            return True


class Board:
    def __init__(self, window, board):
        self.board = board
        # Creates visual board with cells
        self.cells = [[Cell(i*65, j*65, self.board[i][j], window,
                            IMG_CELL_DARK if all(map(lambda x: x in (0, 1, 2, 6, 7, 8), [i, j])) or all(map(lambda x: x in (3, 4, 5), [i, j]))
                            else IMG_CELL_LIGHT) for j in range(9)] for i in range(9)]
        self.window = window
        self.board_solved = []
        self.valid = True

    def draw(self):
        # Drawing cells themselves
        for i in range(9):
            for j in range(9):
                self.cells[i][j].draw()
        # Drawing numbers
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value != 0:
                    self.cells[i][j].display(self.cells[i][j].value, (j*65), (i*65), 65)
        pygame.display.flip()

    def select(self, cell):
        cell.selected = True
        for i in range(9):
            for j in range(9):
                if self.cells[i][j] != cell:
                    self.cells[i][j].selected = False

    def redraw(self):
        self.valid = True
        self.window.fill((0, 0, 0))
        self.draw()
        for i in range(9):
            for j in range(9):
                if not is_valid(self.board, self.cells[i][j].value, (i, j)):
                    self.window.blit(IMG_CELL_INCORRECT, (j*65, i*65))
                    self.valid = False
                if self.cells[i][j].selected:
                    self.window.blit(IMG_CELL_SEL_RED, (i*65, j*65))
        pygame.display.flip()

    def solve_board(self):
        pygame.display.set_caption('Loading...')
        if self.valid and self.board != self.board_solved:
            self.board_solved = deepcopy(self.board)
            solve(self.board_solved)
            if self.board != self.board_solved:
                self.board = deepcopy(self.board_solved)
                for i in range(9):
                    for j in range(9):
                        self.cells[i][j].value = self.board[i][j]
                pygame.display.set_caption('Done! Press C to clear')
        else:
            pygame.display.set_caption('Error: UNSOLVABLE')

    def clear_board(self):
        for i in range(9):
            for j in range(9):
                self.board[i][j] = 0
                self.cells[i][j].value = 0
        pygame.display.set_caption('Sudoku Solver')

    def import_board(self):
        if screen2cells():
            pygame.display.set_caption('Importing...')
            self.board = cells2board()
            for i in range(9):
                for j in range(9):
                    self.cells[i][j].value = self.board[i][j]
            pygame.display.set_caption('Imported successfully')
        else:
            pygame.display.set_caption('No images in clipboard')
