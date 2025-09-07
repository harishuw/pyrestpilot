import httpx
import os
from local import Local
import streamlit as st
from ui import Ui

class PyRestPilot:
    

    def __init__(self):
        self.ui = Ui()
        self.local = Local()

    def start(self):
        if "headers" not in st.session_state:
            st.session_state["headers"] = [{"":""}]
        if "params" not in st.session_state:
            st.session_state["params"] = [{"":""}]
        if 'show_popup' not in st.session_state:
            st.session_state.show_popup = False
        if 'show_save_popup' not in st.session_state:
            st.session_state.show_save_popup = False
        if 'menu_items' not in st.session_state:
            st.session_state.menu_items = self.load_menu_items()
       
        print(st.session_state.menu_items)
        self.ui.start_page()

       
    def load_menu_items(self):

        menu_list = self.local.list_saved_requests()
        return menu_list
      
      
