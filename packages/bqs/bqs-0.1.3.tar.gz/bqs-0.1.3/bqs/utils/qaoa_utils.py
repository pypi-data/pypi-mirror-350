########################################################################################################################
########################################################################################################################
# File for storing the function used for the definition of QAOA
########################################################################################################################
########################################################################################################################
# Packages needed
import dimod
import numpy as np
from itertools import product, chain
from typing import Any
from concurrent.futures import ThreadPoolExecutor

from .vqa_utils import VariationalCircuit, CostFunction
from ..quantum_tools import CirqQuantumObjects, AbstractQuantumObjects

# Sets which are the quantum objects used.
_qo = CirqQuantumObjects


def set_new_quantum_objects(quantum_objects: AbstractQuantumObjects):
    
    if not isinstance(quantum_objects, AbstractQuantumObjects):
        raise ValueError(
            "the new objects to create and executed circuit "
                         "must be a child class of `AbstractQuantumObjects`"
        )
    
    global _qo
    _qo = quantum_objects

########################################################################################################################
# QAOA classes
########################################################################################################################
class QAOACircuit(VariationalCircuit):
    """
    Vanilla QAOA variational circuit.
    """
    def __init__(
        self, 
        model: dimod.BinaryQuadraticModel,
        p: int = 1,
        hyperparameters: list = None,
    ):

        # Storing the model to solve
        self.model = model

        # Storing the original spin model to implement the circuit
        if model.vartype == dimod.SPIN:
            self._model = model
        else:
            self._model = dimod.BinaryQuadraticModel(*model.to_ising(), dimod.SPIN)

        # Storing the number of layers
        self.p = p

        super().__init__(
            hyperparameters=hyperparameters, 
            qubit_name_to_object=(
                {
                    var: _qo.qubit(num) 
                    for num, var in enumerate(model.variables)
                } 
            )
        )



    def get_circuit_from_hyperparameters(self, hyperparameters: np.ndarray= None):
        """
        Updates and returns the attribute `circuit` by generating a new `cirq.Circuit` object from the attribute `hyperparameters` or the input given.
        """

        if (type(hyperparameters) == np.ndarray and (hyperparameters != None).all()):
            self.hyperparameters = hyperparameters
        elif hyperparameters == None:
            pass
        else:
            raise ValueError(f"The hyperparameters must be an array of length {2*self.p}.")

        qasm =  get_qaoa_circuit(
            self.qubit_name_to_object, 
            self._model.linear, 
            self._model.quadratic, 
            self.hyperparameters[:self.p], 
            self.hyperparameters[self.p:]
        )

        self.qasm = qasm

        return qasm


    def sample(self, num_samples: int=100, hyperparameters: np.ndarray=None, original_basis=False, **kwargs):
        """
        Collects the samples from the stored vanilla QAOA circuit.

            args:
                num_samples: number of samples collected,
                hyperparameters: array of hyperparameters to evaluate (optional),
                original_basis: it returns the samples in the original basis if true else it returns the collected samples in the spin basis.

                **kwargs: optional arguments for the function qaoa_sampler

            returns: a list of solutions sampled from the QAOA circuit.
        """
        # Checking the hyperparameter input. In case none are given, the ones stored will be used
        qc = self.get_circuit_from_hyperparameters(
            hyperparameters if type(hyperparameters) == np.ndarray and (hyperparameters != None).all() 
            else self.hyperparameters
            )

        samples = _qo.sample(
            circuit=qc,
            qubit_name_to_object=self.qubit_name_to_object,
            num_samples=num_samples
        )

        return self._samples_to_observable_basis(samples) if original_basis else samples


    def _samples_to_observable_basis(self, samples: list[dict]):
        """
        Maps samples collected from QAOA to the original basis eigenvalues.
        """
        if self.model.vartype == dimod.BINARY:
            return [
                {var: 1 if meas==+1 else 0 for var, meas in sample.items()} for sample in samples
            ]
        else:
            return samples


class pQAOACircuit(VariationalCircuit):
    def __init__(
        self, 
        hyperparameters: np.ndarray, 
        model: dimod.BinaryQuadraticModel,
        models: list[dimod.BinaryQuadraticModel],
        p: int = 1,
    ):

        # Storing the model to solve
        self.model = model

        # Storing the original spin model to implement the circuit
        if model.vartype == dimod.SPIN:
            self._model = model
        else:
            self._model = dimod.BinaryQuadraticModel(*model.to_ising(), dimod.SPIN)

        # Storing the number of layers to use
        self.p = p

       # Creating the qaoa slice circuit of the slices that must be glued up by the optimizer
        self.qaoa_slices = [
            QAOACircuit(
                model=slice_model,
                p=p,
                hyperparameters=hyperparameters[index],
            ) for index, slice_model in enumerate(models)
        ]

        # We store a boolean to identify whether the parameters are in the slice or the optimizer format
        self._optimizer_format = False

        super().__init__(
            hyperparameters=hyperparameters, 
        )


    def get_circuit_from_hyperparameters(self, hyperparameters: np.ndarray=None):
        """
        Updates the attribute `circuit` by generating a list of `cirq.Circuit` object of the slices from the attribute `hyperparameters` or the input given.
        """
        if type(hyperparameters) == np.ndarray and np.array([type(row) == np.ndarray for row in hyperparameters]).all() and len(hyperparameters) == len(self.qaoa_slices):
            self.hyperparameters = hyperparameters
        elif hyperparameters == None:
            pass
        else:
            raise ValueError(f"The hyperparameters must be an array of {len(self.hyperparameters)} arrays of length {2*self.p*len(self.qaoa_slices)}.")

        slice_format_hyperparameters = self._format_slice(self.hyperparameters, self.p, len(self.qaoa_slices)) if self._optimizer_format else self.hyperparameters

        qasms =  [
                qaoa_slice.get_circuit_from_hyperparameters(hyperparameters=slice_format_hyperparameters[i]) for i, qaoa_slice in enumerate(self.qaoa_slices)
        ]

        self.qasm = qasms

        return qasms
        

    @staticmethod
    def _parallel_qaoa_sampler(qaoa_slice: VariationalCircuit, num_samples: int, hyperparameters: np.ndarray, kwargs: dict):

        return qaoa_slice.sample(num_samples=num_samples, hyperparameters=hyperparameters, **kwargs)
        

    def sample(self, num_samples=100, hyperparameters=None, original_basis=False, **kwargs):
        """
        Collects the samples from the stored vanilla QAOA circuit.

            args:
                num_samples: number of samples collected,
                hyperparameters: array of hyperparameters to evaluate (optional),
                original_basis: it returns the samples in the original basis if true else it returns the collected samples in the spin basis.

                **kwargs: optional arguments for the function qaoa_sampler

            returns: a list of solutions sampled from the QAOA circuit.
        """

        # Getting optional argument
        parallel = kwargs.pop('parallel', False)

        if self._optimizer_format:
            input_hyperparameters = self._format_slice(
                hyperparameters=hyperparameters if type(hyperparameters)==np.ndarray and (hyperparameters!=None).all() 
                else self.hyperparameters,
                p=self.p,
                num_slices=len(self.qaoa_slices)
            )
        else:
            input_hyperparameters = hyperparameters if type(hyperparameters)==np.ndarray and (hyperparameters!=None).all() else self.hyperparameters

        # Distribution over the CPUs
        if parallel:

            # Collecting the inputs to parallelize the sample process
            with ThreadPoolExecutor() as executor:

                futures = []
                for i, qaoa_slice in enumerate(self.qaoa_slices):
                    future = executor.submit(self._parallel_qaoa_sampler, qaoa_slice, num_samples, input_hyperparameters[i], kwargs)
                    futures.append(future)

            list_of_samples = [future.result() for future in futures]

        else:
            list_of_samples = [
                qaoa_slice.sample(hyperparameters=input_hyperparameters[i],num_samples=num_samples, original_basis=original_basis, **kwargs)
                for i, qaoa_slice in enumerate(self.qaoa_slices)
            ]

        samples = self._glue_slices(list_of_samples)

        return self._samples_to_observable_basis(samples) if original_basis else samples


    def _samples_to_observable_basis(self, samples: list[dict]):
        """
        Maps samples collected from pQAOA to the original basis eigenvalues.
        """
        if self.model.vartype == dimod.BINARY:
            return [
                {var: 1 if meas==+1 else 0 for var, meas in sample.items()} for sample in samples
            ]
        else:
            return samples


    def _hyperparameters_optimizer_format(self):
        """
        transforms the hyperparameters to a vector containing them. This is needed for the optimizer
        """

        if (
                np.array([type(row) == np.ndarray for row in self.hyperparameters]).all() and 
                len(self.hyperparameters) == len(self.qaoa_slices)
        ):

            self.hyperparameters = np.array(list(chain.from_iterable(self.hyperparameters)))
            self._optimizer_format = True
        
        elif type(self.hyperparameters) == np.ndarray and (len(self.hyperparameters) == 2*self.p*len(self.qaoa_slices)):
            pass
        
        else:
            raise ValueError("Wrong hyperparameters format")


    def _hyperparameters_slice_format(self):
        """
        transorms the hyperparameters to a tensor containing the hyperparameters divided by slice
        """

        if (
            np.array([type(row) == np.ndarray for row in self.hyperparameters]).all() and 
            len(self.hyperparameters) == len(self.qaoa_slices)
        ):
            pass
        
        elif type(self.hyperparameters) == np.ndarray and (len(self.hyperparameters) == 2*self.p*len(self.qaoa_slices)):
            self.hyperparameters = self._format_slice(
                hyperparameters=self.hyperparameters, 
                p=self.p, 
                num_slices=len(self.qaoa_slices)
            )
            self._optimizer_format = False
        
        else:
            raise ValueError("Wrong hyperparameters format")


    @staticmethod
    def _glue_slices(solutions: list[list[dict]]):

        full_sols = []
        for tuple_of_sols in product(*solutions):
            sol = dict()
            for slice_sol in tuple_of_sols:
                sol.update(slice_sol)
            full_sols.append(sol)

        return full_sols


    @staticmethod
    def _format_slice(hyperparameters: np.ndarray, p: int, num_slices: int):
        """
        Transforms a list of parameter in slice format
        
            args
                hyperparameters: vector of hyperparameters to divide
                p: layers of QAOA
                num_slices: the number of slices used in the pQAOA algorithm
            
            returns: hyperparameters object in the slice format
        """

        return np.array(
                [np.array(hyperparameters[i*2*p:(i+1)*2*p]) for i in range(num_slices)]
            )


class ppQAOACircuit(pQAOACircuit):
    """pQAOA but to optimize the parameter a elementwise operation is applied, instead of vectorial product"""
    def __init__(
            self, 
            hyperparameters: np.ndarray, 
            model: dimod.BinaryQuadraticModel, 
            models: list[dimod.BinaryQuadraticModel], 
            p: int = 1, 
            ):
        super().__init__(hyperparameters, model, models, p)


    @staticmethod
    def _glue_slices(solutions: list[list[dict]]):
        full_sols = []
        for tuple_of_sols in zip(*solutions):
            sol = dict()
            for slice_sol in tuple_of_sols:
                sol.update(slice_sol)
            full_sols.append(sol)

        return full_sols


class pQAOASingleParametersCircuit(pQAOACircuit):
    """
    Parallelized version of QAOA circuit with 2 parameters per layers
    """
    def __init__(
        self, 
        hyperparameters: np.ndarray, 
        model: dimod.BinaryQuadraticModel,
        models: list[dimod.BinaryQuadraticModel],
        p: int = 1,
    ):

        # Storing the model to solve
        self.model = model

        # Storing the original spin model to implement the circuit
        if model.vartype == dimod.SPIN:
            self._model = model
        else:
            self._model = dimod.BinaryQuadraticModel(*model.to_ising(), dimod.SPIN)

        # Storing the number of layers to use
        self.p = p

       # Creating the qaoa slice circuit of the slices that must be glued up by the optimizer
        self.qaoa_slices = [
            QAOACircuit(
                model=slice_model,
                p=p,
                hyperparameters=hyperparameters,
            ) for slice_model in models
        ]
        
        # Initializing the mapping between qubit name and qubit
        self.qubit_name_to_object=dict(
            chain.from_iterable(
                slice_model.qubit_name_to_object.items()
                for slice_model in self.qaoa_slices
            )
        )

        # We store a boolean to identify whether the parameters are in the slice or the optimizer format
        self._optimizer_format = False

        # Storing the hyperparameters
        self.hyperparameters=hyperparameters

        # Implementing the circuit
        self.qasm = self.get_circuit_from_hyperparameters()


    def sample(self, num_samples=100, hyperparameters=None, original_basis=False, **kwargs):
        """
        Collects the samples from the stored vanilla QAOA circuit.

            args:
                num_samples: number of samples collected,
                hyperparameters: array of hyperparameters to evaluate (optional),
                original_basis: it returns the samples in the original basis if true else it returns the collected samples in the spin basis.

                **kwargs: optional arguments for the function qaoa_sampler

            returns: a list of solutions sampled from the QAOA circuit.
        """

        # Getting optional argument
        parallel = kwargs.pop('parallel', False)

        input_hyperparameters = hyperparameters if type(hyperparameters)==np.ndarray and len(hyperparameters)==self.p*2 and (hyperparameters!=None).all() else self.hyperparameters

        # Distribution over the CPUs
        if parallel:

            # Collecting the inputs to parallelize the sample process
            with ThreadPoolExecutor() as executor:

                futures = []
                for qaoa_slice in self.qaoa_slices:
                    future = executor.submit(self._parallel_qaoa_sampler, qaoa_slice, num_samples, input_hyperparameters, kwargs)
                    futures.append(future)

            list_of_samples = [future.result() for future in futures]

        else:
            list_of_samples = [
                qaoa_slice.sample(hyperparameters=input_hyperparameters,num_samples=num_samples, original_basis=original_basis, **kwargs)
                for qaoa_slice in self.qaoa_slices
            ]

        samples = self._glue_slices(list_of_samples)

        return self._samples_to_observable_basis(samples) if original_basis else samples


    def _hyperparameters_optimizer_format(self):
        self._optimizer_format = True
        return self.hyperparameters


    def _hyperparameters_slice_format(self):
        self._optimizer_format = False
        return self.hyperparameters


    def get_circuit_from_hyperparameters(self, hyperparameters: np.ndarray=None):
        """
        Updates the attribute `circuit` by generating a list of `cirq.Circuit` object of the slices from the attribute `hyperparameters` or the input given.
        """
        if type(hyperparameters) == np.ndarray and np.array([type(row) == np.ndarray for row in hyperparameters]).all() and len(hyperparameters) == len(self.qaoa_slices):
            self.hyperparameters = hyperparameters
        elif hyperparameters == None:
            pass
        else:
            raise ValueError(f"The hyperparameters must be an array of {len(self.hyperparameters)} arrays of length {2*self.p*len(self.qaoa_slices)}.")

        slice_format_hyperparameters = self._format_slice(self.hyperparameters, self.p, len(self.qaoa_slices)) if self._optimizer_format else self.hyperparameters

        qasms =  [
                qaoa_slice.get_circuit_from_hyperparameters(hyperparameters=slice_format_hyperparameters) for i, qaoa_slice in enumerate(self.qaoa_slices)
        ]

        self.qasm = qasms

        return qasms


    @staticmethod
    def _format_slice(hyperparameters: np.ndarray, p: int, num_slices: int):
        return hyperparameters


class ppQAOASingleParametersCircuit(pQAOASingleParametersCircuit):
    """pQAOA but to optimize the parameter a elementwise operation is applied, instead of vectorial product"""
    def __init__(
            self,
            hyperparameters: np.ndarray, 
            model: dimod.BinaryQuadraticModel, 
            models: list[dimod.BinaryQuadraticModel], 
            p: int = 1, 
        ):
        super().__init__(
            hyperparameters, 
            model, 
            models, 
            p, 
        )


    @staticmethod
    def _glue_slices(solutions: list[list[dict]]):
        full_sols = []
        for tuple_of_sols in zip(*solutions):
            sol = dict()
            for slice_sol in tuple_of_sols:
                sol.update(slice_sol)
            full_sols.append(sol)

        return full_sols


class SingleSliceQAOACircuit(QAOACircuit):
    def __init__(
            self, 
            model: dimod.BinaryQuadraticModel, 
            num_slices: int, 
            slice_var_to_model_var: dict[Any: list[Any]], 
            p: int = 1, 
            hyperparameters: list = None, 
        ):        
        super().__init__(
            model, 
            p, 
            hyperparameters, 
        )

        # Storing the slice model
        self.slice_circuit = QAOACircuit(
            self._model, 
            self.p, 
            self.hyperparameters, 
        )

        # Storing the number of slices
        self.num_slices = num_slices

        # Store the mapping between the variables of the slice model to the variables of the model to evaluate
        self.slice_var_to_model_var = slice_var_to_model_var

    @staticmethod
    def _parallel_qaoa_sampler(qaoa_slice: VariationalCircuit, num_samples: int, hyperparameters: np.ndarray, kwargs: dict):

        return qaoa_slice.sample(num_samples=num_samples, hyperparameters=hyperparameters, **kwargs)
    

    def sample(self, num_samples=100, hyperparameters=None, original_basis=False, **kwargs):
        """
        Collects the samples from the stored vanilla QAOA circuit.

            args:
                num_samples: number of samples collected,
                hyperparameters: array of hyperparameters to evaluate (optional),
                original_basis: it returns the samples in the original basis if true else it returns the collected samples in the spin basis.

                **kwargs: optional arguments for the function qaoa_sampler

            returns: a list of solutions sampled from the QAOA circuit.
        """

        input_hyperparameters = hyperparameters if type(hyperparameters)==np.ndarray and len(hyperparameters)==self.p*2 and (hyperparameters!=None).all() else self.hyperparameters

        parallel = kwargs.pop('parallel', False)

        if parallel:

            # Collecting the inputs to parallelize the sample process
            with ThreadPoolExecutor() as executor:

                futures = []
                for _ in range(self.num_slices):
                    future = executor.submit(self._parallel_qaoa_sampler, self.slice_circuit, num_samples, input_hyperparameters, kwargs)
                    futures.append(future)

            slice_samples = chain.from_iterable([future.result() for future in futures])
        else:
            slice_samples = self.slice_circuit.sample(num_samples=num_samples*self.num_slices, hyperparameters=input_hyperparameters, **kwargs)

        samples = self._glue_slices(
            self._slice_sol_to_model(slice_samples)
        )

        return self._samples_to_observable_basis(samples) if original_basis else samples


    @staticmethod
    def _glue_slices(solutions: list[list[dict]]):

        full_sols = []
        for tuple_of_sols in product(*solutions):
            sol = dict()
            for slice_sol in tuple_of_sols:
                sol.update(slice_sol)
            full_sols.append(sol)

        return full_sols
    

    def _slice_sol_to_model(self, samples: list[dict]):
        return [
            [
                {self.slice_var_to_model_var[var][index]: value for var, value in sol.items()} for sol in samples
            ] for index in range(self.num_slices)
        ]


class QAOACostFunction(CostFunction):
    """
    Cost function that represents the Hamiltonian to evaluate the output of a vanilla QAOA circuit.
    """
    def __init__(self, 
        objective_function: dimod.BinaryQuadraticModel
    ):
        self.objective_function = objective_function


    def evaluate_samples(self, solutions: list[dict]):
        """
        Returns the mean energy of the evaluated samples according to the implemented final Hamiltonian of a vanilla QAOA circuit.
        """

        average_magnetization_solution = {
            key: np.mean([sample[key] for sample in solutions]) for key in solutions[0].keys()
        }

        return np.mean(self.objective_function.energy(average_magnetization_solution))


########################################################################################################################
# Functions to generate the circuits
########################################################################################################################

# Function for implementing the interaction energy term
def append_zz_term(qc, qubit_name_to_object, q1, q2, gamma, quad_term):

    '''
    qc: cirq.Circuit() where the gates are going to be append || type == cirq.Circuit()
    qubit_name_to_object: register of qubits implemented in the quantum circuit || type == dict
    q1, q2: qubit indices || the type depends on the keys of qubit_name_to_object
    gamma: QAOA parameter || type == float
    quad_term: quadratic terms of the Hamiltonian model || type == dict
    '''

    _qo.append(qc, _qo.CNOT(qubit_name_to_object[q1], qubit_name_to_object[q2]))
    _qo.append(qc, _qo.rz(qubit_name_to_object[q2], gamma * quad_term[(q1, q2)]))
    _qo.append(qc, _qo.CNOT(qubit_name_to_object[q1],qubit_name_to_object[q2]))


# Function for computing the local energy term
def append_z_term(qc, qubit_name_to_object, q, gamma, lin_term):  # Preparing the gate decomposition for the linear term

    '''
    qc: cirq.Circuit() where the gates are going to be append || type == cirq.Circuit()
    qubit_name_to_object: register of qubits implemented in the quantum circuit || type == dict
    q: qubit indicx || the type depends on the keys of qubit_name_to_object
    gamma: QAOA parameter || type == float
    lin_term: linear terms of the Hamiltonian model || type == dict
    '''
    _qo.append(qc, _qo.rz(qubit_name_to_object[q], gamma * lin_term[q]))


# Obtaining the cost layer
def get_cost_operator_circuit(qc, qubit_name_to_object, lin_term, quad_term, gamma):  # Computing the exponential matrix for H_f

    '''
    qc: cirq.Circuit() where the gates are going to be append || type == cirq.Circuit()
    qubit_name_to_object: register of qubits implemented in the quantum circuit || type == dict
    lin_term: linear terms of the Hamiltonian model || type == dict
    quad_term: quadratic term of the Hamiltonian model || type == dict
    gamma: QAOA parameter || type == float
    '''

    for kl in lin_term.keys():
        append_z_term(qc, qubit_name_to_object, kl, gamma, lin_term)

    for kq1, kq2 in quad_term.keys():
        append_zz_term(qc, qubit_name_to_object, kq1, kq2, gamma, quad_term)


# Functions for implementing the mixing operator term
def append_x_term(qc, qubit_name_to_object, q, beta):

    '''
    qc: cirq.Circuit() where the gates are going to be append || type == cirq.Circuit()
    qubit_name_to_object: register of qubits implemented in the quantum circuit || type == dict
    q: qubit indicx || the type depends on the keys of qubit_name_to_object
    beta: QAOA parameter || type == float
    '''

    _qo.append(qc, _qo.rx(qubit_name_to_object[q], beta))


def get_mixer_operator_circuit(qc, qubit_name_to_object, beta):

    '''
    qc: cirq.Circuit() where the gates are going to be append || type == cirq.Circuit()
    qubit_name_to_object: register of qubits implemented in the quantum circuit || type == dict
    beta: QAOA parameter || type == float
    '''

    for var in qubit_name_to_object.keys():
        append_x_term(qc, qubit_name_to_object, var, beta)


def get_qaoa_circuit(qubit_name_to_object, lin_term, quad_term, beta_list, gamma_list):

    '''
    qubit_name_to_object: register of qubits implemented in the quantum circuit || type == dict
    lin_term: linear terms of the Hamiltonian model || type == dict
    quad_term: quadratic term of the Hamiltonian model || type == dict
    beta_list: list of QAOA parameters || type == list
    gamma_list: list of QAOA parameters || type == list
    '''
    assert (len(beta_list) == len(gamma_list))
    p = len(beta_list)  # infering number of QAOA steps from the parameters passed
    qc = _qo.circuit(len(qubit_name_to_object))

    # first, apply a layer of Hadamards
    for qubit in qubit_name_to_object.values():
        _qo.append(qc, _qo.H(qubit))

    # second, apply p alternating operators
    for i in range(p):
        get_cost_operator_circuit(qc, qubit_name_to_object, lin_term, quad_term, gamma_list[i])
        get_mixer_operator_circuit(qc, qubit_name_to_object, beta_list[i])

    return qc

