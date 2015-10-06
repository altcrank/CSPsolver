#! /usr/bin/env python

# File: cspproblem
# A class representing CSP problem
# Authors:  Georgi Terziev      g.d.terziev@gmail.com
#           Kasper Bouwens      kas_bouwens@hotmail.com

import copy
import sys

class CSPProblem:
    """A CSP problem.
    
    A class representing an instance of a CSP problem
    and giving various attributes for manipulating that CSP problem.

    The CSP problem is defined as solved when all of the variables
    are assigned only one value, and the values do not contradict
    the constraints."""

    variable_domains = dict()
    """A mapping from variables to their domains of possible values."""

    variable_domain_sizes = []
    """A mapping from variables to domain sizes"""

    constraints = []
    """The constraints describing the CSP problem."""

    def set_variables(self, variable_domains):
        self.variable_domains = copy.deepcopy(variable_domains)
        self.variable_domain_sizes = list(range(len(variable_domains)))
        for variable, domain in self.variable_domains.iteritems():
            self.variable_domain_sizes[variable] = len(domain)

    def set_constraints(self, constraints):
        self.constraints = copy.deepcopy(constraints)

    def add_constraints(self, constraints):
        self.constraints.extend(copy.deepcopy(constraints))

    def constraint_propagation(self):
        """Performs constraint propagation on the CSP problem"""
    
        #TODO: for optimization maybe loop through variables
        #and make all constraints including them arc consistent.
        #TODO: after that order variables by domain sizes. Don't forget to update!!!
        
        #order constriants by their variables' domain sizes
        self.constraints.sort(key=lambda constraint: min(self.variable_domain_sizes[constraint[0]], self.variable_domain_sizes[constraint[1]]))

        #do constraint propagation
        for constraint in self.constraints:
            var1, var2 = constraint
            consistent, stop = self.arc_consistency(var1, var2)
            if not consistent:
                return False
            if stop:
                break

        return True

    def arc_consistency(self, var1, var2):
        """Performs arc consistency on the two domains assuming != constraint.

        Removes from the domains the values that do not have support in the other domain."""

        smaller = var1
        bigger = var2
        if self.variable_domain_sizes[var1] > self.variable_domain_sizes[var2]:
            smaller = var2
            bigger = var1

        #if self.variable_domain_sizes[smaller] > 1:
        #    return True, True

        if not self.half_arc_consistency(smaller, bigger):
            return False, False

        if not self.half_arc_consistency(bigger, smaller):
            return False, False

        return True, False


    def half_arc_consistency(self, var1, var2):
        if self.variable_domain_sizes[var1] == 1:
            domain1 = self.variable_domains[var1]
            domain2 = self.variable_domains[var2]
            for value in domain1:
                if value in domain2:
                    domain2.remove(value)
                    self.variable_domain_sizes[var2] -= 1
                    if self.variable_domain_sizes[var2] == 0:
                        return False
        return True
                
    def is_solved(self):
        """Checks if the CSP is solved.

        A CSP is solved if every variable is assigned exactly 1 value."""

        for variable, domain in self.variable_domains.iteritems():
            if len(domain) != 1:
                return False

        return True
    
        for domain_size in self.variable_domain_sizes:            
            if domain_size != 1:
                return False

        return True

    def get_solution(self):
        """Returns the solution to the CSP.

        Returns the variables with their "assigned values" (i.e. the domains of size 1)"""

        return self.variable_domains

    def display_state(self):
        """Prints a current state of the CSP."""

        state = ''
        sorted_variable_domains = sorted(self.variable_domains.items(), key = lambda el: el[0])
        for variable, domain in sorted_variable_domains:
            state += str(variable) + ': ' + str(domain) + '\n'

        return state

    def get_variable_domain(self, variable):
        """Return the domain of the variable.

        Given a variable return the set of its allowed values."""

        return self.variable_domains[variable]


    def get_variable_for_splitting(self):
        variables = self.get_mrv_vars()

        if not variables:
            raise Exception('Get Variable for Splitting', 'CSP does not have unset variables!')
        
        return variables.pop()

    def get_mrv_vars(self):
        """A Minimum Remaining Values Heuristic function.

        Returns the variable that has still not been assigned a value,
        and has the least amount of possible values."""

        #variables is a list of variables
        best_variables = set()
        smallest_domain_size = sys.maxint

        #for var, domain_size in enumerate(self.variable_domain_sizes):
        for var, domain in self.variable_domains.iteritems():
            domain_size = len(domain)
            if domain_size <= 1:
                continue
    
            if domain_size > smallest_domain_size:
                continue
    
            if domain_size < smallest_domain_size:
                best_variables.clear()
                smallest_domain_size = domain_size
    
            best_variables.add(var)

        return best_variables

    #TODO: This is unused and left because it might turn out needed later.
    #Try not to use it though.
    def get_unassigned_variables(self):
        """Return a list of the unassigned variables.

        Return a list of the the variables,
        which have not yet been assigned a value."""

        unassigned_variables = []
        #for variable, domain_size in self.variable_domain_sizes:
        for variable, domain in self.variable_domains.iteritems():
            domain_size = len(domain)

            if domain_size != 1:
                unassigned_variables.append(variable)

        return unassigned_variables

    def set_variable(self, variable, value):
        """Set the variable 'variable' to have value 'value'.

        Restrict the domain of the variable 'variable' to be
        the set with one element 'value'."""

        self.variable_domains[variable] = {value}
        self.variable_domain_sizes[variable] = 1
        
    def copy(self):
        """Copies the CSP problem.

        Returns a deep copy of the puzzle.
        Changing the copy will not affect the original."""

        csp_copy = CSPProblem()

        csp_copy.variable_domains = copy.deepcopy(self.variable_domains)
        csp_copy.variable_domain_sizes = copy.deepcopy(self.variable_domain_sizes)
        csp_copy.constraints = copy.deepcopy(self.constraints)

        return csp_copy

