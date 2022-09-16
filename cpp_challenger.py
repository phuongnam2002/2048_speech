import subprocess
import sys
import pygame
from classes import ChallengingAgent

BOARD_SIZE = 4
VALID_ACTIONS = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]


def getLog(value):
    if value == 0:
        return 0
    for i in range(20):
        if value == (1 << i):
            return i


class CppChallenger(ChallengingAgent):
    def __init__(self, cmd):
        try:
            self.process = subprocess.Popen(cmd,
                                            stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            bufsize=1,
                                            universal_newlines=True)
        except Exception as ex:
            print("Command '%s' failed to start. Error: " % (cmd))
            print(ex)
            sys.exit(-1)

    # def __del__(self):
    #     print("-1", file=self.process.stdin)
    #     if self.process.poll() is None:
    #         print("Waiting for process to finish...")
    #         self.process.wait()
    #     self.printProcessResult()

    def printProcessResult(self):
        print("Process exited with exit status %d" % self.process.returncode)
        stderr_output = self.process.stderr.read()
        if stderr_output:
            print("Standard error: ")
            sys.stdout.write(stderr_output)
        else:
            print("Standard error is empty.")

    def checkProcessExit(self):
        if self.process.poll() is not None:
            print("ERROR: Process exited unexpectedly!")
            self.printProcessResult()
            sys.exit(-1)

    def readOutput(self):
        self.checkProcessExit()
        try:
            token = self.process.stdout.readline()
            value = int(token)
        except:
            self.checkProcessExit()
            print("ERROR: Unexpected token '%s'" % (token))
            sys.exit(-1)

        return value

    # this function receives the current tileMatrix as a BOARD_SIZE * BOARD_SIZE matrix
    # this returns a tuple (x, y, k) meaning that the cell at x-th row and y-th column should have a new tile of value k
    # rows and columns are numbered from 0 to BOARD_SIZE - 1.
    # the inserted cell (x, y) should be an empty cell in tileMatrix
    def getNewTile(self, tileMatrix):
        for col in range(BOARD_SIZE):
            for row in range(BOARD_SIZE):
                print("%d " % (tileMatrix[row][col]), file=self.process.stdin)
            print("\n", file=self.process.stdin)

        row = self.readOutput()
        col = self.readOutput()
        value = self.readOutput()

        assert 0 <= row and row < 4
        assert 0 <= col and col < 4
        assert value == 2 or value == 4
        assert tileMatrix[row][col] == 0

        return row, col, value


