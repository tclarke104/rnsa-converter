import os
import pandas as pd
import utils

KAGGLE_DATA_ROOT = os.path.abspath('/Users/travisclarke/kaggle-data')
ANNOTATIONS_FILE = os.path.join(KAGGLE_DATA_ROOT, 'stage_1_train_labels.csv')
TRAIN_DIR = os.path.join(KAGGLE_DATA_ROOT, 'stage_1_train_images')
TRAIN_ANNOT_DIR = os.path.join(KAGGLE_DATA_ROOT, 'stage_1_train_annots')

# load and parse images and annotations
raw_annotations = pd.read_csv(ANNOTATIONS_FILE)
images = utils.parse_dataset(raw_annotations)

utils.cvt_annots_to_xml(images, TRAIN_ANNOT_DIR, TRAIN_DIR)