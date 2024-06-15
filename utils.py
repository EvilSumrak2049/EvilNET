import os
from datetime import datetime
import pandas
import cv2
import numpy as np
import streamlit as st
#import tensorflow as tf
import shutil
from collections import deque
import sqlite3


def create_db_state():
    conn = sqlite3.connect('videos.db')
    cur = conn.cursor()

    # Создаем таблицу video_state
    cur.execute('''
    CREATE TABLE IF NOT EXISTS video (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    )
    ''')
    return conn,cur

def upsert_video_state(name,conn,cur):
    cur.execute('''
    INSERT INTO video (name)
    VALUES (?)
    ON CONFLICT(name) DO UPDATE SET
    name = excluded.name
    ''', (name,))
    conn.commit()


def get_video_state_by_name(cur):
    cur.execute('SELECT * FROM video')
    return cur.fetchall()



def create_download_video(path,filename = 'detected.mp4'):
    with open(path, 'rb') as video:
        btn = st.download_button(
            label="Download this video",
            data=video,
            file_name=filename,
            mime='video/mp4'
        )
    return btn

def click():
    print('click')


def create_download_zip(name_out,zip_path,filename='myzip.zip'):
    shutil.make_archive(name_out, 'zip', zip_path)
    with open(f"{name_out}.zip", "rb") as fp:
        btn = st.download_button(
            label="Download ZIP",
            data=fp,
            on_click=click(),
            file_name=filename,
            mime="application/zip",
            key='button_zip'
        )
    return btn



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
dct={'video':True}
def video_input(model_gun,confidence,conn,cur):

    vid_file = None
    button_video = False

    k = 0
    vid_bytes = st.sidebar.file_uploader("Upload a video", type=['mp4', 'mpv', 'avi'])
    if vid_bytes:
        #print(vid_bytes.name)
        #vid_file = "uploaded_data/upload." + vid_bytes.name.split('.')[-1]
        vid_file = "videos/" + vid_bytes.name
        print(vid_file)
        with open(vid_file, 'wb') as out:
            out.write(vid_bytes.read())
    if vid_file:
        vid_file_detected = vid_file[:-4]+'_detected.avi'
        print(f'{vid_file[:-4]}_detected.avi')
        result = cv2.VideoWriter(vid_file_detected,
                                 cv2.VideoWriter_fourcc(*'MJPG'),
                                 30, (640, 640))

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
                upsert_video_state(vid_file_detected.split('/')[-1],conn,cur)
                # button_video = create_download_video(f'uploaded_data/filename.avi')
                # if button_video:
                #     os.remove(f'{vid_file[:-4]}_detected.avi')
                #     os.remove(vid_file)
                break
            if not custom_size:
                frame = cv2.resize(frame, (640, 640))
                result_gun = model_gun.predict(frame, verbose=False, conf=confidence, imgsz=416,device = 0)
            else:
                frame = cv2.resize(frame, (width, height))
                result_gun = model_gun.predict(frame, verbose=False, conf=confidence, imgsz=predict)
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