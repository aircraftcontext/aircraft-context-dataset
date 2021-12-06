import argparse
import csv
import cv2
import glob
import os
import yt_dlp
import logging


class VideoManager:
    def __init__(self, video_dir):
        self.vcap = None
        self.video_path = None
        self.video_dir = video_dir
        os.makedirs(self.video_dir, exist_ok=True)
        self.num_frames = 0
        self.image_width = 0
        self.image_height = 0
        logging.basicConfig(filename='download_errors.log', level=logging.DEBUG)

    def update(self, url, resolution):
        self.delete()
        self.image_width = resolution[0]
        self.image_height = resolution[1]
        path_video_input = glob.glob(os.path.join(self.video_dir, url + '.*'))
        if len(path_video_input) == 0:
            ydl_opts = {'outtmpl': os.path.join(self.video_dir, url + '.%(ext)s')}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.prepare_filename(ydl.extract_info(url))
                except yt_dlp.utils.DownloadError as error_msg:
                    print(f'DownloadError: {url} - {error_msg}')
                    logging.debug(f'DownloadError: {url} - {error_msg}')
                    self.num_frames = 0
                    for path_incomplete in glob.glob(os.path.join(self.video_dir, url + '.*')):
                        os.remove(path_incomplete)
                    return

            path_video_input = glob.glob(os.path.join(self.video_dir, url + '.*'))

        self.video_path = path_video_input[0]
        self.vcap = cv2.VideoCapture(path_video_input[0])
        self.num_frames = int(self.vcap.get(propId=cv2.CAP_PROP_FRAME_COUNT))
        return self.vcap

    def delete(self):
        if self.num_frames > 0:
            self.vcap.release()
            os.remove(self.video_path)

    def get_image(self, frame_idx):
        if frame_idx < self.num_frames:
            self.vcap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            return self.vcap.read()[1]
        else:
            print(f'frame id {frame_idx} out of range {self.num_frames}')
            return None

    def resize_image(self, image):
        height, width, _ = image.shape
        if width != self.image_width or height != self.image_height:
            return cv2.resize(image, (self.image_width, self.image_height), interpolation=cv2.INTER_CUBIC)
        else:
            return image


def download_and_extract():
    parser = argparse.ArgumentParser(description='Download and extract MAV or UAV subset')
    parser.add_argument('csv_path', type=str, help='Absolute csv-file path of MAV or UAV subset')
    args = parser.parse_args()
    image_dir = 'images'

    with open(args.csv_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        video_manager = VideoManager(os.path.join(image_dir, 'videos'))
        for row in csv_reader:
            frame_numbers = [int(x) for x in row['frames'].split(' ')]
            sequence = row['sequence']
            if len(glob.glob(os.path.join(image_dir, sequence + "*"))) != len(frame_numbers):
                if row['url'] != "":
                    video_manager.update(row['url'], [int(n) for n in row['resolution'].split(' ')])
                if video_manager.num_frames > 0:
                    for frame_idx in frame_numbers:
                        image = video_manager.get_image(frame_idx)
                        if image is not None:
                            path_file = os.path.join(image_dir, f'{sequence}-{frame_idx:08d}.jpg')

                            cv2.imwrite(path_file, video_manager.resize_image(image))

        video_manager.delete()


def main():
    download_and_extract()


if __name__ == '__main__':
    main()
