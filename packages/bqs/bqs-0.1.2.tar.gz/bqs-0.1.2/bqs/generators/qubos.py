from .khot import k_hot
import random as rnd
from abc import ABC
from dimod import BinaryQuadraticModel, BINARY, SPIN
from itertools import combinations, chain, product
import matplotlib.pyplot as plt
import networkx as nx

# TODO 1.: we have to fix the visualizers. They must receive a solution.
# Routing problems
class AbstractTravelSalespersonProblem(ABC):

    def __init__(self, distance_matrix, locations, starting_point=None):

        # Distaces between location
        self.locations = locations
        self.loc_ind = {loc: i for i, loc in enumerate(locations)}
        self.distances = distance_matrix

        # By choosing the starting point we can decrease the number of variable by one
        if starting_point is None:
            self.starting_point = rnd.choice(self.locations)
        else:
            self.starting_point = starting_point 

    def bqm(self, eps=1):
        """
        This is an abstract class form which you can create whatever modification of TSP
        """
        pass

    def visualize(self, fixed_bqm, full_bqm, sol=None):
        """
        Create here you own visualizer for TSP
        """
        pass


class TravelingSalespersonProblem(AbstractTravelSalespersonProblem):

    def __init__(self, distance_matrix, locations, initial_point=None):
        super(TravelingSalespersonProblem, self).__init__(distance_matrix, locations, initial_point)

    def bqm(self, eps=1.):

        tsp = BinaryQuadraticModel({}, {}, 0., BINARY)
        number_of_locations = len(self.locations)

        for loc1, loc2 in combinations(self.locations, 2):
            for pos in range(number_of_locations):
                tsp.add_interaction((loc1, pos), (loc2, (pos+1) % number_of_locations), self.distances[self.loc_ind[loc1]][self.loc_ind[loc2]])
                tsp.add_interaction((loc2, pos), (loc1, (pos+1) % number_of_locations), self.distances[self.loc_ind[loc1]][self.loc_ind[loc2]])
        tsp.scale(1./(max(tsp.quadratic.values()) + eps))

        for row in range(number_of_locations):
            tsp.update(k_hot([var for var in tsp.variables if var[1] == row]))

        for loc in self.locations:
            tsp.update(k_hot([var for var in tsp.variables if var[0] == loc]))

        full_tsp = tsp.copy()

        for loc in self.locations:
            if loc != self.starting_point:
                tsp.fix_variable((loc, 0), 0)
            else:
                tsp.fix_variable((loc, 0), 1)

        return tsp, full_tsp

    def visualize(self, bqm, full_bqm, sol=None):

        x_width = .3
        y_width = .1

        g = nx.DiGraph()
        pos = dict()
        labels = dict()

        for loc in self.locations:
            if loc == self.starting_point:
                sol[(loc, 0)] = 1
            else:
                sol[(loc, 0)] = 0

        if sol:
            on_nodes = [n for n, v in sol.items() if (v == 1)]
        else:
            on_nodes = list()

        counting_locations = {value: key for key, value in enumerate(self.locations)}

        for var in full_bqm.variables:
            loc = counting_locations[var[0]]
            step = var[1]

            x = loc * x_width
            y = step * y_width

            pos[var] = (x, y)

            labels[var] = var[0]
            g.add_node(var)

        if sol:
            for var1, var2 in combinations(full_bqm.variables, 2):
                loc1, pos1 = var1
                loc2, pos2 = var2

                if (sol[var1] == 1) and (sol[var2] == 1):
                    if (pos2 - pos1) == 1:
                        g.add_edge(var1, var2)
                    elif (pos2 - pos1) == -1:
                        g.add_edge(var2, var1)

        nx.draw(nx.Graph())
        nx.draw_networkx_nodes(g, pos, nodelist=g.nodes, node_color='white', edgecolors='black')
        nx.draw_networkx_nodes(g, pos, nodelist=on_nodes, node_color='gray', edgecolors='black')
        nx.draw_networkx_edges(g, pos, edgelist=g.edges(), arrowsize=15, arrowstyle='-|>')
        nx.draw_networkx_labels(g, pos, labels=labels)
        plt.show()


class VRP_slice(AbstractTravelSalespersonProblem):

    def __init__(
            self,
            distance_matrix,
            locations,
            depot=None
    ):
        if depot is None:
            raise ValueError("depot must be provided.")
        if depot not in locations:
            raise ValueError("depot must be one of 'locations'.")
        
        self.depot = depot
        
        super(VRP_slice, self).__init__(distance_matrix, locations, starting_point=depot)

    def bqm(self, eps=1., **kwargs):

        tsp = BinaryQuadraticModel({}, {}, 0., BINARY)
        number_of_locations = len(self.locations)

        for loc1, loc2 in combinations(self.locations, 2):
            for pos in range(number_of_locations):
                tsp.add_interaction((loc1, pos), (loc2, (pos+1) % number_of_locations), self.distances[self.loc_ind[loc1]][self.loc_ind[loc2]])
                tsp.add_interaction((loc2, pos), (loc1, (pos+1) % number_of_locations), self.distances[self.loc_ind[loc1]][self.loc_ind[loc2]])
        tsp.scale(1./(2*max(tsp.quadratic.values()) + eps))

        for step in range(number_of_locations):
            tsp.update(k_hot([(loc, step) for loc in self.locations]))

        # This is neede to generate the vehicle routing problem
        self._full_tsp = tsp.copy()

        for loc in self.locations:
            if loc != self.starting_point:
                tsp.fix_variable((loc, 0), 0)
            else:
                tsp.fix_variable((loc, 0), 1)

        if kwargs:
            if 'vehicle_id' in kwargs.keys():
                
                tsp.relabel_variables({
                    (i, j):  (kwargs['vehicle_id'], i, j) for i, j in tsp.variables
                })
                
                self._full_tsp.relabel_variables({
                    (i, j):  (kwargs['vehicle_id'], i, j) for i, j in self._full_tsp.variables
                })

        return tsp


class VehicleRoutingProblem(object):

    def __init__(
            self,
            distance_matrix,
            locations,
            number_of_vehicles,
            depot=None
    ):
        self.loc_ind = {loc: i for i, loc in enumerate(locations)}

        if depot is None:
            raise ValueError("depot must be provided.")
        if depot not in locations:
            raise ValueError("depot must be one of 'locations'.")
        
        self.depot = depot

        # Locations
        self.locations = locations

        # Number of vehicles in the VRP instance
        self.number_of_vehicles = number_of_vehicles

        # Definition of each slice of VRP
        self.slices = {
            k: VRP_slice(distance_matrix, locations, depot=depot) for k in range(number_of_vehicles)
        }
        

    def bqm(self):

        vrp = BinaryQuadraticModel({}, {}, 0., BINARY)
        
        for k in range(self.number_of_vehicles):
            self.slices[k].bqm(vehicle_id=k)
            vrp += self.slices[k]._full_tsp

        for loc in self.locations:
            if loc != self.depot:
                one_hot = [(k, loc, step) for k in range(self.number_of_vehicles) for step in range(len(self.locations))]
                vrp.update(k_hot(one_hot))
                
        for k in range(self.number_of_vehicles):
            for loc in self.locations:
                if loc != self.depot:
                    vrp.fix_variable((k, loc, 0), 0)
                else:
                    vrp.fix_variable((k, loc, 0), 1)

        return vrp


# Paint Shop Problem.
class AbstractPaintShopProblem(ABC):

    def __init__(
        self,
        seq_of_cars,
        groups_of_cars: list,
        black_cars: list
        ) -> None:
        """
        Abstract class for the paintshop problem

        args:
            seq_of_cars: The sequence of cars to optimize.
            groups_of_cars: The group of cars according to their model/optionals
            black_cars: The number of black cars per group of cars
        """

        assert len(groups_of_cars) == len(black_cars)

        # We initialize the sequence of cars to be optimize
        self.seq_of_cars = seq_of_cars

        # Information about the groups of cars to constraint
        self.groups_of_cars = groups_of_cars
        self.black_cars = black_cars

    
    def bqm(self):
        """Method that generates the bqm of the Paint shop problem"""
        pass

    def visualize(self):
        """Method to visualize a solution given"""
        pass


# Multi-car Paint Shop Problem
class MultiCarPaintShopProblem(AbstractPaintShopProblem):

    def __init__(self, seq_of_cars, groups_of_cars: list, black_cars: list) -> None:
        super().__init__(seq_of_cars, groups_of_cars, black_cars)

        # This dictionary is used to have a visualization of variables that are not used in the computation
        self._fixed_variables = dict()

    def bqm(self,):

        # Initialize the bqm
        psp = BinaryQuadraticModel({}, {}, 0., SPIN)

        # Objective function
        for i, j in zip(self.seq_of_cars, self.seq_of_cars[1:]):
            psp.add_interaction(i, j, -1.0)

        psp.scale(1./len(self.seq_of_cars))

        # We constrain the number of black car in the group of cars:
        for group, num_black_cars in zip(self.groups_of_cars, self.black_cars):
            if num_black_cars == 0:
                for var in group:
                    psp.fix_variable(var, -1)
                    self._fixed_variables.update({var: -1})
            elif num_black_cars == len(group):
                for var in group:
                    psp.fix_variable(var, 1)
                    self._fixed_variables.update({var: 1})
            else:
                psp.update(k_hot(group, k=num_black_cars))

        return psp

    def visualize(self, sol=None):
        
        # We fixed the radiant of the edges to always have the same visualization
        rad = {car: 0.3*(-1)**num for num, car in enumerate(self.seq_of_cars)}

        # We initialize the graph
        line = nx.Graph()
        line.add_edges_from(zip(self.seq_of_cars, self.seq_of_cars[1:]))

        for group in self.groups_of_cars:
            for i, j in combinations(group, 2):
                line.add_edge(i, j)

        pos = {
            node: (num, 0) for num, node in enumerate(self.seq_of_cars)
        }

        if sol == None:

            ax = plt.gca()

            nx.draw(nx.Graph())

            for edge in line.edges:
                if not edge in zip(self.seq_of_cars, self.seq_of_cars[1:]):
                    ax.annotate(
                        "", xy=pos[edge[0]], xytext=pos[edge[1]], arrowprops=dict(
                            arrowstyle='-', color='black', connectionstyle= "arc3, rad=0.3", shrinkA=14, shrinkB=14,
                        )             
                    )
                else:
                    ax.annotate(
                        "", xy=pos[edge[0]], xytext=pos[edge[1]], arrowprops=dict(
                            arrowstyle='-', color='black', connectionstyle= "arc3", shrinkA=14, shrinkB=14,
                        ))

            nx.draw_networkx_nodes(line, pos, nodelist=line.nodes, node_color='white', edgecolors='black', node_size=700)

            plt.show()

        else:

            # The solution is updated with the fixed variables
            sol.update(self._fixed_variables)

            # Node to fill
            black_nodes= [node for node, value in sol.items() if value == 1]

            ax = plt.gca()

            nx.draw(nx.Graph())

            for edge in line.edges:
                if not edge in zip(self.seq_of_cars, self.seq_of_cars[1:]):

                    ax.annotate(
                        "", xy=pos[edge[0]], xytext=pos[edge[1]], arrowprops=dict(
                            arrowstyle='-', color='black', connectionstyle= f"arc3, rad={rad[edge[0]]}", shrinkA=14, shrinkB=14,
                        )             
                    )
                else:
                    ax.annotate(
                        "", xy=pos[edge[0]], xytext=pos[edge[1]], arrowprops=dict(
                            arrowstyle='-', color='black', connectionstyle= "arc3", shrinkA=14, shrinkB=14,
                        ))

            nx.draw_networkx_nodes(line, pos, nodelist=line.nodes, node_color='white', edgecolors='black', node_size=700)
            nx.draw_networkx_nodes(line, pos, nodelist=black_nodes, node_color='black', node_size=700)
            plt.show()


# Slice used to define the model for pQAOA and the multi-color model.
class PSP_slice(MultiCarPaintShopProblem):

    def __init__(self, seq_of_cars, groups_of_cars: list, black_cars: list) -> None:
        super().__init__(seq_of_cars, groups_of_cars, black_cars)

    def bqm(self, color=None):
        
        # The bqm is the same, unless a cloro is given. In that case the variables are relabeled according to that color
        if color == None:
            return super().bqm()
        else:

            old_bqm = super().bqm()

            new_linear = {
                (var, color): value for var, value in old_bqm.linear.items()
            }

            new_quadratic = {
                ((var[0], color), (var[1], color)): value for var, value in old_bqm.quadratic.items()
            }

            return BinaryQuadraticModel(new_linear, new_quadratic, 0., SPIN)

    def visualize(self, sol=None):
        return super().visualize(sol)


# Multi-color multi-car paint shop problem
class MultiColorPaintShopProblem(object):

    def __init__(self, seq_of_cars, groups_of_cars: list, colored_cars: dict[list], white_filler_colors=None) -> None:

        # Input changed a bit and therefore we initialize some of thema again
        # We initialize the sequence of cars to be optimize
        self.seq_of_cars = seq_of_cars

        # Information about the groups of cars to constraint
        self.groups_of_cars = groups_of_cars

        # Check on the validity of the input: The number of cars to be colored must be equal to the number of cars in the sequence
        car_count = sum(chain.from_iterable(colored_cars.values()))
        if car_count != len(seq_of_cars):
            raise ValueError("The number of cars to be colored must be equal to the number of cars in the sequence.")

        self.colored_cars = colored_cars

        # Fixed variables needed to visualize the solution
        self._fixed_variables = dict()

        # In case the filler of the coat are given
        self.filler = [sum([color_info[num] for color_tag, color_info in colored_cars.items() if not color_tag in white_filler_colors]) for num in range(len(groups_of_cars))]
        self.white_filler_colors = white_filler_colors


    def _split(self, bqm: BinaryQuadraticModel, binary_sol):
        """Method to create smaller models to solve the paint shop problem, according to a specific solution of the multi-car binary paint shop problem. 
        Notice that an optimal solution of the binary paint shop problem is a skeleton of an optimal solution of the multi-color paint shop problem, but the contrary it is not true."""

        # Collection of bqms resulting from the disconnection created by fixing the variable
        bqms_to_solve = list()

        # Variables fixed in the process

        # White variables
        white_cars_variable = {
            (car, color_key) for car, value in binary_sol.items() if value == -1 for color_key in self.white_filler_colors
        }
        

        # Now we fix all the variables that share with the white filler variables either the same car label but not the same color, or the same color but not car label
        white_bqm = bqm.copy()

        # Cars painted with a white filler
        white_vars_cars = [white_var[0] for white_var in white_cars_variable]

        for var in [var for var in bqm.variables if var[0] in white_vars_cars and not var[1] in self.white_filler_colors] + [var for var in bqm.variables if not var[0] in white_vars_cars and var[1] in self.white_filler_colors]:
            white_bqm.fix_variable(var, -1)

        # We now recover the connected components of the models
        white_graph = white_bqm.to_networkx_graph()
        white_connected_components = list(nx.connected_components(white_graph))

        for component in white_connected_components:
            linear_terms = {var: white_bqm.linear[var] for var in component}
            quadratic_terms = {(var1, var2): white_bqm.quadratic[var1, var2] for var1, var2 in set(product(component, repeat=2)) & set(white_bqm.quadratic.keys())}

            bqms_to_solve.append(BinaryQuadraticModel(linear_terms, quadratic_terms, 0., SPIN))

        return bqms_to_solve


    def bqm(self, binary_sol=None):        
            
        # We first create a list of all the models of the different colors. We create multi-car binary paint shop problem models according to the colors
        model = BinaryQuadraticModel({}, {}, 0., SPIN)

        # We collect all the fixed variables in the slices in suck a way we already know how to fix them in the full model
        for color, black_cars in self.colored_cars.items():

            # For every color an instance is created and stored
            model_slice = PSP_slice(self.seq_of_cars, self.groups_of_cars, black_cars)

            model.update(
                model_slice.bqm(color=color)
            )

            for car, value in model_slice._fixed_variables.items():

                self._fixed_variables[(car, color)] = value

        # We must constraint the number of color a car can receive. Therefore, we update the model with a 1-hot constraint to all the variables related to the same car
        for car in self.seq_of_cars:

            # Set of variables to constraint
            color_hot = [var for var in model.variables if var[0]==car]

            if len(color_hot) != 0:
                model.update(k_hot(
                    color_hot,
                    k=1
                    ))

        # If a solution to the Multi-car binary paint shop problem is given we can further reduce the computational cost of our model by splitting it in two (or more, dependiing on the connectivity) smaller models.
        if binary_sol == None:     
            return model
        else:
            return self._split(model, binary_sol)


    def visualize(self, sol=None, color_mapping=None):

        # We fixed the radiant of the edges to always have the same visualization
        rad = {car: 0.3*(-1)**num for num, car in enumerate(self.seq_of_cars)}

        if color_mapping == None:

            line = nx.Graph()

            # The objective function is displayed
            color_sequence = [((var1, color), (var2, color)) for var1, var2 in zip(self.seq_of_cars, self.seq_of_cars[1:]) for color in self.colored_cars.keys()]
            line.add_edges_from(color_sequence)

            # The constraints are shown
            for color in self.colored_cars.keys():
                for group in self.groups_of_cars:
                    for i, j in combinations(group, 2):
                        line.add_edge((i, color), (j, color))

            # The 1-hot constraint regarding the color is shown
            for car in self.seq_of_cars:
                for color1, color2 in combinations(self.colored_cars.keys(), 2):
                    line.add_edge((car, color1), (car, color2))
            

            pos = {
                (node, col): (num_car, num_col) for num_car, node in enumerate(self.seq_of_cars) for num_col, col in enumerate(self.colored_cars.keys())
            }


            if sol == None:

                ax = plt.gca()

                nx.draw(nx.Graph())

                for edge in line.edges:
                    if not edge in color_sequence:
                        
                        # For the edges between different color
                        if pos[edge[0]][0] == pos[edge[1]][0]:

                            ax.annotate(
                                "", xy=pos[edge[0]], xytext=pos[edge[1]], arrowprops=dict(
                                    arrowstyle='-', color='black', connectionstyle= "arc3, rad=0.3", shrinkA=14, shrinkB=14,
                                )             
                            )
                        # For the edges between the same color
                        else:

                            ax.annotate(
                                "", xy=pos[edge[0]], xytext=pos[edge[1]], arrowprops=dict(
                                    arrowstyle='-', color='black', connectionstyle= f"arc3, rad={rad[edge[0][0]]}", shrinkA=14, shrinkB=14,
                                )             
                            )

                    else:
                        ax.annotate(
                            "", xy=pos[edge[0]], xytext=pos[edge[1]], arrowprops=dict(
                                arrowstyle='-', color='black', connectionstyle= "arc3", shrinkA=14, shrinkB=14,
                            ))

                nx.draw_networkx_nodes(line, pos, nodelist=line.nodes, node_color='white', edgecolors='black', node_size=700)

                plt.show()

            else:

                # The solution is updated with the fixed variables
                sol.update(self._fixed_variables)

                # Node to fill
                black_nodes= [node for node, value in sol.items() if value == 1]

                ax = plt.gca()

                nx.draw(nx.Graph())

                for edge in line.edges:
                    if not edge in color_sequence:
                        
                        # For the edges between different color
                        if pos[edge[0]][0] == pos[edge[1]][0]:

                            ax.annotate(
                                "", xy=pos[edge[0]], xytext=pos[edge[1]], arrowprops=dict(
                                    arrowstyle='-', color='black', connectionstyle= "arc3, rad=0.3", shrinkA=14, shrinkB=14,
                                )             
                            )
                        # For the edges between the same color
                        else:

                            ax.annotate(
                                "", xy=pos[edge[0]], xytext=pos[edge[1]], arrowprops=dict(
                                    arrowstyle='-', color='black', connectionstyle= f"arc3, rad={rad[edge[0][0]]}", shrinkA=14, shrinkB=14,
                                )             
                            )

                    else:
                        ax.annotate(
                            "", xy=pos[edge[0]], xytext=pos[edge[1]], arrowprops=dict(
                                arrowstyle='-', color='black', connectionstyle= "arc3", shrinkA=14, shrinkB=14,
                            ))

                nx.draw_networkx_nodes(line, pos, nodelist=line.nodes, node_color='white', edgecolors='black', node_size=700)
                nx.draw_networkx_nodes(line, pos, nodelist=black_nodes, node_color='black', node_size=700)
                plt.show()

        else:

            # The solution is updated with the fixed variables
            sol.update(self._fixed_variables)

            color_line = nx.Graph()
            color_line.add_edges_from(zip(self.seq_of_cars, self.seq_of_cars[1:]))

            for group in self.groups_of_cars:
                for i, j in combinations(group, 2):
                    color_line.add_edge(i, j)

            color_pos = {
                node: (num, 0) for num, node in enumerate(self.seq_of_cars)
            }

            ax = plt.gca()

            nx.draw(nx.Graph())

            for edge in color_line.edges:
                if not edge in zip(self.seq_of_cars, self.seq_of_cars[1:]):

                    ax.annotate(
                        "", xy=color_pos[edge[0]], xytext=color_pos[edge[1]], arrowprops=dict(
                            arrowstyle='-', color='black', connectionstyle= f"arc3, rad={rad[edge[0]]}", shrinkA=14, shrinkB=14,
                        )             
                    )
                else:
                    ax.annotate(
                        "", xy=color_pos[edge[0]], xytext=color_pos[edge[1]], arrowprops=dict(
                            arrowstyle='-', color='black', connectionstyle= "arc3", shrinkA=14, shrinkB=14,
                        ))

            nx.draw_networkx_nodes(color_line, color_pos, nodelist=color_line.nodes, node_color='white', edgecolors='black', node_size=700)
            for color_key, color in color_mapping.items():
                nx.draw_networkx_nodes(color_line, color_pos, nodelist=[var[0] for var, value in sol.items() if var[1]==color_key and value == 1], node_color=color, node_size=700)
            plt.show()
