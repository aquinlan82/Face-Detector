import numpy as np
import matplotlib.pyplot as plt
import cv2
import random  

def one_channel_to_three(img):
    img_out = np.stack([img, img, img], axis=2)
    return img_out

def sort_eyes(eyes):
    #return left eye, right eye
    eye1, eye2 = eyes
    if eye1[0] < eye2[0]:
        
        return np.array([eye1, eye2])
    else:
        return np.array([eye2, eye1])
        
def get_ycc_image(filename):
    flag = cv2.IMREAD_COLOR
    bgr_img = cv2.imread(filename, flag)
    ycc_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2YCR_CB)
    return ycc_img

def get_rgb_image(filename, color=True, transparency=False):
    if transparency:
        flag = cv2.IMREAD_UNCHANGED
    elif color:
        flag = cv2.IMREAD_COLOR
    else:
        flag = cv2.IMREAD_GRAYSCALE
    bgr_img = cv2.imread(filename, flag)
    rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    return rgb_img
    
def show_image(img, color_space):
    if color_space == "gray":
        plt.figure(figsize=(5,5))
        plt.imshow(img, cmap="gray")
        return
    
    if color_space == "ycc":
        rgb_img = cv2.cvtColor(img, cv2.COLOR_YCR_CB2RGB)
    elif color_space == "bgr":
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        rgb_img = img
    plt.figure(figsize=(5,5))
    plt.imshow(rgb_img)
    
def threshold_img(img, thresh, channel=None, flip=False):
    #image full of thresh value, size of img
    thresh_img = np.zeros((len(img), len(img[0])))
    thresh_img = thresh_img + thresh
    
    #channel to be thresholded (or none if already grayscale)
    if channel is None:
        img_channel = img
    else:
        img_channel = img[:,:,channel]
    
    #apply threshold
    mask = img_channel - thresh_img
    mask = np.ceil(mask)
    mask = np.minimum(mask, 1)
    mask = np.maximum(mask, 0)
    return mask

def get_annotated_image(index=None):
    if index is None:
        index = random.randint(0, 7049)
        
    #get metadata
    with open('landmark_list_part1.txt') as f:
        lines = f.readlines()
    lines = [line.split(" ")  for line in lines]
    data = lines[index]
    
    #get image
    filename = "crop_part1//" + data[0]+".chip.jpg"
    img = get_ycc_image(filename)
    return data, img, index


def get_test_image(index=None):
    if index is None:
        index = random.randint(0, 7049)
        
    #get metadata
    with open('landmark_list_part1.txt') as f:
        lines = f.readlines()
    lines = [line.split(" ")  for line in lines]
    data = lines[index]
    
    #get image
    filename = "part1//" + data[0]
    img = get_ycc_image(filename)
    return data, img, index

def draw_landmark(range_start, range_stop, img, data):
    for i in range(range_start,range_stop,2):
        pt1 = (int(data[i]), int(data[i+1]))
        pt2 = (int(data[i+2]), int(data[i+3]))
        img = cv2.line(img, pt1, pt2, color=(0, 255, 0))
    return img

def annotate_face(img, data):
    img = img.copy()
    img = draw_landmark(1,33, img, data)  #ear down chin to ear
    img = draw_landmark(35,43, img, data) #left eyebrow
    img = draw_landmark(45,53, img, data) #right eyebrow
    img = draw_landmark(55,59, img, data) #line down nose
    img = draw_landmark(63,71, img, data) #bottom of nose
    img = draw_landmark(73,83, img, data) #left eye
    img = draw_landmark(85,95, img, data) #right eye
    img = draw_landmark(97,135, img, data) #lips
    show_image(img, "ycc")
    
def annotate_eyes(img, data):
    img = img.copy()
    img = draw_landmark(73,83, img, data) #left eye
    img = draw_landmark(85,95, img, data) #right eye
    show_image(img, "ycc")

def get_kaggle_test_image(index=None):
    if index is None:
        index = random.randint(0, 7049)
        
    data = np.load('face_images_kaggle.npz')
    lst = data.files
    images = data[lst[0]]
    
    return images[:,:,index]

def get_average_face():
    try:
        img = cv2.imread("face_template.jpg")
        return img[:,:,0]
    except:
        data = np.load('face_images_kaggle.npz')
        lst = data.files
        images = data[lst[0]]

        avg = np.zeros((96,96))
        for x in range(96):
            for y in range(96):
                avg[y,x] = np.mean(images[y,x,:])

        cv2.imwrite("face_template.jpg", avg)

        return avg
    
    
    
    
    