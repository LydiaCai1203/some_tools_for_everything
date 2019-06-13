import base64
import cv2
from PIL import Image


def from_base64_2img(filename, encoded_img):
    """
    save current directory temporary
    if filename has'_', will throw error(no such file or directory)
    """
    print("--<{}>--".format(filename))
    b_img = base64.b64decode(encoded_img)
    with open(filename, 'wb+') as f:
        f.write(b_img)


def show(filename):
    """
    show the picture
    """
    cv2.imshow('Show', filename)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def is_pixel_equal(img1_name, img2_name, x, y):
    """
    判断两张图片是否相似
    if you want to save PIL Image
    img1.save('new_img_name.jpg')
    """
    img1 = Image.open(img1_name)
    img1 = img1.resize((278, 108), Image.ANTIALIAS)
    img2 = Image.open(img2_name)
    img2 = img2.resize((278, 108), Image.ANTIALIAS)
    pix1 = img1.load()[x, y]
    pix2 = img2.load()[x, y]
    threshold = 60
    if (abs(pix1[0] - pix2[0]) < threshold and abs(
        pix1[1] - pix2[1] < threshold) and abs(
            pix1[2] - pix2[2] < threshold
        )):
        return True
    else:
        return False