import numpy as np
from .helpers import linalg_helpers as linalg_help
from .helpers import group_helpers as group_help
from .misc import validators as vd
from .distances import distance_from_brute_force as brute_force
from .distances import distance_from_generators as generators
from .distances import distance_from_gap as qdistrand
from .distances import distance_from_bposd as bposd


class GeneralGroupAlgebraCodes:
    def __init__(self, generators: list[str] = None, relators: list[str] = None, safe_mode: bool = False):
        if relators is not None:
            self.generators = generators or ["x", "y"]
            self.group = group_help.make_base_group(self.generators, relators)

        self.A_expression: list[str] = []
        self.B_expression: list[str] = []
        self.safe_mode = safe_mode

    def validate_relators(self, generators: list[str], relators: list[str]):
        extended_generators = generators + ["i"]
        for relator in relators:
            if all([r not in extended_generators for r in relator]):
                raise ValueError("Relator must contain at least one generator")
        return self

    def set_expression(self, A_expression: list[str], B_expression: list[str]):
        self.A_expression = A_expression
        self.B_expression = B_expression
        return self

    def set_symmetric_base_group(self, order, product_of_groups: bool = False):
        self.group = group_help.make_symmetric_group(order, product_of_groups)
        return self

    def find_distance(self, H_x, H_z, n, k, distance_method):
        if distance_method == 1:
            return brute_force.calculate_distance(H_x, H_z, n, k, status_updates=self.safe_mode)
        if distance_method == 2:
            return generators.calculate_distance(H_x, H_z, n, k, status_updates=self.safe_mode)
        if distance_method == 3:
            return qdistrand.calculate_distance(H_x, H_z, status_updates=self.safe_mode)
        if distance_method == 4:
            return bposd.calculate_distance(H_x, H_z, status_updates=self.safe_mode)


    def make_A_B_matrices(self):
        if self.group is None:
            raise ValueError("Group must be set before generating matrices")
        if not self.A_expression or not self.B_expression:
            raise ValueError("Expressions must be set before generating matrices")

        group_generators = self.group.gens()

        poly_variables = {}
        poly_variables["i"] = self.group([])
        for i, gen in enumerate(self.generators):
            poly_variables[gen] = group_generators[i]

        A_algebra_elements = group_help.make_elements_from_expressions(self.A_expression, poly_variables)
        B_algebra_elements = group_help.make_elements_from_expressions(self.B_expression, poly_variables)

        A_matrix = group_help.make_block_matrix(self.group, A_algebra_elements, action_is_right=False)
        B_matrix = group_help.make_block_matrix(self.group, B_algebra_elements, action_is_right=True)
        return A_matrix, B_matrix


    def create_parity_check_matrices(self):
        A, B = self.make_A_B_matrices()
        H_x = np.concatenate((A, B), axis=1)
        H_z = np.concatenate((B.T, A.T), axis=1)

        if self.safe_mode:
            vd.validate_parity_matrices(H_x, H_z)

        return H_x, H_z


    def generate_bb_code(self, distance_method = 0):
        H_x, H_z = self.create_parity_check_matrices()

        rank_H_x = linalg_help.binary_rank(H_x)
        rank_H_z = linalg_help.binary_rank(H_z)

        # code parameters
        num_physical = 2 * len(H_x)
        num_logical = num_physical - rank_H_x - rank_H_z

        # no need to calculate distance
        if num_logical == 0 or distance_method == 0:
            return num_physical, num_logical, 0

        distance = self.find_distance(H_x, H_z, num_physical, num_logical, distance_method)
        return num_physical, num_logical, distance



