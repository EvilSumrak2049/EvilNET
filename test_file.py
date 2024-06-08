import streamlit as st
import time

progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)
count = 200
perc = count//100
k = 1
i=0
while i < count:
    if i > perc * k:
        my_bar.progress(k, text=progress_text)
        time.sleep(0.1)

        k+=1
    i+=1
my_bar.empty()
print(st.session_state)
st.button("Rerun")