
import numpy as np
import cv2
from scipy.spatial import Delaunay
import imageio


I = cv2.imread('im21.jpg')
J = cv2.imread('im22.jpg')


point1 = [[161, 195], [307, 174], [219, 277], [267, 274], [254, 369], [220, 374], [295, 368], [261, 414], [210, 436], [270, 450], [323, 414], [152, 371], [365, 338], [340, 289], [281, 299], [213, 307], [145, 310], [127, 286], [365, 260], [150, 454], [269, 511], [377, 438], [391, 370], [128, 400], [76, 354], [67, 302], [426, 326], [425, 264], [30, 408], [135, 544], [387, 516], [473, 408], [443, 295], [433, 171], [350, 78], [310, 110], [244, 32], [121, 81], [61, 164], [122, 164], [114, 234], [101, 322], [97, 266], [59, 230], [349, 194], [397, 286], [375, 215], [234, 191], [180, 69], [182, 488], [347, 478], [297, 35], [149, 53], [212, 504], [339, 475]]
point2 = [[206, 203], [357, 193], [257, 294], [307, 294], [287, 396], [243, 398], [319, 390], [284, 441], [227, 456], [287, 476], [338, 447], [170, 373], [389, 365], [375, 313], [315, 315], [244, 319], [173, 315], [153, 286], [399, 289], [147, 457], [287, 542], [384, 469], [404, 402], [126, 396], [71, 346], [70, 286], [435, 354], [443, 288], [9, 387], [112, 542], [379, 528], [482, 437], [458, 314], [464, 191], [400, 90], [367, 126], [293, 30], [139, 67], [72, 160], [156, 162], [137, 242], [113, 312], [115, 259], [63, 219], [401, 216], [422, 302], [412, 241], [282, 206], [227, 69], [184, 502], [356, 504], [351, 42], [184, 38], [219, 526], [350, 506]]



#####   Choosing points  #####

im1_tmp = I.copy()
im2_tmp = J.copy()

cv2.namedWindow('Image 1')
cv2.namedWindow('Image 2')

def mouse_drawing(event, x, y, flags, params):
    global point1,im1_tmp
    if event == cv2.EVENT_LBUTTONDOWN:
        point1.append([x, y])
        cv2.circle(im1_tmp, (x, y), 4, (255, 255, 255), -1)

def mouse_drawing1(event, x, y, flags, params):
    global point2,im2_tmp
    if event == cv2.EVENT_LBUTTONDOWN:
        point2.append([x, y])
        cv2.circle(im2_tmp, (x, y), 4, (255, 255, 255), -1)


cv2.setMouseCallback('Image 1', mouse_drawing)
cv2.setMouseCallback('Image 2', mouse_drawing1)

while (True):
    cv2.imshow('Image 1', im1_tmp)
    cv2.imshow('Image 2', im2_tmp)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('r'):
        point1=[]
        point2=[]
    if k == 27:
        break

cv2.destroyAllWindows()

##########################################


J= cv2.cvtColor(J,cv2.COLOR_BGR2RGB)
I= cv2.cvtColor(I,cv2.COLOR_BGR2RGB)

u=np.array(point1)
v=np.array(point2)

tri = Delaunay(u)

def warp(img1, img2, tri1, tri2):

    warpMat = cv2.getAffineTransform(np.float32(tri1),np.float32(tri2))
    tmp = cv2.warpAffine(img1, warpMat,None)
    mask = np.zeros_like(img2)
    cv2.fillConvexPoly(mask, points=np.int32(tri2),color=(1, 1, 1))
    img2 = img2*(1-mask)+tmp*mask

    return img2

m=10
C=[]
w = np.zeros_like(u)
triIn = np.float32([[[360, 200], [60, 250], [450, 400]]])

for k in range(m):
    C_k1 = I.copy()
    C_k2 = J.copy()
    w = np.int32((k/m)*v + ((m-k)/m)*u)
    for i in range(len(tri.simplices)):
        tri1=([u[tri.simplices[i,0]],u[tri.simplices[i,1]],u[tri.simplices[i,2]]])
        tri2=([v[tri.simplices[i,0]],v[tri.simplices[i,1]],v[tri.simplices[i,2]]])
        triOut=([w[tri.simplices[i,0]],w[tri.simplices[i,1]],w[tri.simplices[i,2]]])
        C_k1=warp(I,C_k1 , tri1, triOut)
        C_k2=warp(J,C_k2 , tri2, triOut)
    C.append(np.int32((k/m)*C_k2 + ((m-k)/m)*C_k1))


for i in range(m):
    C.append(C[m-i-1])

kargs = {}
imageio.mimsave('im2.gif', C, **kargs)


