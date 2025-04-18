import streamlit as st

# 🔧 공통 레이아웃 컴포넌트
def render_layout(title, left_func, col_ratio=(3, 1)):
    with st.container():
        st.markdown(f"### {title}")
        left_col, right_col = st.columns(col_ratio)

        ##  페이지 내용이 들어감
        with left_col:
            left_func()

        ## 오른쪽 사이드바 내용이 들어감
        with right_col:
            st.text("test")
            
            
