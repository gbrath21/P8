import sys
import tkinter as tk
from gui import GML_GUI
from interpreter import run_gml  # Brug den forbedrede version

def run_gml_file(filename):
    with open(filename, "r") as file:
        code = file.read()
        run_gml(code)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as file:
            code = file.read()
        run_gml(code)
    else:
        root = tk.Tk()
        app = GML_GUI(root)
        root.mainloop()