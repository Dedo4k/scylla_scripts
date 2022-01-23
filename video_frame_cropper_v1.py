"""

Description:

    Cuts video into frames.

Parameters:

    -f (--folder): path to your video file
    -fps (--fps): number of dropped frames

Usage:

    python video_frame_cropper_v1.py [-f | --folder] 'your_video_file'
                                     [-fps | --fps] 'frame_number'

Version:

        1.1 (.mp4, .mov, .avi, .wmv extensions only, may be more)

"""

import os
import argparse
import inspect
import cv2


def main(video_file, fps):
    index = 0
    ex = ''
    if video_file.__contains__('.mp4'):
        ex = '.mp4'
    elif video_file.__contains__('.mov'):
        ex = '.mov'
    elif video_file.__contains__('.avi'):
        ex = '.avi'
    elif video_file.__contains__('.wmv'):
        ex = '.wmv'
    dir_name = os.path.join(os.path.dirname(video_file), 'frames')
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    try:
        video = cv2.VideoCapture(video_file)

        counter = 0
        while True:
            ret, frame = video.read()
            counter += 1
            if not ret:
                break
            if counter == fps:
                counter = 0
                c_file = os.path.join(dir_name, os.path.basename(video_file)).replace(ex, '_' + str(index) + '.jpg')
                cv2.imwrite(c_file, frame)
                index += 1
                print('File ' + c_file + ' was created.')

    except FileNotFoundError:
        print('File ' + video_file + ' not found.')
    except Exception:
        print('Unknown exception occurred. File ' + video_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    parser.add_argument('-fps', '--fps', dest='fps', nargs='?', default=75)
    main(parser.parse_args().folder, int(parser.parse_args().fps))
    input('Press ENTER...')
