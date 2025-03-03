import sys
from interpreter import run_gml

if len(sys.argv) != 2:
    print("Usage: python main.py <filename.gml>")
    sys.exit(1)

with open(sys.argv[1], "r") as f:
    code = f.read()

run_gml(code)