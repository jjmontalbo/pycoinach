import argparse
import chalk
import glob
import os
import sys
from . import generate_entry, export_test, pysoundfile_test


parser = argparse.ArgumentParser(description='Converts SCD files in a directory to OGG with loop metadata and FLAC that loops twice.')
parser.add_argument('directory', help='Directory containing SCD files.')
parser.add_argument('-S', '--no-skip', dest='skip', action='store_false', help='Do not skip over SCD files that have corresponding OGG files with the same name.')

args = parser.parse_args()

directory = args.directory
directory = directory.replace('\\', '/')
if directory.endswith('/'):
    directory = directory[:-1]

skip = args.skip

for file in glob.glob(f'{sys.argv[1]}/*.scd'):
    file = file.replace('\\', '/')
    print('Reading', chalk.white(file), '... ', end='')
    sys.stdout.flush()

    if skip:
        name, ext = file.rsplit('/', 1)[-1].rsplit('.', 1)
        if os.path.isfile(f'{sys.argv[1]}/{name}.ogg'):
            print(chalk.yellow('[SKIPPED]'))
            continue

    entry, ogg = generate_entry(file)
    if entry:
        export_test(file, entry, ogg)
        pysoundfile_test(file, entry, ogg)
        print(chalk.green('[SAVED]'))
