import pandas
from ultralytics import YOLO
import cv2
import streamlit as st
#import tensorflow as tf
from utils import video_input,create_download_video,create_download_zip
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from streamlit_option_menu import option_menu
import pandas as pd
import PIL
import os
from collections import deque
from clever_label import auto_label
from utils import create_db_state,upsert_video_state,get_video_state_by_name
import numpy as np

conn, cur = create_db_state()

model_gun = YOLO('best_all_v9_40epoch.pt')


import sqlite3

# Подключаемся к базе данных (если базы нет, то она будет создана)




que = deque()


st.set_page_config(page_title="EvilNet search for drons", page_icon=":cinema:", layout="wide",
                   initial_sidebar_state="expanded")

# side bar
st.sidebar.image("img/EvilNET_logo.jpg", caption="Search for drons")

with st.sidebar:
    selected = option_menu("", ["Мониторинг", "---", "Devises", "Settings", "File mode","Download Video"],
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
            'rtsp://admin:A1234567@188.170.176.190:8028')
        cap_2 = cv2.VideoCapture(
            'rtsp://admin:A1234567@188.170.176.190:8029')






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

        clicked = st.sidebar.button('Browse Folder')
        source_img = st.sidebar.file_uploader(
            "Choose an images...", type=("jpg", "jpeg", "png", 'bmp', 'webp'),accept_multiple_files = True)
        if clicked:
            root = tk.Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            dirname = str(filedialog.askdirectory(master=root))
            print(dirname)
            listdirs = os.listdir(dirname)
            for path in listdirs:
                filename = os.path.join(dirname,path)
                picture = PIL.Image.open(filename)                            #ЗАВТРА ПОЛЮБОМУ НАДО ДОРАБОТАТЬ
                auto_label(model_gun,filename,confidence,dirname)
            if '/' in dirname:
                final_path = dirname.split('/')[-1]
            elif '\\' in dirname:
                final_path = dirname.split('\\')[-1]
            zip_button = create_download_zip(f"{final_path}_labels",f"{dirname}_labels",f"{final_path}_labels.zip")
            print(zip_button)
            if zip_button:
                os.remove(f"{dirname}_labels")
                os.remove(f"{final_path}_labels.zip")
        # if source_img:
        #     mode = st.sidebar.
        # col1, col2 = st.columns(2)

        with col1:
                if isinstance(source_img,list):
                    lst_of_imgs = []
                    for image in source_img:
                        uploaded_image = PIL.Image.open(image)
                        lst_of_imgs.append(uploaded_image)
                        st.image(image, caption="Uploaded Image", use_column_width=True)
                else:
                    uploaded_image = PIL.Image.open(image)
                    lst_of_imgs.append(uploaded_image)
                    st.image(image, caption="Uploaded Image", use_column_width=True)



        with col2:

            if st.sidebar.button('Detect Objects'):
                if isinstance(source_img,list):
                    try:
                        for image in lst_of_imgs:
                            res = model_gun.predict(image,
                                                conf=confidence
                                                )

                            boxes = res[0].boxes
                            res_plotted = res[0].plot()[:, :, ::-1]
                            st.image(res_plotted, caption='Detected Image',    # здесь код пока что чуть-чуть дурацкий, тут может быть ситуация
                                     use_column_width=True)                    # когда загружают одно или несколько фото

                            with st.expander("Detection Results"):
                                for box in boxes:
                                    st.write(box.data)
                        del lst_of_imgs
                    except Exception as ex:
                        # st.write(ex)
                        st.error("No image is uploaded yet!")
                else:
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


        video_input(model_gun,confidence,conn,cur)
        conn.close()
        #create_download_video('uploaded_data/filename.mp4')
        #create_download_zip('archiv','uploaded_data/archiv')


if selected == "Download Video":
    try:
        lst_videos = list(map(lambda x:x[1],get_video_state_by_name(cur)))
        print(lst_videos)
        option = st.selectbox(
            "How would you like to be contacted?",
            lst_videos)

        st.write("You selected:", option)
        button_video = create_download_video(f'videos/{option}',option)
    except:
        st.error("You didn't detect anything")