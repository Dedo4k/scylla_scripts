import os
import argparse
import inspect
import cv2


def video_process(video_file):
    try:
        video = cv2.VideoCapture(video_file)
        fps = video.get(cv2.CAP_PROP_FPS)
        width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # if fps == 0 or width == 0 or height == 0:
        print('File:', video_file)
        print('FPS:', fps.__str__())
        print('Resolution:', width.__str__() + ' X ' + height.__str__())

        video.release()

        if (1280 > width > 0) or (720 > height > 0):
            os.remove(video_file)
            print('File ' + video_file + ' was removed.')

    except Exception:
        print('Unknown exception occurred. File ' + video_file)


def main(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp4'):
                video_process(os.path.join(root, file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder', dest='folder', nargs='?',
                        default=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
    main(parser.parse_args().folder)
    input('Press ENTER...')
