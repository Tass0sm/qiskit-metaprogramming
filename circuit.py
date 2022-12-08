circuit = QuantumCircuit(2, 2)

# Add a H gate on qubit 0
circuit.h(0)

for i in range(4):
    # Add a CX (CNOT) gate on control qubit 0 and target qubit 1
    circuit.cx(0, 1)
    circuit.h(0)

for i in range(15):
    # Add a CX (CNOT) gate on control qubit 0 and target qubit 1
    circuit.h(1)
    
# Map the quantum measurement to the classical bits
circuit.measure([0,1], [0,1])

# Draw the circuit
circuit.draw()

