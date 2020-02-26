import itertools

from lab1.data import *
from lab1.modules.shifted_ideal_method.importance import Importance


class Permutations:
    _decision_support_matrix = []
    _permutation_list = []
    _priority_levels = {}
    _importance = {}

    @staticmethod
    def get_result(decision_support_matrix: list):
        Permutations._decision_support_matrix = decision_support_matrix
        Permutations._init()
        return Permutations._get_json()

    @staticmethod
    def _init():
        result = []
        arr = []

        Permutations._importance = Importance.get_entropy_values(Permutations._decision_support_matrix)

        Permutations._create_priority_levels()

        for index in range(0, len(Permutations._decision_support_matrix)):
            arr.append(index)

        for permutation in itertools.permutations(arr, len(arr)):
            row = {
                LIST: permutation,
                ASSESSMENT: 0,
                CRITERIA: Permutations._get_numbers_for_permutation(permutation)
            }
            row[ASSESSMENT] = Permutations._get_assessment(row[CRITERIA])
            result.append(row)

        result = sorted(result, key=lambda x: x[ASSESSMENT], reverse=True)

        Permutations._permutation_list = result

    @staticmethod
    def _create_priority_levels():
        result = {
            PLAYER_DISTANCE: 0.36,
            PROMO_CODE: 0.28,
            SHOP_DISTANCE: 0.16,
            PORTAL_LEVEL: 0.2
        }

        Permutations._priority_levels = result

    @staticmethod
    def _get_numbers_for_permutation(permutation: tuple):
        result = []

        for value1 in permutation:
            for value2 in permutation:
                if value1 == value2:
                    continue

                new_row = {
                    AGREED: [],
                    NOT_AGREED: [],
                    VALUES_SET: {value1, value2}
                }

                already_have = False

                for row in result:
                    if new_row[VALUES_SET] == row[VALUES_SET]:
                        already_have = True
                        break

                if already_have:
                    continue

                for field in MAJORITY_FIELDS:
                    if (Permutations._decision_support_matrix[value1][field] >
                            Permutations._decision_support_matrix[value2][field]):
                        new_row[AGREED].append(field)
                    else:
                        new_row[NOT_AGREED].append(field)

                for field in MINORITY_FIELDS:
                    if (Permutations._decision_support_matrix[value1][field] <
                            Permutations._decision_support_matrix[value2][field]):
                        new_row[AGREED].append(field)
                    else:
                        new_row[NOT_AGREED].append(field)

                result.append(new_row)

        return result

    @staticmethod
    def _get_assessment(criteria: list):
        result = 0
        for criterion in criteria:
            agreed_sum = 0
            not_agreed_sum = 0

            for agreed in criterion[AGREED]:
                agreed_sum += Permutations._priority_levels[agreed]

            for not_agreed in criterion[NOT_AGREED]:
                not_agreed_sum += Permutations._priority_levels[not_agreed]

            result += agreed_sum - not_agreed_sum

        return result

    @staticmethod
    def _get_json():
        for permutation in Permutations._permutation_list:
            for criterion in permutation[CRITERIA]:
                criterion[VALUES_SET] = list(criterion[VALUES_SET])

        return {
            MATRIX: Permutations._decision_support_matrix,
            PRIORITY_LEVELS: Permutations._priority_levels,
            PERMUTATION_LIST: Permutations._permutation_list,
            COMPLEX_IMPORTANCE: Permutations._importance
        }