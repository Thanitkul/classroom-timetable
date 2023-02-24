import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET
import pandas as pd
from pandas import ExcelWriter

root = tk.Tk()

def open_file():
    global xml_file_path
    xml_file_path = filedialog.askopenfilename(filetypes=[("XML Files", "*.xml")])

def export_file():
    global xml_file_path
    export_file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf"), ("Excel Files", "*.xlsx")])
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    if export_file_path.endswith(".pdf"):
        # export as PDF
        # code to export to PDF
        pass
    elif export_file_path.endswith(".xlsx"):
        # export as Excel
        df = pd.DataFrame(columns=["Element", "Value"])
        for child in root:
            df = df.append({"Element": child.tag, "Value": child.text}, ignore_index=True)
        with ExcelWriter(export_file_path) as writer:
            df.to_excel(writer, index=False)

# create buttons to open file and export file
open_button = tk.Button(root, text="Select XML File", command=open_file)
export_button = tk.Button(root, text="Export", command=export_file)

# grid buttons
open_button.grid(row=0, column=0, padx=10, pady=10)
export_button.grid(row=1, column=0, padx=10, pady=10)

root.mainloop()