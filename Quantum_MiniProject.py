# Import qiskit and numpy libraries
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute
import numpy as np

# Take input number array from user
array = input("Enter a list of numbers separated by space: ")
array = list(map(int, array.split()))

# User will give a random number
target = int(input("Enter a number to search: "))

# Check if the number is present in the array
if target not in array:
    print(f"{target} is not present in the array.")
else:
    # Sort the array in ascending order
    array.sort()

    # Find the index of the number in binary format
    index = format(array.index(target), f"0{len(array).bit_length()}b")

    # Define quantum registers for the index and the oracle qubits
    qr = QuantumRegister(len(index) + 1)
    # Define classical registers for the measurement
    cr = ClassicalRegister(len(index))
    # Define a quantum circuit
    qc = QuantumCircuit(qr, cr)

    # Initialize all qubits to |+> state except the last one
    qc.h(qr[:-1])
    qc.x(qr[-1])
    qc.h(qr[-1])

    # Define the oracle that flips the phase of the target index
    for i in range(len(index)):
        if index[i] == "0":
            qc.x(qr[i])
    qc.mct(qr[:-1], qr[-1]) # multi-controlled-toffoli
    for i in range(len(index)):
        if index[i] == "0":
            qc.x(qr[i])

    # Apply the Grover operator
    qc.barrier()
    qc.h(qr[:-1])
    qc.x(qr[:-1])
    qc.h(qr[-1])
    qc.mct(qr[:-1], qr[-1])
    qc.h(qr[-1])
    qc.x(qr[:-1])
    qc.h(qr[:-1])
    qc.barrier()

    # Measure the index qubits
    qc.measure(qr[:-1], cr)

    # Run the circuit on a simulator backend
    backend = Aer.get_backend("qasm_simulator")
    result = execute(qc, backend, shots=1).result()
    counts = result.get_counts()

    # Print the output
    print(f"{target} is present in the array. Time taken {result.time_taken:.3f} seconds.")