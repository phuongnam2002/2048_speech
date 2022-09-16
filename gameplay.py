import pygame, sys, time
import os.path
from pygame.locals import *
from color import *
from random import *

TOTAL_POINTS = 0
DEFAULT_SCORE = 2
BOARD_SIZE = 4

BREAK_TIME = 0.1

pygame.init()

SURFACE = pygame.display.set_mode((600, 700), 0, 32)
pygame.display.set_caption("2048")

myfont = pygame.font.SysFont("monospace", 25)
scorefont = pygame.font.SysFont("monospace", 50)

tileMatrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
undoMat = []


def playGame(solver, challenger=None):
    for i in range(2):
        placeRandomTile()
    printMatrix()

    while checkIfCanGo():
        key = solver.getAction(tileMatrix)

        assert isArrow(key)
        rotations = getRotations(key)

        for i in range(0, rotations):
            rotateMatrixClockwise()

        if not canMove():
            for j in range(0, (4 - rotations) % 4):
                rotateMatrixClockwise()
            continue

        moveTiles()
        mergeTiles()

        for j in range(0, (4 - rotations) % 4):
            rotateMatrixClockwise()

        if challenger is not None:
            x, y, k = challenger.getNewTile(tileMatrix)
            assert 0 <= x and x < BOARD_SIZE
            assert 0 <= y and y < BOARD_SIZE
            assert k == 2 or k == 4
            assert tileMatrix[x][y] == 0
            tileMatrix[x][y] = k
        else:
            placeRandomTile()

        printMatrix()

        pygame.display.update()
        time.sleep(BREAK_TIME)

    printGameOver()
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


def printMatrix():
    SURFACE.fill(BLACK)

    global BOARD_SIZE
    global TOTAL_POINTS

    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            pygame.draw.rect(SURFACE, getColour(tileMatrix[i][j]),
                             (i * (600 / BOARD_SIZE), j * (600 / BOARD_SIZE) + 100, 600 / BOARD_SIZE, 600 / BOARD_SIZE))

            label = myfont.render(str(tileMatrix[i][j]), 1, WHITE)
            label2 = scorefont.render("Score: " + str(TOTAL_POINTS), 1, WHITE)

            offset = 0

            if tileMatrix[i][j] < 10:
                offset = -10
            elif tileMatrix[i][j] < 100:
                offset = -15
            elif tileMatrix[i][j] < 1000:
                offset = -20
            else:
                offset = -25

            if tileMatrix[i][j] > 0:
                SURFACE.blit(label, (i * (600 / BOARD_SIZE) + (300 / BOARD_SIZE) + offset,
                                     j * (600 / BOARD_SIZE) + 100 + 300 / BOARD_SIZE - 15))
            SURFACE.blit(label2, (10, 20))


def printGameOver():
    global TOTAL_POINTS

    SURFACE.fill(BLACK)

    label = scorefont.render("Game Over!", 1, (255, 255, 255))
    label2 = scorefont.render("Score: " + str(TOTAL_POINTS), 1, (255, 255, 255))

    SURFACE.blit(label, (150, 100))
    SURFACE.blit(label2, (150, 300))


def placeRandomTile():
    count = 0
    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE):
            if tileMatrix[i][j] == 0:
                count += 1

    k = floor(random() * BOARD_SIZE * BOARD_SIZE)

    while tileMatrix[floor(k / BOARD_SIZE)][k % BOARD_SIZE] != 0:
        k = floor(random() * BOARD_SIZE * BOARD_SIZE)

    tileMatrix[floor(k / BOARD_SIZE)][k % BOARD_SIZE] = 2


def floor(n):
    return int(n - (n % 1))


def moveTiles():
    # We want to work column by column shifting up each element in turn.
    for i in range(0, BOARD_SIZE):  # Work through our 4 columns.
        for j in range(0, BOARD_SIZE - 1):  # Now consider shifting up each element by checking top 3 elements if 0.
            while tileMatrix[i][j] == 0 and sum(tileMatrix[i][
                                                j:]) > 0:  # If any element is 0 and there is a number to shift we want to shift up elements below.
                for k in range(j, BOARD_SIZE - 1):  # Move up elements below.
                    tileMatrix[i][k] = tileMatrix[i][k + 1]  # Move up each element one.
                tileMatrix[i][BOARD_SIZE - 1] = 0


def mergeTiles():
    global TOTAL_POINTS

    for i in range(0, BOARD_SIZE):
        for k in range(0, BOARD_SIZE - 1):
            if tileMatrix[i][k] == tileMatrix[i][k + 1] and tileMatrix[i][k] != 0:
                tileMatrix[i][k] = tileMatrix[i][k] * 2
                tileMatrix[i][k + 1] = 0
                TOTAL_POINTS += tileMatrix[i][k]
                moveTiles()


def checkIfCanGo():
    for i in range(0, BOARD_SIZE ** 2):
        if tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] == 0:
            return True

    for i in range(0, BOARD_SIZE):
        for j in range(0, BOARD_SIZE - 1):
            if tileMatrix[i][j] == tileMatrix[i][j + 1]:
                return True
            elif tileMatrix[j][i] == tileMatrix[j + 1][i]:
                return True
    return False


def reset():
    global TOTAL_POINTS
    global tileMatrix

    TOTAL_POINTS = 0
    SURFACE.fill(BLACK)

    tileMatrix = [[0 for i in range(0, BOARD_SIZE)] for j in range(0, BOARD_SIZE)]

    playGame()


def canMove():
    for i in range(0, BOARD_SIZE):
        for j in range(1, BOARD_SIZE):
            if tileMatrix[i][j - 1] == 0 and tileMatrix[i][j] > 0:
                return True
            elif (tileMatrix[i][j - 1] == tileMatrix[i][j]) and tileMatrix[i][j - 1] != 0:
                return True

    return False


def saveGameState():
    f = open("savedata", "w")

    tiles = " ".join([str(tileMatrix[floor(x / BOARD_SIZE)][x % BOARD_SIZE]) for x in range(0, BOARD_SIZE ** 2)])

    f.write(str(BOARD_SIZE) + "\n")
    f.write(tiles + "\n")
    f.write(str(TOTAL_POINTS))
    f.close()


def loadGameState():
    if os.path.isfile("savedata"):
        global TOTAL_POINTS
        global BOARD_SIZE
        global tileMatrix
        f = open("savedata", "r")

        BOARD_SIZE = int(f.readline())
        mat = (f.readline()).split(' ', BOARD_SIZE ** 2)
        TOTAL_POINTS = int(f.readline())

        tileMatrix = [[0 for i in range(0, BOARD_SIZE)] for j in range(0, BOARD_SIZE)]

        for i in range(0, BOARD_SIZE ** 2):
            tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] = int(mat[i])

        f.close()

        playGame(True)


def rotateMatrixClockwise():
    for i in range(0, int(BOARD_SIZE / 2)):
        for k in range(i, BOARD_SIZE - i - 1):
            temp1 = tileMatrix[i][k]
            temp2 = tileMatrix[BOARD_SIZE - 1 - k][i]
            temp3 = tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k]
            temp4 = tileMatrix[k][BOARD_SIZE - 1 - i]

            tileMatrix[BOARD_SIZE - 1 - k][i] = temp1
            tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k] = temp2
            tileMatrix[k][BOARD_SIZE - 1 - i] = temp3
            tileMatrix[i][k] = temp4


def isArrow(k):
    return (k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT)


def getRotations(k):
    if k == pygame.K_UP:
        return 0
    elif k == pygame.K_DOWN:
        return 2
    elif k == pygame.K_LEFT:
        return 1
    elif k == pygame.K_RIGHT:
        return 3


def convertToLinearMatrix():
    mat = []

    for i in range(0, BOARD_SIZE ** 2):
        mat.append(tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE])

    mat.append(TOTAL_POINTS)

    return mat


def addToUndo():
    undoMat.append(convertToLinearMatrix())


def undo():
    if len(undoMat) > 0:
        mat = undoMat.pop()

        for i in range(0, BOARD_SIZE ** 2):
            tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] = mat[i]

        global TOTAL_POINTS
        TOTAL_POINTS = mat[BOARD_SIZE ** 2]

        printMatrix()
