from abc import abstractmethod
from typing import Any
from bidict import bidict

# Abstract Quantum Object rule
class AbstractQuantumObjects:

    @abstractmethod
    def qubit(index, **kwargs):
        pass
    

    @abstractmethod    
    def circuit(*args):
        pass
    

    @abstractmethod
    def append(circuit, operation):
        """
        It appends an operation on a qubit to a quantum circuit"""
        pass


    @abstractmethod   
    def sample(
            circuit, 
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
        pass
    

    @abstractmethod   
    def H(qubit):
        pass


    @abstractmethod    
    def X(qubit):
        pass
    

    @abstractmethod    
    def Y(qubit):
        pass
    

    @abstractmethod
    def Z(qubit):
        pass
    

    @abstractmethod    
    def CNOT(qubit1, qubit2):
        pass


    @abstractmethod    
    def rx(qubit, angle):
        pass
    

    @abstractmethod
    def ry(qubit, angle):
        pass


    @abstractmethod
    def rz(qubit, angle):
        pass
