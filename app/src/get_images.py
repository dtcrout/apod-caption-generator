"""get_images.py"""

import argparse
import json
import os
import requests
import sys
from time import sleep

parser = argparse.ArgumentParser(description='Download APID dataset images.')

parser.add_argument('conf',
                    type=argparse.FileType('r'),
                    default=sys.stdin,
                    help='path to configuration file')

def save_image_from_url(url, download_dir):
    """Saves image at the given URL to file system."""
    # Get the filename from URL
    filename = os.path.basename(url)

    # Check if file has already been downloaded
    if filename in os.listdir(download_dir):
        print('Image already exists: {}'.format(filename))
        return True

    r = requests.get(url, stream=True)
    if r.status_code == 200:
        success = True
        # Download the binary stream in chunks
        with open(os.path.join(download_dir,filename), 'wb') as image_file:
            for chunk in r:
                image_file.write(chunk)
    else:
        success = False

    print('Download Success: {}; URL: {}'.format(success, url))
    # Sleep for a second before making the next request
    sleep(1)
    return success

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
    metadata_dir = os.path.join(app_dir, conf['metadata_dir'])
    download_dir = os.path.join(app_dir, conf['download_dir'])

    # Read available data from metadata directory
    data = []
    for f in os.listdir(conf['metadata_dir']):
        with open(os.path.join(metadata_dir, f), 'r') as json_data:
            data += json.load(json_data)

    # Use only non-copyright protected data
    non_copyright_data = list(
        filter(lambda p: p if "copyright" not in p else None, data)
    )

    # Use only image data
    image_data = list(
        filter(lambda p: p if p["media_type"]=="image" else None,
               non_copyright_data)
    )

    # Print statistics
    print('Total Items:             {}'.format(len(data)))
    print('Public Domain Items:     {}'.format(len(non_copyright_data)))
    print('Public Domain Images:    {}'.format(len(image_data)))

    # Download Images
    for d in image_data:
        url_keys = set(['url', 'hdurl'])
        for image in image_data:
            # See which keys are present in the JSON
            found_keys = filter(lambda url_key: url_key in url_keys, image.keys())
            # Save all the images
            list(map(lambda k: save_image_from_url(k, download_dir),
                 list(map(lambda k: image[k], found_keys))))


if __name__ == "__main__":
    main()
