import streamlit as st

page = st.sidebar.radio("")

if page == "홈":
    st.write("🏠 홈입니다.")
elif page == "페이지1":
    st.write("📄 페이지1입니다.")
elif page == "페이지2":
    st.write("📄 페이지2입니다.")
    
#사이드바에 검색 옵션 구성
st.sidebar.header("검색 옵션")
search_query = st.sidebar.text_input("검색어", "파이썬")
display_count = st.sidebar.slider("검색 결과 수", 10, 100, 50)