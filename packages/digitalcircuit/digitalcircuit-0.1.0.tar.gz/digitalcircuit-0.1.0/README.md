# DigiCircuit

DigiCircuit is a Python library to convert Boolean expressions to circuit diagrams.

## Installation

```bash
pip install digicircuit
```

## Usage

1. Create an input file with Boolean expressions (e.g., `data.txt`):
```
1 f(a,b,c,d) = a'b'cd' + abc'd + ab'c'd
2 f(a,b,c,d) = acd
2 f(a,b,c,d) = (a+b+c+d)(a'+b'+d')
```

2. Run the command to create circuit diagrams:
```bash
digicircuit data.txt
```

The circuit diagrams will be created in the `circuits` directory in the form of LaTeX files.

### Options

- `--output_dir` or `-o`: Specify the output directory (default: `circuits`)
- `--scale` or `-s`: The scale of the circuit diagrams (default: 1.0)

Example:
```bash
digicircuit data.txt --output_dir my_circuits --scale 1.5
```

## Requirements

- Python >= 3.6
- numpy
- pandas
- openpyxl

## License

MIT License 