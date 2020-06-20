import os
import sys
import logging
import json
import yaml


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def build_classes(data_folder, dist_folder):
    classes_filename = os.path.join(data_folder, "classes.yaml")
    objects = []
    # load from yaml file
    with open(classes_filename, 'r') as stream:
        objects = yaml.safe_load(stream)

    # save to json
    json_filename = os.path.join(dist_folder, "classes.json")
    with open(json_filename, 'w') as f:
        json.dump(objects, f, indent=4)
    logging.debug('Classes successfully written to dist folder')


def build_products(data_folder, dist_folder):
    vendor_filename = os.path.join(data_folder, 'vendors.yaml')
    # load from yaml file
    vendors = []
    with open(vendor_filename, 'r') as stream:
        vendors = yaml.safe_load(stream)

    products_folder = os.path.join(data_folder, 'products')
    for product_fn in os.listdir(products_folder):
        _, ext = os.path.splitext(product_fn)
        if not ext == '.yaml':
            continue

        filename = os.path.join(products_folder, product_fn)
        with open(filename, 'r') as stream:
            product = yaml.safe_load(stream)
        (product_id, product_values), = product.items()
        if 'products' not in vendors[product_values['vendorId']]:
            vendors[product_values['vendorId']]['products'] = {}
        vendors[product_values['vendorId']]['products'][product_id] = product_values

    json_filename = os.path.join(dist_folder, "usbid.json")
    with open(json_filename, 'w') as f:
        json.dump(vendors, f, indent=4)
    logging.debug('Usbid successfully written to dist folder')



if __name__ == "__main__":
    if len(sys.argv) <= 1:
        logging.error('You need to pass data folder argument')
    elif len(sys.argv) <= 2:
        logging.error('You need to pass dist folder argument')
    else:
        data_folder = sys.argv[1]
        dist_folder = sys.argv[2]
        if not os.path.exists(dist_folder):
            os.makedirs(dist_folder)
        build_classes(data_folder, dist_folder)
        build_products(data_folder, dist_folder)
