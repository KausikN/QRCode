"""
Stream lit GUI for hosting QRCode
"""

# Imports
import os
import streamlit as st
import json
import functools

from QRCode import *

# Main Vars
config = json.load(open('./StreamLitGUI/UIConfig.json', 'r'))

# Main Functions
def main():
    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    'Choose one of the following',
        tuple(
            [config["PROJECT_NAME"]] + 
            config["PROJECT_MODES"]
        )
    )
    
    if selected_box == config["PROJECT_NAME"]:
        HomePage()
    else:
        correspondingFuncName = selected_box.replace(' ', '_').lower()
        if correspondingFuncName in globals().keys():
            globals()[correspondingFuncName]()
 

def HomePage():
    st.title(config["PROJECT_NAME"])
    st.markdown('Github Repo: ' + "[" + config["PROJECT_LINK"] + "](" + config["PROJECT_LINK"] + ")")
    st.markdown(config["PROJECT_DESC"])

    # st.write(open(config["PROJECT_README"], 'r').read())

#############################################################################################################################
# Repo Based Vars
CACHE_PATH = "StreamLitGUI/CacheData/Cache.json"
DEFAULT_PATH_EXAMPLEIMAGE = "TestData/TestImgs/Example.png"
DEFAULT_PATH_EXAMPLEVIDEO = "TestData/TestVideos/Example.wav"
DEFAULT_URL_EXAMPLEVIDEO = "http://192.168.0.102:8080/shot.jpg"

DISPLAYS = ["QR-CODE-BORDER", "QR-CODE-DATA"]
DEFAULT_IMAGE_EMPTY = np.zeros((10, 10, 3), dtype=np.uint8)

# Util Vars
CACHE = {}

# Util Functions
def LoadCache():
    global CACHE
    CACHE = json.load(open(CACHE_PATH, 'r'))

def SaveCache():
    global CACHE
    json.dump(CACHE, open(CACHE_PATH, 'w'), indent=4)

def Hex_to_RGB(val):
    val = val.lstrip('#')
    lv = len(val)
    return tuple(int(val[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def RGB_to_Hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

# Main Functions
def VisFunc_QRDecode(I, **params):
    qrDatas = QRDecode(I)
    data = UI_DisplayQRData(I, qrDatas, **params)
    return data

# UI Functions
def UI_GetVisParams():
    USERINPUT_DISPLAYS = st.multiselect("Select Displays", DISPLAYS, default=["QR-CODE-BORDER"])
    params = {
        "displays": USERINPUT_DISPLAYS
    }
    # Border
    if "QR-CODE-BORDER" in USERINPUT_DISPLAYS:
        # st.markdown("### QR-CODE-BORDER")
        col1, col2, col3 = st.columns((1, 1, 2))
        params["qr_border_params"] = {
            "color": [
                Hex_to_RGB(col1.color_picker("Outer Border Color", RGB_to_Hex((0, 0, 0)))),
                Hex_to_RGB(col2.color_picker("Inner Border Color", RGB_to_Hex((0, 255, 0)))),
            ],
            "thickness": col3.slider("Border Thickness", 0.005, 0.1, 0.01, 0.005)
        }
    # Data
    if "QR-CODE-DATA" in USERINPUT_DISPLAYS:
        # st.markdown("### QR-CODE-DATA")
        col1, col2 = st.columns(2)
        params["qr_data_params"] = {
            "color": Hex_to_RGB(col1.color_picker("Text Color", RGB_to_Hex((0, 255, 0)))),
            "thickness": col2.slider("Text Thickness", 0.005, 0.1, 0.005, 0.005)
        }

    # LIMIT
    params["LIMIT"] = st.sidebar.number_input("Max QR Codes Limit", 1, 10, 1, 1)

    return USERINPUT_DISPLAYS, params

def UI_LoadImage():
    USERINPUT_ImageData = st.file_uploader("Upload Image", ['png', 'jpg', 'jpeg', 'bmp'])
    if USERINPUT_ImageData is not None:
        USERINPUT_ImageData = USERINPUT_ImageData.read()
    else:
        USERINPUT_ImageData = open(DEFAULT_PATH_EXAMPLEIMAGE, 'rb').read()
    USERINPUT_Image = cv2.imdecode(np.frombuffer(USERINPUT_ImageData, np.uint8), cv2.IMREAD_COLOR)
    USERINPUT_Image = cv2.cvtColor(USERINPUT_Image, cv2.COLOR_BGR2RGB)
    # Display
    st.image(USERINPUT_Image, caption="Input Image", use_column_width=True)

    return USERINPUT_Image

def UI_LoadVideo():
    USERINPUT_VideoInputChoice = st.selectbox("Select Video Input Source", list(INPUTREADERS_VIDEO.keys()))
    USERINPUT_VideoReader = INPUTREADERS_VIDEO[USERINPUT_VideoInputChoice]

    # Upload Video File
    if USERINPUT_VideoInputChoice == "Upload Video File":
        USERINPUT_VideoPath = st.file_uploader("Upload Video", ['avi', 'mp4', 'wmv'])
        if USERINPUT_VideoPath is None:
            USERINPUT_VideoPath = DEFAULT_PATH_EXAMPLEVIDEO
        USERINPUT_VideoReader = functools.partial(USERINPUT_VideoReader, USERINPUT_VideoPath)
    # Video URL
    elif USERINPUT_VideoInputChoice == "Video URL":
        USERINPUT_VideoURL = st.text_input("Video URL", DEFAULT_URL_EXAMPLEVIDEO)
        USERINPUT_VideoReader = functools.partial(USERINPUT_VideoReader, USERINPUT_VideoURL)
    # Webcam
    else:
        pass
    USERINPUT_Video = USERINPUT_VideoReader()
    
    return USERINPUT_Video

def UI_DisplayQRData(I, qrDatas, **params):
    # Sort
    qrDatas_sorted = [x for _, x in sorted(zip([q["data"] for q in qrDatas], qrDatas), reverse=True)]
    qrDatas = qrDatas_sorted
    # Only display top LIMIT QR Codes
    LIMIT = params["LIMIT"]
    qrDatas = qrDatas[:LIMIT]

    # Init
    displayObj = params["displayObj"]
    if displayObj is None:
        displayObj = {
            "overall": {
                "title": st.empty(),
                "image": st.empty()
            },
            "qrcode": []
        }
        for i in range(LIMIT):
            col1, col2 = st.columns((1, 3))
            displayObj["qrcode"].append({
                "image": col1.empty(),
                "data": col2.empty()
            })
    # Title
    displayObj["overall"]["title"].markdown("## QR Code Data")
    # Display QR Image
    I_qrcode = I
    for qrData in qrDatas:
        if "QR-CODE-BORDER" in params["displays"]:
            I_qrcode = GetQRBorderImage(I_qrcode, qrData, **params["qr_border_params"])
        if "QR-CODE-DATA" in params["displays"]:
            I_qrcode = GetQRDataImage(I_qrcode, qrData, **params["qr_data_params"])
    displayObj["overall"]["image"].image(I_qrcode, caption="QR Code Image", use_column_width=True)
    # Display Each QR Data Element
    for i in range(LIMIT):
        if i >= len(qrDatas):
            # for key in displayObj["qrcode"][i]: displayObj["qrcode"][i][key].empty()
            displayObj["qrcode"][i]["image"].image(DEFAULT_IMAGE_EMPTY, caption=str(i+1), use_column_width=True)
            displayObj["qrcode"][i]["data"].markdown("```python\n None \n```")
            continue
        qrData = qrDatas[i]
        
        # Generate Cropped Image
        I_qrcropped = I
        I_qrcropped = GetQRBorderImage(I_qrcropped, qrData, **params["qr_border_params"])
        I_qrcropped = GetQRCroppedImage(I_qrcropped, qrData)
        finalSize = max(I_qrcropped.shape[:2])
        I_qrcropped_padded = np.zeros((finalSize, finalSize, 3), dtype=np.uint8)
        I_qrcropped_padded[:I_qrcropped.shape[0], :I_qrcropped.shape[1], :] = I_qrcropped
        I_qrcropped = I_qrcropped_padded

        # Image
        if 0 in I_qrcropped.shape: I_qrcropped = DEFAULT_IMAGE_EMPTY
        displayObj["qrcode"][i]["image"].image(I_qrcropped, caption=str(i+1), use_column_width=True)
        
        # Data
        qrData_display = Convert_QRDict2DisplayDict(qrData)
        qrData_Str = json.dumps(qrData_display, indent=4)
        displayObj["qrcode"][i]["data"].markdown("```python\n" + qrData_Str + "\n```")

    return displayObj

# Repo Based Functions
def decode_qr_code():
    # Title
    st.header("Decode QR Code")

    # Prereq Loaders

    # Load Inputs
    USERINPUT_MODE = st.selectbox("Select Input", ["Image", "Webcam"])
    
    # Process Inputs and Display Outputs
    # Webcam QR Code
    if USERINPUT_MODE == "Webcam":
        USERINPUT_Video = UI_LoadVideo()
        USERINPUT_DISPLAYS, DisplayParams = UI_GetVisParams()
        VisFunc = functools.partial(VisFunc_QRDecode, **DisplayParams)
        VideoVis_Framewise(VisFunc, USERINPUT_Video)
    # Image QR Code
    else:
        USERINPUT_Image = UI_LoadImage()
        USERINPUT_DISPLAYS, DisplayParams = UI_GetVisParams()
        VisFunc_QRDecode(USERINPUT_Image, **DisplayParams)
    
#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()