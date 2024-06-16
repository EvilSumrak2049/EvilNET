import os
from datetime import datetime
import pandas
import cv2
import numpy as np
import streamlit as st
#import tensorflow as tf
import shutil
import pandas as pd
from collections import deque
import sqlite3

config = {0:"copter",1:"plane",2:"helicopter",3:"bird",4:"drone"}

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


def delete_video_state_by_name(name,conn,cur):
    cur.execute('DELETE FROM video WHERE name = ?', (name,))
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
 #           on_click=upsert_zip('1',conn,cur),
            file_name=filename,
            mime="application/zip",
            key='button_zip'
        )
    return btn






volume = 0

def video_input(model,confidence,conn,cur):
    vid_file = None
    button_video = False
    custom_size = st.sidebar.checkbox("Custom frame size")
    if custom_size:
        predict = st.sidebar.number_input("Predict", min_value=120, step=20, value=480)
    k = 0
    vid_bytes = st.sidebar.file_uploader("Upload a video", type=['mp4', 'mpv', 'avi'])
    if vid_bytes:
        #print(vid_bytes.name)
        #vid_file = "uploaded_data/upload." + vid_bytes.name.split('.')[-1]
        if not os.path.isdir('videos'):
            os.mkdir('videos')
        vid_file = "videos/" + vid_bytes.name
        #print(vid_file)
        with open(vid_file, 'wb') as out:
            out.write(vid_bytes.read())
    if vid_file:
        vid_file_detected = vid_file[:-4]+'_detected.avi'
        #print(f'{vid_file[:-4]}_detected.avi')
        result = cv2.VideoWriter(vid_file_detected,
                                 cv2.VideoWriter_fourcc(*'MJPG'),
                                 30, (640, 640))

        cap = cv2.VideoCapture(vid_file)
        len_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        progress = st.progress(0,text = "Operation in progress. Please wait.")
        status_text=st.empty()






        st.markdown("---")



        count = 0  # Задаем количество выведенных фотографий
        now = datetime.now()  # Задаем точное время и дату

        global volume



        with st.container():
            col1, col2, = st.columns(2)
        col1.header("DETECT OBJECTS")
        col2.header(":blue[Обратите внимание !]")

        output = col1.empty()
        table = col2.empty()

        perc = len_of_frames / 100
        i=1
        df = pd.DataFrame()
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
                result_drone = model.predict(frame, verbose=False, conf=confidence, imgsz=640,device = 0)
            else:
                result_drone = model.predict(frame, verbose=False, conf=confidence, imgsz=predict,device = 0)

            k+=1
            fps = cap.get(cv2.CAP_PROP_FPS)
            boxes = result_drone[0].boxes
            frame1=result_drone[0].plot()
            result.write(frame1)

            if k> i*perc:
                progress.progress(i-1,text="Operation in progress. Please wait.")
                status_text.text(f'Progress: {i}')
                i+=1


            if len(boxes.cls.cpu().numpy()) != 0:

                frame = result_drone[0].plot()

                output.image(frame,channels="BGR")





                volume += np.e ** (fps / 30)
                if volume > 6:



                    if count <5:
                        now = datetime.now()

                        data = pd.DataFrame(data={'Объект': [*list(map(lambda x:config[x],boxes.cls.cpu().numpy()))], 'Дата фиксации': [*[now]*len(boxes.cls.cpu().numpy())]})
                        df = pandas.concat([data, df], axis=0, ignore_index=True)
                        table.table(df)

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
                output.image(frame,channels="BGR")
                volume -= 0.2
                if volume < 0:
                    volume = 0
        progress.empty()
        status_text.empty()
