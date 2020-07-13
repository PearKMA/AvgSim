import gc
import numpy as np
import pandas as pd

def avg_sim(listAB, listEF, listCoordinate, listCoordinate2):
    rwBF = 0    
    for i in listAB:
        listBC = [item[1] for item in listCoordinate if item[0] == i]
        rwCF = 0    
        if listBC:
            for j in listBC:
                listCD = [item[1] for item in listCoordinate2 if item[0] == j]
                if listCD:
                    rwDEF = 0
                    for k in listCD:
                        listDE = [item[1] for item in listCoordinate if item[0] == k]
                        if listDE:
                            rwDEF += len(set(listDE) & set(listEF)) / len(listDE)
                    rwCF += rwDEF / len(listCD)
            rwBF += rwCF / len(listBC)
    return rwBF / len(listAB)


def cal_metapath(matrix_a, matrix_b, matrix_c):
    # get list tuple (app,api) 
    arr = np.where(matrix_a == 1)
    listOfCoordinates = list(zip(arr[0], arr[1]))
    # get list tupe (api,api) 
    arr2 = np.where(matrix_b == 1)
    listOfCoordinates2 = list(zip(arr2[0], arr2[1]))
    # get list tupe (api,api)
    arr3 = np.where(matrix_c == 1)
    listOfCoordinates3 = list(zip(arr3[0], arr3[1]))

    matrix_m = []         
    authors = np.size(matrix_a, 0)
    for author_i in range(authors):
        row = []       
        for author_j in range(authors):
            if author_i == author_j:
                row.append(1)
            else:
                listAB = [item[1] for item in listOfCoordinates if item[0] == author_i]
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


m = cal_metapath(vector_a, vector_b, vector_p)

