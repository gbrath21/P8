import tkinter as tk
from tkinter import scrolledtext, messagebox
from interpreter import run_gml
import os
import plotly.io as pio
import webbrowser

# GUI-klasse
class GML_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Manipulation Language - GUI")

        # Indtastningsfelt
        self.label = tk.Label(root, text="Skriv din GML-kode her:", font=("Arial", 12))
        self.label.pack(pady=5)

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15, font=("Courier", 12))
        self.text_area.pack(padx=10, pady=5)

        # Knap til at køre GML
        self.run_button = tk.Button(root, text="Kør GML", command=self.run_gml_code, font=("Arial", 12), bg="lightblue")
        self.run_button.pack(pady=10)

        # Beskedlabel
        self.output_label = tk.Label(root, text="", font=("Arial", 10), fg="green")
        self.output_label.pack()

    def run_gml_code(self):
        code = self.text_area.get("1.0", tk.END).strip()
        if not code:
            messagebox.showerror("Fejl", "Ingen GML-kode fundet!")
            return
        
        try:
            run_gml(code)
            self.output_label.config(text="GML-koden er kørt succesfuldt!")
        except Exception as e:
            messagebox.showerror("Fejl", f"Der opstod en fejl:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GML_GUI(root)
    root.mainloop()