from random import randint

import cv2
import numpy as np

sm1 = cv2.imread('texture.jpg')
sm = cv2.cvtColor(sm1, cv2.COLOR_BGR2GRAY)

size_sample = (sm.shape[0],sm.shape[1])
resualt1 = cv2.imread('target.jpg')
resualt1 = cv2.cvtColor(resualt1,cv2.COLOR_BGR2GRAY)
resualt = np.zeros((resualt1.shape[0]+100,resualt1.shape[1]+100))
size = resualt.shape
res = np.zeros((size[0],size[1],3))
resualt[0:resualt1.shape[0],0:resualt1.shape[1]]=resualt1[0:resualt1.shape[0],0:resualt1.shape[1]]
patch_size = 20
overlap = 7


def vertical(resualt, sm, point, x,y,overlap,patch_size):
    E_V = np.zeros((patch_size, overlap))
    T_V = np.zeros((patch_size, overlap), dtype=int)
    tmp = np.sqrt((resualt[y+patch_size - 1, x:x + overlap] - sm[point[0] + patch_size - 1,
                                                                   point[1]:point[1] + overlap]) ** 2)
    E_V[patch_size - 1, :] = tmp[:]
    for i in range(patch_size - 2, -1, -1):
        for j in range(0, overlap):
            tmp = np.sqrt((resualt[y+i, x + j] - sm[point[0] + i, point[1] + j])**2)
            if (j == 0):
                E_V[i, j] = tmp + min(E_V[i + 1, j], E_V[i + 1, j + 1])
                tmp = np.argmin([E_V[i + 1, j], E_V[i + 1, j + 1]])
                T_V[i, j] = j + tmp
            elif (j == overlap - 1):
                E_V[i, j] = tmp + min(E_V[i + 1, j], E_V[i + 1, j - 1])
                tmp = np.argmin([E_V[i + 1, j - 1], E_V[i + 1, j]])
                T_V[i, j] = j + tmp - 1
            else:
                E_V[i, j] = tmp + min(E_V[i + 1, j + 1], E_V[i + 1, j], E_V[i + 1, j - 1])
                tmp = np.argmin([E_V[i + 1, j - 1], E_V[i + 1, j], E_V[i + 1, j + 1]])
                T_V[i, j] = j + tmp - 1
    j = np.argmin(E_V[0, :])
    path = np.zeros((patch_size, patch_size))
    path[i, 0] = 1
    x = i
    for i in range(1, patch_size):
        x = T_V[i - 1,x]
        path[i, x] = 1
    path = fill_Path_V(path,0)
    return path,T_V,E_V

def horizental(resualt, sm, point, x,y,overlap,patch_size):
    E_H = np.zeros((overlap,patch_size))
    T_H = np.zeros((overlap,patch_size), dtype=int)
    tmp = np.sqrt((resualt[y + patch_size - 1, x:x + overlap] - sm[point[0] + patch_size - 1,
                                                                point[1]:point[1] + overlap]) ** 2)

    E_H[:,patch_size - 1] = tmp[:]
    for j in range(patch_size - 2, -1, -1):
        for i in range(0, overlap):
            tmp = np.sqrt((resualt[y+i, x + j] - sm[point[0] + i, point[1] + j])**2)
            if (i == 0):
                E_H[i, j] = tmp + min(E_H[i , j+1], E_H[i + 1, j + 1])
                tmp = np.argmin([E_H[i , j+1], E_H[i + 1, j + 1]])
                T_H[i, j] = i + tmp
            elif (i == overlap - 1):
                E_H[i, j] = tmp + min(E_H[i, j+1], E_H[i - 1, j + 1])
                tmp = np.argmin([E_H[i-1, j+1], E_H[i, j + 1]])
                T_H[i, j] = i + tmp - 1
            else:
                E_H[i, j] = tmp + min(E_H[i-1, j + 1], E_H[i, j+1], E_H[i - 1, j + 1])
                tmp = np.argmin([E_H[i-1, j + 1], E_H[i, j+1], E_H[i + 1, j + 1]])
                T_H[i, j] = i + tmp - 1
    i = np.argmin(E_H[:, 0])
    path = np.zeros((patch_size, patch_size))
    path[i, 0] = 1
    t = i
    for i in range(1, patch_size):
        t = T_H[t, i - 1]
        path[t,i] = 1
    path = fill_Path_H(path,0)
    return path,T_H,E_H


def find_I(resualt, sm, E_V, E_H,point,overlap,x,y):
    I_l = 0
    min_l = 1000000000
    for i in range(overlap):

        tmp1 = np.sqrt((resualt[y + i, x + i] - sm[point[0] + i, point[1] + i])**2)
        tmp = E_V[i, i] + E_H[i, i] - tmp1
        if (tmp < min_l):
            min_l = tmp
            i_l = i
    return i_l


def fill_Path_V(path,I_L):
    for i in range(I_L,len(path)):
        for j in range(len(path)):
            if(path[i][j]==1):
                break
            if (path[i][j]==0):
                    path[i][j]=1
    return path

def fill_Path_H(path,I_L):
    for j in range(I_L,len(path)):
        for i in range(len(path)):
            if(path[i][j]==1):
                break
            if (path[i][j]==0):
                    path[i][j]=1
    return path

def fill_Path_L(path,I_L):
    path=fill_Path_H(path,I_L)
    path=fill_Path_V(path,0)
    return path


def make_Path(I_L,T_H, T_V, patch_size,x,y):
    path = np.zeros((patch_size,patch_size))
    path[I_L,I_L] = 1
    x=I_L
    y=I_L
    for i in range(I_L+1, patch_size):
        x = T_V[i-1,x]
        path[i, x] = 1
        y= T_H[y,i-1]
        path[y,i] =1
    path = fill_Path_L(path,I_L)
    return path


def make_resualt(res,resualt, sm, path,x,y,point,patch_size,overlap):
    path_1 = (path +1)%2
    res[y:y+patch_size,x:x+patch_size,0]=sm1[point[0]:point[0]+patch_size,point[1]:point[1]+patch_size,0]*path_1 + res[y:y+patch_size,x:x+patch_size,0]*path
    res[y:y+patch_size,x:x+patch_size,1]=sm1[point[0]:point[0]+patch_size,point[1]:point[1]+patch_size,1]*path_1 + res[y:y+patch_size,x:x+patch_size,1]*path
    res[y:y+patch_size,x:x+patch_size,2]=sm1[point[0]:point[0]+patch_size,point[1]:point[1]+patch_size,2]*path_1 + res[y:y+patch_size,x:x+patch_size,2]*path
    resualt[y:y + patch_size, x:x + patch_size] = sm[point[0]:point[0] + patch_size, point[1]:point[1] + patch_size] * path_1 + resualt[y:y + patch_size, x:x + patch_size] * path

    return resualt,res


for y in range(0,size[0]-patch_size, patch_size-overlap):
    for x in range(0, size[1]-patch_size, patch_size-overlap):
        start_x=0
        start_y=0
        min_SSD = 1000000000
        list=[]
        k=0
        for i in range(500):
            start_x_tmp = randint(0, size_sample[1] - patch_size - 1)
            start_y_tmp = randint(0, size_sample[0] - patch_size - 1)
            tmp1 = 0
            tmp2 = 0
            if (x != 0):
                tmp1 = np.sum(np.abs(resualt[y + overlap:y + patch_size, x:x + overlap] - sm[
                                                                                          start_y_tmp + overlap:start_y_tmp + patch_size,
                                                                                          start_x_tmp:start_x_tmp + overlap]))
            if (y != 0):
                tmp2 = np.sum(np.abs((resualt[y:y + overlap, x + overlap:x + patch_size] - sm[start_y_tmp:start_y_tmp + overlap,
                                                                                 start_x_tmp + overlap:start_x_tmp + patch_size])))
            tmp3 = np.sum(np.abs((resualt[y:y + overlap, x:x + overlap] - sm[start_y_tmp:start_y_tmp + overlap,
                                                                          start_x_tmp:start_x_tmp + overlap])))
            OverlapSSD = tmp1 + tmp2 + tmp3
            TargetSSD = np.sum(np.abs((resualt[y + overlap:y + patch_size, x + overlap:x + patch_size] - sm[
                                                                                                    start_y_tmp + overlap:start_y_tmp + patch_size,
                                                                                                    start_x_tmp + overlap:start_x_tmp + patch_size])))
            a = 0.3
            SSD = (a) * OverlapSSD + (1 - a) * TargetSSD
            if (SSD < min_SSD):
                point = (start_y_tmp, start_x_tmp)
                min_SSD = SSD
                k = k + 1

        if y==0 and x==0:
            res[y:y + patch_size, x:x + patch_size, :] = sm1[point[0]:point[0] + patch_size,
                                                         point[1]:point[1] + patch_size, :]
            resualt[y:y + patch_size, x:x + patch_size] = sm[point[0]:point[0] + patch_size,
                                                          point[1]:point[1] + patch_size]
        if y==0:
            Path_V, T_V, E_V = vertical(resualt, sm, point, x, y, overlap, patch_size)
            resualt,res = make_resualt(res,resualt,sm,Path_V,x,y,point,patch_size,overlap)
        elif x==0:
            Path_H,T_H,E_H = horizental(resualt, sm, point, x, y,overlap,patch_size)
            resualt,res = make_resualt(res,resualt,sm,Path_H,x,y,point,patch_size,overlap)
        elif x!=0 and y!=0:
            Path_H,T_H,E_H = horizental(resualt, sm, point, x, y,overlap,patch_size)
            Path_V, T_V, E_V = vertical(resualt, sm, point, x, y, overlap, patch_size)
            I_L= find_I(resualt,sm,E_V,E_H,point,overlap,x,y)
            Path_L= make_Path(I_L,T_H,T_V,patch_size,x,y)
            resualt,res = make_resualt(res,resualt,sm,Path_L,x,y,point,patch_size,overlap)

cv2.imwrite('im4.jpg',res[0:resualt1.shape[0],0:resualt1.shape[1],:])

