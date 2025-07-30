from .abstract_quantum_objects import AbstractQuantumObjects
from typing import Any
from bidict import bidict

# Cirq set of objects
from cirq import NamedQubit, Circuit # building the circuit
from cirq import H, X, Y, Z, CNOT # Clifford gates
from cirq import rx, ry, rz # Non-Clifford gates
from cirq import measure, Simulator # Measurement

class CirqQuantumObjects(AbstractQuantumObjects):

    @staticmethod    
    def qubit(index, **kwargs):
        return NamedQubit(str(index), **kwargs)
    
    
    @staticmethod    
    def circuit(*args):
        return Circuit()
    
    
    @staticmethod
    def append(circuit: Circuit, operation):
        return circuit.append(operation)
    
    
    @staticmethod
    def sample(
            circuit: Any, 
            qubit_name_to_object: dict, 
            num_samples: int, 
            **kwargs
        ) -> dict[Any, int]:
        """
        Function to sample from the implemented circuit. 
        It must take as an input the circuit of the chosen object type and
        collects samples from it without modifying it (see the example with cirq).
        The output must be a list of dictionary whose keys are the qubit names and 
        values are the qubit measurements in the spin basis.

        args:
            circuit: circuit object.
            qubit_name_to_object: a dictionary, whose keys are the qubit names and 
                values are the qubit objects
            num_samples: the number of samples the user wants to collect.
        
        returns:
            A list of dictionary containing the solutions written as dictionary whose keys
            are the qubit names and values are the measurement in the spin bases.
        """

        # Copy the circuit to not modify it
        qc = circuit.copy()

        var_to_qubit_name = bidict(
            {var: qb.name for var, qb in qubit_name_to_object.items()}
        )

        for var, qb in qubit_name_to_object.items():
            qc.append(measure(qb, key=var_to_qubit_name[var]))

        sols = Simulator().run(
            qc, 
            repetitions=num_samples, 
            **kwargs
        )

        # Converts cirq.Simulator output to dict of solution
        sampled_solutions = [{key: 1 if value==1 else -1 for key, value in sol.items()} for sol in sols.data.to_dict('records')]


        samples = [
            {var_to_qubit_name.inv[var]: value for var, value in sample.items()}
            for sample in sampled_solutions
        ]

        return samples
    
    
    @staticmethod
    def H(qubit):
        return H(qubit)


    @staticmethod
    def X(qubit):
        return X(qubit)
    
    
    @staticmethod
    def Y(qubit):
        return Y(qubit)
    
    
    @staticmethod
    def Z(qubit):
        return Z(qubit)
    
    
    @staticmethod
    def CNOT(qubit1, qubit2):
        return CNOT(qubit1, qubit2)


    @staticmethod
    def rx(qubit, angle):
        return rx(angle)(qubit)
    
    
    @staticmethod
    def ry(qubit, angle):
        return ry(angle)(qubit)


    @staticmethod
    def rz(qubit, angle):
        return rz(angle)(qubit) 

