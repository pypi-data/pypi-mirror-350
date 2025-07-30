import numpy as np
from .helpers import linalg_helpers as linalg_help
from .misc import validators as vd
from .distances import distance_from_brute_force as brute_force
from .distances import distance_from_generators as generators
from .distances import distance_from_gap as qdistrand
from .distances import distance_from_bposd as bposd
from .helpers.graphs import TannerGraph


class BBCode:
    def __init__(self, l: int, m: int, A_expression:list[str], B_expression: list[str], safe_mode = False):
        self.l = l
        self.m = m
        self.A_expression = A_expression
        self.B_expression = B_expression
        self.safe_mode = safe_mode
        self.poly_variables = {}
        self.create_poly_variables()


    def find_distance(self, H_x, H_z, n, k, distance_method):
        if distance_method == 1:
            return brute_force.calculate_distance(H_x, H_z, n, k, status_updates=self.safe_mode)
        if distance_method == 2:
            return generators.calculate_distance(H_x, H_z, n, k, status_updates=self.safe_mode)
        if distance_method == 3:
            return qdistrand.calculate_distance(H_x, H_z, status_updates=self.safe_mode)
        if distance_method == 4:
            return bposd.calculate_distance(H_x, H_z, status_updates=self.safe_mode)


    def create_poly_variables(self):
        # currently using the cyclic groups, and bivariate polynomials
        S_l = linalg_help.create_matrix_S(self.l)
        S_m = linalg_help.create_matrix_S(self.m)

        # Make x and y matrices
        self.poly_variables["i"] = np.eye(self.l * self.m, dtype=int)
        self.poly_variables["x"] = np.kron(S_l, np.eye(self.m, dtype=int))
        self.poly_variables["y"] = np.kron(np.eye(self.l, dtype=int), S_m)

        if self.safe_mode:
            vd.validate_x_y_matrices(self.poly_variables["x"])
            vd.validate_x_y_matrices(self.poly_variables["y"])
        pass


    def construct_matrix_from_expression(self, expression: list[str]):
        size = self.l * self.m
        M = np.zeros((size, size), dtype=int)

        for elements in expression:
            p = np.eye(size, dtype=int)
            for elem in elements.split("."):
                if len(elem) == 1:
                    variable, exponent = elem, 1
                else:
                    variable, exponent = elem[0], int(elem[1:])
                p = p @ np.linalg.matrix_power(self.poly_variables[variable], exponent)
            M = (M + p) % 2
        return M


    def create_parity_check_matrices(self):
        # Make A and B matrices
        A = self.construct_matrix_from_expression(self.A_expression)
        B = self.construct_matrix_from_expression(self.B_expression)

        H_x = np.concatenate((A, B), axis=1)
        H_z = np.concatenate((B.T, A.T), axis=1)

        if self.safe_mode:
            vd.validate_A_B_matrices(A, self.A_expression)
            vd.validate_A_B_matrices(B, self.B_expression)
            vd.validate_parity_matrices(H_x, H_z)
            pass

        return H_x, H_z


    def generate_bb_code(self, distance_method = 0):
        H_x, H_z = self.create_parity_check_matrices()

        rank_H_x = linalg_help.binary_rank(H_x)
        rank_H_z = linalg_help.binary_rank(H_z)

        if self.safe_mode:
            vd.validate_ranks(rank_H_x, rank_H_z)

        # code parameters
        num_physical : int = 2 * self.l * self.m
        num_logical : int = num_physical - 2 * rank_H_x

        # no need to calculate distance
        if num_logical == 0 or distance_method == 0:
            return num_physical, num_logical, 0

        distance = self.find_distance(H_x, H_z, num_physical, num_logical, distance_method)

        return num_physical, num_logical, distance


    def make_graph(self):
        Hx, Hz = self.create_parity_check_matrices()
        Graph = TannerGraph(Hx, Hz).set_l_and_m(self.l, self.m)
        Graph.add_nodes_and_edges()
        return Graph



