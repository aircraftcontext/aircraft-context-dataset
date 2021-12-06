import argparse
import csv
import cv2
import numpy as np
import os
import sys
from tqdm import tqdm

import datasets


def ids2colors(label_ids, dataset):
    label_colors = np.full((label_ids.shape[0], label_ids.shape[1], 3), 255)
    for labelid in dataset.get_label_ids():
        mask = cv2.inRange(label_ids, labelid, labelid)
        label_colors[np.array(mask, dtype=np.uint8) != 0] = dataset.get_label_color(labelid, bgr=True)

    return label_colors.astype(np.uint8)


def visualize_annotations():
    parser = argparse.ArgumentParser(description='Visualize annotations of MAV and UAV subset')
    parser.add_argument('--output_dir', type=str, help='Output directory containing the visualized annotations',
                        default='visualization')
    parser.add_argument('--image_dir', type=str, help='Directory containing the input images', default='images')
    parser.add_argument('--annotation_dir', type=str, help='Directory containing the annotations', default='uav')
    args = parser.parse_args()

    image_dir = args.image_dir
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    bboxes_dir = os.path.join(args.annotation_dir, 'bboxes')
    labelids_dir = os.path.join(args.annotation_dir, 'labelIds')

    labels = {'uav': datasets.DATASETS['UAVSeg'], 'mav': datasets.DATASETS['MAVSeg']}

    for bbox_file in tqdm(sorted(os.listdir(bboxes_dir)), file=sys.stdout, desc='visualize annotations...'):
        bboxes = os.path.join(bboxes_dir, bbox_file)
        image_file = os.path.join(image_dir, bbox_file.replace('.csv', '.jpg'))
        if os.path.exists(image_file):
            image = cv2.imread(image_file)
            with open(bboxes, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',', fieldnames=['x1', 'y1', 'x2', 'y2', 'labelId'])
                for row in csv_reader:
                    cv2.rectangle(image, (int(row['x1']), int(row['y1'])), (int(row['x2']), int(row['y2'])),
                                  color=(0, 255, 0), thickness=2)

            path_labelids = os.path.join(labelids_dir, bbox_file.replace('.csv', '.png'))
            if os.path.exists(path_labelids):
                image = cv2.hconcat([image, ids2colors(cv2.imread(path_labelids, 0), labels[bbox_file[:3]])])

            cv2.imwrite(os.path.join(output_dir, bbox_file.replace('.csv', '.jpg')), image)


def main():
    visualize_annotations()


if __name__ == '__main__':
    main()
