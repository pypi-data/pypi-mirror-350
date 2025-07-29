"""
Module for parsing and processing Boolean expressions.
"""

import re
from .gate import Gate
from .circuit import Circuit

def parse_expression(expr):
    """
    Parse a logical expression and return a list of terms, each containing a list of factors.
    
    Example: a'c'+a'b' -> [['~a', 'c'], ['~a', '~b']]
    
    Args:
        expr (str): Boolean expression in sum-of-products form
        
    Returns:
        list: Nested list of terms and factors
    """
    expr = expr.replace(" ", "")
    or_terms = expr.split("+")  # Split OR terms
    result = []
    for term in or_terms:
        factors = []
        i = 0
        while i < len(term):
            if i + 1 < len(term) and term[i + 1] == "'":
                factors.append("~" + term[i])
                i += 2
            else:
                factors.append(term[i])
                i += 1
        result.append(factors)
    return result

def extract_variables(functions):
    """
    Extract all variables used in the functions.
    
    Args:
        functions (list): List of (index, terms) tuples
        
    Returns:
        list: Sorted list of variable names
    """
    variables = set()
    for _, terms in functions:
        for term in terms:
            for factor in term:
                var = factor[1:] if factor.startswith("~") else factor
                variables.add(var)
    return sorted(list(variables))

def read_boolean_functions(filename):
    """
    Read boolean functions from a file.
    
    Args:
        filename (str): Path to the input file
        
    Returns:
        list: List of (index, terms) tuples representing the parsed functions
    """
    functions = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Improved regex to better match the format
        # Match both numbered and unnumbered functions
        matches = re.findall(r"(\d+)?\s*f\(([a-z,]+)\)\s*=\s*([^.\n]+)", content)
        
        for match in matches:
            idx_str, vars_str, expression = match
            
            # If there's an index number, use it; otherwise, use the current position
            idx = int(idx_str) - 1 if idx_str else len(functions)
            
            variables = vars_str.split(',')
            expression = expression.strip()
            terms = parse_expression(expression)
            functions.append((idx, terms))
            
    except Exception as e:
        print(f"Error reading file: {e}")
    
    # Sort by index
    functions.sort(key=lambda x: x[0])
    
    return functions

def create_circuit_from_boolean(expr_idx, terms, variables=None):
    """
    Create a Circuit object from boolean expression terms.
    
    Args:
        expr_idx (int): Index of the expression/function
        terms (list): List of terms from parse_expression
        variables (list, optional): List of variable names. If None, extracts from terms.
        
    Returns:
        Circuit: Circuit object representing the boolean function
    """
    # Create a new circuit
    circuit = Circuit(name=f"Function_{expr_idx}")
    
    if not terms or not isinstance(terms, list):
        # If terms are invalid, return an empty circuit with just an output
        output_gate = Gate(f"f{expr_idx}", "BUFFER", position=(8, 0))
        circuit.add_gate(output_gate)
        return circuit
    
    if not variables:
        # Extract variables used in this expression
        vars_set = set()
        for term in terms:
            if not isinstance(term, list):
                continue  # Skip invalid terms
            for factor in term:
                if not isinstance(factor, str):
                    continue  # Skip invalid factors
                var = factor[1:] if factor.startswith("~") else factor
                vars_set.add(var)
        variables = sorted(list(vars_set))
    
    # Create input gates for each variable
    input_gates = {}
    for i, var in enumerate(variables):
        input_gate = Gate(var.upper(), "BUFFER", position=(0, i*2))
        circuit.add_gate(input_gate)
        input_gates[var] = var.upper()
    
    # Count the number of times each variable needs a NOT gate
    not_counts = {var: 0 for var in variables}
    for term in terms:
        if not isinstance(term, list):
            continue
        for factor in term:
            if not isinstance(factor, str):
                continue
            if factor.startswith("~"):
                var = factor[1:]
                not_counts[var] += 1
    
    # Create NOT gates for variables that need them
    not_gates = {}
    for i, var in enumerate(variables):
        if not_counts[var] > 0:
            not_gate = Gate(f"NOT_{var}", "NOT", position=(2, i*2))
            circuit.add_gate(not_gate)
            circuit.connect_gates(input_gates[var], f"NOT_{var}")
            not_gates[var] = f"NOT_{var}"
    
    # Create AND gates for each term
    and_gates = []
    for i, term in enumerate(terms):
        if not term:  # Skip empty terms
            continue
            
        # Special case: single variable term
        if len(term) == 1:
            factor = term[0]
            gate_id = None
            if factor.startswith("~"):
                var = factor[1:]
                if var in not_gates:
                    gate_id = not_gates[var]
                else:
                    # This should not happen but just in case
                    continue
            else:
                if factor in input_gates:
                    gate_id = input_gates[factor]
                else:
                    # This should not happen but just in case
                    continue
            
            and_gates.append(gate_id)
        else:
            # Multiple variables need an AND gate
            and_gate = Gate(f"AND_{i}", "AND", position=(4, i*2), fan_in=len(term))
            circuit.add_gate(and_gate)
            
            # Connect inputs to AND gate
            for j, factor in enumerate(term):
                input_gate_id = None
                if factor.startswith("~"):
                    var = factor[1:]
                    if var in not_gates:
                        input_gate_id = not_gates[var]
                    else:
                        # Create NOT gate if it doesn't exist
                        not_gate_id = f"NOT_{var}_special"
                        not_gate = Gate(not_gate_id, "NOT", position=(3, i*2 + j*0.5))
                        circuit.add_gate(not_gate)
                        circuit.connect_gates(input_gates[var], not_gate_id)
                        input_gate_id = not_gate_id
                else:
                    input_gate_id = input_gates[factor]
                
                circuit.connect_gates(input_gate_id, f"AND_{i}")
            
            and_gates.append(f"AND_{i}")
    
    # If we have multiple terms, we need an OR gate
    if len(and_gates) > 1:
        or_gate = Gate(f"OR_f{expr_idx}", "OR", position=(6, 0), fan_in=len(and_gates))
        circuit.add_gate(or_gate)
        
        # Connect AND gates to OR gate
        for gate_id in and_gates:
            circuit.connect_gates(gate_id, f"OR_f{expr_idx}")
        
        # Create output gate
        output_gate = Gate(f"f{expr_idx}", "BUFFER", position=(8, 0))
        circuit.add_gate(output_gate)
        circuit.connect_gates(f"OR_f{expr_idx}", f"f{expr_idx}")
    else:
        # Only one term, connect it directly to output
        output_gate = Gate(f"f{expr_idx}", "BUFFER", position=(6, 0))
        circuit.add_gate(output_gate)
        if and_gates:  # Check if we have any gates
            circuit.connect_gates(and_gates[0], f"f{expr_idx}")
    
    return circuit

def create_circuits_from_file(filename):
    """
    Read boolean functions from a file and create circuits for each.
    
    Args:
        filename (str): Path to the input file
        
    Returns:
        list: List of Circuit objects
    """
    functions = read_boolean_functions(filename)
    variables = extract_variables(functions)
    
    circuits = []
    for idx, terms in functions:
        circuit = create_circuit_from_boolean(idx, terms, variables)
        circuits.append(circuit)
    
    return circuits