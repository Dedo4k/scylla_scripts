import argparse
import inspect
import shutil
import os
from glob import glob


def move_to_folder(file, dirname, folder):
    imagetypes = ('.xml', '.json', '.jpg', '.png', '.jpeg', '.PNG', '.JPEG', '.JPG', '.mp4', '.mp3', '.avi', '.mov')
    dirname = os.path.join(dirname, folder, dirname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    for exte in imagetypes:
        try:
            f_file = file.split('.')[0] + exte
            shutil.move(f_file, dirname)
            print('\tFile ' + f_file + ' moved to ' + dirname)
        except shutil.SameFileError:
            print('\tFile ' + f_file + 'already exists in ' + dirname)
        except shutil.Error:
            print(end='')
        except FileNotFoundError:
            print(end='')
        except Exception:
            print(end='')


def main(folder, count, name):
    extension = ['.jpg', '.jpeg', '.png']
    counter = count
    dir_counter = 0
    current_dir = name + str(dir_counter)
    prev_dir = current_dir
    for ext in extension:
        for file in [y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*' + ext))]:
            if counter != 0:
                counter -= 1
            else:
                dir_counter += 1
                prev_dir = current_dir
                current_dir = name + str(dir_counter)
                counter = count - 1
            move_to_folder(file, current_dir, folder)
    last_dir = [y for x in os.walk(folder + os.sep + current_dir) for y in glob(os.path.join(x[0], '*.*'))]
    if len(last_dir) <= count * 0.33 and dir_counter != 0:
        try:
            for file in last_dir:
                try:
                    shutil.move(file, folder + os.sep + prev_dir)
                except shutil.Error:
                    print(end='')
                except Exception:
                    print('Unknown exception occurred. Couldn\'t move file', file, 'to folder', prev_dir)
            os.removedirs(folder + os.sep + current_dir)
        except Exception:
            print(end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    parser.add_argument('-c', '--count', dest='count', nargs='?', type=int, default=250)
    parser.add_argument('-n', '--name', dest='name', nargs='?', type=str, default='dir')
    main(parser.parse_args().folder, parser.parse_args().count, parser.parse_args().name)
    input('Press ENTER...')
