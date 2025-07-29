class Circuit:
    """
    Represents a digital circuit composed of interconnected gates.
    
    Attributes:
        name (str): Name of the circuit
        gates (dict): Dictionary of gates indexed by gate_id
        connections (list): List of (source_id, target_id) tuples representing connections
    """
    
    def __init__(self, name="Untitled Circuit"):
        """
        Initialize a new Circuit object.
        
        Args:
            name (str, optional): Name of the circuit. Defaults to "Untitled Circuit".
        """
        self.name = name
        self.gates = {}
        self.connections = []  # Added connections attribute
    
    def add_gate(self, gate):
        """
        Add a gate to the circuit.
        
        Args:
            gate (Gate): The gate to add to the circuit.
            
        Returns:
            Gate: The added gate.
        """
        if gate.gate_id in self.gates:
            raise ValueError(f"Gate with ID {gate.gate_id} already exists in the circuit.")
            
        self.gates[gate.gate_id] = gate
        return gate
    
    def connect_gates(self, source_id, target_id):
        """
        Connect two gates in the circuit.
        
        Args:
            source_id (str): ID of the source gate
            target_id (str): ID of the target gate
        """
        if source_id not in self.gates:
            raise ValueError(f"Source gate {source_id} not found in circuit.")
        if target_id not in self.gates:
            raise ValueError(f"Target gate {target_id} not found in circuit.")
            
        source_gate = self.gates[source_id]
        target_gate = self.gates[target_id]
            
        source_gate.add_output(target_id)
        target_gate.add_input(source_id)
        
        # Add the connection to the connections list
        self.connections.append((source_id, target_id))
    
    def get_gate(self, gate_id):
        """
        Get a gate by its ID.
        
        Args:
            gate_id (str): ID of the gate to retrieve.
                
        Returns:
            Gate: The requested gate.
        """
        if gate_id not in self.gates:
            raise ValueError(f"Gate {gate_id} not found in circuit.")
        return self.gates[gate_id]
    
    def __repr__(self):
        """String representation of the circuit."""
        return f"Circuit(name={self.name}, gates={len(self.gates)}, connections={len(self.connections)})"