import cv2
import numpy as np
import math

m = cv2.imread('Q1-09-edge.jpg')
resized = cv2.resize(m, (int(m.shape[1] * 0.05),int(m.shape[0] * 0.05)), interpolation=cv2.INTER_AREA)
resized[resized > 10] = 255
im = resized
img = cv2.imread('Books.jpg')
resized = cv2.resize(img, (int(m.shape[1] * 0.05),int(m.shape[0] * 0.05)), interpolation=cv2.INTER_AREA)
p_len = int(round(math.sqrt(im.shape[0] ** 2 + im.shape[1] ** 2)))
l = []
for i in range(im.shape[0]):
    for j in range(im.shape[1]):
        if (im[i][j] == 255):
            l.append([j, i])

from skimage.feature import peak_local_max

theta = np.arange(-180, 180, 1)

res = np.zeros([30,15,p_len, len(theta)],dtype=int)
for j in l:
    for a in range(10, 40):
        for b in range(10, 25):
            for i in theta:
                t = theta[i] * np.pi / 180.
                sin = np.sin(t)
                cos = np.cos(t)
                d=int(j[0]*cos + sin*j[1])
                res[a-10][b-10][d][i] = res[a-10][b-10][d][i] + 1


def pic(z, q):
    for i in q:
        t = i[3] * np.pi / 180.
        sin = np.sin(t)
        cos = np.cos(t)
        x1=sin*i[2]
        y1=cos*i[2]
        sin = np.sin(-t)
        cos = np.cos(-t)
        rot = np.array([[cos, -1 * sin], [sin, cos]])
        tmp = np.dot(rot, np.transpose([x1, y1]))
        a1 = tmp[0]+i[0]
        b1 = tmp[1]
        a2 = tmp[0]
        b2 = tmp[1]+i[1]
        a3 = tmp[0]+i[0]
        b3 = tmp[1] + i[1]
        arot = np.array([[np.cos(t), -1 * np.sin(t)], [np.sin(t), np.cos(t)]])
        tmp = np.dot(arot, np.transpose([a1, b1]))
        cv2.line(z, (int(x1), int(y1)), (int(tmp[0]), int(tmp[1])), (0, 0, 255), 1)
        tmp = np.dot(arot, np.transpose([a2, b2]))
        cv2.line(z, (int(x1), int(y1)), (int(tmp[0]), int(tmp[1])), (0, 0, 255), 1)
        tmp1 = np.dot(arot, np.transpose([a3, b3]))
        cv2.line(z, (int(tmp1[0]), int(tmp1[1])), (int(tmp[0]), int(tmp[1])), (0, 0, 255), 1)
        tmp = np.dot(arot, np.transpose([a1, b1]))
        cv2.line(z, (int(tmp1[0]), int(tmp1[1])), (int(tmp[0]), int(tmp[1])), (0, 0, 255), 1)
    return z

q = peak_local_max(res, min_distance=7)
cv2.imwrite('Q2.jpg', pic(resized, q))
