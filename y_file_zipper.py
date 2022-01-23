import os
import lzma
import zlib
import bz2
import zipfile
import inspect
import argparse
from tqdm import tqdm
from glob import glob

extensions = ['.xml', '.json', '.jpg', '.png', '.jpeg', '.PNG', '.JPEG', '.JPG', '.mp4', '.mp3', '.avi', '.mov']


def move_to_zip(file, folder, zip_name):
    zip_filename = os.path.join(folder, zip_name) + '.zip'
    with zipfile.ZipFile(zip_filename, compression=zipfile.ZIP_BZIP2, compresslevel=9, mode='a') as zip_file:
        for ext in extensions:
            try:
                m_file = file.split('.')[0] + ext
                if os.path.exists(m_file):
                    zip_file.write(m_file, arcname=os.path.basename(m_file))
                    os.remove(m_file)
            except Exception:
                print('Unknown exception occurred. File', file)


def main(folder, count, name):
    counter = count
    dir_counter = 0
    zip_name = name + '_' + str(dir_counter)
    for file in tqdm([y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*.*'))], desc='Archiving'):
        if counter != 0:
            counter -= 1
        else:
            counter = count - 1
            dir_counter += 1
            zip_name = name + '_' + str(dir_counter)
        move_to_zip(file, folder, zip_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    parser.add_argument('-c', '--count', dest='count', nargs='?', type=int, default=250)
    parser.add_argument('-n', '--name', dest='name', nargs='?', type=str, default='dir')
    main(parser.parse_args().folder, parser.parse_args().count, parser.parse_args().name)
    input('Press ENTER...')
