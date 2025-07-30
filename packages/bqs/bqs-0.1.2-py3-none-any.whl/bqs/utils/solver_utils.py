from abc import ABC, abstractmethod
import cirq

########################################################################################################################
# Functions and classes for the solvers
########################################################################################################################

class Solver(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run(self, quantum_circuit: cirq.Circuit):
        """
        ABSTRACT METHOD: retruns the samples based on the backend used
        """
        pass

# cirq
class cirqSolver(Solver):
    """
    cirq simulator to sample from a cirq circuit
    """
    def __init__(self):
        
        # cirq simulator to simulate and sample the quantum circuit
        self.sample_function = cirq.Simulator()


    def run(self, quantum_circuit: cirq.Circuit, num_samples: int, **kwargs):
        """
        Samples from the simulated circuit and returns samples in the spin basis

            args
                quantum_circuit: the quantum circuit to sample from
                num_samples: the number of samples to collect

                **kwargs: optional arguments of the method cirq.Simulator().run

            returns: solutions in the spin basis
        """
        samples = self.sample_function.run(quantum_circuit, repetitions=num_samples, **kwargs)

        return [{key: 1 if value==1 else -1 for key, value in sol.items()} for sol in samples.data.to_dict('records')]


# IBM
# TODO 1: Fix this script with Qiskit 1.0
try:
    import qiskit
    from qiskit.circuit import Qubit, QuantumRegister
    import qiskit_ibm_runtime
    from qiskit_ibm_runtime import QiskitRuntimeService
    from typing import Iterable

    class IBMSolver(Solver):
        """
        samples from a real IBM hardware implementation of the circuit

            args:
                token: personal token provided by IBM,
                instance: your instance on the IBM Quantum cloud,
                backend: quantum device to use
        """
        def __init__(self, token: str, instance: int, backend: str):
            
            # Information on the qpu
            service = ibm_access(token=token, instance=instance)
            self.qpu = service.get_backend(backend)


        def run(self, quantum_circuit: cirq.Circuit, num_samples: int, optimization_level: int=1, **options):
            """
            Samples from the quantum circuit on th provided device and returns samples in the spin basis

                args
                    quantum_circuit: the quantum circuit to sample from,
                    num_samples: the number of samples to collect,
                    optimization_level: routing on the circuit to compile it into the hardware

                    **options: optional arguments of qiskit_ibm_runtime.Options

                returns: solutions in the spin basis
            """
            # Setting the option
            options = qiskit_ibm_runtime.Options(optimization_level=optimization_level)
            options.execution.shots = num_samples

            sampler = qiskit_ibm_runtime.Sampler(backend=self.qpu, options=options)

            measurement_order = list(quantum_circuit.all_qubits())
            qubit_order = cirq.QubitOrder.explicit(fixed_qubits=measurement_order)
            response = run_cirq_circuit_on_qiskit(quantum_circuit, qubit_order, sampler)
            return results_qiskit_to_cirq(response, num_samples, [qb.name for qb in measurement_order])   


    def ibm_access(token: str, instance: str):
        """
        Subroutine to call the IBM API to the quantum computer.
        
            args
                token: token provided by IBM,
                instance: your personal instance in your IBM account.

            returns: QiskitRuntimeService
        """

        with open('/Users/VWXEII7/VSProjects/pVQA/ibm_token.txt', 'r') as file:
            token = file.read()

        service = QiskitRuntimeService(
            channel='ibm_quantum',
            instance=instance,
            token=token
        )

        return service


    def run_cirq_circuit_on_qiskit(circuit: 'cirq.Circuit', qubit_order: cirq.QubitOrder, sampler):
        """
        Function to run a circuit written with cirq with qiskit. It first transform the circuit in a QASM circuit and the it compiles it in qiskit.
        
        args:
            circuit: Quantum circuit with gates and mesaurements on each qubit.
            qubit_order: The order of the qubits in the QASM quantum circuit.
            sampler: The qiskit solver that connects with the QPU.

        return:
            A dictionary that has as keys the solution written as string bitstrings and as value the distribution of the bitstrings in the final state.
        """

        qasm_output = circuit.to_qasm(qubit_order=qubit_order)
        qasm_circuit = qiskit.QuantumCircuit().from_qasm_str(str(qasm_output))

        physical_circuit = None
        while physical_circuit == None:
            try:
                physical_circuit = qiskit.transpile(qasm_circuit, sampler._backend)
            except:
                print('Failed. Rerunning...')

        # Execute the circuit qiskit backend
        if physical_circuit.layout.final_layout is not None:
            virtual_to_physical = physical_circuit.layout.final_layout.get_physical_bits()
            missing_virtual_qubits = set(range(127)) - set(virtual_to_physical.keys())
            if len(missing_virtual_qubits) != 0:
                missing_physical_qubits = {Qubit(QuantumRegister(127, 'q'), i) for i in range(127)} - set(virtual_to_physical.values())
                physical_circuit.layout.final_layout.from_dict(dict(zip(missing_virtual_qubits, missing_physical_qubits)))

        job = sampler.run(circuits=physical_circuit)
        # Grab results from the job
        return job.result().quasi_dists[0].binary_probabilities(num_bits=len(circuit.all_qubits()))


    def results_qiskit_to_cirq(response: dict, num_samples: int, measurement_order: Iterable):
        """
        Function that returns a compatible format of solution. It takes a dictionary from the function run_cirq_circuit_on_qiskit ans it maps it to a list of solution written as dictionary with qubits as keys and spin values as values.
        
        args:
            response: a dictionary that has as keys the solution written as string bitstrings and as value the distribution of the bitstrings in the final state.
            num_samples: the number of samples collected from the hardware.
            measurement_order: The order of the variable that are defined as qubits in the circuit.
        
        returns: solution in the spin basis
        """

        string_sols = [bit_string for bit_string, percentage in response.items() for _ in range(int(percentage*num_samples))]

        return [dict(zip(measurement_order, [1 - 2*int(spin) for spin in sol])) for sol in string_sols]
except:
    pass

# qsimcirq
# TODO 2 only if qsimcirq is installed
try:

    import cirq
    import qsimcirq

    def create_qsim_options(
        max_fused_gate_size=2,
        disable_gpu=False,
        cpu_threads=1,
        gpu_mode=(0,),
        verbosity=0,
        n_subsvs=-1,
        use_sampler=None,
        debug=False
    ):
        return qsimcirq.QSimOptions(
            max_fused_gate_size=max_fused_gate_size,
            disable_gpu=disable_gpu,
            cpu_threads=cpu_threads,
            gpu_mode=gpu_mode,
            verbosity=verbosity,
            n_subsvs=n_subsvs,
            use_sampler=use_sampler,
            debug=debug
        )


    def qsim_options_from_arguments(ngpus):
        if ngpus > 1:
            return create_qsim_options(gpu_mode=ngpus)
        elif ngpus == 1:
            return create_qsim_options()
        elif ngpus == 0:
            return create_qsim_options(disable_gpu=True, gpu_mode=0, use_sampler=False)


    class qsimcirqSolver(Solver):
        def __init__(self, gpu: int):
            
            # Storing the options for the simulator generated by the number of gpu used
            self.qsim_options = qsim_options_from_arguments(gpu)
            
            
            # Defining the sampler
            self.sampler = qsimcirq.QSimSimulator(qsim_options=self.qsim_options)
            

        def run(self, quantum_circuit: cirq.Circuit, num_samples: int, **kwargs):
            """
            Samples from the simulated circuit and returns samples in the spin basis

                args
                    quantum_circuit: the quantum circuit to sample from
                    num_samples: the number of samples to collect

                    **kwargs: optional arguments of the method cirq.Simulator().run

                returns: solutions in the spin basis
            """
            samples = self.sampler.run(quantum_circuit, repetitions=num_samples, **kwargs)

            return [{key: 1 if value==1 else -1 for key, value in sol.items()} for sol in samples.data.to_dict('records')]


except:
    pass

    