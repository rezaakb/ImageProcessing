import matplotlib.pyplot as plt
import numpy as np



from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
import cv2

m = cv2.imread('im023.jpg')
img = cv2.resize(m, (int(m.shape[1] * 0.3), int(m.shape[0] * 0.3)), interpolation=cv2.INTER_AREA)




segments_fz = slic(img,sigma=2.3, n_segments=4000,compactness=1.3,convert2lab=True)



img_rgb = img.copy()
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('tem4.jpg',0)
w, h = template.shape[::-1]



res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.9
loc = np.where( res >= threshold)
l=[]
for pt in zip(*loc[::-1]):
    if(pt[1]>400 and pt[1]<800):
        l.append(segments_fz[pt[1] + h//2][pt[0] + w//2])
        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
l.append(segments_fz[652][320])
l.append(segments_fz[577][801])
o=segments_fz[577][945]
l=np.unique(l)
plt.imshow(img_rgb)
plt.show()

plt.imshow(mark_boundaries(img, segments_fz))
plt.show()

im = np.zeros(img.shape)
im = im.astype(np.uint8)
for i in l:
    if(i!=o):
        im[segments_fz==i]=img[segments_fz==i]

cv2.imwrite('im09.jpg',im)

