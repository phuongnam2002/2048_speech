from gameplay import playGame
from py_solver import PySolver as Solver
from cpp_challenger import CppChallenger as Challenger
import sys

solver = Solver("direction_recognizer.py" if len(sys.argv) < 2 else sys.argv[1])
challenger = Challenger("./random_challenger" if len(sys.argv) < 3 else sys.argv[2])

playGame(solver, challenger)
