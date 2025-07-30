# Better Quantum Software for the implementation of Variational Quantum Algorithms

In this document you will find a derivation of the algorithm used to solve the knapsack problem with relatively small quantum hardware. All the theoretical aspects of this algorithm are described in the work [Parallel Circuit Implementation of Variational Quantum Algorithms](https://arxiv.org/pdf/2304.03037).

The core idea behind this `Python` library it is to give a viable way for building parallelized variational quantum algorithm as well as having a scalable framework to customized and optimized parameterized quantum circuit in the most flexible way.

## General description of the framework
The idea comes from a black-box optimization problem. Let consider a global problem $P$ described by the black-box function $f_P(\boldsymbol{\theta})$, depending on a set of hyperparameters $\boldsymbol{\theta}\in\mathbb{R}^{p}$ and a model function $f$ that can evaluate the outcome of the black-box function $f_P$. $f_P$ is a probabilistic function whose outcome depends on the hyperparameters $\boldsymbol{\theta}\in\mathbb{R}^{p}$ that encodes the features to describe the solution of the global optimization problem $P$. 

The core idea is to identify $k$ smaller logical sub-problems $SP_i$ that encodes only some features of the global problem $P$. These should be inform by the structure of the global problem $P$ and aiming to identify string features that might be redundant or that constraint too much the search of the solution.

By doing so, to each subproblem $SP_i$ a black-box function $f_{SP_i}(\boldsymbol{\theta})$ is assigned. Then, the black-box functions of the sub-problems are only use to collect a sample set to be evaluated by the global problem function $f$. In general, the whole process can be seen as 

![Parallelization framework](bqs/.images/parallelization_framework.png)

In the picture $S$ describe the sample set obtained by evaluating the subproblem functions $f_{SP_i}$ and by gluing the solution obtained to get a solution that can be evaluated with the global function $f$.

## The QUBO of the knapsack problem

In the multi-knapsack problem we have a set of items $I\coloneqq\{0, \ldots, n-1\}$ associated with utilities $\mathcal{U}\coloneqq\{u_{i}|i\in I\}$ and weights $\mathcal{W}\coloneqq\{w_{i}|i\in I\}$ and a set of $m$ knapsacks that must be with the items and that can contain at most $\mathcal{C}\coloneqq\{ l_b|i=0,\ldots,m-1 \}$. The goal is to maximize the utilities of the items contained in the knapsack by knowing that the knapsacks cannot contain more weight than their capacities and each item can be assigned either to one knapsack or to none. 

We define the decision variables as $x_{i, b}\coloneqq ''1$ if $i$ is in knapsack $b$ else $0$''.

The objective function can be written as
$$Q_{\mathrm{of}}\coloneqq -\sum_{i\in I}\sum_{b=0}^{m-1} \frac{u_i}{U} x_{i,b},$$
where $U\coloneqq\sum_{i\in I}u_i$. In addition, we can impose that the items ca be included in only one knapsack or none by adding to $Q_{\mathrm{of}}$ the function
$$\lambda\cdot Q_{\mathrm{hol}}\coloneqq \lambda\cdot\sum_{i\in I}\sum_{b_1\lt b_2}x_{i,b_1}x_{i,b_2},$$
where $\lambda$ is a parameter that we must set, we will discuss its role later.

Conversely, to ensure the constraints we have to consider the inequalities
$$\sum_{i\in I} u_i x_{i,b}\le l_b\quad\forall b=0,\ldots,m-1$$
we must multiply th left term and the right term with the least common denominator $D$ between the $u_i\mathrm{s}$ and $l_b$ and add slack variables to rewrite this inequalities as equalities. Thus, we can write
$$\lambda\cdot Q_{\mathrm{cap}}=\lambda\cdot\sum_{b=0}^{m-1} \left( D\sum_{i\in I} u_i x_{i,b} + \sum_{a=0}^{\lceil \mathrm{log}_2 D\cdot l_b\rceil}2^{a}x_a - D\cdot l_b \right)^{2}. $$

Finally, the function to minimize is
$$Q=Q_{\mathrm{of}}+\lambda\cdot\left(Q_{\mathrm{hol}} + Q_{\mathrm{cap}}\right),$$

where $\lambda$
 is a penalty term that can be tuned to make the global minimum of this function coincides to the global minimum of the optimization problem. A sufficient condition, to ensure that $\lambda$ fulfills is such, is $\lambda>1$.

 ## The issue with this formulation
Clearly, $Q_{\mathrm{cap}}$ add several auxiliary variables per constraints. This represent an issue especially in the NISQ era since the number of variable used is also the number of qubit required to solve the problem. Thus, we will use the parallelized framework to overcome this issue.

## The Quantum Approximate Optimization Algorithm (QAOA)
In this setting we identify the QAOA to be the global probabilistic black-box function. QAOA is a variational quantum algorithm used to solve combinatorial optimization problems modeled as QUBOs.

The algorithm is made out of two components: a parameterized quantum circuit that depends on the hyperparameters $(\boldsymbol{\gamma}, \boldsymbol{\beta})\in\mathbb{R}^{p\times p}$ and a classical subroutine that minimize the QUBO function evaluated over a sample set collected from executing and measuring the circuit several time.

So, the parameterized quantum circuit is defined as
$$U(\boldsymbol{\gamma}, \boldsymbol{\beta})\coloneqq e^{-i H_i\beta_p}e^{-i H_f \gamma_p}\cdots e^{-i H_i\beta_1}e^{-i H_f \gamma_1}H^{\otimes_{n\cdot m}},$$
where $H_i\coloneqq \sum_{i\in I}\sum_{b=0}^{m-1} X_{i,b}$, $H_f$ is the function $Q$ rewritten under the change of basis $x_{i,b}\mapsto (1-Z_{i,b})/2$, and $H^{\otimes_{n\cdot m}}$ is the application of the Hadamard gate to all the qubits.

After implementing $U(\boldsymbol{\gamma}, \boldsymbol{\beta})$, we execute it and measure it several times, and we create a sample set $S(\boldsymbol{\gamma}, \boldsymbol{\beta})$ with the samples collected from the circuit (that are the measurements of the qubits after the application of $U(\boldsymbol{\gamma}, \boldsymbol{\beta})$). We use $S(\boldsymbol{\gamma}, \boldsymbol{\beta})$ to evaluate the function $H_f$ and, by means of a black-box optimizer we look for the minimum of the function 
$$\frac{1}{|S|}\sum_{s\in S(\boldsymbol{\gamma}, \boldsymbol{\beta})}\langle s|H_f|s \rangle.$$
At each iteration the optimizer compute the next set of hyperparameters to use to compute $U(\boldsymbol{\gamma}, \boldsymbol{\beta})$.

## Decomposition of the problem
Since the increasing number of qubits due to the auxiliary variable is a problem to the optimization, we will change the definition of the function so that it is easy to identify the sub-problems that will be implemented as slices.

We write the new function as 
$$f(\boldsymbol{x})\coloneqq Q_{\mathrm{of}} + \lambda\left(Q_{\mathrm{hol}} + \sum_{b=0}^{m-1} \mathbb{I}_{\sum u_i x_{i,b}\gt l_{b}}(\boldsymbol{x})\right),$$
where $\mathbb{I}_{\sum u_i x_{i,b}\gt l_{b}}(\boldsymbol{x})$ is the indicator function of the capacity constraint, i.e. it returns $1$ if the point $\boldsymbol{x}$ does not satisfy the $b$-th constraint else $0$.

From this description of the function we can see that 
$$Q_{\mathrm{of}} + \lambda\cdot Q_{\mathrm{hol}}=\sum_{i\in I} \left( \sum_{b} -u_ix_{i,b} + \lambda\sum_{b_1\lt b_2}x_{i,b_1}x_{i, b_2}\right)=\sum_{i\in I} Q_i,$$
is a QUBO and that the sums in the brackets are disconnected in the sense that there is no quadratic term that involves two different $i\mathrm{s}$. Thus, those are the sub-problems we were looking for and we can write the subproblem black-box functions as
$$f^{p}_{SP_i}(\boldsymbol{\gamma}, \boldsymbol{\theta}) =  e^{-i H_i'\beta_p}e^{-i H_{SP_i} \gamma_p}\cdots e^{-i H_i'\beta_1}e^{-i H_{SP_i} \gamma_1}H^{\otimes_{m}}\ket{0}^{\otimes_{m}},$$
where $H_i'\coloneqq \sum_{b=0}^{m-1} X_i$, $H_{SP_i}$ is obtained from $Q_i$ using the map $x_{i,b}\mapsto (1-Z_{i,b})/2$, and $\ket{0}^{\otimes_{m}}$ is the state whose all qubits are in the ground state.

Notice that $f^{p}_{SP_i}$ is a QAOA circuit built from the QUBO problem $Q_i$. In the same fashion as before, we can collected the samples from $f^{p}_{SP_i}$ to build a sample set, glue the results back together, and evaluate them with $f$
$$\frac{1}{|S(\boldsymbol{\gamma}, \boldsymbol{\theta})|}\sum_{s\in S(\boldsymbol{\gamma}, \boldsymbol{\theta})}f(s).$$

# The code
The code to execute the parallelized framework is called ``bqs`` and it consists on four main abstract object classes: ``CostFunction``, ``VariationalCircuit``, and ``Optimizer``. Then, there is a final abstract class to implement the VQA: `BaseVQA`.

## Variational Quantum algorithms
The package ``bqs`` has been written to have a flexible way of writing any variational quantum algorithm (VQA). VQA are hybrid classical-quantum algorithms that consist of two part: a quantum part, that is a parameterized quantum circuit that we want to train; and, a classical part, that is a loss function to evaluate the outcome of the quantum circuit and a classical optimizer that returns at each iteration the set of hyperparameters used to initialize the parameterized quantum circuit.

As you can note, the main classes of ``bqs`` represent the main components of the VQA (quantum: `VariationalCircuit`, `Solver`; classical: `Optimizer`, `CostFunction`).

## The parameterized quantum circuit
The class ``VariationalCircuit`` is used to implement the parameterized quantum circuit. Differently from the previous class, the shape of this and its features must be fixed as for the abstract class. Notice that this class is base on ``cirq``. So far this package can only work with object defined with ``cirq``. This specification is done because of some labelling problem of the qubits. In different packages the labelling is done in different ways and so we must stick to one package. However, the simulation of the quantum circuit can be handle by different packages by using the QASM representation of the quantum circuit.

The ``VariationalCircuit`` class looks like:


```
class VariationalCircuit(ABC):
    """
    Variational quantum circuit that store the information on how it is created and its hyperparameters.
    """
    def __init__(
        self,
        hyperparameters: np.ndarray,
        qubit_name_to_object: dict[any: cirq.NamedQubit] = None
    ):

        # Storing the hyperparameter
        self.hyperparameters = hyperparameters

        # Storing or getting the order of the qubits
        if qubit_name_to_object == None:
            self.qubit_name_to_object = {
                qubit.name: qubit for qubit in self.qasm.all_qubits()
            }
        else:
            self.qubit_name_to_object = qubit_name_to_object

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
```

We give a brief description of this class' attributes and the methods.

Attributes:
- ``hyperparameters``: This is an ``numpy.ndarray`` vector, whose length is the number of hyperparameters of the circuit and entries are the hyperparameters.
- ``qubit_name_to_object``: This is a ``dict`` containing a mapping between the label of the qubits and the ``cirq.NamedQubit`` objects. It is important because otherwise the output solutions could not be read.
- ``qasm``: This gives the QASM representation of the quantum circuit.

Methods:
- ``__init__``: This script for the method must be inserted in the ``__init__`` definition of the child class since it is essential for the implementation of the VQA.
- ```get_circuit_from_hyperparameters```: This method is used to initialized the quantum circuit given a set of hyperparameters. It must return an ``cirq.Circuit`` object.
- ``sample``: This method is fundamental as it returns the list of solutions that are evaluated by the loss function. This method is the bridge between the quantum part and the classical part of the VQA.

### The quantum object class definition

There are different `Python` packages to simulate quantum circuits. We allows to embed whichever the user prefer by sticking to a precise structure. The definition of qubits, circuits and gates in the `VariationalCircuit` class depends on classes whose parent class is
```
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

```

Let us break down each of its components:
- `qubit`: takes as input a index (`int`) and return as output the way the qubits are handled in the package to apply operations on them. (e.g. in `cirq` they are `NamedQubit`, in qiskit they are `int` indices of the circuit qubits)
- `circuit`: initializes the circuit, specifying the number of qubits.
- `append`: appends one operation to the circuit. The operation must be a new gate applied to some qubits.
- `sample`: collects samples from the circuit given as input. It takes as input the circuit object and the operation to append. it must return a dictionary whose keys are the qubit names and values are the measurement in the computational basis (eigenvalues: $\pm 1$).

The rest of the methods are the implementation of the main gates to produce quantum circuits.

This class is used as the core of the quantum computing part. You can consider this as the grammar to write quantum circuit in this package. Once a new custom class is written you can use it with:
```
import ... # All your imports
from bqs import set_new_quantum_objects

class CustomQuantumObjects(AbstractQuantumObjects):
    ...

set_new_quantum_objects(CustomQuantumObjects(**your_inputs))
``` 
## The cost function
The cost function is a classical function that evaluates the outcome of a quantum circuit. To make this as flexible as possible there is no restriction on neither the features nor the shape of a ``CostFunction`` class. The only requirement is the implementation of the method ``evaluate_samples`` that takes as input possible solutions to the optimization problem and return a function of their values. The abstract class for the cost function looks like

```
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
        """
        pass
```

Even though the ``__init__`` method is defined it can be customized. The method ``evaluate_samples`` must take as input a list of solutions, whose implementation is customizable, and it must return a float. The function ``CostFunction.evaluate_samples`` is the loss function of our model.

## Optimizer
The optimizer is a classical black-box optimization method that is used to find the optimal hyperparameters that minimize the loss function given. We can consider the quantum circuit and the loss function together as the black-box function to optimize. To write this pythonically, the black-box function is ``CostFunction.evaluate_samples(VariationalCircuit(some_hyperparameters).sample(num_of_samples))``.

Thus this must be included in the ``Optimizer`` definition. Therefore, this class must consider both the ``VariationalCircuit`` and the ``CostFunction`` as input in order to store and optimize the black-box function of the VQA.

The outlook of the ``Optimizer`` class is:

```
class Optimizer(ABC):
    def __init__(
            self,
            cost_function: CostFunction,
            circuit: VariationalCircuit
    ):

        # Get the length of hyperparameters
        self.len_param = len(circuit.hyperparameters)

        # Storing the cost function to optimize
        self.cost_function = cost_function

        # Storing the circuit to optimize
        self.circuit = circuit

        # Store the hyperparameters
        if type(circuit.hyperparameters) != np.ndarray:
            self.hyperparameters = [0. for _ in range(self.len_param)]
        else:
            self.hyperparameters = circuit.hyperparameters

    @abstractmethod
    def _run(self, objective_function, num_iterations: int, display: bool=False, **kwargs):
        """
        Optimizes the hyperparameters of the given VQA.

            args:
                num_iterations: upper limit on the number of iterations before the convergence.,
                display: displays information about the optimization subroutine if true.

                kwargs: optional arguments for the optimizer.
            
            returns: Best hyperparameters found
        """
        pass


    def optimize(
        self, 
        num_samples_training: int, 
        num_iterations: int, 
        display=False, 
        **kwargs
    ):
        """
        Optimizes the hyperparameters.

            args: 
                num_samples_training: number of samples used to evaluate the stored cost function,
                num_iterations: number of random generated sets of hyperparameters,
                display: display the best expectation values and hyperparameters if true,

                circuit_options: dictionary with options for the method VariationalCircuit().sample
                opt_arguments: dictionary containing keywords and argument to give to the optimizer.
                kwargs: optional arguments for the sample evaluation.

            returns: the best hyperparameters found.
        """

        circuit_options = kwargs.pop('circuit_options', {})
        opt_arguments = kwargs.pop('opt_arguments', {})

        if not "display" in opt_arguments.keys():
            opt_arguments["display"] = display

        def _obj_fun(_theta):

            circuit_options['hyperparameters'] = _theta

            solutions = self.circuit.sample(num_samples=num_samples_training, **circuit_options)

            # Storing the mean_energy and deleting the solutions used to save RAM
            mean_energy = np.float32(self.cost_function.evaluate_samples(solutions, **kwargs))
            del solutions

            return mean_energy

        response =  self._run(_obj_fun, num_iterations=num_iterations, **opt_arguments)
        
        # For a nicer visualization
        if display:
            print()

        self.hyperparameters = response['x']
        self.circuit.hyperparameters = self.hyperparameters

        return response
```

Let us give a brief description of the attributes and methods:

Attributes:
- ``len_param``: This is an ``int`` and represents the length of the vector containing the hyperparameters.
- ``cost_function``: The ``CostFunction`` object describing the loss function.
- ``circuit``: The ``VariationalCircuit`` object the returns the list of solutions.
- ``hyperparameters``: This considers the initial hyperparameters and if there are none, it initialized this to the 0 vector.

Methods:
- ``_run``: This is the core method of the VQA. Here the black-box function must be initialized and according to the optimization method, the hyperparameters are optimized. It must take the values: ``num_samples_training`` which represents the number of samples to collect with ``VariationalCircuit.sample``, i.e. in the example before ``num_of_samples == num_samples_training`` during the optimization; and, ``num_iterations`` is the maximum number of iteration that the optimizer can use to reach the minimum.
- `optimize`: Note that this is not an abstract method and it is define such that all the other classes work together. Differently from the above classes, `Optimizer` is less flexible. If the user would like to change the definition of `optimize`, they should be aware of possible conflict with the other classes.

The available and already implemented optimizer are:
- `MonteCarlo`: a random guesser for hyperparameters that collects the best one found.
- `COBYLA`: a gradient-descend black-box optimization algorithm based on the COBYLA method of the package `scipy.optimize`.
- `SPSA`: is another black-box optimization method based on stochastic approximation.

Below it is shown how to define a custom `Optimizer` based on the abstract class and the `scipy.optimize` package.

## The VQA abstract class

The abstract class `BaseVQA` put together all the components already presented. It looks like:
```
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
```

Let us give a brief description of the attributes and methods:

Attributes:
- `hyperparameters`: a set of hyperparameters implemented as a `numpy.ndarray`.
- `optimizer`: the implemented or chosen `Optimizer`.
- `circuit`: the parameterized quantum circuit defined starting from the abstract class `VariationalCircuit`.
- `objective_function`: the loss function class to optimize the hyperparameters. It is implemented starting from `CostFunction`.

Methods:
- `set_optimizer`: set the optimizer using the store `optimizer` and `objective_function`.
- `_set_objective_function`: stores the objective function needed to optime the hyperparameters.
- `_set_circuit`: stores the class which implements the parameterized quantum circuit.
- `get_circuit`: returns the current stored circuit.
- `optimize`: uses the stored classes to execute the VQA.

# Using `bqs`

In this section, the user can find information about the customization of VQA implementation and its execution.

## Defining a custom VQA
In this section we will go through the example of QAOA to understand how such class could be written. We will follow the presentation order given above for the abstract classes and eventually the QAOA classes is explained.

We will implement a version of QAOA where the parameterized quantum circuit is sampled.

### Cost function
In QAOA, the cost function to minimize it the expectation value of the cost Hamiltonian $H_c$ used as observable of the system. Given a set of samples $S\coloneqq\{\ket{s_0},\ldots, \ket{s_{m-1}}\}$ we have to compute the value:
$$\frac{1}{m}\sum_{i=0}^{m-1}\bra{s_i}H_c\ket{s_i}.$$

To implement the optimization problem we use the `dimod` package that is used to implement binary quadratic models. The solutions ot the problem are written as `dict` whose keys are the variable names and values are $0 1$ for binary variables or $\pm1$ for spin variables. Therefore the `CostFunction` can be define as
```
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
``` 

### Solver to simulate the QAOA circuit
The following class wrap the `cirq` class `cirq.Simulator` to be able to use it withing the `bqs` framework. It is important to now that the output solutions must be consistent with the `CostFunction.evaluate_samples` input.
```
class cirqSolver(Solver):
    """
    cirq simulator to sample from a cirq circuit
    """
    def __init__(self):
        
        # cirq simulator to simulate and sample the quantum circuit
        self.sample_function = cirq.Simulator()


    def run(self, quantum_circuit: cirq.Circuit, num_samples: int, **kwargs):
        
        samples = self.sample_function.run(quantum_circuit, repetitions=num_samples, **kwargs)

        return [{key: 1 if value==1 else -1 for key, value in sol.items()} for sol in samples.data.to_dict('records')]
```
### Parameterized quantum circuit

The QAOA parameterized quantum circuit has been explained above. To define the `VariationalCircuit` class, the elementary gates must be defined:
```
def append_zz_term(qc, qubit_name_to_object, q1, q2, gamma, quad_term):
    [...]


# Function for computing the local energy term
def append_z_term(qc, qubit_name_to_object, q, gamma, lin_term):    
    [...]


# Obtaining the cost layer
def get_cost_operator_circuit(qc, qubit_name_to_object, lin_term, quad_term, gamma):  # Computing the exponential matrix for H_f
    [...]


# Functions for implementing the mixing operator term
def append_x_term(qc, qubit_name_to_object, q, beta):
    [...]


def get_mixer_operator_circuit(qc, qubit_name_to_object, beta):
    [...]


def get_qaoa_circuit(qubit_name_to_object, lin_term, quad_term, beta_list, gamma_list):
    [...]
```

All function definitions are available in the package.

To explain and show QAOA `VariationalCircuit` class, we will proceed method by method:
```
class QAOACircuit(VariationalCircuit):
    """
    Vanilla QAOA variational circuit.
    """
    def __init__(
        self, 
        model: dimod.BinaryQuadraticModel,
        p: int = 1,
        hyperparameters: list = None,
        qubit_name_to_object: dict[any, cirq.NamedQubit]=None
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
            qubit_name_to_object={var: cirq.NamedQubit(str(var)) for var in model.variables} if qubit_name_to_object==None 
                else qubit_name_to_object
        )
```
The model is store as a `dimod.BinaryQuadraticModel` and we store a version of the model that represents the Ising cost Hamiltonian to be able to implement the QAOA circuit. We store the number of layers `p`. The rest of the `__init__` is defined by the abstract class.

```
    def get_circuit_from_hyperparameters(self, hyperparameters: np.ndarray= None) -> cirq.Circuit:
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
```
To get the circuit we just needed to put together the functions we defined before. The `cirq.Circuit` object is store as our QASM circuit representation.

Finally, to collect samples from the circuit, we must define the `sample` method with the `Solver` object.
```
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

        # Collecting optional argument
        solver: Solver = kwargs.pop('solver', cirqSolver())

        # Checking the hyperparameter input. In case none are given, the ones stored will be used
        qc = self.get_circuit_from_hyperparameters(
            hyperparameters if type(hyperparameters) == np.ndarray and (hyperparameters != None).all() 
            else self.hyperparameters
            )

        var_to_qubit_name = {var: qb.name for var, qb in self.qubit_name_to_object.items()}
        qubit_name_to_var = {name: var for var, name in var_to_qubit_name.items()}

        for var, qb in self.qubit_name_to_object.items():
            qc.append(cirq.measure(qb, key=var_to_qubit_name[var]))

        sols = solver.run(quantum_circuit=qc, num_samples=num_samples, **kwargs)

        sampled_solutions = sols

        samples = [
            {qubit_name_to_var[var]: value for var, value in sample.items()}
            for sample in sampled_solutions
        ]

        return self._samples_to_observable_basis(samples) if original_basis else samples
```
The most crucial part of the method is the collection of the samples through the `Solver` and the formatting of the solution. Not only we need to change the value from spin-valued to binary-valued variables, but we need to map the qubit names to the variables name we used. 

The below method is used only when the solutions must be printed with the original basis. During the optimization process everything is set to spin variables.
```
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
```

### Optimizer
After collecting the samples the `CostFunction` must be use to compute the loss function. We present the `Optimizer` class `COBYLA` as defined in the package:
```

class COBYLA(Optimizer):
    """
    Constrained Optimization by Linear Approximation optimizer.
    """
    def __init__(self, cost_function: CostFunction, circuit: VariationalCircuit):
        super().__init__(cost_function, circuit)
    

    def _run(self, objective_function, num_iterations: int, display: bool=False, **kwargs):
        """
        Optimizes the hyperparameters of the give VQA by using COBYLA.

            args:
                num_iterations: upper limit on the number of iterations before the convergence.,
                display: displays information about the optimization subroutine if true.

                kwargs: optional arguments for the optimizer.
            
            returns: Best hyperparameters found
        """
        res_sample = minimize(
            objective_function, 
            self.hyperparameters, 
            method='COBYLA', 
            options={'maxiter': num_iterations, 'disp': display},
            **kwargs
        )

        return res_sample
```

As the user might notice, once the `_run` method is defined, the optimizer is ready to be used.

### VQA class
Eventually we must define a VQA class that make use of the above defined classes.

```
class QAOA(BaseVQA):

    def __init__(
        self,
        model,
        p=1,
        hyperparameters=None,
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

    
    def _set_objective_function(self):
        self.objective_function = QAOACostFunction(self.circuit._model)


    def _set_circuit(self):
        self.circuit = QAOACircuit(self.model, self.p, self.hyperparameters)


    def get_circuit(self):
        return self.circuit.qasm

    
    def optimize(self, num_samples_training: int, num_iterations: int, **kwargs):
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
```

### Execution
We break down the execution script to show how the defined `QAOA` class could be used.

We build the model and initialized the class
```
import dimod 

model = dimod.BinaryQuadraticModel(
    {1: 0.5, 2: -0.1},
    {(1, 2): -1},
    0.,
    dimod.BINARY
)

alg = QAOA(
    model=model,
    p=2
)
```

Then we must set the optimizer
```
alg.set_optimizer(bqs.COBYLA)
```
And eventually we can optimize the hyperparameters by giving the number of samples and iterations we want to use
```
alg.optimize(num_iterations=10, num_samples_training=10)
```
The outcome of the las cell will return a `scipy.OptimizeResult` class containing the information about the classical optimization process, amongst them we could find the best set of hyperparameters and the best value of the loss function.

To collect some result we can start a sample process directly from the class, since the best set of hyperparameters are already been stored in it
```
alg.circuit.sample(num_samples=100, original_basis=True)
```

Eventually, the script to plot the best solutions found with QAOA is
```
import dimod

model = dimod.BinaryQuadraticModel(
    {1: 0.5, 2: -0.1},
    {(1, 2): -1},
    0.,
    dimod.BINARY
)

alg = QAOA(
    model=model,
    p=2
)
alg.set_optimizer(bqs.COBYLA)
alg.optimize(num_iterations=10, num_samples_training=10)

print(alg.circuit.sample(num_samples=100, original_basis=True))
```

## Parallel QAOA (pQAOA) for the knapsack problem

We put together all the pieces and we create a class to implement the VQA, based on QAOA, to solve the knapsack problem.

```
class knapsackCostFunction(CostFunction):

    def __init__(self, objective: dict , weight_constraints: list[dict], constant_terms: list, item_repetition_constraint: dict):
        
        # Storing loss function
        sum_of_the_weights = sum(objective.values())
        self.objective = {key: value/sum_of_the_weights for key, value in objective.items()}

        # Storing constraints 
        self.weight_constraints = weight_constraints
        self.item_repetition_constraint = item_repetition_constraint
        self.constant_terms = constant_terms


    def _weight_constraint_evaluation(self, solution: dict):
        [...]


    def _item_repetition_constraint_evaluation(self, solution: dict):
        [...]

    def evaluate_samples(self, solutions):
        """
        Evaluates a list of solutions and it returns a float number that represent the energy of the evaluated cost function.

        The solutions must be stored as list of dictionary. whose keys are the name of the variable and values are the observed measurement.
        """

        return np.mean(
            [sum([-self.objective[key[1]] for key, value in sol.items() if (type(key) == tuple) and (value==1)])+sum(self._weight_constraint_evaluation(sol))+self._item_repetition_constraint_evaluation(sol) for sol in solutions]
        )
```
The cost function is defined as above and as you can see is taking into account all the fundamental component to implement the knapsack problem. In this case we consider the samples to be strings of 0s and 1s (obtained from the circuit by measuring it in the computational basis). The method ``knapsackCostFunction.evaluate_samples`` return the mean over a sample set of solutions evaluated with the function
$$f(\boldsymbol{x})= Q_{\mathrm{of}} + \lambda\left(Q_{\mathrm{hol}} + \sum_{b=0}^{m-1} \mathbb{I}_{\sum u_i x_{i,b}\gt l_{b}}(\boldsymbol{x})\right),$$
as described above. The value of $\lambda$ is set to $2$.

We use the ``scipy`` version of Nelder-Mead method. To write it as our ``Optimizer`` class we have to implement the following:

```
class NM(Optimizer):

    """
    Constrained Optimization by Linear Approximation optimizer.
    """

        
    def __init__(self, cost_function: CostFunction, circuit: VariationalCircuit):
        super().__init__(cost_function, circuit)
    

    def _run(self, objective_function, num_iterations: int, display: bool=False, **kwargs):
    [...]

    res_sample = minimize(
        objective_function, 
        self.hyperparameters, 
        method='Nelder-Mead', 
        options=options,
        **kwargs
    )

    return res_sample
```
The optimizer definition follows the trivial implementation of the ``scipy.optimize.minimize`` function.

Finally, we can put all the pieces together and write out VQA class

```
class knapsack_pQAOA(ppQAOASingleParameters):

    def __init__(
            self,
            model: dimod.BinaryQuadraticModel, 
            models: list[dimod.BinaryQuadraticModel], 
            objective: dict, 
            weight_constraints: list[dict], 
            item_repetition_constraint: dict, 
            constant_terms: list,
            p: int = 1, 
            hyperparameters: np.ndarray = None, 
            **kwargs
        ):
        [...]
```
In the ``__init__``, we initialized all the input we needs and that are used to implement the main classes of the VQA.
```
    def _set_objective_function(self):
        self.objective_function = knapsackCostFunction(
            objective=self.objective,
            weight_constraints=self.weight_constraints,
            item_repetition_constraint=self.item_repetition_constraint,
            constant_terms=self.constant_terms
        )
```

This private method is used to set the loss function.

```
    def _set_circuit(self):
        self.circuit = ppQAOASingleParametersCircuit(
            hyperparameters=self.hyperparameters,
            model=self.model,
            models=self.models,
            p=self.p
        )
```

This private method is used to implement the parallel circuits. We use the ``QAOA`` class from ``bqs``, that implement the QAOA circuit and we can get the circuits from each model $Q_i$.

Afterwards during the script we have to assign an optimizer to the VQA. We will use the method ``knapsack_pQAOA.set_optimizer`` to assign the ``NM`` optimizer to the VQA. The we can run ``knapsack_pQAOA.optimize`` to start the optimization subroutine.

```
    def optimize(self, num_samples_training: int, num_samples_reading: int, num_iterations: int, **kwargs):
        [...]

        # We have to change the hyperparameters object because the optimizers can optimize only a vector, not a tensor
        self.circuit._hyperparameters_optimizer_format()

        results = self.optimizer.optimize(
            num_samples_training=num_samples_training, 
            num_iterations=num_iterations,
            **kwargs
        )

        self.circuit.hyperparameters = results

        # We bring the hyperparameters back to the slice format
        self.circuit._hyperparameters_slice_format()      
        self.hyperparameters = self.circuit.hyperparameters

        samples_from_circuit =  self.circuit.sample(num_samples=num_samples_reading, hyperparameters=self.hyperparameters, original_basis=True)
        # We re-add the solutions that were discard a priori and we return them
        for sol in samples_from_circuit:
            sol.update(self._solution_extension)

        return samples_from_circuit

```

After the optimization the circuit is initialized with the set of best hyperparameters found and the samples are collected from the circuit once more. Among this sample set one can find the best solution.
