import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from PIL import Image, ImageTk
from interpreter import run_gml
import sys
import os

def resource_path(filename):
    # Kørsel fra PyInstaller (.app eller .exe)
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    # Kørsel direkte fra kildekode
    return os.path.join(os.path.dirname(__file__), filename)

class GML_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Manipulation Language")
        self.root.geometry("850x650")
        self.root.configure(bg="white")

        # Logo
        image = Image.open(resource_path("GMLlogo.png"))
        try:
            resample = Image.Resampling.LANCZOS
        except AttributeError:
            resample = Image.ANTIALIAS
        image = image.resize((150, 150), resample)
        self.logo = ImageTk.PhotoImage(image)
        self.logo_label = tk.Label(root, image=self.logo, bg="white")
        self.logo_label.pack(pady=(10, 0))

        # Label
        self.label = tk.Label(root, text="Insert your GML code below:", font=("Segoe UI", 12), bg="white")
        self.label.pack(pady=(10, 5))

        # Text area
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=20,
                                                   font=("Consolas", 12), bg="white", fg="black",
                                                   insertbackground="black", borderwidth=1)
        self.text_area.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        # Buttons
        button_frame = tk.Frame(root, bg="white")
        button_frame.pack(pady=15)

        self.run_button = self.create_modern_button(button_frame, "▶ Create Graph", self.run_gml_code)
        self.run_button.grid(row=0, column=0, padx=10)

        self.save_button = self.create_modern_button(button_frame, "💾 Save GML", self.save_gml_gui)
        self.save_button.grid(row=0, column=1, padx=10)

        self.load_button = self.create_modern_button(button_frame, "📂 Load GML", self.load_gml_gui)
        self.load_button.grid(row=0, column=2, padx=10)

        # Output label
        self.output_label = tk.Label(root, text="", font=("Segoe UI", 10), fg="green", bg="white")
        self.output_label.pack(pady=5)

    def create_modern_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 11),
            bg="#e0e0e0",
            fg="#000000",
            activebackground="#d0d0d0",
            activeforeground="#000000",
            relief=tk.FLAT,
            padx=15,
            pady=6,
            bd=0,
            cursor="hand2"
        )

    def save_gml_gui(self):
        filename = filedialog.asksaveasfilename(defaultextension=".gml", filetypes=[("GML files", "*.gml")])
        if filename:
            code = self.text_area.get("1.0", "end").strip()
            with open(filename, "w") as file:
                file.write(code)
            self.output_label.config(text=f"✔ Saved GML to: {filename}")

    def load_gml_gui(self):
        filename = filedialog.askopenfilename(filetypes=[("GML files", "*.gml")])
        if filename:
            with open(filename, "r") as file:
                code = file.read()
            self.text_area.delete("1.0", "end")
            self.text_area.insert("end", code)
            self.output_label.config(text=f"📂 Loaded GML from: {filename}")

    def run_gml_code(self):
        code = self.text_area.get("1.0", tk.END).strip()
        if not code:
            messagebox.showerror("Error", "No GML code found.")
            return
        try:
            run_gml(code)
            self.output_label.config(text="GML code executed successfully.")
        except Exception as e:
            messagebox.showerror("Execution Error", f"An error occurred:\n{e}")
            self.output_label.config(text="Error during execution.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GML_GUI(root)
    root.mainloop()
