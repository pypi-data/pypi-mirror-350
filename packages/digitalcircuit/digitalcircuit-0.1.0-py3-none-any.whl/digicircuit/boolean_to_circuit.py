import os
import argparse
from .boolean_parser import create_circuits_from_file
from .latex_export import LatexExporter

def main():
    parser = argparse.ArgumentParser(description='Convert Boolean expressions to circuit diagrams.')
    parser.add_argument('input_file', help='Input file with Boolean expressions')
    parser.add_argument('--output_dir', '-o', default='circuits', help='Output directory for circuit diagrams')
    parser.add_argument('--scale', '-s', type=float, default=1.0, help='Scale factor for circuit diagrams')
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' not found")
        return 1
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Read the file and remove the leading number
    with open(args.input_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    functions = [line.split(' ', 1)[1] if line[0].isdigit() else line for line in lines]
    print(f"Functions read from file: {functions}")
    
    # Write to a temporary file without the leading numbers
    temp_file = "temp_data.txt"
    with open(temp_file, 'w') as f:
        f.write("\n".join(functions))
    
    # Create circuits from the temporary file
    circuits = create_circuits_from_file(temp_file)

    # Remove duplicates while preserving order
    seen = set()
    unique_circuits = []
    unique_functions = []
    for circuit, func in zip(circuits, functions):
        if func not in seen:
            seen.add(func)
            unique_circuits.append(circuit)
            unique_functions.append(func)

    # Generate LaTeX files for each unique circuit
    for i, (circuit, func) in enumerate(zip(unique_circuits, unique_functions), 1):
        exporter = LatexExporter(circuit)
        output_file = os.path.join(args.output_dir, f"circuit_f{i}.tex")
        exporter.save_to_file(args.output_dir, f"circuit_f{i}.tex", scale=args.scale, function_str=func)
        print(f"Generated {output_file}")
    
    # Remove the temporary file
    if os.path.exists(temp_file):
        os.remove(temp_file)

    return 0

if __name__ == "__main__":
    exit(main()) 