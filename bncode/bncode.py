import cv2
import numpy as np
import math

All_threshold = cv2.THRESH_OTSU | cv2.THRESH_BINARY
KERNEL_1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
KERNEL_2 = np.ones((3, 3), np.uint8)
############################
# Reference: https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
############################


def order_points(pts):
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped
############################


def resize_INTER_LINEAR(img, size):
    return cv2.resize(img, (size, size), interpolation=cv2.INTER_LINEAR)

def resize_INTER_NEAREST(img, size):
    return cv2.resize(img, (size, size), interpolation=cv2.INTER_NEAREST)


def create(number,image_size=400):
    size = 8
    border = 3
    DATA_SIZE = math.floor(size*size/2)
    # number to binary
    bit = "{0:b}".format(number)
    # reverse bit
    bit = bit[::-1]
    # check size of bit
    if len(bit) > DATA_SIZE:
        # error message
        raise ValueError('Number is too big')
    # add reference bit
    ref = ''
    for i in bit:
        ref += i*2
    # create black image
    img = np.zeros((size+border*2, size+border*2,1), np.uint8)
    # add corners to image
    img[border-1][border-1] = 255
    img[border-1][size+border] = 255
    img[size+border][border-1] = 255
    img[size+border][size+border-1] = 255
    # add white border
    for y in range(size+4):
        for x in range(size+4):
            if y == 0 or y == size+3 or x == 0 or x == size+3:
                img[x+border-2][y+border-2] = 255
    # add data to image
    for y in range(size):
        for x in range(size):
            if x+y*size < len(ref):
                if ref[x+y*size] == '1':
                    img[border+x][border+y] = 255
    return resize_INTER_NEAREST(img,image_size)


def decode(img,debug=False):
    size = 8
    border = 2
    gray_scale = img
    # check if image is gray scale
    if len(img.shape) >= 3:
        gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # resize image
    resized = resize_INTER_LINEAR(gray_scale, size+border*2)
    # check image corners
    isBNcode = False
    if debug :
        cv2.imshow("BNcode.decoder.input", cv2.resize(img, (400, 400),
            interpolation=cv2.INTER_NEAREST))
        cv2.imshow("BNcode.decoder.resized", cv2.resize(resized, (400, 400),
            interpolation=cv2.INTER_NEAREST))
    for i in range(4):
        resized = cv2.rotate(resized, cv2.ROTATE_90_CLOCKWISE)
        point = [
            resized[border-1][border-1], resized[border-1][size+border],
            resized[size+border][border-1], resized[size+border][size+border],
            resized[size+border][size+border-1], resized[size+border-1][size+border]
        ]
        if(point == [255, 255, 255, 0, 255, 0]):
            isBNcode = True
            break
    # check border of image
    m = []
    for i in range(size):
        m.append(resized[border-1][i+border])
        m.append(resized[border+i][border-1])
        m.append(resized[size+border][i+border])
        m.append(resized[border+i][size+border])
    if len(m) == size*4:
        if m == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 0]:
            isBNcode = True
        else:
            isBNcode = False
    else:
        isBNcode = False
    # return None if not a BNcode
    if not isBNcode:
        return None
    bit = ''
    # convert image to binary
    for y in range(size):
        for x in range(size):
            if(resized[x+border][y+border] == 255):
                bit += "1"
            elif(resized[x+border][y+border] == 0):
                bit += "0"
    # compare bit with reference
    data = ''
    for i in range(len(bit)):
        if(i % 2 == 0 and i < len(bit)-1):
            if(bit[i] == bit[i+1]):
                data += bit[i]
            else:
                return
    # binary to number
    return int(data[::-1], 2)

def scan(img,debug=False):
    blur = cv2.GaussianBlur(img, (1, 1), 1000)
    if len(img.shape) >= 3:
        gray_scale = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    else:
        gray_scale = img
    thresh = cv2.threshold(gray_scale, 128, 255, All_threshold)[1]
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, KERNEL_1, iterations=3)
    morph = cv2.bitwise_not(morph)

    canny = cv2.Canny(morph, 50, 150, apertureSize=3)
    cnts, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    decodeds = []
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
            ROI = four_point_transform(gray_scale, approx.reshape(4, 2))
            resized = resize_INTER_LINEAR(ROI, 200)
            median = cv2.medianBlur(resized, 5)
            # remove noise in image
            median = cv2.erode(median, KERNEL_2, iterations=1)
            median = cv2.dilate(median, KERNEL_2, iterations=1)
            # convert to binary image
            thresh = cv2.threshold(median, 128, 255, All_threshold)[1]
            data = decode(thresh,debug)
            if data is not None:
                decodeds.append(data)
            if debug:
                cv2.imshow('BNcode.contours.img', img)
    if debug:
        cv2.imshow('BNcode.canny', canny)
        cv2.imshow('BNcode.morph', morph)
        cv2.imshow('BNcode.input.image', img)
    return decodeds