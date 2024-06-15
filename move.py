#ФУНКЦИЯ ПЕРЕМЕЩЕНИЯ КЛАССА
import shutil
import os
def move_class(path,path_to,num):
  move = False
  f = open(path,'r')
  lines = f.readlines()
  if len(lines)!=0:
    for line in lines:
      if line[0]==str(num):
        move = True
        break

  f.close()
  name_file = path.replace('.txt','.jpg').replace('labels','images')
  if move:
    shutil.move(path, path_to)
    shutil.move(name_file, path_to)



def move_all_class(path,path_to,num):
  for filename in os.listdir(path):
        f = os.path.join(path, filename)
        if os.path.isfile(f) :
          if filename.endswith('.txt'):
            move_class(f,path_to,num)

if __name__=="__main__":
  move_all_class('Airborne-Object-Detection-4-AOD4-6/test/labels','birds',1)