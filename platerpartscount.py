#!/usr/bin/env python

import argparse
import sys
import re
import os

def parse_args():
    parser = argparse.ArgumentParser(
        description='searches directory for STL files and creates ' \
            + 'accent.conf and normal.conf config files for plater ' \
            + 'in the current directory')
    parser.add_argument(
        '--escape', '-e',
        action = 'store_true',
        help   = 'wether or not to escape filenames'
    )
    parser.add_argument(
        '--verbose', '-v',
        action = 'store_true',
        help   = 'print out the contents of the files'
    )
    parser.add_argument(
        'directory',
        help   = 'the directory to search'
    )
    return parser.parse_args()

# _{name}_x{quantity}_{revision}.stl
# _{name}_x{quantity}.stl
# _{name}_{revision}.stl
# _{name}.stl
r = re.compile(r'_x(\d+)(_[^_]+)?.stl$',re.IGNORECASE)
def count_from_filename(filename):
    m = r.search(filename)
    return m and int(m.group(1)) or 1

def escape(filename):
    # TODO more os specific escape? what does plater need on windows?
    return re.sub('( )', r'\\\1', filename)

def process_dir():
    stl      = re.compile(r'.stl$',re.IGNORECASE)
    accented = re.compile(r'^(_|accent_)')

    accents = []
    normals = []
    for root, dirnames, filenames in os.walk(args.directory):
        for filename in filter(stl.search,filenames):
            fullpath = os.path.join(root, filename)
            count    = count_from_filename(filename)
            both     = (fullpath, count)
            if accented.match(filename):
                accents.append(both)
            else:
                normals.append(both)
    return (accents, normals)

def output_files(accents, normals):
    for output, files in [
        ('accent.conf', accents),
        ('normal.conf', normals) ]:

            if args.escape:
                files = [ (escape(fullpath), count) for fullpath, count in files]

            print("Making " + output)
            output_file = open(output, "w+")
            for info in files:
                output_file.write("%s %s\n" % info)

            if args.verbose:
                output_file.seek(0,0)
                for line in output_file:
                    sys.stdout.write(line)
                    sys.stdout.flush()

            output_file.close

if __name__ == "__main__":
    args = parse_args()
    accents, normals = process_dir()
    output_files(accents,normals)
