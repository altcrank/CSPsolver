#! /usr/bin/env python

# File: sudoku
# A class translating a sudoku puzzle to a CSP problem.
# Authors:  Georgi Terziev      g.d.terziev@gmail.com
#           Kasper Bouwens      kas_bouwens@hotmail.com

import math
from constraints import Different

class Sudoku:
    """A Sudoku puzzle.
    
    A class representing an instance of a Sudoku puzzle
    and giving various attributes for manipulating that puzzle"""

    unset_values = {'0', '.'}
    """The characters that can be used for unset variable."""

    domain = set()
    """The initial domain for unset variables of a sudoku puzzle."""

    size = 0

    variables = dict()
    """The initial domain for unset variables of a sudoku puzzle."""

    constraints = []
    """The constraints describing the sudoku rules."""

    constraint_type = Different()

    def __init__(self, sudoku_string = ''):
        """A constructor for a sudoku puzzle

        Given a string of length NxN it saves the size N of the puzzle,
        initializes the variables and their domains,
        initializes the constraints,
        initializes the goal."""
        
        size_squared = len(sudoku_string)
        size = math.sqrt(size_squared)
        self.size = int(size)
        if self.size != size:
            raise Exception('Sudoku', 'Sudoku size must be a square number')

        for value in range(1, self.size+1):
            self.domain.add(value)

        self.initialize_variables(sudoku_string)
        
        self.generate_sudoku_rules_constraints()

    def initialize_variables(self, sudoku_string):
        """Initializes the variables of a sudoku puzzle

        Given a string of length Size x Size, represeting a sudoku,
        this function reads the string character by character and for every
        character that is '0' or '.' initalizes a variable with full domain.
        For all variables with given values it initializes the variable with
        a domain of the given value."""
        
        #NOTE: variables are 0-based
        for variable, value in enumerate(sudoku_string):
            if value not in self.unset_values:
                int_value = int(value)
                self.variables[variable] = {int_value}
            else:
                self.variables[variable] = self.domain.copy()

    def generate_sudoku_rules_constraints(self):
        """Generate the constraints defining the sudoku rules.

        Generates a set of pairs of variables.
        Every pair of variables will be interpreted as a constraint
        that the two variables should have different values."""

        for i in range(0, self.size*self.size):
            row = i / self.size
            column = i % self.size
            for r in range(0, self.size):
                same_row_var = row * self.size + r
                if same_row_var != i:
                    self.add_constraint(i, same_row_var)
                same_col_var = r * self.size + column
                if same_col_var != i:
                    self.add_constraint(i, same_col_var)
            
            quadrant_size = int(math.sqrt(self.size))
            quadrant_x = row / quadrant_size
            quadrant_y = column / quadrant_size
            for x in range(int(quadrant_x * quadrant_size), int((quadrant_x + 1) * quadrant_size)):
                for y in range(int(quadrant_y * quadrant_size), int((quadrant_y + 1) * quadrant_size)):
                    var = x * self.size + y
                    if var != i:
                        self.add_constraint(var, i) 
            

    def add_constraint(self, var1, var2):
        """Adds a constraint to the problem.

        Given two variables, add them as a pair in the constraints,
        signifying that they should have different values.
        For uniqueness the pair alwas has the smalles variable as first."""

        variables = sorted([var1, var2])
        constraint = (self.constraint_type, variables)
        if not constraint in self.constraints:
            self.constraints.append(constraint)

    def get_variables(self):
        return self.variables

    def get_constraints(self):
        return self.constraints

    def translate_solution(self, variables):
        """Returns the solution to the sudoku as a printable string.

        Expects that the sudoku is solved."""

        solution = ''
        sorted_variables = sorted(variables.items(), key = lambda el: el[0])
        for variable, domain in sorted_variables:
            value = domain.pop()
            domain.add(value)
            solution += str(value)
            

        return solution


