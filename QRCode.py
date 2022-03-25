'''
QR Code
'''
import cv2
import numpy as np
from pyzbar.pyzbar import decode

from Utils.Utils import *

# Main Functions
# Encode Decode Functions
def QRDecode(I):
    '''
    Decode QR code from image
    '''
    # Convert to grayscale
    I_gray = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

    # Decode
    decoded_data = decode(I_gray)

    # Add boxes to image
    qrDatas = []
    for obj in decoded_data:
        qrData = Convert_QRObj2QRDict(obj)
        qrDatas.append(qrData) 

    return qrDatas

# Data Format Functions
def Convert_QRObj2QRDict(qrObj):
    '''
    Convert QR Object Data to Dict
    '''
    # Get Data
    x, y, w, h = qrObj.rect
    points = np.array(qrObj.polygon, dtype=np.int32)
    points = points.reshape((-1, 1, 2))
    data = str(qrObj.data.decode('utf-8'))
    codeType = qrObj.type
    # Set Dict
    data = {
        "codeType": codeType,
        "data": data,
        "bounds": {
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "points": points.tolist()
        }
    }

    return data

def Convert_QRDict2DisplayDict(qrDict):
    '''
    Retains displayable data from QR Dict
    '''
    # Get Data
    codeType = qrDict["codeType"]
    data = qrDict["data"]
    # Set Display Dict
    data = {
        "type": codeType,
        "data": data
    }

    return data

# Image Functions
def GetQRBorderImage(I, qrData, color=[(0, 0, 0), (0, 255, 0)], thickness=0.001):
    '''
    Get QR Code Border Image
    '''
    # Construct QR Code Border
    I_border = np.copy(I)
    points = np.array(qrData["bounds"]["points"])
    I_size = (I.shape[0] + I.shape[1]) / 2.0
    # Draw Thick Lines of Black
    cv2.polylines(I_border, [points], True, tuple(color[0]), int(thickness * I_size))
    # Draw Thin Lines
    cv2.polylines(I_border, [points], True, tuple(color[1]), int(thickness * I_size / 2.0))

    return I_border

def GetQRDataImage(I, qrData, color=(0, 255, 0), thickness=0.001):
    '''
    Add QR Data to image as text
    '''
    I = np.copy(I)
    I_size = (I.shape[0] + I.shape[1]) / 2.0
    # Construct display text
    codeType = qrData["codeType"]
    data = qrData["data"]
    displayText = f"[{codeType}]: {data}"
    # Add Text to Image
    cv2.putText(I, displayText, (qrData["bounds"]["x"], qrData["bounds"]["y"]), cv2.FONT_HERSHEY_SIMPLEX, 
        0.8, tuple(color), int(thickness * I_size))

    return I

def GetQRCroppedImage(I, qrData):
    '''
    Crop QR Code part from image
    '''
    # Crop QR Code
    x = qrData["bounds"]["x"]
    y = qrData["bounds"]["y"]
    w = qrData["bounds"]["w"]
    h = qrData["bounds"]["h"]
    I_qrcode = I[y:y+h, x:x+w]

    return I_qrcode

# Driver Code
# # Params
# img_path = 'TestImgs/tes2.png'
# # Params

# # RunCode
# I = cv2.imread(img_path)
# I_display, codeData = QRDecoder(I)

# DisplayImage(I_display)