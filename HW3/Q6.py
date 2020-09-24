
from scipy import signal
import cv2
from skimage.filters import gaussian
import matplotlib.pyplot as plt
from skimage.color import rgb2gray


def gradient(x, i):
    a = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]]) / 4.0
    if i == 0:
        return signal.convolve2d(x, np.transpose(a), boundary='symm', mode='same')
    else:
        return signal.convolve2d(x, a, boundary='symm', mode='same')

img2 = cv2.imread('tasbih.jpg')

img1 = cv2.imread('tasbih.jpg')
img = rgb2gray(img1)

import cv2
import numpy as np
cv2.namedWindow('drawing')

points = []


def mouse_drawing(event, x, y, flags, params):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img2,(x,y),7,(0,255,0),-1)
        points.append([y,x])


cv2.setMouseCallback('drawing', mouse_drawing)
while (True):
    cv2.imshow('drawing', img2)
    k = cv2.waitKey(1) & 0xFF
    if len(points)==4:
        break
    if k == ord('r'):
        break
    elif k == 27:
        break

cv2.destroyAllWindows()
'''
init= np.array([[709, 283], [673, 296], [626 ,294], [587, 272], [559, 226]
                   , [532, 186], [487 ,163], [415, 198], [371, 210],
                [301 ,226], [262, 241], [223 ,265], [200, 315], [200, 384],
                [251, 415], [265, 447], [287, 508], [287, 559], [318, 595], [384, 617], [433, 600], [444, 565], [453, 528], [495, 536], [537, 516],
                [578, 496], [618, 476], [643 ,434], [677, 415], [725, 413], [813, 396], [862, 399], [912, 393], [955, 386],
                [974 ,357], [965, 311], [917,286], [877,281], [837,280], [778,286]])

'''
y1=min(points[0][0],points[1][0],points[2][0],points[3][0])
y2=max(points[0][0],points[1][0],points[2][0],points[3][0])
x1=min(points[0][1],points[1][1],points[2][1],points[3][1])
x2=max(points[0][1],points[1][1],points[2][1],points[3][1])

img = gaussian(img, 0.2)
gx = gradient(img, 0)
gy = gradient(img, 1)
g= (gx**2+gy**2)*(-1)
plt.imshow(g)
plt.show()
s = np.linspace(0, 2 * np.pi, 100)
c = (y1+y2)//2 + (y2-((y1+y2)//2)) * np.sin(s)
r = (x1+x2)//2 + (x2-((x1+x2)//2))  * np.cos(s)
init = np.array([r, c]).T
init = init.astype(int)
plt.imshow(img)
plt.plot(init[:, 0], init[:, 1], 'o')
plt.axis('off')
plt.show()


def e(p, p1, d, g):
    if (p[1] > len(g) - 1 or p[0] > len(g[0]) - 1):
        e_ext = 10000000
    elif (p[1] < 0 or p[0] < 0):
        e_ext = 10000000
    else:
        e_ext = g[p[1]][p[0]]

    e_int = np.abs((np.sqrt((p1[0] - p[0]) **2 + (p1[1] - p[1]) **2) - d))
    return 1400*e_ext +  0.7*e_int



def one_round(init, a, d, o):

    tmp2=(init[0:len(init)-1,0]-init[1:len(init),0])**2
    tmp1=(init[0:len(init)-1,1]-init[1:len(init),1])**2
    d1=np.sqrt(tmp2+tmp1)
    d=np.sum(d1)/len(d1)
    d=d*o

    b=12

    for q in range(len(init)):
        min1 = 1000000
        i1 = 0
        j1 = 0

        for i in range(-b, b+1):
            for j in range(-b, b+1):
                p = init[q]
                p1 = init[(q + 1) % (len(init))]
                p[0] = p[0] + i
                p[1] = p[1] + j
                total = e(p, p1, d, g)
                if (total < min1):
                    min1 = total
                    i1 = i
                    j1 = j

        init[q][1]=init[q][1]+j1//2
        init[q][0]=init[q][0]+i1//2

    return init,d,o

a=15
j = 1
d=0

t = 0
for i in range(len(init) - 1):
    t = t + np.sqrt((init[i][0] - init[i + 1][0]) ** 2 + (init[i][1] - init[i + 1][1]) ** 2)
t = t + np.sqrt((init[len(init) - 1][0] - init[0][0]) ** 2 + (init[len(init) - 1][1] - init[0][1]) ** 2)
t = t / len(init)
d = t
o = 0.87
counter=0
for i in range(100):
    init3 = init.copy()
    init,d,o = one_round(init,i,d,o)

    tmp = np.abs(init-init3)
    tmp1 = np.sum(tmp)
    #payan alghorithm
    if (tmp1==1200):
        counter=counter+1
    else:
        counter=0
    if (counter==3):
        break
    if (0 == i % 3):
        plt.imshow(img1)
        plt.plot(init[:, 0], init[:, 1], '-r', lw=3)
        plt.plot(init[:, 0], init[:, 1], 'o')
        plt.axis('off')
        j += 1
        plt.title('iter=' + str(i), size=20)
        plt.savefig('iteration/it'+str(i)+'.jpg')
        plt.tight_layout(), plt.show()


