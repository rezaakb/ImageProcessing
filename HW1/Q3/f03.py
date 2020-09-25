import numpy as np
import cv2
from matplotlib import pyplot as plt

m = cv2.imread('BW.tif')
m = m[:,:,1]
m = cv2.resize(m,(int(m.shape[1]/3),int(m.shape[0]/3)))

#hazf hashie
crop = np.zeros(4,dtype=int)
for i in range(m.shape[1]):
    if (m[100,i]<250):
        crop[0]=i
        break
for i in range(m.shape[1]-1,0,-1):
    if (m[100,i]<250):
        crop[1]=i
        break
for i in range(m.shape[0]):
    if (m[i,100]<250):
        crop[2]=i
        break
for i in range(m.shape[0]-1,0,-1):
    if (m[i,100]<250):
        crop[3]=i
        break

tmp = m[3*crop[2]:crop[3]-crop[2],2*crop[0]:crop[1]-2*crop[0]]

#tashkil 3 channel
m1= tmp[0:int(tmp.shape[0]/3)]
m2= tmp[int(tmp.shape[0]/3):2*int(tmp.shape[0]/3)]
m3= tmp[2*int(tmp.shape[0]/3):3*int(tmp.shape[0]/3)]

#peyda kardan match
def findMatch(m1,m2,a,b,c):
    tmp1 = 10 ** 31
    min = np.zeros(3,dtype= int)
    for i in range(-a, a, 1):
        for j in range(-a, a, 1):
            min[0] = (abs((m1[c:c + b, c:c + b] - m2[c + i:c + i + b, c + j:c + j + b]))).sum()
            if (min[0] < tmp1):
                min[1] = i
                min[2] = j
                tmp1 = min[0]
            min[0] = 0
    return min

# az rooye match channel ro taghire mide
def fitPicture(t,m):
    t[1]=(-1)*t[1]
    t[2]=(-1)*t[2]
    tmp = np.ones([m.shape[0], m.shape[1]])*255
    if t[1]>=0 and t[2]>=0:
        tmp[t[1]:tmp.shape[0],t[2]:tmp.shape[1]] = m[0:m.shape[0]-t[1],0:m.shape[1]-t[2]]
        return tmp
    elif t[1]>=0 and t[2]<0:
        tmp[t[1]:tmp.shape[0], 0:tmp.shape[1]+t[2]] = m[0:m.shape[0]-t[1], (-1)*t[2]:m.shape[1]]
        return tmp
    elif t[1]<0 and t[2]>=0:
        tmp[0:tmp.shape[0]+t[1], t[2]:tmp.shape[1]] = m[(-1)*t[1]:m.shape[0], 0:m.shape[1]-t[2]]
        return tmp
    else:
        tmp[0:tmp.shape[0]+t[1],0:tmp.shape[1]+t[2]] = m[(-1)*t[1]:m.shape[0],(-1)*t[2]:m.shape[1]]
        return tmp

tmp = np.zeros([m1.shape[0],m1.shape[1],3])
tmp[:,:,0]= m1[:,:]

t = findMatch(m1,m3,300,300,300)
tmp[:,:,2] = fitPicture(t,m3)

t = findMatch(m1,m2,300,300,300)
tmp[:,:,1] = fitPicture(t,m2)

#hazf hashie ha az tasvire nahayi
nm = tmp[0:tmp.shape[0]-27,0:tmp.shape[1]-5,:]
cv2.imwrite('im03.jpg',nm)