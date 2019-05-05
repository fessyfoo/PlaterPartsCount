# platerpartscount.py

creates config files for [Plater][1]  out of [Voron][2] style STL directories.

```
% ./platerpartscount.py -h
usage: platerpartscount.py [-h] [--escape] [--verbose] directory

searches directory for STL files and creates accent.conf and normal.conf
config files for plater in the current directory

positional arguments:
  directory      the directory to search

optional arguments:
  -h, --help     show this help message and exit
  --escape, -e   wether or not to escape filenames
  --verbose, -v  print out the contents of the files

```

## requirements

- python2.7

a simple single python script. run it like any other


[1]: https://github.com/Rhoban/Plater
[2]: http://vorondesign.com/
