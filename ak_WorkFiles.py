import glob
import os
from pprint import pprint
from unittest import result

FileName = 'E:\Python\Projects\Site from description\**'
# for name in glob.glob(FileName):
#     print(name)

FileName = 'E:\\Python\\Projects\\Site from description\\test'

ListFilter = ['.JPEG', '.JPG', '.TXT']
FileDescription = '-Описание-.txt'.upper()

def FindFile(Path, Name):
    files = []
    d = {'Path':Path, 'Name': Name}
    dirs = os.listdir(Path)

    fileDescriptionExist = False
    InnerDirExist = False

    for file in dirs:
        FullPath = os.path.join(Path, file)
        if os.path.isdir(FullPath):
            result = FindFile(FullPath, file)
            if not result is None:
                InnerDirExist = True
                if 'Dirs' in d:
                    d['Dirs'].append(result)
                else:
                    d['Dirs'] = [result]
        else:
            if file.upper() == FileDescription:
                fileDescriptionExist = True
                d['FileDescription'] = FullPath
            else:
                ext = os.path.splitext(file)[1].upper()
                if ext in ListFilter:
                    files.append(file)

    if fileDescriptionExist or InnerDirExist:
        d['Files'] = files
        result = d
    else:
        result = None

    return result

def DeleteFiles(Path):
    '''Удалим все файлы в каталоге'''

    files = os.listdir(Path)

    fileDescriptionExist = False
    InnerDirExist = False

    for file in files:
        FullPath = os.path.join(Path, file)

        if os.path.isdir(FullPath):
            DeleteFiles(FullPath)
            os.rmdir(FullPath)
        else:
            os.remove(FullPath)

def MakeHTMLFileName(Path, Name):
    '''Создадим путь к HTML файлу'''
    if Path == '':
        result = '{0}.html'.format(Name)
    else:
        result = os.path.join(Path, '{0}.html'.format(Name))

    return result

def LinkToHTMLFile(FileName):
    '''Создает ссылку на html файл на диске
    Пример:
    FileName: C:\www\localsite\Исследование\3-Отладка.html
    Результат: file:///C:\www\localsite\Исследование\3-Отладка.html
    '''

    return 'file:///' + FileName.replace('\\\\', '\\')

def isLinckFile(FileName):
    '''Проверим является ли ссылка файлом'''

    return FileName[1] == ':'

def GetParamFileFromPath(FullPathToFile):
    '''Получим параметры файла из пути:
    Путь к файлу
    Имя файла
    Расширение'''

    ls = FullPathToFile.split(sep='\\')

    Name = ''
    Exception = ''
    FileName = ''
    PathToFile = ''

    if 1 < len(ls):
        FileName = ls[-1]

        lsFileName = FileName.split(sep='.')

        if len(lsFileName) == 1:
            Name = FileName
        else:
            Exception = lsFileName[-1]
            del(lsFileName[-1])
            Name = '.'.join(lsFileName)

        del(ls[-1])

        PathToFile = '\\'.join(ls)

    result = {'Name': Name,
            'Exception': Exception,
            'FileName': FileName,
            'PathToFile': PathToFile}

    return result

# pprint(FindFile(FileName, 'site'))

if __name__ == '__main__':
    Path = 'E:\\Python\\Projects\\Site from description\\site'
    DeleteFiles(Path)



