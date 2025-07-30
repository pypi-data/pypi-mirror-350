# General packages
from abc import ABC, abstractmethod
import numpy as np

# Packages for quantum computing
import cirq

class VariationalCircuit(ABC):
    """
    Variational quantum circuit that store the information on how it is created and its hyperparameters.
    """
    def __init__(
        self,
        hyperparameters: np.ndarray,
        qubit_name_to_object: dict = None
    ):

        # Storing the hyperparameter
        self.hyperparameters = hyperparameters

        # Storing or getting the order of the qubits
        self.qubit_name_to_object = qubit_name_to_object

        # Implementing the circuit
        self.qasm = self.get_circuit_from_hyperparameters()


    @abstractmethod
    def get_circuit_from_hyperparameters(self, hyperparameters: np.ndarray=None) -> cirq.Circuit:
        """
        Returns and stores a new circuit based on the attribute 'hyperparameters' .
        """
        pass

    @abstractmethod
    def sample(self, num_samples=100, hyperparameters=None):
        """
        Collects samples from the circuit store in the attribute 'qasm' .
        """
        pass


class CostFunction(ABC):
    """
    Functions to evaluate to optimize the hyperparameters of a variational quantum circuit.
    """
    def __init__(
        self
    ):
        pass

    @abstractmethod
    def evaluate_samples(self, solutions):
        """
        Evaluates a list of solutions or a state vector and it returns a float number that represent the energy of the evaluated cost function.

        The solutions must be stored as list of dictionary. whose keys are the name of the variable and values are the observed measurement.
        """
        pass


class BaseVQA(ABC):
    def __init__(
            self
    ):
        self._set_circuit()
        self._set_objective_function()

    
    def set_optimizer(self, optimizer, **kwargs):
        """
        Stores the optimizer to optimize the variational quantum algorithm.
        """
        self.optimizer = optimizer(self.objective_function, self.circuit, **kwargs)   


    @abstractmethod
    def _set_objective_function(self):
        """
        ABSTRACT method: defines the objective function used to optimize the hyperparameters.
        """
        pass    


    @abstractmethod
    def _set_circuit(self):
        """
        ABSTRACT method: defines the circuit object that defines the QAOA circuit.
        """
        pass


    @abstractmethod
    def get_circuit(self):
        """
        Returns the current store QAOA circuit saved as a cirq.Circuit .
        """
        pass


    @abstractmethod
    def optimize(self, num_samples_training: int, num_iterations: int, **kwargs):
        pass
