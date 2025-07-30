########################################################################################################################
########################################################################################################################
# Here the whole QAOA is implemented. THIS IS THE FILE THAT YOU NEED TO RUN!
########################################################################################################################
########################################################################################################################

# Packages needed
from abc import abstractmethod
import numpy as np
import random as rnd
import dimod
from typing import Any

# Test
from ..utils import QAOACostFunction, QAOACircuit, pQAOACircuit, pQAOASingleParametersCircuit, \
    SingleSliceQAOACircuit, ppQAOACircuit, ppQAOASingleParametersCircuit, BaseVQA

########################################################################################################################
# Implementation
########################################################################################################################

class BaseQAOA(BaseVQA):
    def __init__(
            self,
            model: dimod.BinaryQuadraticModel,
            p: int=1,
            hyperparameters: np.ndarray=None,
    ):
        # Storing the model
        self.model = model

        # Number of QAOA levels
        self.p = p

        # Initial point where to let the optimization process start
        if type(hyperparameters) == np.ndarray and (hyperparameters != None).all():
            if len(hyperparameters) != 2*p:
                raise ValueError("The number of hyperparameters must double the number of layers.")
            else:
                self.hyperparameters = hyperparameters
        elif hyperparameters == None:
            self.hyperparameters = np.array([rnd.uniform(0., 2 * np.pi) for _ in range(2 * self.p)])
        else:
            raise ValueError("The hyperparameter should be store in a np.ndarray with well-defined entries.")

        self.hyperparameters = self.hyperparameters
        self.optimizer = None

        self.circuit = None
        super().__init__()


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


    def optimize(self, num_samples_training: int, num_iterations: int, **kwargs) -> np.ndarray:
        """
        Optimizes the hyperparameter according to the selected optimizer.

            args:
                num_samples_training: number of samples used to train the hyperparameters,
                num_samples_reading: number of samples collected and returned to the user,
                num_iterations: upper limit on the number of iterations the optimizer can use if it does not reach convergence.

                circuit_options: dictionary with options for the method VariationalCircuit().sample
                opt_arguments: dictionary containing keywords and argument to give to the optimizer.
                kwargs: optional arguments for the sample evaluation.

            returns: A list of samples collected from the circuit after optimizing the hyperparameters.
        """

        if not self.optimizer:
            raise ValueError("No optimizer set to train parameters.")
            
        results = self.optimizer.optimize(
            num_samples_training=num_samples_training, 
            num_iterations=num_iterations,
            **kwargs
        )

        self.hyperparameters = results['x']
        self.circuit.hyperparameters = results['x']

        return results


class QAOA(BaseQAOA):
    """
    Vanilla version of the Quantum Approximate Optimization Algorithm.
    """
    def __init__(
        self,
        model,
        p=1,
        hyperparameters=None,
    ):
        super().__init__(model, p=p, hyperparameters=hyperparameters)

    
    def _set_objective_function(self):
        self.objective_function = QAOACostFunction(self.circuit._model)


    def _set_circuit(self):
        self.circuit = QAOACircuit(self.model, self.p, self.hyperparameters)


    def get_circuit(self):
        return self.circuit.qasm


class pQAOA(BaseQAOA):
    """
    Parallel version of the Quantum Approximate Optimization Algorithm

        args:
            model: the binary quadratic model implementing the combinatorial optimization problem to solve,
            models: list of binary quadratic models that are used to describe the ansatz of the slices.
            p: number of layers of the algorithm,
            hyperparameters: list containing the hyperparameters structured as a list containing the list of hyperparameters 
                of the slices
    """
    def __init__(self, model: dimod.BinaryQuadraticModel, models: list[dimod.BinaryQuadraticModel], p: int = 1, hyperparameters: np.ndarray = None):

        # Storing the model
        self.models = models

        # Storing the model
        self.model = model

        # Number of QAOA levels
        self.p = p

        # Initial point where to let the optimization process start
        if type(hyperparameters) == np.ndarray:
            if len(hyperparameters) == len(models) and np.array([type(row) == np.ndarray for row in hyperparameters]).all() and np.array([len(row) == 2*p for row in hyperparameters]).all():
                self.hyperparameters = hyperparameters
            else:
                raise ValueError("The shape of the hyperparameter tensor is not correct. It should be a matrix where rows are slices and columns are hyperparameters in the slices.")
        elif hyperparameters == None:
            self.hyperparameters = np.array([np.array([rnd.uniform(0., 2 * np.pi) for _ in range(2 * self.p)]) for _ in range(len(models))])
        else:
            raise ValueError(f"The hyperparameter must be a np.ndarray containing as many arrays as number of slices and their size must be {2*p}.")

        self.optimizer = None
        self.circuit = None

        self._set_circuit()
        self._set_objective_function()


    def _set_objective_function(self):
        self.objective_function = QAOACostFunction(
            self.circuit._model
        )


    def _set_circuit(self):
        self.circuit = pQAOACircuit(
            hyperparameters=self.hyperparameters,
            model=self.model,
            models=self.models,
            p=self.p
        )


    def set_optimizer(self, optimizer, **kwargs):
        """
        Sets the optimizer to search the optimal angles of the gates
        """

        # Change the hyperparameters format for the optimization process
        self.circuit._hyperparameters_optimizer_format()

        # Initialize the optimizer
        super().set_optimizer(optimizer, **kwargs)

        # Bringing the hyperparameters back to the slice form
        self.circuit._hyperparameters_slice_format()


    def optimize(self, num_samples_training: int, num_iterations: int, **kwargs):
        """
        Optimizes the hyperparameter according to the selected optimizer.

            args:
                num_samples_training: number of samples used to train the hyperparameters,
                num_samples_reading: number of samples collected and returned to the user,
                num_iterations: upper limit on the number of iterations the optimizer can use if it does not reach convergence.

                circuit_options: dictionary with options for the method VariationalCircuit().sample
                opt_arguments: dictionary containing keywords and argument to give to the optimizer.
                kwargs: optional arguments for the sample evaluation.

            returns: A list of samples collected from the circuit after optimizing the hyperparameters.
        """

        if not self.optimizer:
            raise ValueError("No optimizer set to train parameters.")

        # We have to change the hyperparameters object because the optimizers can optimize only a vector, not a tensor
        self.circuit._hyperparameters_optimizer_format()

        results = self.optimizer.optimize(
            num_samples_training=num_samples_training, 
            num_iterations=num_iterations,
            **kwargs
        )

        self.circuit.hyperparameters = results['x']

        # We bring the hyperparameters back to the slice format
        self.circuit._hyperparameters_slice_format()      
        self.hyperparameters = self.circuit.hyperparameters

        return results


    def get_circuit(self) -> list:
        return [qaoa_slice.get_circuit() for qaoa_slice in self.circuit.qaoa_slices]


class pQAOASingleParameters(pQAOA):
    """
    A parallelized version of QAOA, where each slice has only two parameters per layer.
    """
    def __init__(self, model: dimod.BinaryQuadraticModel, models: list[dimod.BinaryQuadraticModel], p: int = 1, hyperparameters: np.ndarray = None):

        # Storing the model
        self.models = models

        # Storing the model
        self.model = model

        # Number of QAOA levels
        self.p = p

        # Initial point where to let the optimization process start
        if type(hyperparameters) == np.ndarray and (hyperparameters != None).all():
            if len(hyperparameters) != 2*p:
                raise ValueError("The number of hyperparameters must double the number of layers.")
            else:
                self.hyperparameters = hyperparameters
        elif hyperparameters == None:
            self.hyperparameters = np.array([rnd.uniform(0., 2 * np.pi) for _ in range(2 * self.p)])
        else:
            raise ValueError("The hyperparameter should be store in a np.ndarray with well-defined entries.")

        self.optimizer = None
        self.circuit = None

        self._set_circuit()
        self._set_objective_function()


    def _set_circuit(self):
        self.circuit = pQAOASingleParametersCircuit(
            hyperparameters=self.hyperparameters,
            model=self.model,
            models=self.models,
            p=self.p
        )


class SingleSliceQAOA(BaseQAOA):
    """
    Parallelized version of QAOA where all of the slices are identical and only one unique circuit is implemented
    """
    def __init__(
        self, 
        model: dimod.BinaryQuadraticModel, 
        slice_model: dimod.BinaryQuadraticModel,
        slice_var_to_model_var: dict[Any, list[Any]],
        p: int = 1, 
        hyperparameters: np.ndarray = None
        ):

        # Store the unique slice and the number of slices used
        self.slice_model = slice_model

        # Store the mapping between the variables of the slice model to the variables of the model to evaluate
        set_of_model_variables_length = set(map(len, slice_var_to_model_var.values()))
        if len(set_of_model_variables_length) != 1:
            raise ValueError("Every variable in the slice model must have the same number of correspondent variables in the original model.")
        self.slice_var_to_model_var = slice_var_to_model_var
        self.num_slices = set_of_model_variables_length.pop()
        
        super().__init__(model, p, hyperparameters)


    def _set_circuit(self):
        self.circuit = SingleSliceQAOACircuit(
            model=self.slice_model, 
            num_slices=self.num_slices, 
            slice_var_to_model_var=self.slice_var_to_model_var, 
            p=self.p, 
            hyperparameters=self.hyperparameters
            ) 


    def _set_objective_function(self):
        self.objective_function = QAOACostFunction(
            self.model if self.model.vartype == dimod.SPIN else 
            dimod.BinaryQuadraticModel(*self.model.to_ising(), dimod.SPIN)
        )


    def get_circuit(self):
        return self.circuit.qasm


class ppQAOA(pQAOA):
    """pQAOA version where the samples are glued element-wise, instead of using the vectorial product of the space"""
    def __init__(self, model: dimod.BinaryQuadraticModel, models: list[dimod.BinaryQuadraticModel], p: int = 1, hyperparameters: np.ndarray = None):
        super().__init__(model, models, p, hyperparameters)


    def _set_circuit(self):
        self.circuit = ppQAOACircuit(
            hyperparameters=self.hyperparameters,
            model=self.model,
            models=self.models,
            p=self.p
        )


class ppQAOASingleParameters(pQAOASingleParameters):
    """pQAOA version where every slice have the same angles and the samples are glued element-wise"""
    def __init__(self, model: dimod.BinaryQuadraticModel, models: list[dimod.BinaryQuadraticModel], p: int = 1, hyperparameters: np.ndarray = None):
        super().__init__(model, models, p, hyperparameters)


    def _set_circuit(self):
        self.circuit = ppQAOASingleParametersCircuit(
            hyperparameters=self.hyperparameters,
            model=self.model,
            models=self.models,
            p=self.p
        )
    