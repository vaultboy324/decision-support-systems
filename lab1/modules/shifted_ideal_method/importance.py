import math

from lab1.data import *


class Importance:
    _decision_support_matrix = []
    _norming_matrix = []
    _entropy = {}
    _variability = {}
    _expert_assessment = {}
    _complex_importance = {}
    _n = 0
    _m = 0

    @staticmethod
    def _init(decision_support_matrix: list):
        Importance._decision_support_matrix = decision_support_matrix
        Importance._create_norming_matrix()
        Importance._create_entropy_list()
        Importance._create_variability()
        Importance._create_expert_assessment()
        Importance._create_complex_importance()

    @staticmethod
    def _create_norming_matrix():
        result = []
        sums = {}
        for field in FIELD_LIST:
            current_sum = 0
            for decision in Importance._decision_support_matrix:
                current_sum += decision[field]
            sums[field] = current_sum

        for decision in Importance._decision_support_matrix:
            current_row = {}
            for field in decision:
                current_row[field] = decision[field] / sums[field]
            result.append(current_row)

        Importance._norming_matrix = result

    @staticmethod
    def _create_entropy_list():
        result = {}

        Importance._n = len(Importance._decision_support_matrix[0])
        Importance._m = len(Importance._decision_support_matrix)
        k = 1 / math.log(Importance._n)

        for field in FIELD_LIST:
            current_entropy = 0
            for row in Importance._norming_matrix:
                current_entropy += row[field] * math.log(row[field])
            current_entropy = -k * current_entropy
            result[field] = current_entropy

        Importance._entropy = result

    @staticmethod
    def _create_variability():
        result = {}
        for field in Importance._entropy:
            result[field] = 1 - Importance._entropy[field]

        Importance._variability = result

    @staticmethod
    def _create_expert_assessment():
        result = {}

        variability_sum = 0
        for field in Importance._variability:
            variability_sum += Importance._variability[field]

        for field in Importance._variability:
            result[field] = Importance._variability[field] / variability_sum

        Importance._expert_assessment = result

    @staticmethod
    def _create_complex_importance():
        result = {}

        importance_sum = 0
        for field in Importance._expert_assessment:
            importance_sum += Importance._expert_assessment[field] * Importance._variability[field]

        for field in Importance._expert_assessment:
            result[field] = Importance._expert_assessment[field] * Importance._variability[field] / importance_sum

        Importance._complex_importance = result

    @staticmethod
    def _get_json():
        return {
            MATRIX: Importance._decision_support_matrix,
            NORMING_MATRIX: Importance._norming_matrix,
            ENTROPY: Importance._entropy,
            VARIABILITY: Importance._variability,
            EXPERT_ASSESSMENT: Importance._expert_assessment,
            COMPLEX_IMPORTANCE: Importance._complex_importance,
            N: Importance._n,
            M: Importance._m
        }

    @staticmethod
    def get_entropy_values(decision_support_matrix: list):
        Importance._init(decision_support_matrix)
        return Importance._get_json()
