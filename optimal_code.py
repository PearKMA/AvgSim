import gc
import numpy as np
import pandas as pd

def avg_sim(listAB, listEF, listCoordinate, listCoordinate2):
    rwBF = 0      # RW(B -> F)
    for paper1 in listAB:
        # get list paper 2 (C)
        listBC = [item[1] for item in listCoordinate if item[0] == paper1]
        rwCF = 0       # RW(C -> F)
        if listBC:
            for paper2 in listBC:
                # get list paper 3 (D)
                listCD = [item[1] for item in listCoordinate2 if item[0] == paper2]
                if listCD:
                    rwDEF = 0
                    for paper3 in listCD:
                        # get list paper 4 (E)
                        listDE = [item[1] for item in listCoordinate if item[0] == paper3]
                        if listDE:
                            rwDEF += len(set(listDE) & set(listEF)) / len(listDE)
                    rwCF += rwDEF / len(listCD)
            rwBF += rwCF / len(listBC)
    return rwBF / len(listAB)


def cal_metapath(matrix_a, matrix_b, matrix_c):
    # get list tuple (author,paper) -- (author write paper)
    arr = np.where(matrix_a == 1)
    listOfCoordinates = list(zip(arr[0], arr[1]))
    # get list tupe (paper1,paper2) -- (paper 1, 2 same author)
    arr2 = np.where(matrix_b == 1)
    listOfCoordinates2 = list(zip(arr2[0], arr2[1]))
    # get list tupe (paper1,paper2) -- (paper 1, 2 same subject)
    arr3 = np.where(matrix_c == 1)
    listOfCoordinates3 = list(zip(arr3[0], arr3[1]))

    matrix_m = []          # matrix m
    authors = np.size(matrix_a, 0)
    for author_i in range(authors):
        row = []        # row in matrix m
        for author_j in range(authors):
            if author_i == author_j:
                row.append(1)
            else:
                # get list paper 1 (B)
                listAB = [item[1] for item in listOfCoordinates if item[0] == author_i]
                # get list paper 4 (E)
                listFE = [item[1] for item in listOfCoordinates if item[0] == author_j]
                if not listAB:
                    row.append(0)
                else:
                    rw = avg_sim(listAB, listFE, listOfCoordinates2, listOfCoordinates3)
                    rw_reverse = avg_sim(listFE, listAB, listOfCoordinates2, listOfCoordinates3)
                    row.append(1 / 2 * (rw + rw_reverse))
        matrix_m.append(row)
    return np.array(matrix_m)

df = pd.read_csv("vector_a.csv", sep=',', header=None)
vector_a = df.values
vector_a = np.delete(vector_a, (0), axis=0)

dfb = pd.read_csv("vector_b.csv", sep=',', header=None)
vector_b = dfb.values
vector_b = np.delete(vector_b, (0), axis=0)

dfp = pd.read_csv("vector_p.csv", sep=',', header=None)
vector_p = dfp.values
vector_p = np.delete(vector_p, (0), axis=0)

dfi = pd.read_csv("vector_i.csv", sep=',', header=None)
vector_i = dfi.values
vector_i = np.delete(vector_i, (0), axis=0)

cal_metapath(vector_a, vector_b, vector_p, "vector_m.csv")
print("done")
