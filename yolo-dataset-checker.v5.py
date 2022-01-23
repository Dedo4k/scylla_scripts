import argparse
import os
import inspect
import shutil
import re
from glob import glob
from tqdm import tqdm
import cv2

try:
    from lxml import etree
except ImportError:
    print(end='')

pred_labels = ['car', 'person', 'truck', 'bus', 'motorcycle', 'bicycle', 'hhelmet', 'pizza', 'helmet', 'rifle', 'van', 'pickup']
bad_classes = ['sniper']


def ask_user():
    # check = input("Do you want to delete the files with issues? (y/n): ")
    check = str(input("\nDo you want to delete the files with issues? (Y/N): ")).lower().strip()
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


def check_image(image_file):
    try:
        image = cv2.imread(image_file)
        if image is not None:
            return True
        else:
            return False
    except Exception:
        print('Couldn\'t open image. File:', image_file)


def move_to_folder(file, dirname, folder):
    imagetypes = ('.xml', '.json', '.jpg', '.png', '.jpeg', '.PNG', '.JPEG', '.JPG')
    dirname = os.path.join(dirname, folder)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    for exte in imagetypes:
        try:
            f_file = file.split('.')[0] + exte
            shutil.move(f_file, dirname)
#            print('\tFile ' + f_file + ' moved to ' + dirname)
        except shutil.SameFileError:
            print('\tFile ' + f_file + 'already exists in ' + dirname)
        except FileNotFoundError:
            print(end='')
        except Exception:
            print(end='')


def remove_from_folder(file):
    file_types = ['.xml', '.json', '.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
    file_name = file.split('.')[0]
    for extension in file_types:
        try:
            d_file = file_name + extension
            os.remove(d_file)
            print('\tFile', d_file, 'removed')
        except FileNotFoundError:
            print(end='')
        except Exception:
            print('Unknown exception occurred. File ' + file)


def checking_labels_in_file(xml_file):
    try:
        tree = None
        try:
            tree = etree.parse(xml_file)
        except Exception:
            print('Couldn\'t parse XML file', xml_file)
            return False

        tree_root = tree.getroot()

        for elm in tree_root.findall('./object'):
            name = elm.find('name')
            if name.text not in pred_labels:
                return False
            if name.text in bad_classes:
                return False

        return True
    except FileNotFoundError:
        print('File Not Found Error. File:', xml_file)
    except Exception:
        print('Unknown exception occurred. File', xml_file)


def lowercasing_extensions(folder):
    print('\nLowercasing extensions')
    try:
        for file in [y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*.*'))]:
            filename, file_extension = os.path.splitext(os.path.basename(file))
            if file_extension.isupper():
                try:
                    n_file = os.path.dirname(file) + os.sep + filename + file_extension.lower()
                    os.rename(file, n_file)
                    print('\t' + file, ' --> ', n_file)
                except Exception:
                    print('Couldn\'t rename file', file)
        print('Lowercasing is finished')
    except Exception:
        print('Unknown exception occurred. Folder:', folder)


def moderating_filenames(folder):
    print('\nModerating filenames')
    try:
        for file in [y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*.*'))]:
            try:
                filename, file_extension = os.path.splitext(os.path.basename(file))
                if file_extension in ['.xml', '.json', '.jpg', '.png', '.jpeg', '.PNG', '.JPEG', '.JPG']:
                    f1 = filename.replace('(', '_')
                    f1 = f1.replace(')', '_')
                    f1 = f1.replace('[', '_')
                    f1 = f1.replace(']', '_')
                    f1 = f1.replace('{', '_')
                    f1 = f1.replace('}', '_')
                    f1 = f1.replace(' ', '_')
                    f1 = f1.replace('-', '_')
                    f1 = f1.replace('.', '_')
                    f1 = f1.replace(',', '_')
                    f1 = f1.replace('____', '_')
                    f1 = f1.replace('___', '_')
                    f1 = f1.replace('__', '_')
                    n_file = os.path.dirname(file) + os.sep + f1 + file_extension
                    if not file==n_file :
                        os.rename(file, n_file)
                        print('\t' + file + ' -> ' + n_file)
            except Exception:
                print('Could\'t rename file', file)

        print('Moderating filenames finished')
    except Exception:
        print('Unknown exception occurred. Folder:', folder)


def checking_labels_in_folder(folder):
    try:
        print('\nChecking labels in folder')
        files_to_move = []
        for file in [y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*.xml*'))]:
            mst = checking_labels_in_file(file)
            if mst is None or mst is False:
                files_to_move.append(file)
        if len(files_to_move) != 0:
            print('Wrong labels found in ', len(files_to_move), ' files.')
            for file in files_to_move:
                move_to_folder(file, folder, 'mistake')
        print('Checking labels is finished.')
    except Exception:
        print('Unknown exception occurred. Folder:', folder)


def checking_small_boxes_in_folder(folder):
    try:
        print('\nChecking small boxes in folder')
        files_to_move = []
        for file in [y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*.xml*'))]:
            mst = checking_cords_in_file(file)
            if mst is None or mst is False:
                files_to_move.append(file)
        if len(files_to_move) != 0:
            print('****   Small BBoxes found in ', len(files_to_move), ' images!   ****')
            for file in files_to_move:
                move_to_folder(file, folder, '2small')
        print('Checking small boxes is finished.')
    except Exception:
        print('Unknown exception occurred. Folder:', folder)


def checking_cords_in_file(xml_file):
    try:
        tree = None
        try:
            tree = etree.parse(xml_file)
        except Exception:
            print('Couldn\'t parse XML file', xml_file)
            return False
        tree_root = tree.getroot()
        for elm in tree_root.findall('./object'):
            try:
                xmin = int(elm.find('.//xmin').text)
                xmax = int(elm.find('.//xmax').text)
                ymin = int(elm.find('.//ymin').text)
                ymax = int(elm.find('.//ymax').text)
                if xmax - xmin <= 5 or ymax - ymin <= 5:
                    return False
            except Exception:
                print('Couldn\'t get cords from object bndbox in file', xml_file)
                return False
        return True
    except FileNotFoundError:
        print('File Not Found Error. File:', xml_file)
    except Exception:
        print('Unknown exception occurred. File', xml_file)


def checking_missing_images(folder):
    try:
        print('\nChecking for missing images')
        files_to_delete = []
        for file in [y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*.xml'))]:
            filename, file_extension = os.path.splitext(os.path.basename(file))
            png_name = os.path.dirname(file) + os.sep + filename + '.png'
            jpg_name = os.path.dirname(file) + os.sep + filename + '.jpg'
            jpeg_name = os.path.dirname(file) + os.sep + filename + '.jpeg'
            PNG_name = os.path.dirname(file) + os.sep + filename + '.PNG'
            JPG_name = os.path.dirname(file) + os.sep + filename + '.JPG'
            JPEG_name = os.path.dirname(file) + os.sep + filename + '.JPEG'        
            if not os.path.isfile(png_name) and not os.path.isfile(jpg_name) and not os.path.isfile(jpeg_name) and not os.path.isfile(PNG_name) and not os.path.isfile(JPG_name) and not os.path.isfile(JPEG_name):
                files_to_delete.append(file)
                print('\t' + file)
        print('Checking is finished')
        if len(files_to_delete) != 0:
            print('Wrong files founded:', len(files_to_delete))
            if ask_user():
                print('DELETING:')
                for file in files_to_delete:
                    if os.path.isfile(file):
                        remove_from_folder(file)
    except Exception:
        print('Unknown exception occurred. Folder:', folder)


def checking_missing_xmls(folder):
    print('\nChecking missing xml files')
    result = []
    files_to_delete = []
    for ext in ('*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG', '*.JPEG'):
        result.extend([y for x in os.walk(folder) for y in glob(os.path.join(x[0], ext))])

    for file in result:
        filename, file_extension = os.path.splitext(os.path.basename(file))
        xmlname = os.path.dirname(file) + os.sep + filename + '.xml'
        if not os.path.isfile(xmlname):
            files_to_delete.append(file)
            print('\t' + file)
    print('Checking is finished')
    if len(files_to_delete) != 0:
        print('Wrong files founded:', len(files_to_delete))
        if ask_user():
            print('DELETING:')
            for file in files_to_delete:
                if os.path.isfile(file):
                    remove_from_folder(file)


def checking_image_integrity(folder):
    print('\nChecking image integrity')
    files_to_delete = []
    try:
        for file in tqdm([y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*.*'))]):
            filename, file_extension = os.path.splitext(os.path.basename(file))
            if file_extension in ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']:
                if not check_image(file):
                    files_to_delete.append(file)
        if len(files_to_delete) != 0:
            if ask_user():
                print('DELETING:')
                for file in files_to_delete:
                    if os.path.isfile(file):
                        remove_from_folder(file)
        print ('***   ' + len(files_to_delete) + ' Damaged images found and deleted! ***') 
        print('Checking is finished')
    except Exception:
        print('Unknown exception occurred. Folder:', folder)


def checking_boxes(folder):
    print('\nChecking object boxes')
    try:
        for file in [y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*.xml*'))]:
            if check_boxes_in_xml(file):
                move_to_folder(file, folder, 'overlap')
        print('Checking is finished')
    except Exception:
        print('Unknown exception occurred. Folder:', folder)


def check_boxes_in_xml(xml_file):
    try:
        tree = None
        try:
            tree = etree.parse(xml_file)
        except Exception:
            print('Couldn\'t parse XML file', xml_file)

        tree_root = tree.getroot()
        flag = False
        elems1 = tree_root.findall('./object')
        elems2 = list(elems1)
        for elm1 in elems1:
            elems2.pop(0)
            for elm2 in elems2:
                if elm1 != elm2:
                    if check_box_names(elm1, elm2) is True and check_box_coverage(elm1, elm2) == 100:
                        try:
                            elm2.getparent().remove(elm2)
                            print('\tElement was removed from file', xml_file)
                        except Exception:
                            print(end='')
                        tree.write(xml_file)
                    elif check_box_coverage(elm1, elm2) >= 96:
                        flag = True
        if flag:
            return True
        return False
    except Exception:
        print('Unknown exception occurred. File:', xml_file)


def check_box_names(box1, box2):
    if box1.find('name').text == box2.find('name').text:
        return True
    return False


def check_box_coverage(box1, box2):
    cords1 = [int(box1.find('.//xmin').text),
              int(box1.find('.//ymin').text),
              int(box1.find('.//xmax').text),
              int(box1.find('.//ymax').text)]
    cords2 = [int(box2.find('.//xmin').text),
              int(box2.find('.//ymin').text),
              int(box2.find('.//xmax').text),
              int(box2.find('.//ymax').text)]
    if cords1.__eq__(cords2):
        return 100
    else:
        area1 = (cords1[2] - cords1[0]) * (cords1[3] - cords1[1])
        area2 = (cords2[2] - cords2[0]) * (cords2[3] - cords2[1])
        height = (min(cords1[3], cords2[3]) - max(cords1[1], cords2[1]))
        width = (min(cords1[2], cords2[2]) - max(cords1[0], cords2[0]))
        coverage = 0
        if height > 0 and width > 0:
            coverage = (min(cords1[3], cords2[3]) - max(cords1[1], cords2[1])) * \
                       (min(cords1[2], cords2[2]) - max(cords1[0], cords2[0]))
            if area1 > area2:
                return coverage / area1 * 100
            else:
                return coverage / area2 * 100
        else:
            return coverage


def main(folder):
    lowercasing_extensions(folder)
    moderating_filenames(folder)
    checking_labels_in_folder(folder)
    checking_small_boxes_in_folder(folder)
    checking_missing_images(folder)
    checking_missing_xmls(folder)
    checking_image_integrity(folder)
    checking_boxes(folder)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    main(parser.parse_args().folder)
    input('Press ENTER...')
