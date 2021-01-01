import numpy as np

def create_help_matrix(matrix, n):
    new_matrix = np.zeros(matrix.shape)
    height, width = matrix.shape
    for i in range(0, height, n + 1):
        for j in range(0, width, n + 1):
            end_j2 = min(j + n + 1, width)
            for j2 in range(j, end_j2):
                upper = i
                upper_max = matrix[upper, j2]
                new_matrix[upper, j2] = upper_max
                upper += 1
                lower = min(i + n, height - 1)
                lower_max = matrix[lower, j2]
                new_matrix[lower, j2] = lower_max
                lower -= 1

                while upper != n // 2 + i and upper != height:
                    if matrix[upper, j2] > upper_max:
                        upper_max = matrix[upper, j2]
                    else:
                        new_matrix[upper, j2] = upper_max

                    if matrix[lower, j2] > lower_max:
                        lower_max = matrix[lower, j2]
                    else:
                        new_matrix[lower, j2] = lower_max
                    upper += 1
                    if lower == n // 2 + 1:
                        lower -= 1
                if upper == height:
                    upper -= 1
                new_matrix[upper, j2] = max(upper_max, lower_max, matrix[upper, j2])
    return new_matrix


def nms_2d(matrix, size_filter=29, tau=80):
    new_matrix = np.zeros(matrix.shape)
    maxes = []
    height, width = matrix.shape
    n = (size_filter - 1) // 2
    accum_matrix = create_help_matrix(matrix, n)

    for i in range(0, height, n + 1):
        for j in range(0, width, n + 1):
            is_not_max = False
            mi, mj = i, j

            for i2 in range(i, min(i + n + 1, height)):
                for j2 in range(j, min(j + n + 1, width)):
                    if matrix[i2, j2] > matrix[mi, mj]:
                        mi, mj = i2, j2
            i2 = max(mi - n, 0)
            max_i2 = min(mi + n, height - 2) + 1
            while i2 < max_i2:
                j2 = max(mj - n, 0)
                max_j2 = min(mj + n, width - 2) + 1
                while j2 < max_j2:
                    if i2 < i:
                        if i2 < i - n // 2 - 1:
                            if matrix[i2, j2] > matrix[mi, mj]:
                                mi, mj = i2, j2
                                is_not_max = True
                                break
                        elif i2 == i - n // 2 - 1:
                            if matrix[i2, j2] == accum_matrix[i2, j2]:
                                if matrix[i2, j2] > matrix[mi, mj]:
                                    mi, mj = i2, j2
                                    is_not_max = True
                                    break
                        else:
                            if matrix[i2, j2] > matrix[mi, mj]:
                                mi, mj = i2, j2
                                is_not_max = True
                                break
                            if j2 + 1 == max_j2:
                                i2 = i - 1
                    elif i2 > i + n:
                        if i2 == i + n + n // 2 or i2 + 1 == max_i2:
                            if matrix[i2, j2] > matrix[mi, mj]:
                                mi, mj = i2, j2
                                is_not_max = True
                                break
                            if j2 + 1 == max_j2:
                                i2 += 1
                        elif i2 == i + n + n // 2 + 1:
                            if matrix[i2, j2] == accum_matrix[i2, j2]:
                                if matrix[i2, j2] > matrix[mi, mj]:
                                    mi, mj = i2, j2
                                    is_not_max = True
                                    break
                        elif i2 > i + n + n // 2 + 1:
                            if matrix[i2, j2] > matrix[mi, mj]:
                                mi, mj = i2, j2
                                is_not_max = True
                                break
                    elif j2 < j or j2 > j + n:
                        if matrix[i2, j2] > matrix[mi, mj]:
                            mi, mj = i2, j2
                            is_not_max = True
                            break
                        if j2 + 1 == max_j2:
                            i2 = i + n
                    j2 += 1
                if is_not_max:
                    break
                i2 += 1
            if not is_not_max and tau <= matrix[mi, mj]:
                maxes.append((mi, mj, matrix[mi, mj]))
    for t in maxes:
        i, j, m = t
        new_matrix[i, j] = m
    return new_matrix

if __name__ == '__main__':
    matrix = np.random.rand(10,10)*255
    print(np.round(nms_2d(matrix,3),0))