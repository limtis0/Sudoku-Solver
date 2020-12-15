import pygame
from ctypes import windll
from GUI import *

# Removes DPI-Scaling
windll.user32.SetProcessDPIAware()

# Some basic things
pygame.init()
size_x = 585
size_y = 585
pygame.display.set_caption('Sudoku Solver')
screen = pygame.display.set_mode((size_x, size_y))
screen.fill((0, 0, 0))

# Creating board
sudoku = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for _ in range(9)]
bo = Board(screen, sudoku)
bo.redraw()
selected = (-1, -1)

# Continue to play until set to False
isRunning = True
clock = pygame.time.Clock()
# --Main loop--
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quits
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Quits
                exit()
            if selected != (-1, -1):
                # Keys 0-9
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE or event.key == pygame.K_0:
                    bo.cells[selected[0]][selected[1]].value = 0
                    bo.board[selected[0]][selected[1]] = 0
                if event.key == pygame.K_1:
                    bo.cells[selected[0]][selected[1]].value = 1
                    bo.board[selected[0]][selected[1]] = 1
                if event.key == pygame.K_2:
                    bo.cells[selected[0]][selected[1]].value = 2
                    bo.board[selected[0]][selected[1]] = 2
                if event.key == pygame.K_3:
                    bo.cells[selected[0]][selected[1]].value = 3
                    bo.board[selected[0]][selected[1]] = 3
                if event.key == pygame.K_4:
                    bo.cells[selected[0]][selected[1]].value = 4
                    bo.board[selected[0]][selected[1]] = 4
                if event.key == pygame.K_5:
                    bo.cells[selected[0]][selected[1]].value = 5
                    bo.board[selected[0]][selected[1]] = 5
                if event.key == pygame.K_6:
                    bo.cells[selected[0]][selected[1]].value = 6
                    bo.board[selected[0]][selected[1]] = 6
                if event.key == pygame.K_7:
                    bo.cells[selected[0]][selected[1]].value = 7
                    bo.board[selected[0]][selected[1]] = 7
                if event.key == pygame.K_8:
                    bo.cells[selected[0]][selected[1]].value = 8
                    bo.board[selected[0]][selected[1]] = 8
                if event.key == pygame.K_9:
                    bo.cells[selected[0]][selected[1]].value = 9
                    bo.board[selected[0]][selected[1]] = 9

                # Arrow keys
                if event.key == pygame.K_UP:
                    if selected[0] > 0:
                        selected = (selected[0] - 1, selected[1])
                        bo.select(bo.cells[selected[1]][selected[0]])
                if event.key == pygame.K_DOWN:
                    if selected[0] < 8:
                        selected = (selected[0] + 1, selected[1])
                        bo.select(bo.cells[selected[1]][selected[0]])
                if event.key == pygame.K_LEFT:
                    if selected[1] > 0:
                        selected = (selected[0], selected[1] - 1)
                        bo.select(bo.cells[selected[1]][selected[0]])
                if event.key == pygame.K_RIGHT:
                    if selected[1] < 8:
                        selected = (selected[0], selected[1] + 1)
                        bo.select(bo.cells[selected[1]][selected[0]])

                # Auto-solving
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    bo.solve_board()
                if event.key == pygame.K_c:
                    bo.clear_board()
                if event.key == pygame.K_v or event.key == pygame.K_i:
                    bo.import_board()

                bo.redraw()

        elif event.type == pygame.MOUSEBUTTONUP:
            mousePos = pygame.mouse.get_pos()
            for m in range(9):
                for n in range(9):
                    if bo.cells[m][n].isClicked(mousePos):
                        selected = (n, m)
                        bo.select(bo.cells[m][n])
                        bo.redraw()
    clock.tick(60)
