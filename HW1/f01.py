
import numpy as np
import cv2


i = cv2.imread('im030.jpg')

y=0.04
u=(-1)*np.ones(i.shape)

def log(a,b,y):
    u[(a <= i) & (i < b)] = np.floor((b - a) * np.log(1 + y * i[(a <= i) & (i < b)]) / np.log((b - a) * y + 1))
    return

def power(a,b,y):
    u[(a <= i) & (i < b)] = (255)*( i[(a <= i) & (i < b)]/(255))**y
    return

def identity(a,b,y):
    u[(a <= i) & (i < b)] = y*i[(a <= i) & (i < b)]
    return

log(0,128,0.2)
identity(128,256,1)

u=u.astype(np.int16)

cv2.imwrite('im01.jpg',u)
