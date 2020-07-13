import gc
import numpy as np


def avg_sim(listAB, listCD, listCoordinate):
    listLen = []   
    listLen.append(len(set(listAB)))

    listBC = [item[1] for item in listCoordinate if item[0] in listAB]
    listLen.append(len(set(listBC)))

    if not listLen or max(listLen) == 0 :
        return 0
    else:
        return len(set(listBC) & set(listCD)) / max(listLen)

def cal_metapath(matrix_a, matrix_b):
    # get list tuple (app,api) 
    arr = np.where(matrix_a == 1)
    listOfCoordinates = list(zip(arr[0], arr[1]))
    # get list tupe (api,api) 
    arr2 = np.where(matrix_b == 1)
    listOfCoordinates2 = list(zip(arr2[0], arr2[1]))

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
                    rw = avg_sim(listAB, listFE, listOfCoordinates2)
                    rw_reverse = avg_sim(listFE, listAB, listOfCoordinates2)
                    row.append(1 / 2 * (rw + rw_reverse))
        matrix_m.append(row)
    return np.array(matrix_m)

a = np.array([
  [1,0,0,0,1,0,0],
  [1,1,0,0,0,0,1]
])
b = np.array([
  [1,1,0,0,0,0,0],
  [1,1,0,0,0,0,0],
  [0,0,1,0,0,0,0],
  [0,0,0,1,0,0,0],
  [0,0,0,0,1,0,1],
  [0,0,0,0,0,1,0],
  [0,0,0,0,1,0,1]
])



m = cal_metapath(a,b)
print(m)
