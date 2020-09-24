from random import randint
import cv2
import numpy as np


sm = cv2.imread('sample.jpg')
size_sample = (sm.shape[0],sm.shape[1])
size = (450,650,3)
resualt = np.zeros(size)
batch_size = 100
for y in range(0,size[0]-50,batch_size):
    for x in range(0, size[1]-50, batch_size):
        start_x = randint(0, size_sample[1]-batch_size-1)
        start_y = randint(0, size_sample[0]-batch_size-1)
        resualt[y:y+batch_size,x:x+batch_size,:]=sm[start_y:start_y+batch_size,start_x:start_x+batch_size,:]
cv2.imwrite('im1.jpg',resualt[0:400,0:600,:])