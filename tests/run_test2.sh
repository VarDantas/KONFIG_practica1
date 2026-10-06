#!/bin/bash
cd "$(dirname "$0")/.."
python3 src/main.py --vfs test_vfs/vfs_several.zip --script scripts/start1.txt
