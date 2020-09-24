import cv2
import numpy as np
import math
img = cv2.imread('Books.jpg')
rows,cols,r = img.shape

#mohasebe ab'ad tasvire jadid ke arz an 200px ast
def calculateSize(x1):
    f1 = math.sqrt((x1[0][0] - x1[1][0]) ** 2 + (x1[0][1] - x1[1][1]) ** 2)
    f2 = math.sqrt((x1[0][0] - x1[2][0]) ** 2 + (x1[0][1] - x1[2][1]) ** 2)
    s = int((f2 / f1) * 200)
    return s

#rotate tasivir va noghate motanazer ba tasvir
def rotate(x1,ims):
    t1 = -1 * (np.arctan2(x1[1][1] - x1[0][1], x1[1][0] - x1[0][0]))
    t2 = -1 * (np.arctan2(x1[3][1] - x1[2][1], x1[3][0] - x1[2][0]))
    t = (t1 + t2) / 2
    rot = np.array([[np.cos(t), -1 * np.sin(t)], [np.sin(t), np.cos(t)]])
    x1n = []
    for i in range(len(x1)):
        x1n.append([])
        tmp = np.dot(rot, np.transpose(x1[i]))
        x1n[i].append(int(tmp[0]+ims[0]))
        x1n[i].append(int(tmp[1]+ims[1]))

    M = np.array([[np.cos(t), -1 * np.sin(t),ims[0]], [np.sin(t), np.cos(t), ims[1]]])
    dst = cv2.warpAffine(img, M, (cols, rows))
    return x1n,dst

#peyda kardane negasht az noghat avalie be noghate nahayi
def perspective(x1n,dst,s):
    h, status = cv2.findHomography(np.array(x1n), np.array([[200, s], [0, s], [200, 0], [0, 0]]))
    im_dst = cv2.warpPerspective(dst, h, (200, s))
    return im_dst

def findBooks(x1):
    x1n,im=rotate(x1,(300,-300))
    res=perspective(x1n,im,calculateSize(x1))
    return res

cv2.imwrite('Q3_book1.jpg',findBooks([[207, 429], [404, 467], [155, 707], [357, 739]]))
cv2.imwrite('Q3_book2.jpg',findBooks([[422,796],[622,670],[610,1099],[810,967]]))
cv2.imwrite('Q3_book3.jpg',findBooks([[320,287],[384,106],[600,391],[662,210]]))

