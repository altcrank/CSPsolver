#! /usr/bin/env python

# File: sudoku
# A class representing a sudoku puzzle.
# Authors:  Georgi Terziev      g.d.terziev@gmail.com
#           Kasper Bouwens      kas_bouwens@hotmail.com

import math
import copy
from collections import deque

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

    constraints = set()
    """The constraints describing the sudoku rules."""

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

        if var1 < var2:
            constraint = (var1, var2)
        else:
            constraint = (var2, var1)
        if not constraint in self.constraints:
            self.constraints.add(constraint)

    def add_constraints(self, constraints):
        """Adds more constraints to the sudoku puzzle.

        The constraints should be paris of variables, which should be different."""

        for constraint in constraints:
            self.constraints.add(constraint)

    def constraint_propagation(self):
        """Performs constraint propagation on the sudoku"""
    
        #TODO: for optimization maybe loop through variables
        #and make all constraints including them arc consistent.
        #TODO: after that order variables by domain sizes. Don't forget to update!!!
        for constraint in self.constraints:
            var1, var2 = constraint
            if var1 == var2:
                print 'WTF!!!'
            domain_var1 = self.variables[var1]
            domain_var2 = self.variables[var2]
            if not self.arc_consistency(domain_var1, domain_var2):
                return False
        return True
    def arc_consistency(self, domain1, domain2):
        """Performs arc consistency on the two domains assuming != constraint.

        Removes from the domains the values that do not have support in the other domain."""
        
        if len(domain1) == 1:
            for value in domain1:
                domain2.discard(value)
                if len(domain2)==0:
                    return False
        if len(domain2) == 1:
            for value in domain2:
                domain1.discard(value)
                if len(domain1)==0:
                    return False
        return True
                
    def is_solved(self):
        """Checks if the sudoku is solved.

        A sudoku is solved if every variable is assigned exactly 1 value."""

        for variable, domain in self.variables.iteritems():            
            if len(domain) != 1:
                return False

        return True

    def is_unsolvable(self):
        """Check if the sudoku became unsolvable.

        Check if any of the variables is left with an empty domain."""
        
        for variable, domain in self.variables.iteritems():
            if not domain:#TODO: check if this really means if the len(domain) == 0
                return True
        
        return False

    def get_solution(self):
        """Returns the solution to the sudoku as a printable string.

        Expects that the sudoku is solved."""

        solution = ''
        sorted_variables = sorted(self.variables.items(), key = lambda el: el[0])
        for variable, domain in sorted_variables:
            value = domain.pop()
            domain.add(value)
            solution += str(value) + ' '
            column = variable % self.size
            if column == self.size - 1:
                solution += '\n'

        return solution

    def display_state(self):
        """Prints a current state of the sudoku."""

        solution = ''
        sorted_variables = sorted(self.variables.items(), key = lambda el: el[0])
        for variable, domain in sorted_variables:
            solution += str(domain) + '\t'
            column = variable % self.size
            if column == self.size - 1:
                solution += '\n\n'

        return solution

    def get_variable_domain(self, variable):
        """Return the domain of the variable.

        Given a variable return the set of its allowed values."""

        return self.variables[variable]

    def get_unassigned_variables(self):
        """Return a list of the unassigned variables.

        Return a list of the the variables,
        which have not yet been assigned a value."""

        unassigned_variables = []
        for variable, domain in self.variables.iteritems():
            if len(domain) != 1:
                unassigned_variables.append(variable)

        return unassigned_variables

    def set_variable(self, variable, value):
        """Set the variable 'variable' to have value 'value'.

        Restrict the domain of the variable 'variable' to be
        the set with one element 'value'."""

        self.variables[variable] = {value}
        
    def copy(self):
        """Copies the puzzle.

        Returns a copy of the puzzle. Changing the assigned values and
        the possible values in the coppy will not affect the original puzzle,
        thus the original and the copy are different from each other."""

        sudoku_copy = Sudoku()

        sudoku_copy.domain = self.domain
        sudoku_copy.size = self.size
        sudoku_copy.variables = copy.deepcopy(self.variables)
        sudoku_copy.constraints = copy.deepcopy(self.constraints)

        return sudoku_copy

