#!/bin/bash
cd "$(dirname "$0")/.."
python3 src/main.py --vfs test_vfs/vfs_minimal.zip
