import os
import inspect
import argparse
import shutil
import cv2


def move(file, root):
    dir_name = os.path.join(root, 'wrong')
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    shutil.move(file, dir_name)
    print('File ' + file + ' moved into ' + dir_name)


def video_process(video_file, root):
    try:
        video = cv2.VideoCapture(video_file)
        width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

        video.release()

        if height > width:
            move(video_file, root)

    except Exception:
        print('Unknown exception occurred. File ' + video_file)


def main(directory):
    roots = []
    for root, dirs, files in os.walk(directory):
        roots.append(root)
        for file in files:
            if file.endswith('.mp4'):
                video_process(os.path.join(root, file), roots[0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    main(parser.parse_args().folder)
    input('Press ENTER...')
