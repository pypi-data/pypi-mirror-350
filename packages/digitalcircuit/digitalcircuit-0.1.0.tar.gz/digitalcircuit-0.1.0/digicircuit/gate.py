"""
Definition of Gate class for digital circuit representation.
"""

class Gate:
    """
    Represents a logic gate in a digital circuit.
    
    Attributes:
        gate_id (str): Unique identifier for the gate
        operation (str): The operation type (AND, OR, NOT, etc.)
        position (tuple): (x, y) coordinates for placement
        fan_in (int): Number of input connections
        fan_out (int): Number of output connections (optional, for reference only)
        inputs (list): List of input gate IDs
        outputs (list): List of output gate IDs
    """
    
    VALID_OPERATIONS = ['AND', 'OR', 'NOT', 'NAND', 'NOR', 'XOR', 'XNOR', 'BUFFER']
    
    def __init__(self, gate_id, operation, position=(0, 0), fan_in=None, fan_out=None):
        """
        Initialize a new Gate object.
        
        Args:
            gate_id (str): Unique identifier for the gate
            operation (str): The operation type (AND, OR, NOT, etc.)
            position (tuple, optional): (x, y) coordinates. Defaults to (0, 0).
            fan_in (int, optional): Number of input connections. Defaults to None.
            fan_out (int, optional): Number of output connections. Defaults to None.
        """
        self.gate_id = gate_id
        
        if operation.upper() not in self.VALID_OPERATIONS:
            raise ValueError(f"Operation must be one of {self.VALID_OPERATIONS}")
        self.operation = operation.upper()
        
        self.position = position
        
        # Set default fan_in based on operation if not specified
        if fan_in is None:
            if self.operation in ['NOT', 'BUFFER']:
                self.fan_in = 1
            else:
                self.fan_in = 2
        else:
            self.fan_in = fan_in
            
        # Fan_out is optional and not used as a hard limit
        self.fan_out = fan_out if fan_out is not None else float('inf')  # Vô hạn nếu không chỉ định
        self.inputs = []
        self.outputs = []
    
    def add_input(self, gate_id):
        """Add an input connection to this gate."""
        if len(self.inputs) < self.fan_in:
            self.inputs.append(gate_id)
        else:
            raise ValueError(f"Cannot add more inputs. Maximum fan-in is {self.fan_in}")
    
    def add_output(self, gate_id):
        """Add an output connection to this gate without hard limit."""
        self.outputs.append(gate_id)
        # Optional: Log if exceeding a reference fan_out
        if self.fan_out != float('inf') and len(self.outputs) > self.fan_out:
            print(f"Cảnh báo: Gate {self.gate_id} vượt quá fan-out tham chiếu {self.fan_out}")
    
    def __repr__(self):
        """String representation of the gate."""
        return f"Gate(id={self.gate_id}, op={self.operation}, pos={self.position})"
    