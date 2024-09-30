#!/bin/bash
cd "$(dirname "$0")"
chmod +x ./gfxutil
python3 set_gpu.py
