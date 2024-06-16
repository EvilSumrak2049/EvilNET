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
from clever_label import auto_label
from utils import create_db_state,upsert_video_state,get_video_state_by_name,delete_video_state_by_name
import numpy as np

conn, cur = create_db_state()

model = YOLO('best_all_v9_40epoch.pt')


import sqlite3

# Подключаемся к базе данных (если базы нет, то она будет создана)







st.set_page_config(page_title="EvilNet search for drons", page_icon=":cinema:", layout="wide",
                   initial_sidebar_state="expanded")

# side bar
st.sidebar.image("img/EvilNET_logo.jpg", caption="Search for drons")

with st.sidebar:
    selected = option_menu("", ["Мониторинг", "---", "File mode","Download Video","Devises"],
                           icons=['images', '','gear' , 'camera-video', 'card-image'], menu_icon="cast",
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
        image_vid_1 = Image.open('img/pribor96_hubsan_zino_pro_2.jpg')
        st.image(image_vid_1)
    with col2:
        ##output = st.empty()
        image_vid_2 = Image.open('img/helicopter.jpg')
        st.image(image_vid_2)
    with col3:
        ##output = st.empty()
        image_vid_3 = Image.open('img/plain.jpg')
        st.image(image_vid_3)

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


            data= pd.DataFrame(data={'Объект': ["Аэропорт №1"], 'Название': [name_camera],
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



# File mode
if selected == "File mode":
    # Header
    confidence = float(st.sidebar.slider("Select Model Confidence", 25, 100, 40)) / 100
    st.subheader('File mode. Сценарий с видео/фото (базовый) Возможность загрузить папку фото/интерактивный режим или видеозаписи для тестирования')
   # st.subheader("Image/Video Config")

    source_radio = st.sidebar.radio("Select Source", ['Image', 'Video'])  # , horizontal=True)
    with st.container():
        col1, col2,  = st.columns(2)

    source_img = None
    # If image is selected
    if source_radio == "Image":
        custom_size = st.sidebar.checkbox("Custom frame size")
        if custom_size:
            predict = st.sidebar.number_input("Predict", min_value=120, step=20, value=420)
        clicked = st.sidebar.button('Browse Folder')
        source_img = st.sidebar.file_uploader(
            "Choose an images...", type=("jpg", "jpeg", "png", 'bmp', 'webp'),accept_multiple_files = True)
        if clicked:
            #upsert_zip(0,conn,cur)
            root = tk.Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            dirname = str(filedialog.askdirectory(master=root))
            if dirname!='':
                #print(dirname)
                if '/' in dirname:
                    dirname = dirname.split('/')[-1]
                    listdirs = os.listdir(dirname)
                elif '\\' in dirname:
                    dirname = dirname.split('\\')[-1]
                    listdirs = os.listdir(dirname)


                for path in listdirs:
                    filename = os.path.join(dirname,path)
                    picture = PIL.Image.open(filename)                            #ЗАВТРА ПОЛЮБОМУ НАДО ДОРАБОТАТЬ
                    if custom_size:
                        auto_label(model,filename,confidence,dirname,predict)
                    else:
                        auto_label(model, filename, confidence, dirname)
                if '/' in dirname:
                    final_path = dirname.split('/')[-1]
                else:
                    final_path = dirname.split('\\')[-1]
                zip_button = create_download_zip(f"{final_path}_labels",f"{dirname}_labels",f"{final_path}_labels.zip")
     #   print(get_mode_zip(cur))
       # if len(get_mode_zip(cur))!=0 and get_mode_zip(cur)[0][1]:
                if zip_button:
                    #print('i here')
                    if os.path.isdir(f"{final_path}_labels"):
                        print(True)
                        os.remove(f"{final_path}_labels")

                    if os.path.isfile(f"{final_path}_labels.zip"):
                        print(True)
                        os.remove(f"{final_path}_labels.zip")
          #  upsert_zip(0,conn,cur)
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
                            if not custom_size:
                                res = model.predict(image,
                                                    conf=confidence
                                                    )
                            else:
                                res = model.predict(image,
                                                    conf=confidence,
                                                    imgsz = predict
                                                    )


                            boxes = res[0].boxes
                            res_plotted = res[0].plot()[:, :, ::-1]
                            st.image(res_plotted, caption='Detected Image',    # здесь код пока что чуть-чуть дурацкий, тут может быть ситуация
                                     use_column_width=True)                    # когда загружают одно или несколько фото

                            with st.expander("Detection Results"):
                                for box in boxes:
                                    st.write(box.xywhn)
                        del lst_of_imgs
                    except Exception as ex:
                        # st.write(ex)
                        st.error("No image is uploaded yet!")
                else:
                    try:
                        res = model.predict(uploaded_image,
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


        video_input(model,confidence,conn,cur)
        conn.close()
        #create_download_video('uploaded_data/filename.mp4')
        #create_download_zip('archiv','uploaded_data/archiv')


if selected == "Download Video":
    try:
        lst_videos = list(map(lambda x:x[1],get_video_state_by_name(cur)))
        #print(lst_videos)
        option = st.selectbox(
            "How would you like to be contacted?",
            lst_videos)
        #print(option)
        st.write("You selected:", option)
        button_video = create_download_video(f'videos/{option}',option)
        del_video_button = st.button('Delete this video')
        if button_video:
            #print(f"videos/{option.replace('_detected.avi', '.mp4')}")
            if os.path.isfile(f"{os.path.join('videos',option.replace('_detected.avi','.mp4'))}"):
               # print(f"videos/{option.replace('_detected.avi','.mp4')}")
                os.remove(f"{os.path.join('videos',option.replace('_detected.avi','.mp4'))}")
        if del_video_button:
            if os.path.isfile(f"{os.path.join('videos',option.replace('_detected.avi','.mp4'))}"):
               # print(f"videos/{option.replace('_detected.avi','.mp4')}")
                os.remove(f"{os.path.join('videos',option.replace('_detected.avi','.mp4'))}")
            if os.path.isfile(f"{os.path.join('videos', option)}"):
                # print(f"videos/{option.replace('_detected.avi','.mp4')}")
                os.remove(f"{os.path.join('videos', option)}")
            delete_video_state_by_name(option,conn,cur)





    except:
        st.error("You didn't detect anything")
        del_video_button = st.button('Delete this name')
        if del_video_button:
            if option is not None:
                if os.path.isfile(f"{os.path.join('videos',option.replace('_detected.avi','.mp4'))}"):
                   # print(f"videos/{option.replace('_detected.avi','.mp4')}")
                    os.remove(f"{os.path.join('videos',option.replace('_detected.avi','.mp4'))}")
                    delete_video_state_by_name(option, conn, cur)
            else:
                st.write("You didn't have anything")