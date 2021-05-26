import streamlit as st
from PIL import Image

st.title("Lahore Garrison University")
st.text("Lahore Garrison University is located in the metropolitan city of Lahore")
st.header("Digital Forensics Research and Service Centre")
st.info("This is the first ever Private Digital Forensics and Cyber Security Research centre")

st.subheader("4th Semester")
#a = 5

#Addition application
#st.info("Please enter the number between 0 and 9")
a = st.number_input("Please enter the number between 0 and 9")
b = st.number_input("Please enter another number between 0 and 9")
c = a + b


#a = st.text_input("Please enter the number between 0 and 9")
#b = st.text_input("Please enter another number between 0 and 9")
#c = a + b
st.text("The result after addition is")
st.write(c)

image = Image.open('Type_Error.png')
st.image(image)
