import shutil
import os

import cv2
from ultralytics import YOLO

model = YOLO('yolov9c.pt')
def auto_label(model,path_from,conf,dir_name,predict = None):
  if not os.path.isdir(f'{dir_name}_labels'):
      os.mkdir(f"{dir_name}_labels")
  if not predict:
    res = model(path_from,conf = conf/100)
  else:
      res = model(path_from,conf = conf/100,imgsz = predict)
  st=''

  boxes=res[0].boxes

  name_file=path_from.replace('.jpg','.txt')


  if len(boxes.cls.cpu().numpy())!=0:
    for i in range(len(boxes.cls.cpu().numpy())):
      if boxes.conf.cpu().numpy()[i]*100 > conf:

        for j in boxes.cpu().numpy().xywhn[i]:
          if j >1:
            j=0.990000
            st+=(str(int(boxes.cls.cpu().numpy()[i])) + ' ' + str(round(j,5)))
          else:
            st+=(str(int(boxes.cls.cpu().numpy()[i])) + ' ' + str(round(j,5)))



        st+='\n'



  print(name_file)
  if len(st)!=0:
      st=st[:-1]
      text_file = open(os.path.join(dir_name+"_labels",name_file.split("\\")[-1]), "w")

      text_file.write(st)

      text_file.close()

  else:
      text_file = open(os.path.join(dir_name+"_labels",name_file.split("\\")[-1]), "w")

      text_file.write(st)

      text_file.close()



if __name__ == '__main__':
    FOLDER_PATH = 'frames/images_fly'
    lst_of_link=os.listdir(FOLDER_PATH)
   # lst_of_link=[i for i in lst_of_link if i!='.ipynb_checkpoints'] #только для колаба
    for path in lst_of_link:
      name=os.path.join(FOLDER_PATH,path)#
      print(name)
      auto_label(model,name,'frames',35)
    #print(lst_of_link)