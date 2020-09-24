import cv2
import sklearn.cluster as cl
import matplotlib.pyplot as plt
import numpy as np
from skimage.filters import gaussian

img = cv2.imread('IMG_2805.JPG')
img = gaussian(img,0.5)
m= img/np.max(img)
m = m.astype('float32')
m = cv2.cvtColor(m, cv2.COLOR_BGR2LUV)

image2 = cv2.resize(m, (int(m.shape[1] * 0.2), int(m.shape[0] * 0.2)),
                   interpolation=cv2.INTER_AREA)
image = image2[:,:,1:2].flatten()
image1 = np.array(image)
image = np.reshape(image1, [-1, 3])
q = image.astype('int16')

bandwidth2 = cl.estimate_bandwidth(image, quantile=0.1, n_samples=1000)
ms = cl.MeanShift(bandwidth2, bin_seeding=True)
ms.fit(image)
labels = ms.labels_
labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print("number of estimated clusters : %d" % n_clusters_)

a = np.max(ms.labels_)
colors = ms.cluster_centers_
tmp = np.reshape(labels, [int(m.shape[0] * 0.2), int(m.shape[1] * 0.2)])
pic = np.zeros((tmp.shape[0], tmp.shape[1], 3))
s=np.zeros((tmp.shape[0], tmp.shape[1], 3))
for i in range(n_clusters_):
    q=tmp==i
    t=np.where(tmp==i)[1]
    pic[q, 0] = colors[i][0]
    pic[q, 1] = colors[i][1]
    pic[q, 2] = colors[i][2]

pic = pic.astype('float32')
res = cv2.cvtColor(pic, cv2.COLOR_LUV2BGR) * 255
res = res.astype('float32')

plt.imshow(res)
cv2.imwrite('im05.jpg', res)
plt.axis('off')
plt.show()
