import numpy as np
# from numpy_ml.neural_nets.optimizers import Adam as adamopt
import random as rnd
from typing import List, Callable, Tuple, Optional, Dict
from scipy.optimize import OptimizeResult, minimize
from abc import ABC, abstractmethod


from .qaoa_utils import *
from .vqa_utils import CostFunction, VariationalCircuit

########################################################################################################################
# Optimizer
########################################################################################################################

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

        
class MonteCarlo(Optimizer):
    """
    Random guesser that inspects the search space by generating a random set of hyperparameters. It keeps the best set of hyperparameters generated.
    """
    def __init__(self, cost_function: CostFunction, circuit: VariationalCircuit):
        super().__init__(cost_function, circuit)


    def _run(self, objective_function, num_iterations: int, display: bool=False, **kwargs):
        """
        Optimizes the hyperparameters of the give VQA by using a random guesser a lá Monte Carlo.
            
            returns: Best hyperparameters found
        """

        iter = 0
        expectation_value = np.inf

        while iter < num_iterations:
            
            hyperparameters = self.circuit.hyperparameters if iter==0 else np.array([rnd.uniform(0., 2*np.pi) for _ in range(self.len_param)])

            new_expectation_value = objective_function(hyperparameters)

            if new_expectation_value < expectation_value:
                expectation_value = new_expectation_value
                self.circuit.hyperparameters = hyperparameters
            iter += 1

        self.hyperparameters = self.circuit.hyperparameters
        self.circuit.get_circuit_from_hyperparameters()

        if display:
            print("\n\tFinished", end='\n'*2)
            print("\t\t{:^10}\t {:^10}\n\n".format('Best value:'+str(expectation_value), 'Best hyperparameters:'+str(self.circuit.hyperparameters)))

        return OptimizeResult(
            fun=expectation_value,
            x=self.hyperparameters
        )


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


class SPSA(Optimizer):
    """
    Simultaneous perturbation stochastic approximation optimizer.
    """
    def __init__(self, cost_function: CostFunction, circuit: VariationalCircuit):
        super().__init__(cost_function, circuit)


    def optimize(
        self, 
        num_samples_training: int, 
        num_iterations: int, 
        display: bool= False, 
        bounds: list= None,
        **kwargs
    ):
        """
        Optimizes the hyperparameters.

            args: 
                num_samples_training: number of samples used to evaluate the stored cost function,
                num_iterations: number of random generated sets of hyperparameters,
                display: display the best expectation values and hyperparameters if true,
                bounds: list that contains the bounds for each hyperparameter.

                circuit_options: dictionary with options for the method VariationalCircuit().sample
                opt_arguments: dictionary containing keywords and argument to give to the optimizer.
                kwargs: optional arguments for the sample evaluation.

            returns: the best hyperparameters found.
        """
        # Collects the bound of the parameters
        if bounds == None:
            bounds = [[0., 2 * np.pi] for _ in range(self.len_param)]

        circuit_options = kwargs.pop('circuit_options', {})
        opt_arguments = kwargs.pop('opt_arguments', {})

        def _obj_fun(_theta):

            circuit_options['hyperparameters'] = _theta

            solutions = self.circuit.sample(num_samples=num_samples_training, **circuit_options)

            # Storing the mean energy and free allocation memory
            mean_energy = np.float32(self.cost_function.evaluate_samples(solutions, **kwargs))
            del solutions

            return mean_energy

        response = self._run(_obj_fun, x0=self.hyperparameters, maxiter=num_iterations, display=display, bounds=bounds, **opt_arguments)
        self.hyperparameters = response['x']
        self.circuit.hyperparameters = self.hyperparameters

        if display:
            print("\n\tFinished", end='\n'*2)
            print("\t\t{:^10}\t {:^10}\n\n".format('Best value:'+str(response['fun']), 'Best hyperparameters:'+str(self.hyperparameters)))

        return response


    def _run(
            self,
            fun: Callable,
            x0: List[float],
            args: Tuple = (),
            bounds: np.array = None,
            maxfev: int = np.inf,
            maxiter: Optional[int] = None,
            a: float = 1.0,
            alpha: float = 0.602,
            c: float = 1.0,
            gamma: float = 0.101,
            callback: Optional[Callable] = None,
            stages: Optional[bool] = False,
            iteration_counter: Optional[int] = None,
            **options: Dict

    )->OptimizeResult:
        if maxiter is None:
            maxiter = int(np.ceil(maxfev / 2))
        current_params = np.asarray(x0)
        n_params = self.len_param
        A = 100  # 0.01 * maxiter

        best_params = None
        best_feval = np.inf
        FEs_best = 0
        if bounds is not None:
            bounds = np.asarray(bounds)
            if np.shape(bounds) != (n_params, 2):
                raise ValueError(
                    'Pass a min and max bound for each parameter. \n {} \n {}'.format(bounds, n_params))

            def project(x):
                return np.clip(
                    x, bounds[:, 0], bounds[:, 1])

        if iteration_counter is not None:
            iteration_counter = iteration_counter
            n_fevals = 2 * iteration_counter
        else:
            iteration_counter = 0
            n_fevals = 0

        while (iteration_counter < maxiter and n_fevals < maxfev):

            ak = a / (iteration_counter + 1.0 + A) ** alpha
            ck = c / (iteration_counter + 1.0) ** gamma
            Deltak = np.random.choice([-1, 1], size=n_params)

            iteration_counter += 1
            # Each iteration takes 2 function evaluations
            # for gradient evaluation.
            n_fevals += 2
            if bounds is not None:
                # ensure evaluation points are feasible
                # print(current_params + ck * Deltak)
                xplus = project(current_params + ck * Deltak)
                xminus = project(current_params - ck * Deltak)
                grad = (fun(xplus, *args) - fun(xminus, *args)) / (xplus - xminus)
                current_params = project(current_params - ak * grad)
            else:
                grad = ((fun(current_params + ck * Deltak, *args) -
                         fun(current_params - ck * Deltak, *args)) /
                        (2 * ck * Deltak))
                current_params = current_params - (grad * ak)

            current_feval = fun(current_params, *args)

            if current_feval < best_feval:
                best_feval = current_feval
                best_params = np.array(current_params)
                FE_best = n_fevals

            if callback:
                # Takes best parameters, best function evaluation
                # gradient and current iteration number.
                callback(best_params, best_feval,
                         current_feval, grad, iteration_counter)

        if stages:
            return iteration_counter, best_params
        else:
            # print(best_params)
            return OptimizeResult(fun=best_feval,
                                  x=best_params,
                                  FE_best=FE_best,
                                  nit=iteration_counter,
                                  nfev=n_fevals)
