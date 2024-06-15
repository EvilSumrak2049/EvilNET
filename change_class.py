import os


def change_class(path,num):

    f = open(path,'r')
    lines = f.readlines()
    s = ''
    if len(lines)!=0:
        for line in lines:
            if line[1].isdigit():
                line=str(num)+line[2:]
            else:
                line=str(num)+line[1:]


            print(line)
            s+=line

    f.close()

    # Открываем файл для записи
    save_changes = open(path, 'w')

    # Сохраняем список строк
    save_changes.writelines(s)

    # Закрываем файл
    save_changes.close()


def change_class_inside(path,num):
    for filename in os.listdir(path):
        f = os.path.join(path, filename)
        if os.path.isfile(f):
            if filename.endswith('.txt'):
                change_class(f,num)

if __name__=='__main__':
    change_class_inside('birds',0)