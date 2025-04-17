import streamlit as st

page = st.sidebar.radio("페이지 선택", ["홈", "페이지1", "페이지2"])

if page == "홈":
    st.write("🏠 홈입니다.")
elif page == "페이지1":
    st.write("📄 페이지1입니다.")
elif page == "페이지2":
    st.write("📄 페이지2입니다.")