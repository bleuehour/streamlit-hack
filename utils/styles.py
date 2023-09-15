import streamlit as st
def styles():

    st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"]{
        min-width: 531px;
    }
    """,
    unsafe_allow_html=True,
)   
