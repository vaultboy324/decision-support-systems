# import

from lab1.data import *
from lab1.modules.shifted_ideal_method.importance import Importance


class ShiftedIdeal:
    _p_max = 5
    _decision_support_matrix = []
    _relative_units_matrix = []
    _ideal_object = {}
    _defective_object = {}
    _priority_levels = {}
    _distance_table = {}
    _ranged_distance_table = {}
    _importance = {}
    _worst_alternative = 0

    @staticmethod
    def get_result(decision_support_matrix: list):
        result = {
            REPORT: [],
            BEST_ALTERNATIVE: {}
        }

        ShiftedIdeal._decision_support_matrix = decision_support_matrix
        while len(ShiftedIdeal._decision_support_matrix) > 1:
            result[REPORT].append(ShiftedIdeal._shifted_ideal_method())

        result[BEST_ALTERNATIVE] = ShiftedIdeal._decision_support_matrix[0]
        return result

    @staticmethod
    def _shifted_ideal_method():
        ShiftedIdeal._importance = Importance.get_entropy_values(ShiftedIdeal._decision_support_matrix)
        ShiftedIdeal._create_objects()
        ShiftedIdeal._create_relative_units_matrix()
        ShiftedIdeal._create_priority_levels()
        ShiftedIdeal._create_distance_table()
        ShiftedIdeal._create_ranged_distance_table()
        ShiftedIdeal._create_worst_alternative()
        ShiftedIdeal._delete_worst_alternative()
        return ShiftedIdeal._get_json()

    @staticmethod
    def _create_objects():
        ideal_object = {}
        defective_object = {}

        for field in MAJORITY_FIELDS:
            sequence = (decision[field] for decision in ShiftedIdeal._decision_support_matrix)
            ideal_object[field] = max(sequence)
            sequence = (decision[field] for decision in ShiftedIdeal._decision_support_matrix)
            defective_object[field] = min(sequence)

        for field in MINORITY_FIELDS:
            sequence = (decision[field] for decision in ShiftedIdeal._decision_support_matrix)
            ideal_object[field] = min(sequence)
            sequence = (decision[field] for decision in ShiftedIdeal._decision_support_matrix)
            defective_object[field] = max(sequence)

        ShiftedIdeal._ideal_object = ideal_object
        ShiftedIdeal._defective_object = defective_object

    @staticmethod
    def _create_relative_units_matrix():
        result = []

        for row in ShiftedIdeal._decision_support_matrix:
            current_row = {}
            for field in row:
                try:
                    current_row[field] = ((ShiftedIdeal._ideal_object[field] - row[field]) /
                                          (ShiftedIdeal._ideal_object[field] - ShiftedIdeal._defective_object[field]))
                except ZeroDivisionError:
                    current_row[field] = 0
            result.append(current_row)

        ShiftedIdeal._relative_units_matrix = result

    @staticmethod
    def _create_priority_levels():
        result = {
            PLAYER_DISTANCE: 0.36,
            PROMO_CODE: 0.28,
            SHOP_DISTANCE: 0.16,
            PORTAL_LEVEL: 0.2
        }

        ShiftedIdeal._priority_levels = result

    @staticmethod
    def _create_distance_table():
        result = {}

        for p in range(1, ShiftedIdeal._p_max + 1):
            current_distance_row = []
            index = 0
            for row in ShiftedIdeal._relative_units_matrix:
                distance = 0
                for field in row:
                    distance += (ShiftedIdeal._priority_levels[field] * (1 - row[field])) ** p
                distance **= 1 / p
                alternative = {
                    ALTERNATIVE_NUMBER: index,
                    MITKOVSKIY_DISTANCE: distance
                }
                current_distance_row.append(alternative)
                index += 1
            result[p] = current_distance_row

        ShiftedIdeal._distance_table = result

    @staticmethod
    def _create_ranged_distance_table():
        for p in ShiftedIdeal._distance_table:
            row = sorted(ShiftedIdeal._distance_table[p].copy(), key=lambda i: i[MITKOVSKIY_DISTANCE], reverse=True)

            ShiftedIdeal._ranged_distance_table[p] = row

    @staticmethod
    def _create_worst_alternative():
        m = ShiftedIdeal._importance[M]

        counters = {}

        for i in range(0, m):
            counters[i] = 0

        for p in ShiftedIdeal._ranged_distance_table:
            alternative_number = ShiftedIdeal._ranged_distance_table[p][m - 1][ALTERNATIVE_NUMBER]
            counters[alternative_number] += 1

        worst_alternative = 0

        for alternative_number in range(0, m):
            if counters[alternative_number] > counters[worst_alternative]:
                worst_alternative = alternative_number

        ShiftedIdeal._worst_alternative = worst_alternative

    @staticmethod
    def _delete_worst_alternative():
        ShiftedIdeal._decision_support_matrix.pop(ShiftedIdeal._worst_alternative)

    @staticmethod
    def _get_json():
        return {
            MATRIX: ShiftedIdeal._decision_support_matrix,
            PRIORITY_LEVELS: ShiftedIdeal._priority_levels,
            IDEAL: ShiftedIdeal._ideal_object,
            DEFECTIVE: ShiftedIdeal._defective_object,
            RELATIVE_UNITS: ShiftedIdeal._relative_units_matrix,
            COMPLEX_IMPORTANCE: ShiftedIdeal._importance,
            DISTANCE_TABLE: ShiftedIdeal._distance_table,
            RANGED_DISTANCE_TABLE: ShiftedIdeal._ranged_distance_table,
            WORST_ALTERNATIVE: ShiftedIdeal._worst_alternative
        }

    # @staticmethod
    # def get_json():
