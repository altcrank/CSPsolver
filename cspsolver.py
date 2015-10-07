#! /usr/bin/env python

# File: cspsolver
# A Constraint Satisfaction Problems Solver.
# Authors:  Georgi Terziev      g.d.terziev@gmail.com
#           Kasper Bouwens      kas_bouwens@hotmail.com

import sys
from sudoku import Sudoku

states = 0
"""A global variable used by the solve_sudoku function,
and the constraint_satisfaction function to count the number of states
generated while solving the puzzle."""


def solve_sudoku(puzzle):
    """Solves a given sudoku puzzle.

    Given a sudoku puzzle it will try to solve it using costraint satisfaction.
    If it succeeds it will print the solution.
    Otherwise prints 'No solution'."""
    
    global states
    states = 0
    
    (has_solution, solution) = constraint_satisfaction(puzzle)
    if has_solution:
        print solution + '\n Explored states: ' + str(states)
    else:
        print 'No solution.\n Explored states: ' + str(states)

def constraint_satisfaction(puzzle):
    """Solves a sudoku puzzle using a constraint satisfaction algorithm.

    Given a sudoku puzzle it solves it using a constraint satisfaction
    algorithm. Uses Minimum Remaining Values heuristic to choose
    the next variable to be assigned a value. Performs forward checking."""

    global states

    #print 'before CP:'
    #print puzzle.display_state()
    
    if not puzzle.constraint_propagation():
        return False, 'No solution.'
    
    #puzzle.constraint_propagation()
    #print 'after CP:'
    #print puzzle.display_state()

    if puzzle.is_solved():
        return True, puzzle.get_solution()

    variable = mrv_var(puzzle)
    domain = puzzle.get_variable_domain(variable)
    for value in domain:
        new_puzzle = puzzle.copy()
        states += 1
        new_puzzle.set_variable(variable, value)
        (has_solution, solution) = constraint_satisfaction(new_puzzle)
        if has_solution:
            return has_solution, solution
    
    return False, 'No solution.'

def mrv_var(puzzle):
    """A Minimum Remaining Values Heuristic function.

    Given a puzzle it returns the variable from that puzzle that has still
    not been assigned a value, and has the least amount of possible values."""

    #variables is a list of variables
    best_variables = set()
    smallest_domain_size = sys.maxint
    variables = puzzle.get_unassigned_variables()
    assert len(variables) > 0
    if len(variables) == 0:
        raise Exception('Minimum Remaining Values Heuristic', 'Puzzle does not have unset variables!')

    for var in variables:
        domain = puzzle.get_variable_domain(var)
        domain_size = len(domain)
        if domain_size == smallest_domain_size:
            best_variables.add(var)
        if domain_size < smallest_domain_size:
            best_variables.clear()
            best_variables.add(var)
            smallest_domain_size = domain_size

    assert len(best_variables) > 0
    variable = best_variables.pop()
    return variable


#Different puzzles follow.
def main(argv):
    #print argv
    sudokus = [line.rstrip('\n') for line in open(argv[1])]
    #sudokus = [line.rstrip('\n') for line in open('1000sudokus.txt')]
    for i in range(3):
        solve_sudoku(Sudoku(sudokus[i]))
    
if __name__ == '__main__':
    main(sys.argv)
#pik = Sudoku(lines[0])
#solve_sudoku(pik)
#for line in range(0,len(sudokustring),len(sudokustring)/1000):
#    print sudokustring[line:len(sudokustring)/1000]
#print len(sudokustring)/1000
#solve_sudoku(sudoku1)
