"""generate_bottleneck_features.py"""

import argparse
import json
import numpy as np
import os
import sys
from keras import backend
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator

parser = argparse.ArgumentParser(description='Download APID dataset images.')

parser.add_argument('conf',
                    type=argparse.FileType('r'),
                    default=sys.stdin,
                    help='path to configuration file')

def main():
    """Reads the data and saves the images."""
    # Read configuration file
    conf = None
    args = parser.parse_args()
    with open(args.conf.name, 'r') as conf_file:
        conf = json.load(conf_file)

    if not conf:
        raise SystemExit('Invalid Configuration File')

    # Paths initialization
    src_dir = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.dirname(src_dir)

    # Images directory
    im_dir = os.path.join(app_dir, conf['download_dir'])

    # Configurations for generating bottleneck features
    gen_features_conf = conf['bottleneck_features']

    # Image target size
    img_width = gen_features_conf['img_width']
    img_height = gen_features_conf['img_height']
    crop_size = (img_width, img_height)

    # Save features to
    features_dir = gen_features_conf['features_dir']
    features_file = gen_features_conf['features_file']
    features_path = os.path.join(app_dir, features_dir, features_file)

    # Arguments for ImageDataGenerator
    data_gen_args = dict(rescale=1./255)

    # Initialize image data generator
    image_datagen = ImageDataGenerator(**data_gen_args)

    # Get an image generator
    image_generator = image_datagen.flow_from_directory(
        im_dir,
        target_size=crop_size,
        class_mode=None,
        shuffle=False)

    # Load the pre-trained model
    model = VGG16(weights='imagenet', include_top=False)

    # Extract bottleneck features
    features = model.predict_generator(
        image_generator,
        verbose=gen_features_conf['predict_generator']['verbose'],
        use_multiprocessing=gen_features_conf['predict_generator']['use_multiprocessing'])

    # Save bottleneck features
    np.save(features_path, features)

if __name__ == "__main__":
    main()
