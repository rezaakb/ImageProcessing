import numpy as np
import cv2
import math

from matplotlib import pyplot as plt

m = cv2.imread('Books.jpg')
im = m[:,:,0]

from scipy import signal

#tashkil gauss
def gauss(shape,sigma):
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp(-(x * x +y*y) / (2. * sigma * sigma))
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

#moshtaghe ofoghi ya amoodi migirad



z,x,y=makeFilter(11,1.3)

x_prime=gradient(x,0)
y_prime=gradient(y,1)


ver_row=np.absolute(signal.convolve2d(im,x_prime,boundary='symm', mode='same'))
cv2.imwrite('Q1-02-ver-row.jpg',ver_row)
hor_row=np.absolute(signal.convolve2d(im,x,boundary='symm', mode='same'))
cv2.imwrite('Q1-01-hor-row.jpg',hor_row)
ver_col=np.absolute(signal.convolve2d(ver_row,y,boundary='symm', mode='same'))
cv2.imwrite('Q1-04-ver-col.jpg',ver_col)
hor_col=np.absolute(signal.convolve2d(hor_row,y_prime,boundary='symm', mode='same'))
cv2.imwrite('Q1-03-hor-col.jpg',hor_col)


z_prime_x=gradient(z,0)
z_prime_y=gradient(z,1)

hor=np.absolute(signal.convolve2d(im,z_prime_y,boundary='symm', mode='same'))
cv2.imwrite('Q1-05-hor.jpg',hor)
ver=np.absolute(signal.convolve2d(im,z_prime_x,boundary='symm', mode='same'))
cv2.imwrite('Q1-06-ver.jpg',ver)

c = np.sqrt(np.power(hor,2) + np.power(ver,2))

cv2.imwrite('Q1-07-grad-mag.jpg', c)
d=np.arctan2(hor,ver) * 180 / np.pi
cv2.imwrite('Q1-08-grad-dir.jpg', d)
c[c<=7]=0
c[c>7]=255
cv2.imwrite('Q1-09-edge.jpg', c)