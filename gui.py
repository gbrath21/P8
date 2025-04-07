import tkinter as tk
from tkinter import scrolledtext, messagebox
from interpreter import run_gml
import os
import plotly.io as pio
import webbrowser
from tkinter import filedialog

class GML_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Manipulation")

        # Indtastningsfelt
        self.label = tk.Label(root, text="Insert your GML code here:", font=("Arial", 12))
        self.label.pack(pady=5)

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15, font=("Courier", 12))
        self.text_area.pack(padx=10, pady=5)

        # Knap til at køre GML
        self.run_button = tk.Button(root, text="Create graph", command=self.run_gml_code, font=("Arial", 12), bg="lightblue")
        self.run_button.pack(pady=10)

        # Beskedlabel
        self.output_label = tk.Label(root, text="", font=("Arial", 10), fg="green")
        self.output_label.pack()
        
        self.save_button = tk.Button(root, text="Save GML", command=self.save_gml_gui, font=("Arial", 12), bg="lightgreen")
        self.save_button.pack(pady=5)

        self.load_button = tk.Button(root, text="Load GML", command=self.load_gml_gui, font=("Arial", 12), bg="lightblue")
        self.load_button.pack(pady=5)

        from tkinter import filedialog

    def save_gml_gui(self):
        filename = filedialog.asksaveasfilename(defaultextension=".gml", filetypes=[("GML files", "*.gml")])
        if filename:
            code = self.text_area.get("1.0", "end").strip()
            with open(filename, "w") as file:
                file.write(code)
            self.output_label.config(text=f"Saved GML to {filename}")

    def load_gml_gui(self):
        filename = filedialog.askopenfilename(filetypes=[("GML files", "*.gml")])
        if filename:
            with open(filename, "r") as file:
                code = file.read()
            self.text_area.delete("1.0", "end")
            self.text_area.insert("end", code)
            self.output_label.config(text=f"Loaded GML from {filename}")

    def run_gml_code(self):
        code = self.text_area.get("1.0", tk.END).strip()
        if not code:
            messagebox.showerror("Error", "Found no GML code.")
            return
        
        try:
            run_gml(code)
            self.output_label.config(text="GML-koden er kørt succesfuldt.")
        except Exception as e:
            messagebox.showerror("Error", f"Der opstod en fejl:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GML_GUI(root)
    root.mainloop()