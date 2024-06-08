from datetime import datetime
import pandas
import cv2
import numpy as np
import streamlit as st
#import tensorflow as tf
import shutil
from collections import deque






def create_download_video(path):
    with open(path, 'rb') as video:
        btn = st.download_button(
            label="Download video",
            data=video,
            file_name="detected.mp4",
            mime='video/mp4'
        )

def click():
    print('click')


def create_download_zip(zip_directory,zip_path,filename='myzip.zip'):
    shutil.make_archive(zip_path, 'zip', zip_directory)
    with open("uploaded_data/archiv.zip", "rb") as fp:
        btn = st.download_button(
            label="Download ZIP",
            data=fp,
            on_click=click(),
            file_name=filename,
            mime="application/zip",
            key='button_zip'
        )



def crop(image,name=None):
    if name=='tl':
        image_top_left = image[:image.shape[0] // 2, :image.shape[1] // 2]
        return image_top_left
    elif name=='tr':
        image_top_right = image[:image.shape[0] // 2, image.shape[1] // 2:]
        return image_top_right
    elif name == 'bl':
        image_bottom_left = image[image.shape[0] // 2:, :image.shape[1] // 2]
        return image_bottom_left
    elif name == 'br':

        image_bottom_right = image[image.shape[0] // 2:, image.shape[1] // 2:]
        return image_bottom_right



volume = 0

def video_input(model_gun,confidence):

    vid_file = None
    k = 0
    vid_bytes = st.sidebar.file_uploader("Upload a video", type=['mp4', 'mpv', 'avi'])
    if vid_bytes:
        vid_file = "uploaded_data/upload." + vid_bytes.name.split('.')[-1]
        with open(vid_file, 'wb') as out:
            out.write(vid_bytes.read())
    if vid_file:
        result = cv2.VideoWriter('uploaded_data/filename.avi',
                                 cv2.VideoWriter_fourcc(*'MJPG'),
                                 30, (416, 416))

        cap = cv2.VideoCapture(vid_file)
        len_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(len_of_frames)
        progress = st.progress(0,text = "Operation in progress. Please wait.")
        status_text=st.empty()
        custom_size = st.sidebar.checkbox("Custom frame size")
        # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if custom_size:
            width = st.sidebar.number_input("Width", min_value=120, step=20, value=420)
            height = st.sidebar.number_input("Height", min_value=120, step=20, value=420)
            predict = st.sidebar.number_input("Predict", min_value=120, step=20, value=420)



        st.markdown("---")



        count = 0  # Задаем количество выведенных фотографий
        now = datetime.now()  # Задаем точное время и дату

        global volume
        #global k

        st.title('Detected video')
        output = st.empty()
       # status_text = st.empty()
        #print(stop)
        perc = len_of_frames / 100
        i=1

        while True:


            ret, frame = cap.read()


            if not ret:
                result.release()
                st.write("Can't read frame, stream ended? Exiting ....")
                create_download_video('uploaded_data/filename.avi')
                break
            if not custom_size:
                frame = cv2.resize(frame, (416, 416))
                result_gun = model_gun.predict(frame, verbose=True, conf=confidence, imgsz=416,device = 0)
            else:
                frame = cv2.resize(frame, (width, height))
                result_gun = model_gun.predict(frame, verbose=True, conf=confidence, imgsz=predict)
            #result_gun = model_gun.predict(frame, verbose=True, conf=confidence, imgsz=416)
            k+=1
            fps = cap.get(cv2.CAP_PROP_FPS)
            boxes = result_gun[0].boxes
            frame1=result_gun[0].plot()
            result.write(frame1)
            print(k,i*perc,i)
            if k> i*perc:
                progress.progress(i-1,text="Operation in progress. Please wait.")
                status_text.text(f'Progress: {i}')
                i+=1


            if len(boxes.cls.cpu().numpy()) != 0:
                frame = result_gun[0].plot()
                # x, y, w, h = boxes.cpu().numpy().xywh[0].tolist()
                #
                #
                # if x < frame.shape[1] // 2 and y < frame.shape[0] // 2:
                #     frame = crop(frame, 'tl')
                # elif x > frame.shape[1] // 2 and y < frame.shape[0] // 2:
                #     frame = crop(frame, 'tr')
                # elif x < frame.shape[1] // 2 and y > frame.shape[0] // 2:
                #     frame = crop(frame, 'bl')
                # elif x > frame.shape[1] // 2 and y > frame.shape[0] // 2:
                #     frame = crop(frame, 'br')
                # # frame=cv2.resize(frame,(1280,1080),interpolation=cv2.INTER_CUBIC)
                # result1 = model_gun.predict(frame, conf=0.5, imgsz=1280)
                # frame = result1[0].plot()
                output.image(frame)





                volume += np.e ** (fps / 30)
                if volume > 6:

                        # result = model.predict(source=frame, persist=True, conf=0.7, imgsz=416)

                        # result_pose = model_pose.predict(source=frame, conf=0.7, imgsz=416)

                    if count <5:
                        now = datetime.now()
                        st.title(':blue[Обратите внимание !]')
                        st.error(f'Warning {now}')  # выводим уведомление
                        # st.image(frame)  # Выводим картинку

                            #st.download_button('coordinates_' + str(count), line, file_name='coordinates_' + str(count)+'.txt')
                        

                        count += 1  # увеличиваем счетчик

                  # считаем разницу между "сейчас" и предыдущим временем
                    else:
                        delta = datetime.now() - now
                        if delta.seconds > 5:  # если прошло больше 5 секунд
                            now = datetime.now()  # обновляем дату и счетчик
                            count = 0

                if volume > 7:
                    volume = 6.5
            else:
                output.image(frame)
                volume -= 0.2
                if volume < 0:
                    volume = 0
        progress.empty()
        status_text.empty()
     #   k=0