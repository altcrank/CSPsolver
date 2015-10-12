#! /usr/bin/env python

# File: csproblem
# A class representing CSP problem
# Authors:  Georgi Terziev      g.d.terziev@gmail.com
#           Kasper Bouwens      kas_bouwens@hotmail.com

import copy
import sys
import constraints as cs

class CSProblem:
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

    diff = cs.Different()

    def set_variables(self, variable_domains):
        self.variable_domains = copy.deepcopy(variable_domains)
        self.variable_domain_sizes = list(range(len(variable_domains)))
        for variable, domain in self.variable_domains.iteritems():
            self.variable_domain_sizes[variable] = len(domain)

    def set_constraints(self, constraints):
        self.constraints = copy.deepcopy(constraints)
        self.only_different = True
        different = cs.Different()
        for constraint in self.constraints:
            if not constraint[0] == different:
                self.only_different = False


    def add_constraints(self, constraints):
        self.constraints.extend(copy.deepcopy(constraints))

    def constraint_propagation(self, optimized):
        """Performs constraint propagation on the CSP problem"""

        if optimized and self.only_different:
            return self.optimized_constraint_propagation()

        return self.general_constraint_propagation()
    
    def general_constraint_propagation(self):
        for constraint in self.constraints:
            if not self.arc_consistency(constraint[0], constraint[1])[0]:
                return False

        return True

    def constraint_key(self, constraint):
        return min(map(lambda var: self.variable_domain_sizes[var], constraint[1]))

    def optimized_constraint_propagation(self):
        #order constriants by their variables' domain sizes
        self.constraints.sort(key=self.constraint_key)
        
        all_binary = max(map(lambda constraint: len(constraint[1]), self.constraints)) == 2

        #do constraint propagation
        while self.constraints and self.constraint_key(self.constraints[0]) == 1:
            i = 0
            constraints_count = len(self.constraints)
            while i < constraints_count: 
                constraint_type, variables = self.constraints[i]
                consistent, stop, delete = self.arc_consistency(constraint_type, variables)
                if not consistent:
                    return False
                if delete:
                    self.constraints.pop(i)
                    constraints_count -= 1
                    i -= 1
                if stop:
                    break
                i += 1

            if not all_binary:
                break

            self.constraints.sort(key=self.constraint_key)

        return True

    def arc_consistency(self, constraint_type, variables):
        """Performs arc consistency on the two domains assuming != constraint.

        Removes from the domains the values that do not have support in the other domain."""

        domain_sizes = map(lambda var: self.variable_domain_sizes[var], variables)
        if not 1 in domain_sizes:
            return True, True, False

        delete_constraint = True
        domain_sizes = map(lambda var: self.variable_domain_sizes[var], variables)
        has_domain_with_several_values = False
        for domain_size in domain_sizes:
            if domain_size != 1:
                if has_domain_with_several_values == True:
                    delete_constraint = False
                    break
                has_domain_with_several_values = True

        domains = map(lambda var: self.variable_domains[var], variables)
        domains = constraint_type(domains)
        for i, domain in enumerate(domains):
            self.variable_domain_sizes[variables[i]] = len(domain)
            self.variable_domains[variables[i]] = domain

        domain_sizes = map(lambda var: self.variable_domain_sizes[var], variables)
        consistent = not 0 in domain_sizes
        
        return consistent, False, delete_constraint
                
    def is_solved(self):
        """Checks if the CSP is solved.

        A CSP is solved if every variable is assigned exactly 1 value."""

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

        print state

    def get_variable_domain(self, variable, sort_values):
        """Return the domain of the variable.

        Given a variable return the set of its allowed values."""

        if sort_values == 0:
            return self.variable_domains[variable]
        elif sort_values == 1:
            return self.sort_values_by_tightness(variable)
        else:
            return self.sort_values_by_related_domain_sizes(variable)

    def sort_values_by_tightness(self, variable):
        values = list(self.variable_domains[variable])
        related_variables = set()
        for constraint in self.constraints:
            variables = constraint[1]
            if variable in variables:
                for var in variables:
                    if variable != var:
                        related_variables.add(var)

        values_tightness = []
        for value in values:
            tightness = 0
            for var in related_variables:
                if value in self.variable_domains[var]:
                    tightness += 1
            values_tightness.append((tightness, value))

        values_tightness.sort(reverse=True)#default = smallest tightness first
        return zip(*values_tightness)[1]

    def sort_values_by_related_domain_sizes(self, variable):
        values = list(self.variable_domains[variable])
        related_variables = set()
        for constraint in self.constraints:
            variables = constraint[1]
            if variable in variables:
                for var in variables:
                    if variable != var:
                        related_variables.add(var)

        related_domain_sizes = []
        for value in values:
            smallest_domain_size = sys.maxint
            for var in related_variables:
                domain = self.variable_domains[var]
                if value in domain:
                    domain_size = len(domain)
                    if domain_size == 1:
                        smallest_domain_size = sys.maxint
                        break
                    if domain_size < smallest_domain_size:
                        smallest_domain_size = domain_size
            related_domain_sizes.append((smallest_domain_size, value))

        related_domain_sizes.sort()#default = smallest tightness first
        return zip(*related_domain_sizes)[1]

    def get_variable_for_splitting(self, use_mrv, use_mcv):
        variables = {}
        if use_mrv:
            variables = self.get_mrv_vars()

        if len(variables) == 1:
			return variables.pop()
		
        if use_mcv:
            return self.get_mcv_vars(variables)	

        if len(variables) > 0:
            return variables.pop()

        for variable, domain_size in enumerate(self.variable_domain_sizes):
            if domain_size > 1:
                return variable
        
        return 0

    def get_mrv_vars(self):
        """A Minimum Remaining Values Heuristic function.

        Returns the variable that has still not been assigned a value,
        and has the least amount of possible values."""

        #variables is a list of variables
        best_variables = set()
        smallest_domain_size = sys.maxint

        for var, domain_size in enumerate(self.variable_domain_sizes):
            if domain_size <= 1:
                continue
    
            if domain_size > smallest_domain_size:
                continue
    
            if domain_size < smallest_domain_size:
                best_variables.clear()
                smallest_domain_size = domain_size
    
            best_variables.add(var)

        return best_variables

    def get_mcv_vars(self, variables):
        if not variables:
            variables = self.get_unassigned_variables()

        nconstraints = dict()
        for var in variables:
            nconstraints[var] = 0

        for constraint in self.constraints:
            for var in constraint[1]:
                if var in variables:
                    nconstraints[var] += 1

        return max(nconstraints.iteritems(), key=lambda k_v_pair: k_v_pair[1])[0]

    #TODO: This is unused and left because it might turn out needed later.
    #Try not to use it though.
    def get_unassigned_variables(self):
        """Return a list of the unassigned variables.

        Return a list of the the variables,
        which have not yet been assigned a value."""

        unassigned_variables = []
        for variable, domain_size in enumerate(self.variable_domain_sizes):
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

        csp_copy = CSProblem()

        csp_copy.variable_domains = copy.deepcopy(self.variable_domains)
        csp_copy.variable_domain_sizes = copy.deepcopy(self.variable_domain_sizes)
        csp_copy.constraints = copy.deepcopy(self.constraints)
        csp_copy.only_different = self.only_different

        return csp_copy

