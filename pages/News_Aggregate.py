import streamlit as st
from components.layout import render_layout
from components.sidebar import render_sidebar




def test():

    st.title("📄 페이지 2")
    st.write("Test12314")
    

render_sidebar()
render_layout("test", test)