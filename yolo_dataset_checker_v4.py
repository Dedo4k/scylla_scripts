# -*- coding: utf-8 -*-
""" Created on Thu Jun 28 18:23:47 2018

a routine to check files marked up for YOLO

* lowercases the extension JPG->jpg, PNG -> png 
* chackes if xml is proper and the labels are one of the predefined list
* checks for dublicates
* checkes xml-img couple
* checks and corrects image type-extension missmatches (jpeg formats changed to jpegs )
* checks for <xmin> field in XML (error happens if bounding box is deleted, XML stays, but empty) 
* checks the filename for spaces and brackets and replaces with underscore & XML

@author: Ara
"""
import tqdm
import os
# import xml.etree.ElementTree
from xml.etree import ElementTree as et
import shutil
from lxml import etree
from io import StringIO
import sys
from glob import glob
# import imghdr

from skimage import io


def verify_image(img_file):
    try:
        img = io.imread(img_file)
    except:
        return False
    return True


bad_classes = ['sniper']


# PATH = 'D:\\PYTHON\\SCYLLA_DATASET\\ALL\\test' #input folder


def ask_user():
    # check = input("Do you want to delete the files with issues? (y/n): ")
    check = str(input("Do you want to delete the files with issues? (Y/N): ")).lower().strip()
    try:
        if check == 'y':
            return True
        elif check == 'n':
            return False
        else:
            print('Invalid Input')
            return ask_user()
    except Exception as error:
        print("Please enter valid inputs")
        print(error)
        return ask_user()


if len(sys.argv) <= 1:
    import inspect

    directory_in_str = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
else:
    directory_in_str = sys.argv[1]

predlabels = ['car', 'person', 'truck', 'bus', 'motorcycle', 'bicycle', 'hhelmet', 'pizza', 'helmet', 'rifle', 'van', 'pickup']

print('Checking Yolo sets recursively in ' + directory_in_str)


def labelextract(filepath):  # parse and return all labels in xml file
    weaponclasses = []
    with open(filepath, 'r') as xml_file:
        xml_to_check = xml_file.read()
    try:
        doc = etree.parse(StringIO(xml_to_check))
        for objct in doc.findall('object'):
            classs = objct.find('name').text
            weaponclasses.append(classs)
    except IOError:
        print('Invalid File: ' + filepath)
    except etree.XMLSyntaxError as err:
        print('XML Syntax Error in file ' + filepath)
    except:
        print(filepath)

    for w in weaponclasses:
        if w not in predlabels:
            return 'mistake'
        if w in bad_classes:
            return w

    return False


def movetofolder(file, directory, label):
    imagetypes = ('.jpg', '.png', '.jpeg', '.PNG', '.JPEG', '.JPG')

    filename, file_extension = os.path.splitext(os.path.basename(file))

    dirpath = directory + os.sep + label
    destfile = dirpath + os.sep + filename + file_extension
    destimage = dirpath + os.sep + filename
    # create folder  os.sep
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
        print('New markup class found: ' + label)
    for imtype in imagetypes:
        imgfile = os.path.join(directory, directory_in_str, filename + imtype)
        if os.path.exists(imgfile):
            os.rename(imgfile, destimage + imtype.lower())
            break

    os.rename(file, destfile)


def move_to_folder(file, dirname, folder):
    imagetypes = ('.xml', '.jpg', '.png', '.jpeg', '.PNG', '.JPEG', '.JPG')
    dirname = os.path.join(dirname, folder)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    for exte in imagetypes:
        try:
            f_file = file.split('.')[0] + exte
            shutil.move(f_file, dirname)
            print('File ' + f_file + ' moved to ' + dirname)
        except shutil.SameFileError:
            print('File ' + f_file + 'already exists in ' + dirname)
        except FileNotFoundError:
            print(end='')
        except Exception:
            print(end='')


print('Sorting Yolo sets recursively in ' + directory_in_str)

result = [y for x in os.walk(directory_in_str) for y in glob(os.path.join(x[0], '*.xml'))]  # Search for all .xml files
for files in result:
    filename, file_extension = os.path.splitext(os.path.basename(files))
    is_mistake = labelextract(files)

    if is_mistake:
        if is_mistake == 'mistake':
            movetofolder(files, directory_in_str, 'mistake')
        else:
            movetofolder(files, directory_in_str, is_mistake)

i = 0
files2delete = []
extensions = ['.xml', '.png', '.jpg', '.jpeg']
errfiles = 'Errors found in files :' + '\n'
wronglabels = '\n' + 'Wrong labels found in files :' + '\n'
dublicatefls = '\n' + 'files with dublicate names :' + '\n'
wrongtypefls = '\n' + 'files with image type mismatch :' + '\n'
curruptFls = '\n' + 'files with unknown image types :' + '\n'
XMLFilenameMismatch = '\n' + 'Filename in XML mismatch in  :' + '\n'

print('\n\n   lowercasing UPPERCASE extensions: ')

result = [y for x in os.walk(directory_in_str) for y in glob(os.path.join(x[0], '*.*'))]  # Search for all mp4 files
for files in result:
    filename, file_extension = os.path.splitext(os.path.basename(files))
    file_extension = file_extension[1:]
    if file_extension in ('JPEG', 'JPG', 'PNG'):
        ext = file_extension.lower()
        xmlfile = os.path.dirname(files) + os.sep + filename + '.xml'
        if os.path.isfile(xmlfile):
            tree = et.parse(xmlfile)
            tree.find('filename').text = filename + '.' + ext
            tree.write(xmlfile)
        shutil.move(files, os.path.dirname(files) + os.sep + filename + '.' + ext)  # rename
        print('Changed to ' + filename + '.' + ext)
        i += 1

files2delete = []

print('\n   Missing images')

result = [y for x in os.walk(directory_in_str) for y in glob(os.path.join(x[0], '*.xml'))]  # Search for all mp4 files
for files in result:
    filename, file_extension = os.path.splitext(os.path.basename(files))
    pngname = os.path.dirname(files) + os.sep + filename + '.png'
    jpgname = os.path.dirname(files) + os.sep + filename + '.jpg'
    jpegname = os.path.dirname(files) + os.sep + filename + '.jpeg'
    if not os.path.isfile(pngname) and not os.path.isfile(jpgname) and not os.path.isfile(jpegname):
        files2delete.append(files)
        print(filename + file_extension)

print('\n   Missing XMLs')

result = []
for ext in ('*.png', '*.jpg', '*.jpeg'):
    result.extend([y for x in os.walk(directory_in_str) for y in glob(os.path.join(x[0], ext))])

for files in result:
    filename, file_extension = os.path.splitext(os.path.basename(files))
    xmlname = os.path.dirname(files) + os.sep + filename + '.xml'
    if not os.path.isfile(xmlname):
        files2delete.append(files)
        print(filename + file_extension)

# supplement files2delete with relevant pair
if len(files2delete):
    for files in files2delete:
        for exts in extensions:
            filename, file_extension = os.path.splitext(files)
            newfiles = filename + exts
            if not newfiles in files2delete:
                files2delete.append(newfiles)

# Prompt for and delete files with mistakes found
if len(files2delete):
    if ask_user():
        print('DELETING:')
        for files in files2delete:
            if os.path.isfile(files):
                os.remove(files)
                print(files)

files2delete = []
# checks XML ingerity and label consistency (existance of xmin value)
print('\n   Checking XML ingerity and label consistency    ******************************** ')
result = [y for x in os.walk(directory_in_str) for y in glob(os.path.join(x[0], '*.xml'))]  # Search for all mp4 files
for files in result:
    filename, file_extension = os.path.splitext(os.path.basename(files))
    xmin = -1
    with open(files, 'r') as xml_file:
        xml_to_check = xml_file.read()
    try:
        doc = etree.parse(StringIO(xml_to_check))
        obj = doc.findall('object')
        bnd = obj[0].findall('bndbox')
        xm = bnd[0].findall('xmin')
        xmin = int(xm[0].text)
        for objct in doc.findall('object'):
            classs = objct.findall('name')
            for classnames in classs:
                if not classnames.text in predlabels:
                    print('Wrong label ' + classs.text + ' in ' + os.path.basename(files))
                    wronglabels = wronglabels + files + '\n'
                    i += 1

            if int(objct.find('./bndbox/xmax').text) - int(objct.find('./bndbox/xmin').text) <= 5 or \
                    int(objct.find('./bndbox/ymax').text) - int(objct.find('./bndbox/ymin').text) <= 5:
                wronglabels = wronglabels + files + '\n'
                print('Coordinates to small in ' + files)
                move_to_folder(files, directory_in_str, '2small')
                i += 1

    # checks if the name in XML corresponds to the filename
    # xmlFlname = os.path.basename(doc.find('filename').text)
    # imagefilepath = os.path.dirname(files) + os.sep + xmlFlname
    # if not os.path.isfile(imagefilepath):
    #     XMLFilenameMismatch =  XMLFilenameMismatch + files + '\n'
    #     print ('Filename in XML missmatch in ' + os.path.basename(files))
    #   #  files2delete.append(files)
    #   i +=1

    except IOError:
        print('Invalid File')
        errfiles = errfiles + files + '\n'
        i += 1
    except etree.XMLSyntaxError as err:
        print('XML Syntax Error in file ' + os.path.basename(files) + ', see error_syntax.log')
        errfiles = errfiles + files + '\n'
        i += 1
    except:
        errfiles = errfiles + files + '\n'
    if int(xmin) < 0:
        wronglabels = wronglabels + files + '\n'
        print('Coordinates missing in ' + filename)
        files2delete.append(files)
        i += 1


print('\n   Checking Image integrity ')

result = [y for x in os.walk(directory_in_str) for y in glob(os.path.join(x[0], '*.*'))]  # Search for all mp4 files
for files in tqdm.tqdm(result):
    filename, file_extension = os.path.splitext(os.path.basename(files))
    file_extension = file_extension[1:]
    if file_extension in ['jpeg', 'jpg', 'png']:
        if not verify_image(files):
            xmlname = os.path.dirname(files) + os.sep + filename + '.xml'
            files2delete.append(files)
            files2delete.append(xmlname)
            print("corrupted file:" + filename + "." + file_extension)

if len(files2delete):
    if ask_user():
        print('DELETING:')
        for files in files2delete:
            if os.path.isfile(files):
                os.remove(files)
                print(files)

print('\n   Image integrity is finished')
# finds dublicate files (by name)
# print ('\n   Looking for Dublicates  ********************************' )
# justname = []
# for subdir, dirs, files in os.walk(directory_in_str):
#     for fls in files:
#         filepath = subdir + os.sep + fls
#         if filepath.endswith(".jpg") or filepath.endswith(".jpeg") or filepath.endswith(".png"):
#             currentname = os.path.splitext(fls)[0]
#             if currentname in justname and (currentname[0:4]!='viol'):
#                 dublicatefls = dublicatefls + filepath + '\n' 
#                 print (fls)
#                 files2delete.append(filepath)
#                 i +=1
#             else: 
#                 justname.append(os.path.basename(currentname))

# Chekcs if the file extension corresponds to file type. 
# Corrects jpeg-jpg inconsistency by rename and XML change               
# print ('\n   Looking for unknown or missmutched image types  ********************************')
# result=[]
# for ext in ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif'):
#     result.extend([y for x in os.walk(directory_in_str) for y in glob(os.path.join(x[0], ext))]) 

# for files in result: 
#     filename, file_extension = os.path.splitext(os.path.basename(files))    
#     file_extension = file_extension[1:]
#     if file_extension == 'gif' or file_extension=='bmp' :
#         files2delete.append(files)
#         curruptFls = curruptFls + files + '\n'
#         print ('unwanted file ' + os.path.basename(files))
#         i +=1
#     if file_extension == 'jpeg':
#         xmlfile = os.path.dirname(files) + os.sep + filename + '.xml'
#         if os.path.isfile(xmlfile): 
#             tree = et.parse(xmlfile)
#             tree.find('filename').text =  filename + '.jpg'
#             tree.write(xmlfile)
#         shutil.move(files, os.path.dirname(files) + os.sep + filename + '.jpg') #rename 
#     else:
#         imageTyp= imghdr.what(files)
#         if imageTyp == None :
#             files2delete.append(files)
#             curruptFls = curruptFls + files + '\n'
#             print ('unknown image type: ' + os.path.basename(files))

#             i +=1
#         else:
#             if not imageTyp == file_extension:# and (imageTyp =='png' or file_extension =='png'):
#                 print (imageTyp + ' is not ' + file_extension)
#                 if imageTyp=='jpeg' or imageTyp=='JPEG'  or imageTyp=='JPG'  or imageTyp=='jpg': 
#                     xmlfile = os.path.dirname(files) + os.sep + filename + '.xml'
#                     if os.path.isfile(xmlfile): 
#                         tree = et.parse(xmlfile)
#                         tree.find('filename').text =  filename + '.jpg'
#                         tree.write(xmlfile)
#                     shutil.move(files, os.path.dirname(files) + os.sep + filename + '.jpg') #rename 
#                     print('Changed to ' + os.path.dirname(files) + os.sep + filename + '.jpg')
#                 if imageTyp=='PNG'  or imageTyp=='png': 
#                     xmlfile = os.path.dirname(files) + os.sep + filename + '.xml'
#                     if os.path.isfile(xmlfile): 
#                         tree = et.parse(xmlfile)
#                         tree.find('filename').text =  filename + '.png'
#                         tree.write(xmlfile)
#                     shutil.move(files, os.path.dirname(files) + os.sep + filename + '.png') #rename 
#                     print('Changed to ' + os.path.dirname(files) + os.sep + filename + '.png')
#                 wrongtypefls = wrongtypefls + filepath + '\n'
#                 i +=1

# supplement files2delete with relevant pair
extensions = ['.xml', '.png', '.jpg', '.jpeg']
if len(files2delete):
    for files in files2delete:
        for exts in extensions:
            filename, file_extension = os.path.splitext(files)
            newfiles = filename + exts
            if not newfiles in files2delete:
                files2delete.append(newfiles)

# Prompt for and delete files with mistakes found
if len(files2delete):
    if ask_user():
        print('DELETING:')
        for files in files2delete:
            if os.path.isfile(files):
                os.remove(files)
                print(files)

print('\n   Moderating filenames  "("," ",")" -> "_","_","_" ********************************')

result = []
for ext in ('*.png', '*.jpg', '*.jpeg'):
    result.extend([y for x in os.walk(directory_in_str) for y in glob(os.path.join(x[0], ext))])

for files in result:
    filename, file_extension = os.path.splitext(os.path.basename(files))

    f1 = filename.replace("(", "_")
    f1 = f1.replace(" ", "_")
    f1 = f1.replace("[", "_")
    f1 = f1.replace("]", "_")
    f1 = f1.replace(")", "_")
    f1 = f1.replace("-", "_")
    f1 = f1.replace(".", "_")
    f1 = f1.replace(",", "_")
    f1 = f1.replace("____", "_")
    f1 = f1.replace("___", "_")
    f1 = f1.replace("__", "_")

    if f1[-1] == "_":
        f1 = f1[:-1]
    if f1[0] == "_":
        f1 = f1[1:]
    if not filename == f1:  # and (imageTyp =='png' or file_extension =='png'):
        print(filename)
        shutil.move(files, os.path.dirname(files) + os.sep + f1 + file_extension)
        if os.path.isfile(os.path.dirname(files) + os.sep + filename + '.xml'):
            xmlfile = os.path.dirname(files) + os.sep + f1 + '.xml'
            shutil.move(os.path.dirname(files) + os.sep + filename + '.xml', xmlfile)

            tree = et.parse(xmlfile)
            tree.find('filename').text = f1 + file_extension
            tree.write(xmlfile)
        # wrongtypefls = wrongtypefls + filepath + '\n'
        i += 1

# writing log of errors in error file 

# with open('error_syntax.log', 'w') as error_log_file:
#    error_log_file.write(errfiles + wronglabels + dublicatefls + wrongtypefls + curruptFls + XMLFilenameMismatch)

print('\n    Mistakes found: ' + str(i))

print('done!')
r = input('Press ENTER to continue')
