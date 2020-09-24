import cv2
import numpy as np
from matplotlib import pyplot as plt

def gauss(shape,sigma):
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp(-(x * x +y*y) / (2. * sigma * sigma))
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh

    return h

def fft(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    return fshift

def calculateF(shift):
    m = 10*np.log(np.abs(shift)+0.000001)
    return m

def RGBfft(img):
    imB = img[:, :, 0]
    imG = img[:, :, 1]
    imR = img[:, :, 2]
    f1 = fft(imB)
    f2 = fft(imG)
    f3 = fft(imR)
    return f1,f2,f3

def RGBfft2(f1,f2,f3,shape):
    res = np.zeros(shape)
    ifshift1 = np.fft.ifftshift(f1)
    ifshift2 = np.fft.ifftshift(f2)
    ifshift3 = np.fft.ifftshift(f3)
    res[:, :, 0] = np.real(np.fft.ifft2(ifshift1))
    res[:, :, 1] = np.real(np.fft.ifft2(ifshift2))
    res[:, :, 2] = np.real(np.fft.ifft2(ifshift3))
    return res

#finds where two points match
def findMatch(m1,m2):
   z=np.ones(m1.shape)*255
   resized = cv2.resize(m2, (m1.shape[1], int(m2.shape[0]*m1.shape[1]/m2.shape[1])), interpolation=cv2.INTER_AREA)
   z[0:m1.shape[0]][1:m1.shape[0]]=resized[5:m1.shape[0]+5][0:m1.shape[0]-1]
   return z

im2 = cv2.imread('Q4_01_near.jpg')
im1 = cv2.imread('Q4_02_far.jpg')


im2=findMatch(im1,im2)
cv2.imwrite('Q4_03_near.jpg',im2)
cv2.imwrite('Q4_04_far.jpg',im1)

f11,f12,f13 = RGBfft(im1)
new_f1 = (f11+f12+f13)/3
m1=calculateF(new_f1)
cv2.imwrite('Q4_05_dft_near.jpg',m1)

f21,f22,f23 = RGBfft(im2)
new_f2 = (f21+f22+f23)/3
m2=calculateF(new_f2)
cv2.imwrite('Q4_06_dft_far.jpg',m2)

g1=gauss((280,280),15)
g11=gauss((280,280),15)

g3=g11-np.min(g11)
g3=g3*(255/(np.max(g3)-np.min(g3)))
cv2.imwrite('Q4_08_lowpass_15.jpg',g3)
filter1= np.zeros(m1.shape)
filter1[g1>0.00001]=g11[g1>0.00001]
g3=filter1-np.min(filter1)
g3=g3*(255/(np.max(g3)-np.min(g3)))
cv2.imwrite('Q4_10_lowpass_cutoff.jpg',g3)

nf11 = f11*filter1
nf12 = f12*filter1
nf13 = f13*filter1

cv2.imwrite('Q4_12_lowpass.jpg',calculateF((nf11+nf12+nf13))/3)

res1=RGBfft2(nf11,nf12,nf13,(280,280,3))
res1=res1-np.min(res1)
res1=res1*(255/(np.max(res1)-np.min(res1)))

a=gauss((280,280),10)
g2=np.ones((280,280))-a
g3=g2-np.min(g2)
g3=g3*(255/(np.max(g3)-np.min(g3)))
cv2.imwrite('Q4_07_highpass_10.jpg',g3)
filter2= np.zeros(m1.shape)
filter2[g1<0.0005]=g2[g1<0.0005]
g3=filter2-np.min(filter2)
g3=g3*(255/(np.max(g3)-np.min(g3)))
cv2.imwrite('Q4_9_highpass_cutoff.jpg',g3)

nf21 = f21*filter2
nf22 = f22*filter2
nf23 = f23*filter2

cv2.imwrite('Q4_11_highpass.jpg',calculateF((nf21+nf22+nf23))/3)

a=2750
b=1
lf1=(a*nf11+b*nf21)/(a+b)
lf2=(a*nf12+b*nf22)/(a+b)
lf3=(a*nf13+b*nf23)/(a+b)

cv2.imwrite('Q4_13_hybrid_frequency.jpg',calculateF((lf1+lf2+lf3))/3)
res=RGBfft2(lf1,lf2,lf3,(280,280,3))
res=res-np.min(res)
res=res*(255/np.max(res))
resized = cv2.resize(res, (int(res.shape[1] * 1.7),int(res.shape[0] * 1.7)), interpolation=cv2.INTER_AREA)
cv2.imwrite('Q4_13_hybrid_near.jpg',resized)

resized = cv2.resize(res, (int(res.shape[1] * 0.3),int(res.shape[0] * 0.3)), interpolation=cv2.INTER_AREA)
cv2.imwrite('Q4_13_hybrid_far.jpg',resized)