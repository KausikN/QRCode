'''
Util scripts and functions for qr code reader
'''

# Imports
import cv2
import numpy as np
import matplotlib.pyplot as plt

from pyzbar.pyzbar import decode

# Utils Functions
def DisplayImage(I):
    '''
    Display image
    '''
    plt.imshow(I)
    plt.show()

# Main Functions
def QRDecoder(I):
    '''
    Decode qr code from image
    '''

    # Convert to grayscale
    I_gray = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

    # Decode
    decoded_data = decode(I_gray)

    # Add boxes to image
    for obj in decoded_data:
        x, y, w, h = obj.rect

        points = np.array(obj.polygon, dtype=np.int32)
        points = points.reshape((-1, 1, 2))

        # Draw Thick Lines of Black
        cv2.polylines(I, [points], True, (0, 0, 0), 7)
        # Draw Thin Lines
        cv2.polylines(I, [points], True, (0, 255, 0), 3)

        # Get Data
        data = str(obj.data.decode('utf-8'))
        codeType = obj.type

        displayText = f"[{codeType}]: {data}"

        # Add Text to Image
        cv2.putText(I, displayText, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    return I, decoded_data

# Driver Code
# Params
img_path = 'TestImgs/tes2.png'
# Params

# RunCode
I = cv2.imread(img_path)
I_display, codeData = QRDecoder(I)

DisplayImage(I_display)