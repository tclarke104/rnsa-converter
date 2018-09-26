import xml.etree.cElementTree as ET
import os

def parse_dataset(raw_annotations):
    images = {}

    for index, raw_annotation in raw_annotations.iterrows():
        current_bbox = BoundBox(raw_annotation.x,
                                raw_annotation.y,
                                raw_annotation.width,
                                raw_annotation.height,
                                raw_annotation.Target)

        if raw_annotation.patientId not in images:
            if current_bbox.label:
                images[raw_annotation.patientId] = [current_bbox]
        else:
            images[raw_annotation.patientId].append(current_bbox)

    return images


class BoundBox(object):
    def __init__(self, x_min, y_min, width, height, target=0):
        self.xmin = x_min
        self.ymin = y_min
        self.xmax = x_min + width
        self.ymax = y_min + height
        self.label = target


def cvt_annots_to_xml(annot, annot_path, train_path):
    xml_dict = {}
    fps = list(annot.keys())
    for fp in fps:
        root = ET.Element('annotation')
        folder = ET.SubElement(root, 'folder')
        folder.text = 'stage_1_test_images'
        ET.SubElement(root, "filename").text = fp + '.dcm'
        ET.SubElement(root, "path").text = os.path.join(train_path, fp + '.dcm')
        size = ET.SubElement(root, 'size')
        ET.SubElement(size, "width").text = '1024'
        ET.SubElement(size, "height").text = '1024'
        ET.SubElement(size, "depth").text = '1'
        ET.SubElement(root, "segmented").text = '0'
        for bbox in annot[fp]:
            object = ET.SubElement(root, 'object')
            ET.SubElement(object, "name").text = 'opacity'
            ET.SubElement(object, "pose").text = 'Unspecified'
            ET.SubElement(object, "truncated").text = '0'
            ET.SubElement(object, "difficult").text = '0'
            bndbox = ET.SubElement(object, 'bndbox')
            ET.SubElement(bndbox, "xmin").text = str(bbox.xmin)
            ET.SubElement(bndbox, "ymin").text = str(bbox.ymin)
            ET.SubElement(bndbox, "xmax").text = str(bbox.xmax)
            ET.SubElement(bndbox, "ymax").text = str(bbox.ymax)
        tree = ET.ElementTree(root)
        tree.write(os.path.join(annot_path, fp + '.xml'))



