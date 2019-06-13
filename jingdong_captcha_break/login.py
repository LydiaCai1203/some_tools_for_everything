import os
import cv2
import time
import base64
import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from config import (
    URL, ACCOUNT, PASSWORD, IMG_PREFIX, BAC_IMG_PATH, SMALL_IMG_PATH, ) 
from utils import (
    from_base64_2img, is_pixel_equal, show)

class SlideCaptcha:

    def __init__(self, bac_img_path, small_img_path):
        self.bac_img_path = bac_img_path
        self.small_img_path = small_img_path

    def save_img(self, browser):
        """
        save img to folder(captcha)
        """
        # 以后再把regular抽象出来
        bac_img = browser.find_element(By.XPATH, '//div[@class="JDJRV-bigimg"]//img')
        encode_bac = bac_img.get_attribute('src').split(',')[1]
        from_base64_2img(self.bac_img_path, encode_bac)

        small_img = browser.find_element(By.XPATH, '//div[@class="JDJRV-smallimg"]//img')
        encode_small = small_img.get_attribute('src').split(',')[1]
        from_base64_2img(self.small_img_path, encode_small)

    def calc_position(self, browser):
        """
        using opencv to recognize the position of small_captcha
        """
        # absolute path && return type of img; flag==0 means return grey-scale map;
        target = cv2.imread(self.small_img_path, 0)  
        template = cv2.imread(self.bac_img_path, 0)
        target.resize()

        w, h = target.shape[::-1]  # return tuple(width, heigth)
        cmp_w, cmp_h = template.shape[::-1]

        # save as grey map image
        target_new = './captcha/targ.jpg'
        template_new = './captcha/temp.jpg'
        cv2.imwrite(target_new, target)
        cv2.imwrite(template_new, template)

        target = cv2.imread(target_new)
        # conversion from a RGB img to gray
        target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        target = abs(255-target)   # get the complememtray color
        cv2.imwrite(target_new, target)
        target = cv2.imread(target_new)

        template = cv2.imread(template_new)
        # CV_TM_CCOEFF_NORMED 归一化相关系数匹配法
        result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
        # return the index of a pixel in the rectangle which we point
        x, y = np.unravel_index(result.argmax(), result.shape)
        cv2.imwrite('./captcha/template1.jpg', template)  # old img
        cv2.rectangle(template, (y, x), (y+w, x+h), (7, 249, 151), 2)   
        cv2.imwrite('./captcha/template2.jpg', template)   # new img
        return x, y

    def get_offset(self, target_path, template_path):
        """
        得到位移值方便滑块进行移动
        """
        target = Image.open(target_path)
        target = target.resize((278, 108), Image.ANTIALIAS)

        template = Image.open(template_path)
        template = template.resize((278, 108), Image.ANTIALIAS)

        left = 0
        for i in range(target.size[0]):
            for j in range(target.size[1]):
                if not is_pixel_equal(target_path, template_path, i, j):
                    left = i
                    return left
        return left         

    def get_tracks(self, offset):
        """
        得到滑块的移动轨迹,首先以加速度a=2m/s^2匀加速滑动，再以加速度a=-3m/s^2匀减速滑动
        该函数返回值类型为数组，数组的每个元素都是滑块需要移动的子位移
        v1 = v0 + at
        v2^2 - v1^2 = 2ax
        """
        tracks = []
        ofs0 = offset/2
        ofs = 0
        v0 = 0
        v1 = 0

        # the first satge
        while True:
            if ofs < ofs0:
                v1 = v0 + 2 * 1   # a=2, delta t = 1
                x = (v1 * v1 - v0 * v0) / (2 * 3)
                ofs += x
                v0 = v1
                tracks.append(x)
            else:
                break
        
        print("----current v0<{}>--x<{}>".format(v0, x))
        # the second stage
        while True:
            if ofs < offset:
                v1 = v0 + (-1.5) * 1   # a=-1.5, delta t = 1 
                x = (v1 * v1 - v0 * v0) / (2 * -1.5)
                ofs += x
                v0 = v1
                print("--v1:<{}>--delta x:<{}>--".format(v1, x))
                tracks.append(x)
            else:
                break

        # the last one may be not correct
        ofs -= tracks[-1]
        tracks[-1] =  offset - ofs
        # tracks[-1] = offset
        return tracks


    def move2(self, browser):
        """
        complete actions of sliding captcha
        """
        self.save_img(browser)
        self.calc_position(browser)
        
        offset = self.get_offset('./captcha/template1.jpg', './captcha/template2.jpg')
        print("offset calc by get_offset() is: {}".format(offset))
        tracks = self.get_tracks(offset)
        print("the track array is: {}".format(tracks))

        slider = browser.find_element_by_class_name("JDJRV-slide-btn")
        action = ActionChains(browser)
        action.click_and_hold(slider).perform()
        action.reset_actions()

        for i in tracks:
            action.move_by_offset(round(i), 0).perform()
            print('should move--<{}>--'.format(i))
            print('moving--<{}>--'.format(slider.location['x']))
            time.sleep(0.1)
            # in order to prevent accumulation actions
            action.reset_actions()   # useful
            # action = ActionChains(browser)   # useful 

        time.sleep(4)
        action.release().perform()


class JD:
    
    def __init__(self, browser, captcha, url, account, password):
        self.url = url
        self.account = account
        self.password = password
        self.browser = browser
        self.captcha = captcha
    
    def account_login(self):
        """
        use account/pwd to login
        """
        self.browser.find_element_by_class_name("login-tab-r").click()
        account_ele = self.browser.find_element_by_name('loginname')
        password_ele = self.browser.find_element_by_name('nloginpwd')
        account_ele.send_keys(self.account)
        password_ele.send_keys(self.password)
        login_btn = self.browser.find_element_by_class_name('login-btn')
        time.sleep(1)
        login_btn.click()
    
    def qr_login(self):
        """
        by scanning qr_code to login
        """
        browser.find_element_by_class_name("login-tab-l").click() 

    def login(self, slide_captcha):
        self.browser.get(self.url)
        self.account_login()
        time.sleep(4)
        slide_captcha.move2(self.browser)
        # login process complete

    def shop(self, key):
        """
        key: production name
        """
        search = self.browser.find_element_by_xpath("//input[@id='key']")
        search.send_keys(key)
        s_btn = self.browser.find_element_by_class_name("button").click()
        # choose production u want
        goods = self.browser.find_elements_by_xpath("//div[@class='p-operate']//a[@class='p-o-btn addcart']")
        good_car = self.browser.find_element_by_xpath("//div[@class='dorpdown']")
        # good_urls = [good.get_attribute("href") for good in goods]
        for good in goods:  # add goods
            good.click()

        good_car.click()    # check the goods we added
        browser.find_element_by_xpath("//div[@class='btn-area']").click()   # 结算按钮


# just consider about the neccessary of BrowserClass again 
# class Browser:
#     driver = webdriver.Chrome()

#     def __init__(self):
#         pass
    
#     def get(self):
#         pass


if __name__ == '__main__':
    browser = webdriver.Chrome()
    captcha = SlideCaptcha(IMG_PREFIX+BAC_IMG_PATH, IMG_PREFIX+SMALL_IMG_PATH)
    jd = JD(browser, captcha, URL, ACCOUNT, PASSWORD)

    while True:
        jd.login(captcha)
        time.sleep(4)
        try:
            browser.find_element(By.XPATH, '//div[@class="JDJRV-bigimg"]//img')
        except:
            break

    print("==========browser will be closed=============")
    jd.shop('北极甜虾')    # 自动下单 只到添加进购物车为止
    browser.quit()
















