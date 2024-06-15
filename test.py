import streamlit as st
import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd
import shutil

#
# shutil.make_archive('img', 'zip', 'img')
#
# # with st.sidebar:
# #     root = tk.Tk()
# #     root.withdraw()
# #     root.wm_attributes('-topmost', 1)
# #     st.write('Please select a folder:')
# #     clicked = st.button('Browse Folder')
# #
# # if clicked:
# #     dirname = str(filedialog.askdirectory(master=root))
# #     pdf_reports = [file for file in os.listdir(dirname) if file.endswith('.jpg')]
# #     output = pd.DataFrame({"File Name": pdf_reports})
# #     st.table(output)

with open(f"img_labels.zip", "rb") as fp:
    btn = st.download_button(
        label="Download ZIP",
        data=fp,
        #on_click=click(),
        file_name='mizip.zip',
        mime="application/zip",
        key='button_zip'
    )