import streamlit as st
import os
from slide_reader import slideReader
st.title("Video To Slide Converter")

video = st.file_uploader("Choose the Video File",type=["mp4"])


if video is not None:
    name= video.name
    result_directory = os.path.join('Results',name[0:-4])

    if not os.path.exists(result_directory):
        os.makedirs(result_directory)
    
    
    with open(os.path.join(result_directory, name), "wb") as f:
        f.write(video.getbuffer())
    
    video_path = os.path.join(result_directory,name)

    end_time = st.number_input("End Time (in seconds)", value=0)
    starting_time = st.number_input("Starting Time (in seconds)", value=0)
    
    up = st.number_input("Upper Ratio to be trimmed", value=0)
    down = st.number_input("Lower Ratio to be trimmed", value=0)
    left = st.number_input("Left side to be trimmed", value=0)
    right = st.number_input("Right side to be trimmed", value=0)
    
    
    if st.button("Start Execution"):
        st.write("Executing...")
        st.write("This may take a while")
        slideReader(video_path,result_directory,starting_time,end_time,up,down,left,right)
        os.remove(video_path)
        st.write('Slides Captured and Stored Successfully')


