#!python
from __future__ import print_function

import argparse
import sys

import pydmtx
from pydmtx.pydmtx import decode


def main(args=None):
    if args is None:
        args = sys.argv[1:]
 
    parser = argparse.ArgumentParser(
        description='Reads datamatrix barcodes in images'
    )
    parser.add_argument('image', nargs='+')
    parser.add_argument(
        '-v', '--version', action='version',
        version='%(prog)s ' + pydmtx.__version__
    )
    args = parser.parse_args(args)

    from PIL import Image

    for image in args.image:
        for barcode in decode(Image.open(image)):
            print(barcode.data)


if __name__ == '__main__':
    main()
