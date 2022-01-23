import argparse
import os
from glob import glob


def main(folder):
    for ext in ['.mp4', '.avi']:
        for file in [y for x in os.walk(folder) for y in glob(os.path.join(x[0], '*' + ext))]:
            try:
                output = file.split('.')[0] + '_.' + file.split('.')[1]
                command = f'ffmpeg -err_detect ignore_err -i {file} {output}'
                os.system(command)
                os.remove(file)
                print('File', file, 'was removed.')
            except Exception:
                print('Unknown exception occurred. File:', file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?', required=True)
    main(parser.parse_args().folder)
    # input('Press ENTER...')
