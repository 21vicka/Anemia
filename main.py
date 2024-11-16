import streamlit as st
from streamlit_option_menu import option_menu
import baru, about


#  set_page_config di bagian paling awal setelah import

st.set_page_config(
    page_title="🩸AneMinder",
    layout="wide"  #  layout 'wide'
)


#kelas Multiapp
class Multiapp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):  # parameter self
        with st.sidebar:
            app = option_menu(
                menu_title='AneMinder',
                options=['Prediksi', 'About', ],
                icons=[ 'trophy-fill', 'chat-fill', ],  
                menu_icon='chat-text-fill',
                default_index=0,  
                styles={
                    "container": {"padding": "5!important", "background-color": '#C4DAD2'},  # Perbaikan typo di 'container'
                    "icon": {"color": "#1C4DAD2", "font-size": "23px"},
                    "nav-link": {"color": "black", "font-size": "20px", "text-align": "left", "margin": "0px"},
                    "nav-link-selected": {"background-color": "#16423C"}
                }
            )

        # Pengkondisian untuk menjalankan aplikasi berdasarkan pilihan menu
        #if app == 'Home':
            #home.app()
        if app == 'Prediksi':
            baru.app()
        elif app == 'About':
            about.app()
        #elif app == 'Gaya':
            #gaya_hidup.app()

# Menjalankan aplikasi
app = Multiapp()
app.run()
