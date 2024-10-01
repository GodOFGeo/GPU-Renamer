#!/bin/bash

check_package() {
    python3 -c "import $1" 2>/dev/null
}

if ! check_package requests; then
    echo "Installing requests module..."
    pip3 install requests
fi

cd "$(dirname "$0")"
python3 set_gpu.py
