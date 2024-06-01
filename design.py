import pandas
# ultralytics import YOLO
import cv2
import streamlit as st
#import tensorflow as tf
from utils import video_input,create_download_video
from PIL import Image
from streamlit_option_menu import option_menu
import pandas as pd
import PIL
import os
from collections import deque
import numpy as np
#model_gun = YOLO('weights.pt')





que = deque()


st.set_page_config(page_title="EvilNet search for drons", page_icon=":cinema:", layout="wide",
                   initial_sidebar_state="expanded")

# side bar
st.sidebar.image("img/EvilNET_logo.jpg", caption="Search for drons")

with st.sidebar:
    selected = option_menu("", ["Мониторинг", "---", "Devises", "Settings", "File mode"],
                           icons=['images', '', 'camera-video', 'gear', 'card-image'], menu_icon="cast",
                           default_index=0,
                           styles={
                               "container": {"padding": "0!important", "background-color": "#fafafa"},
                               "nav-link-selected": {"background-color": "#b0b7c6"},
                           })




# Main Page Мониторинг
st.subheader("Раздел события")
if selected == "Мониторинг":
    stream_on_off = st.checkbox('Включить / выключить демонстрацию с камер')
    if stream_on_off:
        cap_1 = cv2.VideoCapture(
            'rtsp://admin:A1234567@188.170.176.190:8028/Streaming/Channels/101?transportmode=unicast&profile=Profile_1')
        cap_2 = cv2.VideoCapture(
            'rtsp://admin:A1234567@188.170.176.190:8029/Streaming/Channels/101?transportmode=unicast&profile=Profile_1')






        with st.container():
            col1, col2 = st.columns(2)
        with col1:
            output_1 = st.empty()
        with col2:
            output_2 = st.empty()


        while True:
            ret, frame = cap_1.read()

            output_1.image(frame, width=400)

            ret, frame = cap_2.read()
            output_2.image(frame, width=400)

        st.divider()

    ####################################




#################################

    with st.container():
        col1, col2, col3 = st.columns(3)
    with col1:

        ##output=st.empty()
        image_vid_1 = Image.open('from git/pic_vid.png')
        st.image(image_vid_1, caption='Указать объект - время - дату')
    with col2:
        ##output = st.empty()
        image_vid_2 = Image.open('from git/pic_vid.png')
        st.image(image_vid_2, caption='Указать объект - время - дату')
    with col3:
        ##output = st.empty()
        image_vid_3 = Image.open('from git/pic_vid.png')
        st.image(image_vid_3, caption='Указать объект - время - дату')

    st.divider()


if selected == "Devises":
    with st.container():
        col1, col2, col3 = st.columns(3)
    with col1:
        name_camera = st.text_input("Название камеры",)
    with col2:
        name_ip = st.text_input("IP адрес",)
    with col3:
        add_camera = st.button('Добавить камеру')
        del_camera = st.button('Удалить камеру')


    st.subheader(":movie_camera: Камеры")
    try:
        df = pd.read_csv('list_of_camera.csv',index_col=0)
    except:
        df=pd.DataFrame()
    # Header
    if add_camera:
        if name_ip and name_camera:


            data= pd.DataFrame(data={'Объект': ["Школа №1"], 'Название': [name_camera],
                            'IP адрес': [name_ip], "Состояние": ['отключено']})
            df = pandas.concat([data, df], axis=0,ignore_index=True)
            df.to_csv('list_of_camera.csv')
        else:
            st.error('Заполните пропущенные поля')
    if del_camera:

        if name_ip and name_camera:
            #df=df[np.logical_and.reduce((df['Название'] != name_camera, df['IP адрес'] != str(name_ip)))]
            df=df[(df['Название'] != name_camera) & (df['IP адрес'] != name_ip)]
            df.to_csv('list_of_camera.csv')
        else:
            st.error('Заполните пропущенные поля')







    st.table(df)

    # if(st.button('Submit')):
#	result = name.title()
# st.success(result)

# Settings
if selected == "Settings":
    # Header
    st.title('Welcome to Settings')
    #st.subheader('*A new tool to find similar locations across the United States.*')

# File mode
if selected == "File mode":
    # Header
    confidence = float(st.sidebar.slider("Select Model Confidence", 25, 100, 40)) / 100
    st.subheader('File mode. Сценарий с видео (базовый) Возможность загрузить архив видеозаписей для тестирования')
    st.subheader("Image/Video Config")

    source_radio = st.sidebar.radio("Select Source", ['Image', 'Video'])  # , horizontal=True)
    with st.container():
        col1, col2,  = st.columns(2)

    source_img = None
    # If image is selected
    if source_radio == "Image":

        source_img = st.sidebar.file_uploader(
            "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

        col1, col2 = st.columns(2)

        with col1:
            if source_img:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image", use_column_width=True)

        with col2:

            if st.sidebar.button('Detect Objects'):
                try:
                    res = model_gun.predict(uploaded_image,
                                        conf=confidence
                                        )

                    boxes = res[0].boxes
                    res_plotted = res[0].plot()[:, :, ::-1]
                    st.image(res_plotted, caption='Detected Image',
                             use_column_width=True)

                    with st.expander("Detection Results"):
                        for box in boxes:
                            st.write(box.data)
                except Exception as ex:
                    # st.write(ex)
                    st.error("No image is uploaded yet!")


    elif source_radio == 'Video':


        video_input(model_gun,model_pose,confidence)
        #create_download_video('uploaded_data/filename.mp4')
        #create_download_zip('archiv','uploaded_data/archiv')


