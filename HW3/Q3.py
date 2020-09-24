
import numpy as np
import cv2


img = cv2.imread('im054.jpg')
img1 = cv2.imread('im054.jpg')
newmask = np.ones(img1.shape) * 100

mask = np.zeros(img.shape[:2], np.uint8)

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

cv2.namedWindow('drawing')
cv2.namedWindow('resault')

mode = 0
drawing = False
point1 = ()
point2 = ()


def mouse_drawing(event, x, y, flags, params):
    global point1, point2, drawing, img1, mode
    if event == cv2.EVENT_LBUTTONDOWN:
        if drawing == False:
            drawing = True
            point1 = (x, y)
        else:
            drawing = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True and mode == 0:
            img2 = img1.copy()
            cv2.rectangle(img2, point1, (x, y), (0, 255, 0), 2)
            cv2.imshow('drawing', img2)
        if drawing == True and mode == 1:
            cv2.circle(img1, (x, y), 4, (0, 0, 0), -1)
            cv2.circle(newmask, (x, y), 4, (0, 0, 0), -1)
        if drawing == True and mode == 2:
            cv2.circle(img1, (x, y), 4, (255, 255, 255), -1)
            cv2.circle(newmask, (x, y), 4, (255, 255, 255), -1)
    elif event == cv2.EVENT_LBUTTONUP:
        point2 = (x, y)
        drawing = False
        if mode == 0:
            cv2.rectangle(img1, point1, point2, (0, 255, 0), 2)


cv2.setMouseCallback('drawing', mouse_drawing)
cv2.setMouseCallback('resault', mouse_drawing)

while (True):
    cv2.imshow('drawing', img1)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('b'):
        mode = 1
    elif k == ord('r'):
        print('waiting...')
        rect = (min(point1[0], point2[0]), min(point1[1], point2[1]),
                abs(point2[0] - point1[0]), abs(point2[1] - point1[1]))
        mask, bgdModel, fgdModel = cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 10, cv2.GC_INIT_WITH_RECT)

        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img = img * mask2[:, :, np.newaxis]
        cv2.imwrite('im07.jpg', img)
        cv2.imshow('resault', img)
        print('done!')
    elif k == ord('e'):
        print('waiting...')
        newmask = newmask[:, :, 0]
        mask[newmask == 0] = 0
        mask[newmask == 255] = 1

        mask, bgdModel, fgdModel = cv2.grabCut(img, mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)

        mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img = img * mask[:, :, np.newaxis]
        cv2.imwrite('im07.jpg', img)
        cv2.imshow('resault', img)
        newmask = np.ones(img1.shape) * 100
        print('done!')
    elif k == ord('f'):
        mode = 2
    elif k == 27:
        break

cv2.destroyAllWindows()




img = cv2.imread('im053.jpg')
img1 = cv2.imread('im053.jpg')
newmask = np.ones(img1.shape) * 100

mask = np.zeros(img.shape[:2], np.uint8)

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

cv2.namedWindow('drawing')
cv2.namedWindow('resault')
cv2.resizeWindow('drawing', img1.shape[0] // 3, img1.shape[1] // 3)
cv2.resizeWindow('resault', img1.shape[0] // 3, img1.shape[1] // 3)

mode = 0
drawing = False
point1 = ()
point2 = ()


def mouse_drawing(event, x, y, flags, params):
    global point1, point2, drawing, img1, mode
    if event == cv2.EVENT_LBUTTONDOWN:
        if drawing == False:
            drawing = True
            point1 = (x, y)
        else:
            drawing = False
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True and mode == 0:
            img2 = img1.copy()
            cv2.rectangle(img2, point1, (x, y), (0, 255, 0), 2)
            cv2.imshow('drawing', img2)
        if drawing == True and mode == 1:
            cv2.circle(img1, (x, y), 4, (0, 0, 0), -1)
            cv2.circle(newmask, (x, y), 4, (0, 0, 0), -1)
        if drawing == True and mode == 2:
            cv2.circle(img1, (x, y), 4, (255, 255, 255), -1)
            cv2.circle(newmask, (x, y), 4, (255, 255, 255), -1)
    elif event == cv2.EVENT_LBUTTONUP:
        point2 = (x, y)
        drawing = False
        if mode == 0:
            cv2.rectangle(img1, point1, point2, (0, 255, 0), 2)


cv2.setMouseCallback('drawing', mouse_drawing)
cv2.setMouseCallback('resault', mouse_drawing)

while (True):
    cv2.imshow('drawing', img1)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('b'):
        mode = 1
    elif k == ord('r'):
        rect = (min(point1[0], point2[0]), min(point1[1], point2[1]),
                abs(point2[0] - point1[0]), abs(point2[1] - point1[1]))
        mask, bgdModel, fgdModel = cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 10, cv2.GC_INIT_WITH_RECT)

        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img = img * mask2[:, :, np.newaxis]
        cv2.imwrite('im06.jpg', img)
        cv2.imshow('resault', img)
    elif k == ord('e'):
        newmask = newmask[:, :, 0]
        mask[newmask == 0] = 0
        mask[newmask == 255] = 1

        mask, bgdModel, fgdModel = cv2.grabCut(img, mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)

        mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img = img * mask[:, :, np.newaxis]
        cv2.imwrite('im06.jpg', img)
        cv2.imshow('resault', img)
        newmask = np.ones(img1.shape) * 100

    elif k == ord('f'):
        mode = 2
    elif k == 27:
        break

cv2.destroyAllWindows()


