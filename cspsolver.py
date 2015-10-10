#! /usr/bin/env python

# File: cspsolver
# A Constraint Satisfaction Problems Solver.
# Authors:  Georgi Terziev      g.d.terziev@gmail.com
#           Kasper Bouwens      kas_bouwens@hotmail.com

import sys
from sudoku import Sudoku
from csproblem import CSProblem

splits = 0
"""A global variable used by the solve_CSP function,
and the constraint_satisfaction function to count the number of splits
done while solving the CSP problem."""

total_splits = 0


def solve_sudoku(sudoku_translator, sudoku_string):
    """Solves a given sudoku puzzle.

    Given a sudoku puzzle it will try to solve it using costraint satisfaction.
    If it succeeds it will return the solution.
    Otherwise returns 'No solution'."""
    
    global splits
    splits = 0
    
    csp = sudoku_translator.translate_sudoku_to_CSP(sudoku_string)
    
    (has_solution, solution) = solve_CSP(csp)
    
    if not has_solution:
        return False, 'No solution.'
    else:
        return True, sudoku_translator.translate_solution(solution)
        
def solve_CSP(problem):
    """Solves a CSP problem using a constraint satisfaction algorithm.

    Given a CSP problem it solves it using a constraint satisfaction
    algorithm. Uses Minimum Remaining Values heuristic to choose
    the variable for splitting. Performs constraint propagation."""

    global splits

    if not problem.constraint_propagation(True):#optimized?
        return False, 'No solution.'
    
    if problem.is_solved():
        return True, problem.get_solution()

    variable = problem.get_variable_for_splitting(True, False)#MRV?, MCV?
    domain = problem.get_variable_domain(variable, 0)#SVH: 0 == None, 1 == by tightness, otherwise domain sizes

    for value in domain:
        new_problem = problem.copy()
        splits += 1
        new_problem.set_variable(variable, value)
        (has_solution, solution) = solve_CSP(new_problem)
        if has_solution:
            return has_solution, solution
    
    return False, 'No solution.'


#Different puzzles follow.
def main(argv):
    global total_splits
    total_splits = 0
    sudokus = open(argv[1], 'r')
    solutions = open(argv[2], 'w')
    number_of_sudokus = 0

    if len(argv) > 3:
        number_of_sudokus = int(argv[3])

    nsudokus = 0
    sudoku_translator = Sudoku()
    for line in sudokus:
        if number_of_sudokus != 0 and nsudokus == number_of_sudokus:
            break
        sudoku = line.rstrip('\n')
        solved, solutionString = solve_sudoku(sudoku_translator, sudoku)
        solutions.write(solutionString+ '\n')
        solutions.flush()
        total_splits += splits
        nsudokus +=1

    print 'Total number of splits done: ' + str(total_splits)
    sudokus.close()
    solutions.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('usage: python cspsolver.py inputfile.txt outputfile.txt')
        sys.exit()

    main(sys.argv)
