#! /usr/bin/env python

# File: sudoku
# A class translating a sudoku puzzle to a CSP problem.
# Authors:  Georgi Terziev      g.d.terziev@gmail.com
#           Kasper Bouwens      kas_bouwens@hotmail.com

import math
from constraints import Different
from csproblem import CSProblem

class Sudoku:
    """A Sudoku puzzle.
    
    A class translating a Sudoku puzzle to a CSP problem."""

    unset_values = {'0', '.'}
    """The characters that can be used for unset variable."""

    constraint_type = Different()

    def translate_sudoku_to_CSP(self, sudoku_string):
        """Translates a sudoku string to CSProblem

        Given a string of length NxN this function creates a CSProblem and:
        initializes the variables and their domains,
        initializes the constraints.
        In case the string is not of the right length to be a sudoku string
        it throws an exception."""

        context = 'translate_sudoku_to_CSP'
        message = 'Sudoku size must be a square number'
        size_squared = len(sudoku_string)
        size = math.sqrt(size_squared)
        if size != int(size):
            raise Exception(context, message)

        size = int(size)
        subgrid_size = math.sqrt(size)
        if subgrid_size != int(subgrid_size):
            raise Execption(context, message)

        domain = set()
        for value in range(1, size+1):
            domain.add(value)

        variables = self.initialize_variables(sudoku_string, domain)
        
        constraints = self.generate_sudoku_rules_constraints(size)
        #constraints = self.generate_sudoku_rules_constraints_binary(size)

        csp = CSProblem()
        csp.set_variables(variables)
        csp.set_constraints(constraints)

        return csp

    def initialize_variables(self, sudoku_string, domain):
        """Initializes the variables of a sudoku puzzle

        Given a string of length Size x Size, represeting a sudoku,
        this function reads the string character by character and for every
        character that is '0' or '.' initalizes a variable with full domain.
        For all variables with given values it initializes the variable with
        a domain of the given value."""
        
        variables = dict()
        #NOTE: variables are 0-based
        for variable, value in enumerate(sudoku_string):
            if value not in self.unset_values:
                int_value = int(value)
                variables[variable] = {int_value}
            else:
                variables[variable] = domain.copy()

        return variables

    def generate_sudoku_rules_constraints(self, size):
        constraints = []
        for row in range(0, size):
            same_row = []
            same_col = []
            for col in range(0, size):
                same_row.append(row * size + col)
                same_col.append(col * size + row)
            constraints.append((self.constraint_type, same_row))
            constraints.append((self.constraint_type, same_col))

        quadrant_size = int(math.sqrt(size))
        for quadrant_x in range(0, quadrant_size):
            for quadrant_y in range(0, quadrant_size):
                same_quadrant = []
                for x in range(0, quadrant_size):
                    for y in range(0, quadrant_size):
                        row = quadrant_x * quadrant_size + x
                        col = quadrant_y * quadrant_size + y
                        same_quadrant.append(row * size + col)
                constraints.append((self.constraint_type, same_quadrant))
        
        return constraints

    def generate_sudoku_rules_constraints_binary(self, size):
        """Generate the constraints defining the sudoku rules.

        Generates a set of pairs of variables.
        Every pair of variables will be interpreted as a constraint
        that the two variables should have different values."""
        
        constraints = []
        for i in range(0, size*size):
            row = i / size
            column = i % size
            for r in range(0, size):
                same_row_var = row * size + r
                if same_row_var != i:
                    self.add_constraint(constraints, i, same_row_var)
                same_col_var = r * size + column
                if same_col_var != i:
                    self.add_constraint(constraints, i, same_col_var)
            
            quadrant_size = int(math.sqrt(size))
            quadrant_x = int(row / quadrant_size)
            quadrant_y = int(column / quadrant_size)
            for x in range(quadrant_x * quadrant_size, (quadrant_x + 1) * quadrant_size):
                for y in range(quadrant_y * quadrant_size, (quadrant_y + 1) * quadrant_size):
                    var = x * size + y
                    if var != i:
                        self.add_constraint(constraints, var, i) 

        return constraints
            

    def add_constraint(self, constraints, var1, var2):
        """Adds a constraint to the problem.

        Given two variables, add them as a pair in the constraints,
        signifying that they should have different values.
        For uniqueness the pair alwas has the smalles variable as first."""

        variables = sorted([var1, var2])
        constraint = (self.constraint_type, variables)
        if not constraint in constraints:
            constraints.append(constraint)

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


