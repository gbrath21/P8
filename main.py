import sys
from interpreter import run_gml
from gui import GML_GUI
import tkinter as tk

def run_gml_file(filename):
    """Kør en GML-fil fra terminalen."""
    with open(filename, "r") as file:
        code = file.read()
        run_gml(code)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        run_gml_file(sys.argv[1])  # Kør fra en GML-fil
    else:
        # Start GUI, hvis ingen fil er angivet
        root = tk.Tk()
        app = GML_GUI(root)
        root.mainloop()