import numpy as np 
from PyQt5 import QtGui
import matplotlib.pyplot as plt
import cv2

def convert_cv_qt(cv_img):
    """Convert from an opencv image to QPixmap"""
    #https://gist.github.com/docPhil99/ca4da12c9d6f29b9cea137b617c7b8b1
    #Thank you docPhil99
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
    #p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
    p=convert_to_Qt_format
    return QtGui.QPixmap.fromImage(p)

def read_image(url):
    src=cv2.imread(url)
    return src


def crop(src,x1,y1,x2,y2):
    image=src[y1:y2,x1:x2]
    return image

def rotate(src,angle):
    h,w=src.shape[:2]
    image_center=(w/2,h/2)
    r=cv2.getRotationMatrix2D((w/2,h/2), angle, 1.0)
    abs_cos = abs(r[0,0]) 
    abs_sin = abs(r[0,1])
    bound_w = int(h * abs_sin + w * abs_cos)
    bound_h = int(h * abs_cos + w * abs_sin)
    r[0, 2] += bound_w/2 - image_center[0]
    r[1, 2] += bound_h/2 - image_center[1]
    image = cv2.warpAffine(src,r, (bound_w, bound_h))

    return image

def filter(src,filter):
    image1= cv2.cvtColor(src, cv2.COLOR_BGR2GRAY )
    image=cv2.filter2D(src=image1, kernel=filter, ddepth=-1)

    return image

def gray_scale(src):
    try:
        image = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY )
        return image
    except:
        print('Image is GrayScale itself')
        return None

def blur(src,k):
    image1= cv2.cvtColor(src, cv2.COLOR_BGR2GRAY )
    image = cv2.blur(image1,(k,k)) 
    return image

def resize(src,x,y):
    image=cv2.resize (src,(y,x),interpolation=cv2.INTER_AREA)
    return image

def show(image,name="image"):
    cv2.imshow(name,image)
    

def save_im(url,image):
    cv2.imwrite(url, image)

def random_crop(src):
    x=src.shape[0]
    y=src.shape[1]
    x1=np.random.randint(x)
    x2=x1+np.random.randint(x-x1)
    y1=np.random.randint(y)
    y2=x1+np.random.randint(y-y1)
    image=crop(src,x1,y1,x2,y2)
    return image



if __name__=="__main__":
#     src=read_image("im1.jpg")
#     image=resize(src,300,300)
#     imgra=gray_scale(image)
#     image1=rotate(image,360)
#     show(imgra,name="imagr")
#     show(image)
#     show(image1,name="image1")
    cv2.waitKey()
    cv2.destroyAllWindows()
    pass
