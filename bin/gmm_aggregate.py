#! /usr/bin/env python

# © Copyright IBM Corp. 2023 All Rights Reserved
# SPDX-License-Identifier: Apache2.0

import argparse
import os
import shutil
import tarfile

parser = argparse.ArgumentParser(description='Aggregate GMM simulations results.')
parser.add_argument('--case_folders',
                    type=str,
                    required=True,
                    action='store',
                    nargs='+',
                    metavar='CASE_FOLDERS',
                    help='Case folders storing parse_results.h5 files.')
arg = parser.parse_args()

num_replicas = len(arg.case_folders)

# Copy parse_results.h5 from all given case folders to AggregateGMMResults folder
for i in range(num_replicas):
    src = os.path.join(arg.case_folders[i], 'case_input', 'parse_results.h5')
    shutil.copyfile(src, f'case_{i}_results.h5')

# Compress to create isotherms.tgz
with tarfile.open('results.tgz', 'w') as tar:
    for file in os.listdir():
        if file.endswith('.h5'):
            tar.add(file)
