import pandas
from ultralytics import YOLO
import cv2
import streamlit as st
from utils import video_input,create_download_video,create_download_zip
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from streamlit_option_menu import option_menu
import pandas as pd
import PIL
import os
from clever_label import auto_label
from utils import create_db_state,get_video_state_by_name,delete_video_state_by_name


conn, cur = create_db_state()

model = YOLO('best_all_v9_40epoch.pt')


st.set_page_config(page_title="EvilNet search for drones", page_icon=":small_airplane:", layout="wide",
                   initial_sidebar_state="expanded")

# side bar
st.sidebar.image("img/EvilNET_logo.jpg", caption="Search for drones")

with st.sidebar:
    selected = option_menu("", ["Monitoring", "---", "File mode","Download Video","Devices"],
                           icons=['display', '','images' , 'download', 'database-fill'], menu_icon="cast",
                           default_index=0
                           )


# Main Page Monitoring
st.header("Flying objects detection")
if selected == "Monitoring":
    stream_on_off = st.checkbox('On/off camera streaming')
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


        image_vid_1 = Image.open('img/pribor96_hubsan_zino_pro_2.jpg')
        st.image(image_vid_1)
    with col2:

        image_vid_2 = Image.open('img/helicopter.jpg')
        st.image(image_vid_2)
    with col3:

        image_vid_3 = Image.open('img/plain.jpg')
        st.image(image_vid_3)

    st.divider()


if selected == "Devices":
    with st.container():
        col1, col2, col3 = st.columns(3)
    with col1:
        name_camera = st.text_input("Camera name",)
    with col2:
        name_ip = st.text_input("IP address",)
    with col3:
        add_camera = st.button('Add camera', type='primary')
        del_camera = st.button('Remove camera')


    st.subheader(":movie_camera: Cameras")
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
            st.error('Fill in the missing fields')
    if del_camera:

        if name_ip and name_camera:

            df=df[(df['Название'] != name_camera) & (df['IP адрес'] != name_ip)]
            df.to_csv('list_of_camera.csv')
        else:
            st.error('Fill in the missing fields')







    st.table(df)



# File mode
if selected == "File mode":

    confidence = float(st.sidebar.slider("Select Model Confidence", 25, 100, 40)) / 100
    st.subheader('File mode')
    st.info('Here you can upload single image / images folder / video for detection')

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
            "Choose images...", type=("jpg", "jpeg", "png", 'bmp', 'webp'),accept_multiple_files = True)
        if clicked:

            root = tk.Tk()
            root.withdraw()
            root.wm_attributes('-topmost', 1)
            dirname = str(filedialog.askdirectory(master=root))
            if dirname!='':

                if '/' in dirname:
                    dirname = dirname.split('/')[-1]
                    listdirs = os.listdir(dirname)
                elif '\\' in dirname:
                    dirname = dirname.split('\\')[-1]
                    listdirs = os.listdir(dirname)


                for path in listdirs:
                    filename = os.path.join(dirname,path)
                    picture = PIL.Image.open(filename)
                    if custom_size:
                        auto_label(model,filename,confidence,dirname,predict)
                    else:
                        auto_label(model, filename, confidence, dirname)
                if '/' in dirname:
                    final_path = dirname.split('/')[-1]
                else:
                    final_path = dirname.split('\\')[-1]
                zip_button = create_download_zip(f"{final_path}_labels",f"{dirname}_labels",f"{final_path}_labels.zip")
                if zip_button:

                    if os.path.isdir(f"{final_path}_labels"):

                        os.remove(f"{final_path}_labels")

                    if os.path.isfile(f"{final_path}_labels.zip"):

                        os.remove(f"{final_path}_labels.zip")

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

            if st.sidebar.button('Detect Objects', type='primary'):
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
                            st.image(res_plotted, caption='Detected Image',
                                     use_column_width=True)

                            with st.expander("Detection Results"):
                                for box in boxes:
                                    st.write(box.xywhn)
                        del lst_of_imgs
                    except Exception as ex:

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

                        st.error("No image is uploaded yet!")


    elif source_radio == 'Video':


        video_input(model,confidence,conn,cur)
        conn.close()



if selected == "Download Video":
    try:
        lst_videos = list(map(lambda x:x[1],get_video_state_by_name(cur)))

        option = st.selectbox(
            "How would you like to be contacted?",
            lst_videos)

        st.write("You selected:", option)
        button_video = create_download_video(f'videos/{option}',option)
        del_video_button = st.button('Delete this video')
        if button_video:

            if os.path.isfile(f"{os.path.join('videos',option.replace('_detected.avi','.mp4'))}"):

                os.remove(f"{os.path.join('videos',option.replace('_detected.avi','.mp4'))}")
        if del_video_button:
            if os.path.isfile(f"{os.path.join('videos',option.replace('_detected.avi','.mp4'))}"):

                os.remove(f"{os.path.join('videos',option.replace('_detected.avi','.mp4'))}")
            if os.path.isfile(f"{os.path.join('videos', option)}"):

                os.remove(f"{os.path.join('videos', option)}")
            delete_video_state_by_name(option,conn,cur)
            conn.close()




    except:
        st.error("You didn't detect anything")
        del_video_button = st.button('Delete this name')
        if del_video_button:
            if option is not None:
                if os.path.isfile(f"{os.path.join('videos',option.replace('_detected.avi','.mp4'))}"):

                    os.remove(f"{os.path.join('videos',option.replace('_detected.avi','.mp4'))}")
                delete_video_state_by_name(option, conn, cur)
                conn.close()
            else:
                st.write("You didn't have anything")