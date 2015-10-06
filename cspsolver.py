#! /usr/bin/env python

# File: cspsolver
# A Constraint Satisfaction Problems Solver.
# Authors:  Georgi Terziev      g.d.terziev@gmail.com
#           Kasper Bouwens      kas_bouwens@hotmail.com

import sys
from sudoku import Sudoku
from cspproblem import CSPProblem

splits = 0
"""A global variable used by the solve_CSP function,
and the constraint_satisfaction function to count the number of splits
done while solving the CSP problem."""


def solve_sudoku(puzzle):
    """Solves a given sudoku puzzle.

    Given a sudoku puzzle it will try to solve it using costraint satisfaction.
    If it succeeds it will print the solution.
    Otherwise prints 'No solution'."""
    
    global splits
    splits = 0
    
    csp = CSPProblem()
    csp.set_variables(puzzle.get_variables())
    csp.set_constraints(puzzle.get_constraints())
    
    (has_solution, solution) = solve_CSP(csp)
    
    if not has_solution:
        print 'No solution.\n Splits performed: ' + str(splits)
    else:
        print puzzle.translate_solution(solution) + '\n Splits performed: ' + str(splits)
        

def solve_CSP(problem):
    """Solves a CSP problem using a constraint satisfaction algorithm.

    Given a CSP problem it solves it using a constraint satisfaction
    algorithm. Uses Minimum Remaining Values heuristic to choose
    the variable for splitting. Performs constraint propagation."""

    global splits

    #print 'before CP:'
    #print puzzle.display_state()
    
    if not problem.constraint_propagation():
        return False, 'No solution.'

    #print 'after CP:'
    #print puzzle.display_state()

    if problem.is_solved():
        return True, problem.get_solution()

    variable = problem.get_variable_for_splitting()
    domain = problem.get_variable_domain(variable)
    for value in domain:
        new_problem = problem.copy()
        splits += 1
        new_problem.set_variable(variable, value)
        (has_solution, solution) = solve_CSP(new_problem)
        if has_solution:
            return has_solution, solution
    
    return False, 'No solution.'


#Different puzzles follow.
sudoku1 = Sudoku('4...3.......6..8..........1....5..9..8....6...7.2........1.27..5.3....4.9........')

solve_sudoku(sudoku1)
