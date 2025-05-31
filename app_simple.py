import streamlit as st
import os

st.title("Simple Streamlit App")
st.write("This is a test app to verify basic deployment.")

# Add a simple interactive element to ensure the app is running
user_input = st.text_input("Enter some text:")
if user_input:
    st.write(f"You entered: {user_input}")
