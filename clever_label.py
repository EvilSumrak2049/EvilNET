import shutil
import os

import cv2
from ultralytics import YOLO

model = YOLO('yolov9c.pt')
def auto_label(model,path_from,conf,dir_name):
  if not os.path.isdir(f'{dir_name}_labels'):
      os.mkdir(f"{dir_name}_labels")
  res = model(path_from,conf = conf/100)
  st=''
  #st_conf=''
  boxes=res[0].boxes
  #res = model(path_from)
 # res_plotted = res[0].plot()
  name_file=path_from.replace('.jpg','.txt')#.split('.')[0] + '.txt'
  #text_file = open(name_file, "w")
  name_file_conf = name_file+'_conf'+'.txt'
  #text_file_conf=open(name_file_conf, "w")
  if len(boxes.cls.cpu().numpy())!=0:
    for i in range(len(boxes.cls.cpu().numpy())):
      if boxes.conf.cpu().numpy()[i]*100 > conf:
       # if boxes.cls.cpu().numpy()[i] == 4:
        for j in boxes.cpu().numpy().xywhn[i]:
          if j >1:
            j=0.990000
            st+=(str(int(boxes.cls.cpu().numpy()[i])) + ' ' + str(round(j,5)))
          else:
            st+=(str(int(boxes.cls.cpu().numpy()[i])) + ' ' + str(round(j,5)))

            #text_file.write(str(int(boxes.cls.numpy()[i])) + ' ' + str(j))
        #st_conf+=(str(boxes.conf.cpu().numpy()[i]*100)+' ')
        st+='\n'
        #text_file_conf.write(str(boxes.conf.numpy()[i]*100)+' ')
        #text_file.write('\n')

        #text_file.close()
        #text_file_conf.close()
  print(name_file)
  if len(st)!=0:
      st=st[:-1]
      text_file = open(os.path.join(dir_name+"_labels",name_file.split("\\")[-1]), "w")
      #text_file_conf = open(name_file_conf, "w")
      text_file.write(st)
      #text_file_conf.write(st_conf)
      text_file.close()
      #text_file_conf.close()
      #shutil.move(path_from,path_to)
     # shutil.move(name_file,f"{dir_name}_labels")
    #  cv2.imwrite(f'{os.path.join(path_to,path_from.split("/")[-1])}',res_plotted)
      #shutil.move(name_file_conf,path_to)
  else:
      text_file = open(os.path.join(dir_name+"_labels",name_file.split("\\")[-1]), "w")
      # text_file_conf = open(name_file_conf, "w")
      text_file.write(st)
      # text_file_conf.write(st_conf)
      text_file.close()
      # text_file_conf.close()
      #shutil.move(path_from, path_to)
     # shutil.move(name_file, f"{dir_name}_labels")
      # shutil.move(name_file_conf,path_to)


if __name__ == '__main__':
    FOLDER_PATH = 'frames/images_fly'
    lst_of_link=os.listdir(FOLDER_PATH)
   # lst_of_link=[i for i in lst_of_link if i!='.ipynb_checkpoints'] #только для колаба
    for path in lst_of_link:
      name=os.path.join(FOLDER_PATH,path)#
      print(name)
      auto_label(model,name,'frames',35)
    #print(lst_of_link)