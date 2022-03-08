'''
Summary
This script has functions for reading qr codes, preprocessing images to retrieve the qr code

- QR Code GIF
'''
import cv2
import matplotlib.pyplot as plt
import numpy as np

import Utils

# Main Functions

# Driver Code
plt.imshow(Utils.Image_Threshold(cv2.imread('C:/Users/Kausik N/Desktop/Sig.png', 0), (254, 255)), 'gray')
# imgPath = 'test2.jpg'
# I = cv2.imread(imgPath, 0)
# I_th = Utils.Image_Threshold(I, (127, 128))
# ax = plt.subplot(1, 2, 1)
# ax.title.set_text('Original')
# plt.imshow(I, 'gray')
# ax = plt.subplot(1, 2, 2)
# ax.title.set_text('Threshold')
# plt.imshow(I_th, 'gray')

plt.show()