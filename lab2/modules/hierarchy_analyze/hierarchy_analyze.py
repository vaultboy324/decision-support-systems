import numpy
from scipy.stats.mstats import gmean

from data import fields


class HierarchyAnalyze:
    _dataset = []
    _dataset_matrix = []
    _prefers_table = {}
    _prefers_matrix = []
    _v = []
    _lambda_max = 0
    _paired_comparisons = []
    _random_index = 1.12
    _levels = []

    @staticmethod
    def _init(dataset, prefers_table):
        HierarchyAnalyze._dataset = dataset
        HierarchyAnalyze._prefers_table = prefers_table

        for criteria in HierarchyAnalyze._prefers_table:
            row = []
            for comparable_criteria in HierarchyAnalyze._prefers_table[criteria]:
                row.append(HierarchyAnalyze._prefers_table[criteria][comparable_criteria])
            HierarchyAnalyze._prefers_matrix.append(row)

        for row in HierarchyAnalyze._dataset:
            new_matrix_row = []
            for criteria in fields.FIELD_LIST:
                new_matrix_row.append(row[criteria])
            HierarchyAnalyze._dataset_matrix.append(new_matrix_row)

    @staticmethod
    def _create_own_vector(matrix):
        return HierarchyAnalyze._iteration_method(matrix)
        # return HierarchyAnalyze._directed_method(matrix)

    @staticmethod
    def __add_parameters(result):
        result[fields.IS] = numpy.abs((result[fields.LAMBDA_MAX] - result[fields.N]) / (result[fields.N] - 1))
        result[fields.OS] = (result[fields.IS] / HierarchyAnalyze._random_index)

    @staticmethod
    def _directed_method(matrix):
        n = len(matrix)
        avgs = []
        for row in matrix:
            avgs.append(gmean(row))

        sum_avgs = numpy.sum(avgs)

        norming_values = numpy.divide(avgs, sum_avgs)

        matrix_transpose = numpy.transpose(matrix)
        columns_sums = []
        for row in matrix_transpose:
            columns_sums.append(numpy.sum(row))

        result = {
            fields.NORMING_VALUES: norming_values,
            fields.LAMBDA_MAX: numpy.dot(norming_values, columns_sums),
            fields.N: n
        }
        HierarchyAnalyze.__add_parameters(result)
        return result

    @staticmethod
    def _iteration_method(matrix):
        eps = 0.01
        e = []
        n = len(matrix)
        for index in range(0, n):
            e.append(1)
        e_transpose = numpy.transpose(e)

        numerator = numpy.dot(matrix, e)

        denominator = numpy.dot(e_transpose, matrix)
        denominator = numpy.dot(denominator, e)

        v1 = list(numpy.divide(numerator, denominator))
        v1 = numpy.divide(v1, 1)

        matrix_power = numpy.dot(matrix, matrix)

        numerator = numpy.dot(matrix_power, e)

        denominator = numpy.dot(e_transpose, matrix_power)
        denominator = numpy.dot(denominator, e)

        v2 = list(numpy.divide(numerator, denominator))
        v2 = numpy.divide(v2, 1)

        current_eps = numpy.subtract(v2, v1)
        current_eps = numpy.abs(current_eps)
        current_eps = numpy.dot(e_transpose, current_eps)

        while current_eps > eps:
            v1 = v2
            matrix_power = numpy.dot(matrix_power, matrix)

            numerator = numpy.dot(matrix_power, e)

            denominator = numpy.dot(e_transpose, matrix_power)
            denominator = numpy.dot(denominator, e)

            v2 = list(numpy.divide(numerator, denominator))
            v2 = numpy.divide(v2, 1)

            current_eps = numpy.subtract(v2, v1)
            current_eps = numpy.abs(current_eps)
            current_eps = numpy.dot(e_transpose, current_eps)

        lambda_max = numpy.dot(e_transpose, matrix)
        lambda_max = numpy.dot(lambda_max, v2)

        result = {
            fields.NORMING_VALUES: v2,
            fields.LAMBDA_MAX: lambda_max,
            fields.N: n
        }
        HierarchyAnalyze.__add_parameters(result)
        return result

    @staticmethod
    def _create_paired_comparisons():
        paired_comparisons = []
        for criteria in fields.FIELD_LIST:
            paired_comparison = {criteria: []}
            for numerator_row in HierarchyAnalyze._dataset:
                comparison_row = []
                for denominator_row in HierarchyAnalyze._dataset:
                    comparison_value = numerator_row[criteria] / denominator_row[criteria]
                    if criteria in fields.MINORITY_FIELDS:
                        comparison_value = 1 / comparison_value
                    comparison_row.append(comparison_value)
                paired_comparison[criteria].append(comparison_row)
            paired_comparison[fields.PARAMETERS] = HierarchyAnalyze._create_own_vector(paired_comparison[criteria])
            paired_comparisons.append(paired_comparison)
        HierarchyAnalyze._paired_comparisons = paired_comparisons

    @staticmethod
    def _create_levels():
        first_level = 1
        second_level = numpy.dot(HierarchyAnalyze._prefers_table[fields.PARAMETERS][fields.NORMING_VALUES], 1)
        third_level = []

        paired_comparisons = HierarchyAnalyze._paired_comparisons

        for index in range(0, len(HierarchyAnalyze._dataset)):
            weight = 0
            for criteria_number in range(0, len(paired_comparisons)):
                z = second_level[criteria_number]
                weight += paired_comparisons[criteria_number][fields.PARAMETERS][fields.NORMING_VALUES][index] * z
            third_level.append(weight)

        HierarchyAnalyze._levels.append(first_level)
        HierarchyAnalyze._levels.append(second_level)
        HierarchyAnalyze._levels.append(third_level)
        print(HierarchyAnalyze._levels)

    @staticmethod
    def get_result(dataset, prefers_table):
        HierarchyAnalyze._init(dataset, prefers_table)
        prefers_table[fields.PARAMETERS] = HierarchyAnalyze._create_own_vector(HierarchyAnalyze._prefers_matrix)
        HierarchyAnalyze._create_paired_comparisons()
        print(prefers_table)
        print(HierarchyAnalyze._paired_comparisons)
        HierarchyAnalyze._create_levels()
