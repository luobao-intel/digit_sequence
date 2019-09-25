import cv2
import random
import numpy as np
from PIL import Image
import math

class DataAugmentation(object):
    """
    Augment the sampled digit sequence with some tricks, like
    add noise points
    erode or dilate the image
    """
    def __init__(self, rotate_angle=40, angle=15, noise=True, dilate=True, erode=True, warp=True, rotate=True):
        self.rotate_angle = rotate_angle
        self.angle = angle
        self.warp_angle = angle
        self.noise = noise
        self.dilate = dilate
        self.erode = erode
        self.warp = warp
        self.rotate = rotate

    @classmethod
    def add_noise(cls, img):
        for _ in range(10):  # add n noise points
            temp_x = np.random.randint(0, img.shape[0])
            temp_y = np.random.randint(0, img.shape[1])
            img[temp_x][temp_y] = 255
        return img

    @classmethod
    def add_erode(cls, img):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        img = cv2.erode(img, kernel)
        return img

    @classmethod
    def add_dilate(cls, img):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        img = cv2.dilate(img, kernel)
        return img

    @classmethod
    def Warp(cls, image, angle):
        angle = random.uniform(0,angle)
        a = math.tan(angle * math.pi / 180.0)
        H = image.shape[0]
        W = int(image.shape[1] + H * a)
        size = (H, W)
        iWarp = np.zeros(size, np.uint8)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                y = int(j + i * a)
                iWarp[i, y] = image[i, j]
        return iWarp

    @classmethod
    def Rotate(cls, img, rotate_angle):
        img = Image.fromarray(img)
        angle = random.uniform(-rotate_angle, rotate_angle)
        img = img.rotate(angle)
        img = np.asarray(img)
        return img

    def do(self, img_list=[]):
        aug_list = []
        # aug_list = copy.deepcopy(img_list)
        for i in range(len(img_list)):
            im = img_list[i]
            if self.noise and random.random() < 0.5:
                im = self.add_noise(im)
            if self.warp and random.random() < 0.7:
                im = self.Warp(im, self.angle)
            if self.rotate and random.random() < 0.5:
                im = self.Rotate(im, self.rotate_angle)
            if random.random() < 0.5:
                if self.dilate and random.random() < 0.5:
                    im = self.add_dilate(im)
                elif self.erode:
                    im = self.add_erode(im)
            aug_list.append(im)
        return aug_list

class PreprocessResizeKeepRatio(object):
    """
    Scale the image equally
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def do(self, cv2_img):
        max_width = self.width
        max_height = self.height

        cur_height, cur_width = cv2_img.shape[:2]

        ratio_w = float(max_width) / float(cur_width)
        ratio_h = float(max_height) / float(cur_height)
        ratio = min(ratio_w, ratio_h)

        new_size = (min(int(cur_width * ratio), max_width),
                    min(int(cur_height * ratio), max_height))

        new_size = (max(new_size[0], 1),
                    max(new_size[1], 1),)

        resized_img = cv2.resize(cv2_img, new_size)
        return resized_img

class FindImageBBox(object):
    """
    Find the minimum inclusive rectangle of the digits
    Scanning from left to right, the left edge of the digit is the non-zero pixel point.
    Scanning from right to left, the right boundary of the digit is the non-zero pixel point.
    Scanning from top to bottom, the top boundary of the digit is the non-zero pixel point.
    Scanning from bottom to top, the bottom edge of the digit is the non-zero pixel point.
    """
    def __init__(self, ):
        pass

    def do(self, img):
        height = img.shape[0]
        width = img.shape[1]
        v_sum = np.sum(img, axis=0)
        h_sum = np.sum(img, axis=1)
        left = 0
        right = width - 1
        top = 0
        low = height - 1
        for i in range(width):
            if v_sum[i] > 0:
                left = i
                break

        for i in range(width - 1, -1, -1):
            if v_sum[i] > 0:
                right = i
                break

        for i in range(height):
            if h_sum[i] > 0:
                top = i
                break

        for i in range(height - 1, -1, -1):
            if h_sum[i] > 0:
                low = i
                break
        return (left, top, right, low)

class Digit2Image(object):
    """
    Cut out the redundant border of the image
    Rotate the digit randomly
    """
    def __init__(self,
                 width, height,set_height, margin):
        self.width = width
        self.height = height
        self.set_height = set_height
        self.margin = margin

    def do(self, res):
        find_image_bbox = FindImageBBox()
        np_img = res
        cropped_box = find_image_bbox.do(np_img)
        left, upper, right, lower = cropped_box
        np_img = np_img[upper: lower + 1, left: right + 1]
        np_img = cv2.copyMakeBorder(np_img, self.margin, self.margin, 0, 0, cv2.BORDER_CONSTANT, value=0)
        np_img = cv2.resize(np_img,(int(self.width*(right-left+1)/self.height), self.set_height))
        return np_img
