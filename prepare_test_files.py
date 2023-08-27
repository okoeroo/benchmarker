#!/usr/bin/python3

import os
import sys
import argparse
import uuid
import hashlib
import math
from progress.bar import Bar


def argparsing():
    # Parser
    parser = argparse.ArgumentParser(os.path.basename(__file__))
    parser.add_argument("-v", "--verbose",
                        dest='verbose',
                        help="Verbose mode. Default is off",
                        action="store_true",
                        default=False)
    parser.add_argument("--num-of-files",
                        dest='num_of_files',
                        help="Number of generated files.",
                        default=1,
                        type=int)
    parser.add_argument("--root-dir",
                        dest='root_dir',
                        help="Root directory in which all files generated files will be stored",
                        default="/tmp",
                        type=str)

    return parser.parse_args()


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])


def create_file(path, num_of_bytes):
    # Write random data to file
    with open(path, 'wb') as fout:
        fout.write(os.urandom(num_of_bytes))
        fout.flush()


def construct_path(root_dir, case_name, file_name):
    return "/".join([root_dir, case_name, file_name])


def generate_random_name():
    return str(uuid.uuid4())


def calc_sha256_from_path_in_hex(path):
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def file_generation(args, case_name, file_count, file_size):
    conv_size = convert_size(file_size)
    with Bar(f'{case_name}: Generating {file_count} files of {conv_size}',
                suffix='%(percent).1f%% - %(eta)ds') as bar:
        for x in range(file_count):
            # Create path
            path = construct_path(args.root_dir,
                                  case_name,
                                  generate_random_name())

            # Check if directory exists
            if not os.path.exists(os.path.dirname(path)):
                os.mkdir(os.path.dirname(path))
                if args.verbose:
                    print(f"Notice: {os.path.dirname(path)} created")

            # Generate file
            create_file(path, file_size)

            # SHA256
            sha256_hex_val = calc_sha256_from_path_in_hex(path)

            # Move file to hashvalue
            path2 = construct_path(args.root_dir,
                                   case_name,
                                   sha256_hex_val)
            os.rename(path, path2)
            if args.verbose:
                print(f"Notice: file {path2} ({file_size}) created")

            bar.next()

### Main
def main(args):

    print("Case 1: Create 1000 files of 1k size")
    file_generation(args, "case_1", 1000, 1024)

    sys.exit(0)

    print("Case 2: Create 10.000 files of 1k size")
    file_generation(args, "case_2", 10 * 1000, 1024)

    print("Case 3: Create 100.000 files of 1k size")
    file_generation(args, "case_3", 100 * 1000, 1024)

    print("Case 4: Create 1000 files of 1M size")
    file_generation(args, "case_4", 1000, 1024 ** 2)

    print("Case 5: Create 100 files of 1G size")
    file_generation(args, "case_5", 100, 1024 ** 3)




### Start up
if __name__ == "__main__":
    # initialize
    args = argparsing()

    # test
    if not os.path.exists(args.root_dir):
        os.makedirs(args.root_dir)

    # Go
    main(args)
