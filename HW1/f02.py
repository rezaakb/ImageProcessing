import numpy as np
import cv2

m = cv2.imread('IMG_2919.JPG')

#histogram nahayi
s = (1.5) * np.ones(256) * int((m.shape[1] * m.shape[0] * m.shape[2]) / 256)
p = np.zeros(256)

#tashkil tabe tajamoei
for i in range(256):
    if (i == 0):
        p[i] = s[i]
    else:
        p[i] = s[i] + p[i - 1]

#histogram avvalie
tmp, counts = np.unique(m, return_counts=True)
cum = np.zeros(256)

#tashkil histogram nahayi
j: int = 0
tmp = 0
for i in range(256):
    tmp = counts[0:j + 1].sum()
    if (tmp <= p[i]):
        cum[j] = i
        if (j == 0):
            p[i] = tmp
        else:
            p[i] = tmp - counts[0:j].sum()
        j = j + 1
    else:
        p[i] = 0

j = 0

#tashkil aks jadid
nm = np.copy(m)
for i in range(256):
    if (cum[i] == 0 or cum[i]> 240):
        break
    nm[m == i] = cum[i]

cv2.imwrite('im02.jpg', nm)

