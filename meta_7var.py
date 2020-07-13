import gc
import numpy as np


def avg_sim(listAB, listGH, listCoordinate, listCoordinate2,listCoordinate3):
    listLen = []   

    listBC = [item[1] for item in listCoordinate if item[0] in listAB]
    listLen.append(len(set(listBC)))
    
    listCD = [item[1] for item in listCoordinate2 if item[0] in listBC]
    listLen.append(len(set(listCD)))

    listDE = [item[1] for item in listCoordinate3 if item[0] in listCD]
    listLen.append(len(set(listDE)))

    listEF = [item[1] for item in listCoordinate2 if item[0] in listDE]
    listLen.append(len(set(listEF)))

    listFG = [item[1] for item in listCoordinate if item[0] in listEF]
    listLen.append(len(set(listFG)))

    if not listLen or max(listLen) == 0 :
        return 0
    else:
        return len(set(listFG) & set(listGH)) / max(listLen)

def cal_metapath(matrix_a, matrix_b, matrix_c, matrix_d):
    # get list tuple (app,api) 
    arr = np.where(matrix_a == 1)
    listOfCoordinates = list(zip(arr[0], arr[1]))
    # get list tupe (api,api) 
    arr2 = np.where(matrix_b == 1)
    listOfCoordinates2 = list(zip(arr2[0], arr2[1]))
    # get list tupe (api,api)
    arr3 = np.where(matrix_c == 1)
    listOfCoordinates3 = list(zip(arr3[0], arr3[1]))

    arr4 = np.where(matrix_d == 1)
    listOfCoordinates4 = list(zip(arr4[0], arr4[1]))

    matrix_m = []         
    authors = np.size(matrix_a, 0)
    for author_i in range(authors):
        row = []       
        for author_j in range(authors):
            if author_i == author_j:
                row.append(1)
            else:
                listAB = [item[1] for item in listOfCoordinates if item[0] == author_i]
                listGH = [item[1] for item in listOfCoordinates if item[0] == author_j]
                if not listAB:
                    row.append(0)
                else:
                    rw = avg_sim(listAB, listGH, listOfCoordinates2, listOfCoordinates3,listOfCoordinates4)
                    rw_reverse = avg_sim(listGH, listAB, listOfCoordinates2, listOfCoordinates3,listOfCoordinates4)
                    row.append(1 / 2 * (rw + rw_reverse))
        matrix_m.append(row)
    return np.array(matrix_m)

a = np.array([
  [1,0,1,0],
  [1,1,0,1]
])
b = np.array([
  [1,1,0,0],
  [1,1,0,0],
  [0,0,1,0],
  [0,0,0,1]
])

c= np.array([
  [1,0,0,0],
  [0,1,0,0],
  [0,0,1,1],
  [0,0,1,1]
])
d = np.array([
  [1,0,0,0],
  [0,1,1,0],
  [0,1,1,0],
  [0,0,0,1]
])

m = cal_metapath(a,b,c,d)
print(m)
