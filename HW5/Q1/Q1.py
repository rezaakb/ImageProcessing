import scipy.sparse
import numpy as np
import cv2
from scipy.sparse.linalg import cg


def findX(s, t, p, m, A):
    n= len(p)
    b = np.zeros(n)

    for i in range(n):
        point = p[i]
        b[i] = 4 * s[point[0], point[1]] - s[point[0] - 1, point[1]] - s[point[0], point[1] - 1] - s[
            point[0] + 1, point[1]] - s[point[0], point[1] + 1]
        if m[point[0] - 1][point[1]] == 0:
            b[i] = b[i] + t[point[0] - 1][point[1]]
        if m[point[0] + 1][point[1]] == 0:
            b[i] = b[i] + t[point[0] + 1][point[1]]
        if m[point[0]][point[1] - 1] == 0:
            b[i] = b[i] + t[point[0]][point[1] - 1]
        if m[point[0]][point[1] + 1] == 0:
            b[i] = b[i] + t[point[0]][point[1] + 1]

    # Solve Ax=b.
    x = cg(A, b)
    x=x[0]
    x[x>255]=255
    x[x<0]=0

    tmp = t.copy()

    for i in range(n):
        point = p[i]
        tmp[point[0], point[1]] = x[i]

    return tmp


def findA(m,p):

    # Number of unknown points
    n = len(p)

    # Define A
    A = scipy.sparse.lil_matrix((n, n))
    A.setdiag(4)
    for i in range(n):
        point = p[i]
        if m[point[0] - 1][point[1]] == 1:
            A[i, p.index((point[0] - 1, point[1]))] = -1

        if m[point[0] + 1][point[1]] == 1:
            A[i, p.index((point[0] + 1, point[1]))] = -1

        if m[point[0]][point[1] - 1] == 1:
            A[i, p.index((point[0], point[1] - 1))] = -1

        if m[point[0]][point[1] + 1] == 1:
            A[i, p.index((point[0], point[1] + 1))] = -1
    return A


def poissionBlending(s, t, m):

    m = cv2.cvtColor(m, cv2.COLOR_BGR2GRAY)
    m[m > 0] = 1

    # List of unknown points
    p = list(zip(*np.where(m == 1)))

    # define A
    A = findA(m,p)

    r = np.zeros_like(t)

    # Define b regards to each channel
    # Find x by solving Ax=b
    r[:, :, 0]=findX(s[:, :, 0], t[:, :, 0], p, m, A)
    r[:, :, 1]=findX(s[:, :, 1], t[:, :, 1], p, m, A)
    r[:, :, 2]=findX(s[:, :, 2], t[:, :, 2], p, m, A)

    return r



t = cv2.imread('1target.jpg')
s = cv2.imread('1source.jpg')
m = cv2.imread('1mask.jpg')

cv2.imwrite('1resault.jpg',poissionBlending(s,t,m))


t = cv2.imread('2target.jpg')
s = cv2.imread('2source.jpg')
m = cv2.imread('2mask.jpg')

cv2.imwrite('2resualt.jpg',poissionBlending(s,t,m))