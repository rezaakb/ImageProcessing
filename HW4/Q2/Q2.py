from random import randint

import cv2
import numpy as np

sm1 = cv2.imread('sample.jpg')
sm = cv2.cvtColor(sm1,cv2.COLOR_BGR2GRAY)
size_sample = (sm.shape[0],sm.shape[1])
size = (500,700,3)
resualt = np.zeros((size[0],size[1]))
res = np.zeros(size)
patch_size = 100
overlap = 20
start_x = randint(0, size_sample[1]-patch_size-1)
start_y = randint(0, size_sample[0]-patch_size-1)
resualt[0:patch_size, 0:patch_size] = sm[start_y:start_y + patch_size, start_x:start_x + patch_size]
res[0:patch_size, 0:patch_size, :] = sm1[start_y:start_y + patch_size, start_x:start_x + patch_size, :]

for y in range(0,size[0]-100, patch_size-overlap):
    for x in range(0, size[1]-100, patch_size-overlap):
        if (x==0 and y==0):
            x=x+patch_size-overlap
        start_x=0
        start_y=0
        min_a = 1000000000
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
            tmp = tmp1 + tmp2 + tmp3
            if (tmp < min_a):
                start_y=start_y_tmp
                start_x=start_x_tmp
                min_a = tmp
        if y==0:
            res[y:y+patch_size,x:x+overlap,:]=(res[y:y+patch_size,x:x+overlap,:]+sm1[start_y:start_y+patch_size,start_x:start_x+overlap,:])//2
            resualt[y:y+patch_size,x:x+overlap]=(resualt[y:y+patch_size,x:x+overlap]+sm[start_y:start_y+patch_size,start_x:start_x+overlap])//2
            res[y:y+patch_size,x+overlap:x+patch_size,:]=sm1[start_y:start_y+patch_size,start_x+overlap:start_x+patch_size,:]
            resualt[y:y+patch_size,x+overlap:x+patch_size]=sm[start_y:start_y+patch_size,start_x+overlap:start_x+patch_size]
        elif x==0:
            res[y:y+overlap,x:x+patch_size,:]=(res[y:y+overlap,x:x+patch_size,:]+sm1[start_y:start_y+overlap,start_x:start_x+patch_size,:])//2
            res[y+overlap:y+patch_size,x:x+patch_size,:]=sm1[start_y+overlap:start_y+patch_size,start_x:start_x+patch_size,:]
            resualt[y+overlap:y+patch_size,x:x+patch_size]=sm[start_y+overlap:start_y+patch_size,start_x:start_x+patch_size]
            resualt[y:y+overlap,x:x+patch_size]=(resualt[y:y+overlap,x:x+patch_size]+sm[start_y:start_y+overlap,start_x:start_x+patch_size])//2

        elif x!=0 and y!=0:
            res[y:y+overlap,x:x+patch_size,:]=(res[y:y+overlap,x:x+patch_size,:]+sm1[start_y:start_y+overlap,start_x:start_x+patch_size,:])//2
            resualt[y:y+overlap,x:x+patch_size]=(resualt[y:y+overlap,x:x+patch_size]+sm[start_y:start_y+overlap,start_x:start_x+patch_size])//2
            res[y+overlap:y+patch_size,x:x+overlap,:]=(res[y+overlap:y+patch_size,x:x+overlap,:]+sm1[start_y+overlap:start_y+patch_size,start_x:start_x+overlap,:])//2
            resualt[y+overlap:y+patch_size,x:x+overlap]=(resualt[y+overlap:y+patch_size,x:x+overlap]+sm[start_y+overlap:start_y+patch_size,start_x:start_x+overlap])//2
            resualt[y+overlap:y+patch_size,x+overlap:x+patch_size]=sm[start_y+overlap:start_y+patch_size,start_x+overlap:start_x+patch_size]
            res[y+overlap:y+patch_size,x+overlap:x+patch_size,:]=sm1[start_y+overlap:start_y+patch_size,start_x+overlap:start_x+patch_size,:]


cv2.imwrite('im2.jpg',res[0:400,0:600,:])