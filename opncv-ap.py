import numpy as np 

import matplotlib.pyplot as plt
import cv2


def read_image(url):
    src=cv2.imread(url)
    return src


def crop(src,x1,y1,x2,y2):
    image=src[y1:y2,x1:x2]
    return image

def rotate(src,angle):
    h,w=src.shape[:2]
    r=cv2.getRotationMatrix2D((w/2,h/2), angle, 1.0)
    image = cv2.warpAffine(src,r, (w, h))

    return image

def filter(src,filter):
    image1= cv2.cvtColor(src, cv2.COLOR_BGR2GRAY )
    image=cv2.filter2D(src=image1, kernel=sharpenKernel, ddepth=-1)

    return image

def gray_scale(src):
    image = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY )
    return image

def blur(src,k):
    image1= cv2.cvtColor(src, cv2.COLOR_BGR2GRAY )
    image = cv2.blur(image1,(k,k)) 
    return image

def resize(src,x,y):
    image=cv2.resize (src,(y,x),interpolation=cv2.INTER_AREA)
    return image

def show(image,name="image"):
    cv2.imshow(name,image)
    pass



if __name__=="__main__":
    src=read_image("im1.jpg")
    image=resize(src,300,300)
    imgra=gray_scale(image)
    image1=rotate(image,360)
    show(imgra,name="imagr")
    show(image)
    show(image1,name="image1")
    cv2.waitKey()
    cv2.destroyAllWindows()
    pass
