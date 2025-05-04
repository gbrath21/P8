#!/usr/bin/env python3
from interpreter import run_gml
import sys

if len(sys.argv) != 2:
    print("Usage: gml <file.gml>")
    sys.exit(1)

with open(sys.argv[1], 'r') as f:
    code = f.read()

run_gml(code)