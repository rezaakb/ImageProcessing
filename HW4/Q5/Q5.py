
import cv2
import numpy as np
import imageio

im11 = cv2.imread('01.png')
im1 = cv2.cvtColor(im11,cv2.COLOR_BGR2GRAY)
im22 = cv2.imread('02.png')
im2 = cv2.cvtColor(im22,cv2.COLOR_BGR2GRAY)
flow = cv2.calcOpticalFlowFarneback(im1,im2, None, 0.5, 3, 20, 10, 7, 1.4, 0)

##  from:
#   https://github.com/npinto/opencv/blob/master/samples/python2/opt_flow.py

h, w = flow.shape[:2]
flow = -flow
flow[:, :, 0] += np.arange(w)
flow[:, :, 1] += np.arange(h)[:, np.newaxis]
res = cv2.remap(im11, flow, None, cv2.INTER_LINEAR)
cv2.imwrite('im5.jpg',res)

##


images = []
images.append(im22)
images.append(res)
kargs = { 'duration': 0.5 }

imageio.mimsave('flow.gif', images,**kargs)






