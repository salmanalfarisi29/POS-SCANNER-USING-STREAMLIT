import streamlit as st
from PIL import Image
def main_page():
    Original_Image = Image.open("img/kopma logo.png")
    img = Original_Image
    st.title("Praktikum 6 Pengantar Sistem Informasi")
    
    st.header("Profile")
    with st.container():
        col1, col2 = st.columns([9,3])
        with col1:
            st.write('MUHAMAD FARID AKBAR', '| SALMAN ALFARISI')
            st.write('PROGRAM STUDI', 'D3 TEKNIK INFORMATIKA')
            st.write('KELAS', '2B')
        with col2:
            st.image(img)
if __name__ == '__main__':
	main_page()