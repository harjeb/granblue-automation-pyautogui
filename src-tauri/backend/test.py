import cv2
import requests
from hashlib import md5
from utils.image_utils import ImageUtils

print(9)
header_center_post = ImageUtils.find_button("captcha_header")
print(88)
print(header_center_post)
top_left = (header_center_post[0]-96,header_center_post[1]+175)
bottom_right = (header_center_post[0]+100,header_center_post[1]+250)
print(top_left)
print(bottom_right)

captcha_img = cv2.imread("temp/source.png")
cropped = captcha_img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
cv2.imwrite("temp/captcha.png", cropped)