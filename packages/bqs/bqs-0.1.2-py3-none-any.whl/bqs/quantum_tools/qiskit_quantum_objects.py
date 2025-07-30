from .abstract_quantum_objects import AbstractQuantumObjects
from typing import Any
from bidict import bidict

# Qiskit set of objects
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit_aer import Aer

class QiskitQuantumObjects(AbstractQuantumObjects):

    def __init__(self, backend_name="aer_simulator", **kwargs):

        # Gets backend name
        self.backend_name = backend_name

        # Collects optional inputs
        token = kwargs.pop('token', None)
        url = kwargs.pop('url', None)

        if backend_name == 'quantum_ibm':
            # IBM quantum computer
            QiskitRuntimeService.save_account(channel="ibm_quantum",
                                                token=token,
                                                overwrite=True, set_as_default=True)
            service = QiskitRuntimeService(channel='ibm_quantum')
            self.backend = service.least_busy()

        elif backend_name == "aer_simulator":
            # Local CPU simulator
            self.backend = Aer.get_backend('qasm_simulator')

        else:
            raise ValueError("Backend not recognized.")

    @staticmethod
    def qubit(index):
        return index
    

    @staticmethod
    def circuit(num_qubits, *args):
        return QuantumCircuit(num_qubits)
    

    @staticmethod
    def append(
        circuit: QuantumCircuit, 
        operation, 
    ):
        """
        Appends an operation to the current quantum circuit.
        
        args:
            circuit: is a QuantumCircuit object of length the number of qubits used in the circuit.
            operation: is a tuple of length 2 containing:
                - the method that implements the gate you want to append.
                - the list og arguments, first extra argument 
                    (e.g. angles for rotational gates), 
                    followed by the qubit(s) upon which the gate is applies 
        """

        if len(operation) != 2:
            raise ValueError(
                "Only tuple with gate name and arguments (qubit"
                " + possible argument like rotational angles)"
                " must be provided."
            )
        
        # Collects the information to create the correct operation to append
        gate, args = operation

        # Gets the method needed to apply the gate to the qubit
        applied_gate = getattr(circuit, gate)

        # Stores the operation
        applied_gate(*args)


    def sample(
            self,
            circuit: Any, 
            qubit_name_to_object: dict, 
            num_samples: int, 
            **kwargs
        ) -> dict[Any, int]:

        qc = circuit.copy()

        qc.measure_all()
        sampler = Sampler(mode=self.backend)
        pub = (qc,)
        job = sampler.run([pub], shots=num_samples)


        # A set of bitstrings collected as samples
        results = job.result()
        bitstrings = [
            bitstring[::-1] for bitstring in results[0].data.meas.get_bitstrings()
        ]

        # Creates the bidict version of the qubit_name_to_object variable
        qubit_name_to_object = bidict(qubit_name_to_object)

        solutions = [
            {
                qubit_name: 1-2*int(bitstring[index]) 
                for index, qubit_name in enumerate(qubit_name_to_object)
            }
            for bitstring in bitstrings
        ]

        return solutions


    @staticmethod
    def H(qubit):
        return ('h', [qubit])
    

    @staticmethod
    def X(qubit):
        return ('x', [qubit])
    

    @staticmethod
    def Y(qubit):
        return ('y', [qubit])
    

    @staticmethod
    def rx(qubit, angle):
        return ('rx', [angle, qubit])
    

    @staticmethod
    def ry(qubit, angle):
        return ('ry', [angle, qubit])
    

    @staticmethod
    def rz(qubit, angle):
        return ('rz', [angle, qubit])
    

    @staticmethod
    def CNOT(qubit1, qubit2):
        return ('cx', [qubit1, qubit2])
    
