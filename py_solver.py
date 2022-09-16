import subprocess
import sys
import pygame
from classes import *

BOARD_SIZE = 4
VALID_ACTIONS = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]


def getLog(value):
    if value == 0:
        return 0
    for i in range(20):
        if value == (1 << i):
            return i


class PySolver(SolvingAgent):
    def __init__(self, cmd):
        try:
            self.proc = subprocess.Popen(cmd,
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
    #     print("-1", file=self.proc.stdin)
    #     if self.proc.poll() is None:
    #         print("Waiting for process to finish...")
    #         self.proc.wait()
    #     self.printProcessResult()

    def printProcessResult(self):
        print("Process exited with exit status %d" % self.proc.returncode)
        stderr_output = self.proc.stderr.read()
        if stderr_output:
            print("Standard error: ")
            sys.stdout.write(stderr_output)
        else:
            print("Standard error is empty.")

    def checkProcessExit(self):
        if self.proc.poll() is not None:
            print("ERROR: Process exited unexpectedly!")
            self.printProcessResult()
            sys.exit(-1)

    def readOutput(self):
        self.checkProcessExit()
        try:
            token = self.proc.stdout.readline()
            move = int(token)
            if (move < 0) or (move > 3):
                raise Exception()
        except:
            self.checkProcessExit()
            print("ERROR: Unexpected token '%s'" % (token))
            sys.exit(-1)

        return move

    # this function receives the tileMatrix as a BOARD_SIZE x BOARD_SIZE array
    # returns one of the four values in VALID_ACTIONS corresponding to the moving direction
    def getAction(self, tileMatrix):
        print("%d" % (tileMatrix[0][0]), file=self.proc.stdin)

        move = self.readOutput()
        return VALID_ACTIONS[move]
