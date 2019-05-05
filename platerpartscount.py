#!/usr/bin/env python

import argparse
import sys
import re
import os

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
args = parser.parse_args()


r = re.compile(r'_x(\d+).stl$',re.IGNORECASE)
def count_from_filename(filename):
    m = r.search(filename)
    return m and int(m.group(1)) or 1

def escape(filename):
    # TODO more os specific escape? what does plater need on windows?
    return re.sub('( )', r'\\\1', filename)

stl      = re.compile(r'.stl$',re.IGNORECASE)
accented = re.compile(r'^_')

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

for output, files in [
    ('accent.conf', accents),
    ('normal.conf', normals) ]:

        if args.escape:
            files = [ (escape(fullpath), count) for fullpath, count in files]

        print("Making " + output)
        output_file = open(output, "w+")
        output_file.truncate()
        for info in files:
            output_file.write("%s %s\n" % info)

        if args.verbose:
            output_file.seek(0,0)
            for line in output_file:
                sys.stdout.write(line)
                sys.stdout.flush()

        output_file.close
