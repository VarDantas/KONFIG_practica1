#!/bin/bash
cd "$(dirname "$0")/.."
python3 src/main.py --vfs test_vfs/vfs_deep.zip --script scripts/start2.txt
