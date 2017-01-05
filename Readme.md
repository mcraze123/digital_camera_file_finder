Finds digital camera files recursively starting at the given directory

DCIM Finder:
Finds most personal photo files recursively starting at source_dir,
and copies them to dest_dir.

Usage: python dcim_finder.py -i <source_dir> -o <dest_dir> [-hvasfp]
-h: this usage screen
-v: be verbose
-a: match all image files
-s: minimum file size in KB
-f: perform facial detection
-p: perform HoG pedestrian detection (not implemented yet)

e.g.:
python dcim_finder.py -i test -o test1 -s 200 -v

Copyright(c) 2013-2017 Michael Craze
