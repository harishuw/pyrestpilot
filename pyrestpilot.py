import httpx
import os
from local import Local
import streamlit as st
from ui import Ui

class PyRestPilot:
    

    def __init__(self):
        if "rest_params" not in st.session_state:
            st.session_state["rest_params"] = {"method":"", "url":"", "data":[{"": ""}], "body": "", "headers":[{"":""}], "files": [{"":""}]}         
        if "headers" not in st.session_state:
            st.session_state["headers"] = [{"":""}]
        if "data" not in st.session_state:
            st.session_state["data"] = [{"":""}]
        if "files" not in st.session_state:
            st.session_state["files"] = [{"":""}]    
        if 'show_popup' not in st.session_state:
            st.session_state.show_popup = False
        if 'show_save_popup' not in st.session_state:
            st.session_state.show_save_popup = False
        if 'menu_items' not in st.session_state:
            st.session_state.menu_items = self.load_menu_items()
        self.ui = Ui()
        

    def start(self):    
        self.ui.start_page()
       
    def load_menu_items(self):
        self.local = Local()
        menu_list = self.local.list_saved_requests()
        return menu_list
      
      