import re
import os
import argparse
from typing import Dict, List, Optional, Set

class LatexExporter:
    def __init__(self, circuit: Optional[Dict] = None) -> None:
        """Initialize the LatexExporter with an optional circuit dictionary."""
        self.circuit = circuit

    def save_to_file(self, output_dir: str, filename: str, scale: float = 1.0, function_str: Optional[str] = None) -> None:
        """
        Save the generated LaTeX code to a file in the specified output directory.

        Args:
            output_dir (str): Directory to save the LaTeX file.
            filename (str): Name of the LaTeX file (e.g., 'circuit_1.tex').
            scale (float): Scale factor for the circuit diagram.
            function_str (str, optional): Boolean function string to convert to a circuit.
        """
        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Construct the full path for the output file
        output_file = os.path.join(output_dir, filename)
        
        # Generate LaTeX code for the circuit
        latex_code = self.generate_latex(scale, function_str)
        
        # Write the LaTeX code to the file
        with open(output_file, 'w') as file:
            file.write(latex_code)
        print(f"LaTeX code saved to {output_file}")

    def parse_boolean_function(self, expression: str) -> Dict:
        """
        Parse a boolean expression into a structured format (SOP, POS, constant, or simple).

        Args:
            expression (str): Boolean expression (e.g., "a'b' + a'c").

        Returns:
            Dict: Parsed expression with type and terms.
        """
        expression = expression.replace(" ", "")  # Remove spaces

        # Handle constant 0
        if expression == "(0)":
            return {'type': 'constant', 'value': 0}

        # Handle simple expressions like "a" or "a'"
        if not any(c in expression for c in "+*()'") or (expression[-1] == "'" and not any(c in expression[:-1] for c in "+*()")):
            return {'type': 'simple', 'value': expression}

        # Check for Product of Sums (POS) format: (a+b)(c+d)
        if '(' in expression and ')' in expression:
            pattern = r'\(([^()]+)\)'  # Match terms in parentheses
            terms = re.findall(pattern, expression)

            if terms:
                parsed_terms = []
                for term in terms:
                    if '+' in term:  # Sum term like a+b+c
                        literals = term.split('+')
                    else:  # Single literal like a' or b
                        literals = [term]

                    parsed_literals = []
                    for literal in literals:
                        if "'" in literal:
                            var_name = literal.rstrip("'")
                            parsed_literals.append(f"{var_name}'")
                        else:
                            parsed_literals.append(literal)
                    parsed_terms.append(parsed_literals)

                # If all terms are sums, it's POS
                if all(len(term) > 1 or '+' in term for term in terms):
                    return {'type': 'product_of_sums', 'terms': parsed_terms}
                # If single term with + (e.g., (a+b+c)), treat as SOP
                elif len(terms) == 1 and '+' in terms[0]:
                    return {'type': 'sum_of_products', 'terms': [parsed_terms[0]]}
                # Otherwise, it's POS with single literals (e.g., (a')(b'))
                else:
                    return {'type': 'product_of_sums', 'terms': parsed_terms}

        # Handle Sum of Products (SOP) format: a'b + cd
        if '+' in expression:
            terms = expression.split('+')
            parsed_terms = []

            for term in terms:
                if "*" in term:  # Explicit product notation: a*b*c
                    product_terms = term.split("*")
                    parsed_literals = []
                    for product in product_terms:
                        product = product.strip()
                        if "'" in product:
                            var_name = product.rstrip("'")
                            parsed_literals.append(f"{var_name}'")
                        else:
                            parsed_literals.append(product)
                    parsed_terms.append(parsed_literals)
                else:  # Implicit product notation: a'b'c
                    current_term = []
                    i = 0
                    while i < len(term):
                        if term[i].isalpha():
                            var_name = term[i]
                            i += 1
                            if i < len(term) and term[i] == "'":
                                current_term.append(f"{var_name}'")
                                i += 1
                            else:
                                current_term.append(var_name)
                        else:
                            i += 1
                    if current_term:
                        parsed_terms.append(current_term)

            if parsed_terms:
                return {'type': 'sum_of_products', 'terms': parsed_terms}

        # Fallback: treat as single term SOP
        return {'type': 'sum_of_products', 'terms': [[expression]]}

    def extract_boolean_function(self, function_str: str) -> Optional[Dict]:
        """
        Extract variables and expression from a function string like 'f(a,b,c) = a'b' + a'c'.

        Args:
            function_str (str): Function string to parse.

        Returns:
            Dict: Dictionary containing variables, expression, and parsed form, or None if parsing fails.
        """
        # Try to match the function string with or without leading number
        match = re.match(r'f\((.*?)\)\s*=\s*(.*)', function_str)
        if not match:
            print(f"Error: Could not parse function string: '{function_str}'. Expected format: 'f(a,b,c) = expression'")
            return None
        variables = [v.strip().lower() for v in match.group(1).split(',')]
        expression = match.group(2).strip()
        parsed_expression = self.parse_boolean_function(expression)
        return {'variables': variables, 'expression': expression, 'parsed': parsed_expression}

    def generate_latex(self, scale: float = 1.0, function_str: Optional[str] = None) -> str:
        """
        Generate LaTeX code for the circuit diagram.

        Args:
            scale (float): Scale factor for the circuit diagram.
            function_str (str, optional): Boolean function string to convert.

        Returns:
            str: LaTeX code as a string.
        """
        if function_str:
            function_dict = self.extract_boolean_function(function_str)
            if function_dict:
                return self._generate_from_function(function_dict, scale)
            else:
                print(f"Warning: Failed to generate LaTeX for function '{function_str}'. Using default empty circuit.")
        
        return "\\documentclass{standalone}\n\\usepackage{circuitikz}\n\\begin{document}\n\\begin{circuitikz}\n\\end{circuitikz}\n\\end{document}"

    def _extract_used_variables(self, parsed: Dict) -> Set[str]:
        """
        Extract the set of variables used in the parsed expression.

        Args:
            parsed (Dict): Parsed boolean expression.

        Returns:
            Set[str]: Set of used variable names.
        """
        used_vars = set()
        if parsed['type'] == 'simple':
            var = parsed['value'].rstrip("'")
            if var.isalpha():
                used_vars.add(var.lower())
        elif parsed['type'] in ['sum_of_products', 'product_of_sums']:
            for term in parsed['terms']:
                for literal in term:
                    var = literal.rstrip("'")
                    if var.isalpha():
                        used_vars.add(var.lower())
        return used_vars

    def _draw_input_lines(self, filtered_vars: List[str], vertical_extent: float) -> List[str]:
        """
        Generate LaTeX code for drawing input lines.

        Args:
            filtered_vars (List[str]): List of variables to draw.
            vertical_extent (float): Vertical extent of the circuit.

        Returns:
            List[str]: LaTeX code lines for input lines.
        """
        var_spacing = 2.5  # Horizontal spacing between variables
        latex_code = []
        for i, var in enumerate(filtered_vars):
            x_pos = f"{(-i * var_spacing):.1f}"  # Format with one decimal place
            latex_code.append(f"  \\draw ({x_pos},4) node[above] {{$ {var} $}} to[short] ({x_pos},-{vertical_extent:.1f});")
        return latex_code

    def _handle_constant(self) -> List[str]:
        """Generate LaTeX code for a constant 0 output."""
        return [
            "  \\draw (2,0) node[right] {{$ f = 0 $}};",
            "\\end{circuitikz}",
            "\\end{document}"
        ]

    def _handle_simple_expression(self, simple_value: str, filtered_vars: List[str], var_spacing: float) -> List[str]:
        """
        Generate LaTeX code for a simple expression (e.g., 'a', 'a'', 'acd').

        Args:
            simple_value (str): The simple expression.
            filtered_vars (List[str]): List of variables.
            var_spacing (float): Spacing between variables.

        Returns:
            List[str]: LaTeX code lines.
        """
        latex_code = []
        
        # Tách các biến từ chuỗi
        variables = []
        i = 0
        while i < len(simple_value):
            if simple_value[i].isalpha():
                var = simple_value[i]
                i += 1
                if i < len(simple_value) and simple_value[i] == "'":
                    variables.append(f"{var}'")
                    i += 1
                else:
                    variables.append(var)
            else:
                i += 1

        # Nếu chỉ có một biến
        if len(variables) == 1:
            var_name = variables[0].rstrip("'")
            is_inverted = "'" in variables[0]
            if var_name in filtered_vars:
                var_idx = filtered_vars.index(var_name)
                x_pos = f"{(-var_idx * var_spacing):.1f}"
                if is_inverted:
                    latex_code.append(f"  \\draw ({x_pos},0) -- ++(1,0) node[notcirc] (not{var_name}) {{}};")
                    latex_code.append(f"  \\draw (not{var_name}.out) -- ++(1,0) node[right] {{$ f $}};")
                else:
                    latex_code.append(f"  \\draw ({x_pos},0) -- ++(2,0) node[right] {{$ f $}};")
            else:
                latex_code.append(f"  \\draw (0,0) node[right] {{$ f = {simple_value} $}};")
        else:
            # Xử lý trường hợp tích của nhiều biến
            num_inputs = len(variables)
            if num_inputs > 0:
                latex_code.append(f"  \\draw (4,0) node[and port, number inputs={num_inputs}] (and1) {{}};")
                
                # Kết nối các đầu vào
                for j, var in enumerate(variables):
                    input_num = j + 1
                    var_name = var.rstrip("'")
                    is_inverted = "'" in var
                    
                    if var_name in filtered_vars:
                        var_idx = filtered_vars.index(var_name)
                        x_pos = f"{(-var_idx * var_spacing):.1f}"
                        
                        # Tính toán vị trí y cho đầu vào
                        if num_inputs == 1:
                            y_offset = 0.3
                        elif num_inputs == 2:
                            y_offset = 0.3 if input_num == 1 else -0.3
                        elif num_inputs == 3:
                            y_offset = 0.3 if input_num == 1 else (0.0 if input_num == 2 else -0.3)
                        elif num_inputs == 4:
                            y_offset = 0.45 if input_num == 1 else (num_inputs + 1 - 2 * input_num) * 0.2
                        else:
                            y_offset = (num_inputs + 1 - 2 * input_num) * 0.2
                        
                        y_input = y_offset
                        y_input = f"{y_input:.2f}"
                        
                        if is_inverted:
                            latex_code.append(f"  \\draw (and1.in {input_num}) node[notcirc, anchor=out] (not_and1_{j}) {{}};")
                            latex_code.append(f"  \\draw (not_and1_{j}.out) -- ({x_pos},{y_input}) to[short, -*] ({x_pos},{y_input});")
                        else:
                            latex_code.append(f"  \\draw (and1.in {input_num}) -- ({x_pos},{y_input}) to[short, -*] ({x_pos},{y_input});")
                
                # Kết nối đầu ra
                latex_code.append(f"  \\draw (and1.out) -- ++(1,0) node[right] {{$ f $}};")
            else:
                latex_code.append(f"  \\draw (0,0) node[right] {{$ f = {simple_value} $}};")

        latex_code.extend(["\\end{circuitikz}", "\\end{document}"])
        return latex_code

    def _generate_sop_circuit(self, terms: List[List[str]], filtered_vars: List[str]) -> List[str]:
        """
        Generate LaTeX code for a Sum of Products (SOP) circuit.

        Args:
            terms (List[List[str]]): List of product terms.
            filtered_vars (List[str]): List of variables.

        Returns:
            List[str]: LaTeX code lines.
        """
        latex_code = []
        var_spacing = 2.5  # Horizontal spacing between variables
        and_gates = []

        # Create AND gates for each product term
        for i, term in enumerate(terms):
            y_pos = -i * 2.5  # Vertical spacing between gates
            num_inputs = len(term)
            if num_inputs > 0:
                # Sort literals to minimize wire crossing
                sorted_literals = sorted(term, key=lambda x: filtered_vars.index(x.rstrip("'").lower()))
                and_gates.append({"id": f"and{i}", "y_pos": y_pos, "inputs": num_inputs, "literals": sorted_literals})

        # Draw AND gates and connect inputs
        for i, gate in enumerate(and_gates):
            y_pos = f"{gate['y_pos']:.1f}"
            latex_code.append(f"  \\draw (4,{y_pos}) node[and port, number inputs={gate['inputs']}] ({gate['id']}) {{}};")
            for j, literal in enumerate(gate['literals']):
                input_num = j + 1
                var_name = literal.rstrip("'").lower()
                is_inverted = "'" in literal
                if var_name in filtered_vars:
                    var_idx = filtered_vars.index(var_name)
                    x_pos = f"{(-var_idx * var_spacing):.1f}"
                    # Calculate the y-coordinate of the AND gate input
                    # Adjust y-coordinate to align with input lines
                    if gate['inputs'] == 1:
                        y_offset = 0.3  # Single input, align with gate center
                    elif gate['inputs'] == 2:
                        y_offset = 0.3 if input_num == 1 else -0.3
                    elif gate['inputs'] == 3:
                        y_offset = 0.3 if input_num == 1 else (0.0 if input_num == 2 else -0.3)
                    elif gate['inputs'] == 4:
                            y_offset = 0.45 if input_num == 1 else (num_inputs + 1 - 2 * input_num) * 0.2
                    else:
                        # For more than 3 inputs, distribute evenly
                        y_offset = (gate['inputs'] + 1 - 2 * input_num) * 0.2
                    y_input = gate['y_pos'] + y_offset
                    y_input = f"{y_input:.2f}"
                    if is_inverted:
                        latex_code.append(f"  \\draw ({gate['id']}.in {input_num}) node[notcirc, anchor=out] (not_{gate['id']}_{j}) {{}};")
                        # Draw a straight horizontal line from NOT gate to input
                        latex_code.append(f"  \\draw (not_{gate['id']}_{j}.out) -- ({x_pos},{y_input}) to[short, -*] ({x_pos},{y_input});")
                    else:
                        # Draw a straight horizontal line from AND gate input to input
                        latex_code.append(f"  \\draw ({gate['id']}.in {input_num}) -- ({x_pos},{y_input}) to[short, -*] ({x_pos},{y_input});")

        # If multiple AND gates, combine with an OR gate
        if len(and_gates) > 1:
            or_y_pos = sum(gate['y_pos'] for gate in and_gates) / len(and_gates)
            or_y_pos = f"{or_y_pos:.2f}"
            latex_code.append(f"  \\draw (8,{or_y_pos}) node[or port, number inputs={len(and_gates)}] (or1) {{}};")
            for i, gate in enumerate(and_gates):
                input_num = i + 1
                latex_code.append(f"  \\draw ({gate['id']}.out) -| (or1.in {input_num});")
            latex_code.append(f"  \\draw (or1.out) -- ++(1,0) node[right] {{$ f $}};")
        elif len(and_gates) == 1:
            latex_code.append(f"  \\draw (and0.out) -- ++(1,0) node[right] {{$ f $}};")

        return latex_code

    def _generate_pos_circuit(self, terms: List[List[str]], filtered_vars: List[str]) -> List[str]:
        """
        Generate LaTeX code for a Product of Sums (POS) circuit.

        Args:
            terms (List[List[str]]): List of sum terms.
            filtered_vars (List[str]): List of variables.

        Returns:
            List[str]: LaTeX code lines.
        """
        latex_code = []
        var_spacing = 2.5  # Horizontal spacing between variables
        or_gates = []

        # Create OR gates for each sum term
        for i, term in enumerate(terms):
            y_pos = -i * 2.5  # Vertical spacing between gates
            num_inputs = len(term)
            if num_inputs > 0:
                # Sort literals to minimize wire crossing
                sorted_literals = sorted(term, key=lambda x: filtered_vars.index(x.rstrip("'").lower()))
                or_gates.append({"id": f"or{i}", "y_pos": y_pos, "inputs": num_inputs, "literals": sorted_literals})

        # Draw OR gates and connect inputs
        for i, gate in enumerate(or_gates):
            y_pos = f"{gate['y_pos']:.1f}"
            latex_code.append(f"  \\draw (4,{y_pos}) node[or port, number inputs={gate['inputs']}] ({gate['id']}) {{}};")
            for j, literal in enumerate(gate['literals']):
                input_num = j + 1
                var_name = literal.rstrip("'").lower()
                is_inverted = "'" in literal
                if var_name in filtered_vars:
                    var_idx = filtered_vars.index(var_name)
                    x_pos = f"{(-var_idx * var_spacing):.1f}"
                    # Calculate the y-coordinate of the OR gate input
                    # Adjust y-coordinate to align with input lines
                    if gate['inputs'] == 1:
                        y_offset = 0.3  # Single input, align with gate center
                    elif gate['inputs'] == 2:
                        y_offset = 0.3 if input_num == 1 else -0.3
                    elif gate['inputs'] == 3:
                        y_offset = 0.35 if input_num == 1 else (0.0 if input_num == 2 else -0.35)
                    elif gate['inputs'] == 4:
                        y_offset = 0.4 if input_num == 1 else (num_inputs + 1 - 2 * input_num) * 0.2 + 0.1
                    else:
                        # For more than 3 inputs, distribute evenly
                        y_offset = (gate['inputs'] + 1 - 2 * input_num) * 0.2
                    y_input = gate['y_pos'] + y_offset
                    y_input = f"{y_input:.2f}"
                    if is_inverted:
                        latex_code.append(f"  \\draw ({gate['id']}.in {input_num}) node[notcirc, anchor=out] (not_{gate['id']}_{j}) {{}};")
                        # Draw a straight horizontal line from NOT gate to input
                        latex_code.append(f"  \\draw (not_{gate['id']}_{j}.out) -- ({x_pos},{y_input}) to[short, -*] ({x_pos},{y_input});")
                    else:
                        # Draw a straight horizontal line from OR gate input to input
                        latex_code.append(f"  \\draw ({gate['id']}.in {input_num}) -- ({x_pos},{y_input}) to[short, -*] ({x_pos},{y_input});")

        # If multiple OR gates, combine with an AND gate
        if len(or_gates) > 1:
            and_y_pos = sum(gate['y_pos'] for gate in or_gates) / len(or_gates)
            and_y_pos = f"{and_y_pos:.2f}"
            latex_code.append(f"  \\draw (8,{and_y_pos}) node[and port, number inputs={len(or_gates)}] (and1) {{}};")
            for i, gate in enumerate(or_gates):
                input_num = i + 1
                latex_code.append(f"  \\draw ({gate['id']}.out) -| (and1.in {input_num});")
            latex_code.append(f"  \\draw (and1.out) -- ++(1,0) node[right] {{$ f $}};")
        elif len(or_gates) == 1:
            latex_code.append(f"  \\draw (or0.out) -- ++(1,0) node[right] {{$ f $}};")

        return latex_code

    def _generate_from_function(self, function_dict: Dict, scale: float = 1.0) -> str:
        """
        Generate LaTeX code for the circuit based on the parsed function.

        Args:
            function_dict (Dict): Dictionary containing variables, expression, and parsed form.
            scale (float): Scale factor for the circuit diagram.

        Returns:
            str: LaTeX code as a string.
        """
        variables = function_dict['variables']
        expression = function_dict['expression']
        parsed = function_dict['parsed']

        # Extract used variables
        used_vars = self._extract_used_variables(parsed)
        filtered_vars = [var for var in variables if var in used_vars] or variables

        # Initialize LaTeX code with document preamble
        latex_code = [
            "\\documentclass{standalone}",
            "\\usepackage{circuitikz}",
            "\\usepackage{amsmath}",
            "\\begin{document}",
            f"% f({', '.join(variables)}) = {expression}",
            f"\\begin{{circuitikz}}[scale={scale}]"
        ]

        # Calculate vertical extent based on number of gates
        num_terms = len(parsed.get('terms', [])) if parsed['type'] in ['sum_of_products', 'product_of_sums'] else 1
        vertical_extent = max(6, num_terms * 2.5 + 4)  # Adjusted to match example

        # Draw input lines
        latex_code.extend(self._draw_input_lines(filtered_vars, vertical_extent))

        # Handle different types of expressions
        if parsed['type'] == 'constant':
            latex_code.extend(self._handle_constant())
        elif parsed['type'] == 'simple':
            latex_code.extend(self._handle_simple_expression(parsed['value'], filtered_vars, var_spacing=2.5))
        elif parsed['type'] == 'sum_of_products':
            latex_code.extend(self._generate_sop_circuit(parsed['terms'], filtered_vars))
            latex_code.extend(["\\end{circuitikz}", "\\end{document}"])
        elif parsed['type'] == 'product_of_sums':
            latex_code.extend(self._generate_pos_circuit(parsed['terms'], filtered_vars))
            latex_code.extend(["\\end{circuitikz}", "\\end{document}"])

        return "\n".join(latex_code)

def main() -> int:
    """
    Main function to parse command-line arguments and generate LaTeX circuit diagrams.

    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert boolean functions to circuit diagrams in LaTeX.")
    parser.add_argument("input_file", help="Path to the input .txt file containing boolean functions.")
    parser.add_argument("--output_dir", default="circuits", help="Directory to save the output .tex files (default: 'circuits').")
    parser.add_argument("--scale", type=float, default=0.8, help="Scale factor for the circuit diagram (default: 0.8).")
    
    args = parser.parse_args()

    # Read functions from the input file
    try:
        with open(args.input_file, 'r') as f:
            functions = []
            for line in f.readlines():
                line = line.strip()
                if line:  # Ignore empty lines
                    functions.append(line.split(None, 1)[1].strip())
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found. Please create the file and add your functions.")
        return 1

    # Remove duplicates while preserving order
    seen = set()
    unique_functions = []
    for func in functions:
        if func not in seen:
            seen.add(func)
            unique_functions.append(func)

    # Generate .tex files for each function
    exporter = LatexExporter()
    for i, func in enumerate(unique_functions):
        filename = f"circuit_{i+1}.tex"
        exporter.save_to_file(args.output_dir, filename, scale=args.scale, function_str=func)

    return 0

if __name__ == "__main__":
    exit(main())