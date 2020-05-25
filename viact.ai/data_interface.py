"""Python program to convert 'annotations.xml' to PASCAL VOC annotation format."""
import os
import argparse

import cv2
import xml.etree.ElementTree as ET
from tqdm import tqdm

from utils import _annotation_xml

parser = argparse.ArgumentParser()
parser.add_argument('--xml-path', help='path to annotation xml')
parser.add_argument('--image-path', help='path to images directory')
parser.add_argument('--dest-path', help='path to save annotations and images')

args = parser.parse_args()

def parse_annotation(xml_path):
    """Function to parse annotation xml.

    Args:
        xml_path(str):  path to annotation xml.

    Returns:
        image2annotation(dict): dictionary containing image name to annotations mapping.

    """

    tree = ET.parse(xml_path)
    root = tree.getroot()
    images = root.findall('image')
    print('[/] total number of image annotations present: {}'.format(len(images)))

    image2annotation = {}
    for image in images:
        image_id = image.attrib['id']
        image2annotation[image_id] = []

        for box in image.findall('box'):
            label = box.attrib['label']
            # skip if label is not head
            if label != "head":
                continue

            annotation = {}
            minx, miny = int(float(box.attrib['xtl'])), int(float(box.attrib['ytl']))
            maxx, maxy = int(float(box.attrib['xbr'])), int(float(box.attrib['ybr']))

            # parse attributes for the box and create labels accordingly
            safety_helmet, mask = False, False
            for attribute in box.findall('attribute'):
                if attribute.attrib['name'] == 'has_safety_helmet' and attribute.text == 'yes':
                    safety_helmet = True
                elif attribute.attrib['name'] == 'mask' and attribute.text == 'yes':
                    mask = True

            # 3 classes: mask+safety_helmet, safety_helmet and mask
            if safety_helmet and mask:
                class_label = "mask+safety_helmet"
            elif safety_helmet:
                class_label = "safety_helmet"
            elif mask:
                class_label = "mask"

            # save bbox coordinates and class label.
            annotation['bbox'] = [minx, miny, maxx, maxy]
            annotation['class'] = class_label
            image2annotation[image_id].append(annotation)


    return image2annotation

def save_annotations(image2annotation, image_dir, xml_dir):
    """Function to save images and annotations in PASCAL VOC format.

    Args:
        image2annotation(dict): dictionary containing image name to annotations mapping.
        image_dir(str): path to image dir.
        xml_dir(str):   path to xml dir.

    """

    for image_id in tqdm(image2annotation):
        annotations = image2annotation[image_id]
        image_name, xml_name = image_id + '.jpg', image_id + '.xml'
        image = cv2.imread(os.path.join(args.image_path, image_name))

        objects = []
        for annotation in annotations:
            bbox = annotation['bbox']
            class_label = annotation['class']
            obj = {class_label: {'xmin': bbox[0], 'ymin': bbox[1], 'xmax': bbox[2], 'ymax': bbox[3]}}
            objects.append(obj)

        # save image and xml to destination folder.
        w = os.system('cp {}/{} {}'.format(args.image_path, image_name, image_dir))

        xml_content = _annotation_xml(objects, image_id, image.shape)
        with open(os.path.join(xml_dir, xml_name), 'w') as f:
            f.write(xml_content)


if __name__ == '__main__':

    image_dir = os.path.join(args.dest_path, 'JPEGImages')
    xml_dir = os.path.join(args.dest_path, 'Annotations')
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(xml_dir, exist_ok=True)

    print('[/] parsing annotations...')
    image2annotation = parse_annotation(args.xml_path)
    print('[/] saving images and xmls in PASCAL VOC format...')
    save_annotations(image2annotation, image_dir, xml_dir)