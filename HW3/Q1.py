import numpy as np
import matplotlib.pyplot as plt
import sklearn.cluster as cl

f = open("Points.txt", "rt")

n=int(f.readline())
print(n)
l=np.zeros((n,2))
i=0

for line in f:
    tmp=line.split()
    l[i][0]=float(tmp[0])
    l[i][1]=float(tmp[1])
    i=i+1

plt.plot(l[:,0],l[:,1],'o')
plt.savefig('im01.jpg')
plt.axis('off')
plt.show()

kmeans = cl.KMeans(n_clusters=2,random_state=3).fit(l)
c=kmeans.labels_
plt.plot(l[c==0,0],l[c==0,1],'o',color='b')
plt.plot(l[c==1,0],l[c==1,1],'o',color='r')
plt.savefig('im02.jpg')
plt.axis('off')
plt.show()

colors=['b','c','r','g','y','k', '0.6', '0.3','0.1','#59524c','#5e2d68','3790e3']

bandwidth = cl.estimate_bandwidth(l, quantile=0.15)
print(bandwidth)
ms = cl.MeanShift(bandwidth=bandwidth, bin_seeding=True).fit(l)
c = ms.labels_
print(len(c))
for i in c:
    plt.plot(l[c==i,0],l[c==i,1],'o',color=colors[i%11])
plt.savefig('im03.jpg')
plt.axis('off')
plt.show()

z=np.zeros((n,3))
z[:,0]=l[:,0]
z[:,1]=l[:,1]
z[:,2]=np.sqrt(l[:,0]**2+l[:,1]**2)*10

kmeans = cl.KMeans(n_clusters=2).fit(z)
c=kmeans.labels_

plt.plot(l[c==0,0],l[c==0,1],'o',color='b')
plt.plot(l[c==1,0],l[c==1,1],'o',color='r')
plt.savefig('im04.jpg')
plt.axis('off')
plt.show()
