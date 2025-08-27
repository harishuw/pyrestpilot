import httpx
import os
import streamlit as st
from ui import Ui

class PyRestPilot:
    

    def __init__(self):
        self.ui = Ui()
        try:
            os.mkdir("saved_requests")   
        except FileExistsError:
            print(f"Folder '' already exists.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def start(self):
        if "headers" not in st.session_state:
            st.session_state["headers"] = [{"":""}]
        if "params" not in st.session_state:
            st.session_state["params"] = [{"":""}]

        
        self.ui.start_page()

       
       
      
      
