import os
import streamlit as st
from server import Server

class Ui:

    def __init__(self):
        self.server = Server()
        self.rest_params  = {"method":"","url":"", "params":{}, "body": "", "headers":{}, "files": {}}
        cwd = os.getcwd()
        self.folders = [f for f in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, f))]
        


    def start_page(self):
        self.main()
        self.rest_form()
        self.tabs()
        self.action_button()
        self.footer()

    def main(self):

        st.title("PyRestPilot")
        st.set_page_config(page_title="PyRestPilot")
        st.write("A simple REST API testing tool.")
        self.sidebar()
    
    def rest_form(self):
        method_col, url_col = st.columns([.2, .8])
        with method_col:
            self.rest_params['method'] = st.selectbox("HTTP Method", ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"])
        self.url_placeholder = st.empty()
        with url_col:
            self.rest_params['url'] = st.text_input("URL", "")
        
    def tabs(self):
        param_tab, body_tab, header_tab, file_tab = st.tabs(["Params", "Body", "Headers", "Files"])
      
        self.params = {}
        self.body = ""
        with param_tab:
           self.custom_tab_view("Params")
           
        with body_tab:
            self.rest_params['body'] = st.text_area("Body", "")
            
        with header_tab:
            self.custom_tab_view("Headers")
        

    def param_tab_view(self):  
        headers = {}
        for i,e in enumerate(st.session_state["headers"]):    
            for key, value in e.items():                
                param_col1, param_col2 = st.columns([.4, .6])
                header_key = ""
                header_value = ""
                with param_col1:
                    header_key = st.text_input("Key", key, key=f"header_key_{i}")
                    headers[header_key] = ""
                with param_col2:
                    header_value = st.text_input("Value", value, key=f"header_value_{i}")
                    headers[header_key] = header_value

        if st.button("Add Param"):
            st.session_state["headers"].append({"":""})

    def custom_tab_view(self, tab_name):
        tab_key = tab_name.lower()
        for i,e in enumerate(st.session_state[tab_key]):    
            for key, value in e.items():                
                param_col1, param_col2 = st.columns([.4, .6])
                header_key = ""
                header_value = ""
                with param_col1:
                    header_key = st.text_input("Key", key, key=f"{tab_key}_key_{i}")
                    self.rest_params[tab_key][header_key] = ""
                with param_col2:
                    header_value = st.text_input("Value", value, key=f"{tab_key}_value_{i}")
                    self.rest_params[tab_key][header_key] = header_value

        if st.button(f"Add {tab_name}"):
            st.session_state[tab_key].append({"":""})
            
    def action_button(self):
        if st.button("Send Request"):
            if not self.rest_params['url']:
                self.url_placeholder.error("Please enter a URL.")
                return
            self.url_placeholder.empty()
            response = self.server.send_request(self.rest_params)
            self.display_result(response)
            
    def display_result(self, response):
        st.write(f"Status Code: {response.status_code}")
        st.write("Response Body:")
        response_text = response.text
        response_json = None
        try:
            response_json = response.json()
            st.json(response_json)
        except Exception as e:       
            print(e)
        if not response_json:     
            st.text(response.text)
        else:
            st.json(response_json)
        st.write("Response Headers:")
        st.json(dict(response.headers))
        st.write("Response Cookies:")
        st.json(dict(response.cookies))
        st.write("Request Headers:")
        st.json(dict(response.request.headers))
        st.write(f"Request URL: {response.request.url}")
        st.write(f"Request Method: {response.request.method}")
        if response.history:
            st.write("Redirect History:")
            for resp in response.history:
                st.write(f"{resp.status_code} -> {resp.url}")

    def sidebar(self):
        st.sidebar.title("Saved Items")

    
    def footer(self):
        st.markdown("---")
        st.markdown("Developed by [HUW](https://devappzone.com)")