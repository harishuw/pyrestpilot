import os
from local import Local
import streamlit as st
from server import Server

class Ui:

    def __init__(self):
        self.server = Server()
        self.rest_params  = {"method":"","url":"", "params":{}, "body": "", "headers":{}, "files": {}}
        self.local = Local()

    def start_page(self):        
        self.main()
        self.rest_form()
        self.tabs()
        self.action_button()
        self.footer()

    def main(self):
        st.set_page_config(page_title="PyRestPilot")
        if 'page_config_set' not in st.session_state:
            
            st.session_state.page_config_set = True
        st.title("PyRestPilot")        
        st.write("A simple REST API testing tool.")
        self.sidebar()
    
    def rest_form(self):
        method_col, url_col = st.columns([.2, .8])
        methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        
        # Set index for selectbox based on loaded request
        method_index = methods.index(self.rest_params['method']) if self.rest_params['method'] in methods else 0

        with method_col:
            self.rest_params['method'] = st.selectbox("HTTP Method", methods, index=method_index)
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
            self.rest_params['body'] = st.text_area("Body", self.rest_params.get('body', ''))
            
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
        action_col1, action_col2, action_col3 = st.columns([.4, .4, .2])
        with action_col1:
            if st.button("Send Request"):
                if not self.rest_params['url']:
                    self.url_placeholder.error("Please enter a URL.")
                    return
                self.url_placeholder.empty()
                response = self.server.send_request(self.rest_params)
                self.display_result(response)

        with action_col2:
            if st.button("Save Request"):
                st.session_state.show_save_popup = True
            if st.session_state.show_save_popup:
                with st.container(border=True):
                
                # Implement save request functionality here
        
        with action_col3:
            if st.button("Clear"):
                self.rest_params  = {"method":"","url":"", "params":{}, "body": "", "headers":{}, "files": {}}
                st.session_state['params'] = [{"":""}]
                st.session_state['headers'] = [{"":""}]
                
                self.url_placeholder.empty()
                st.rerun()
     
            
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
        st.sidebar.title("Saved Requests")
        with st.sidebar:
            create_folder = st.button("Create Group")
            if create_folder:
                st.session_state.show_popup = True
            if st.session_state.show_popup:
                with st.container(border=True):
                    st.subheader("Enter group Name")
                    new_group_name = st.text_input("Group Name:", key="new_group_input")                    
                    col1, col2 = st.columns(2)                    
                    with col1:
                        if st.button("Save", key="group_save_button"):
                            if new_group_name and new_group_name.strip() not in st.session_state.menu_items.keys():      
                                if self.local.create_group(new_group_name.strip()):                          
                                    st.session_state.menu_items[new_group_name] = {}
                                else:
                                    st.warning("Group already exists.")                                
                                st.session_state.show_popup = False
                                st.rerun() # Rerun to update the menu immediately
                            elif new_group_name.strip() in st.session_state.menu_items.keys():
                                st.warning("Group already exists.")
                            else:
                                st.warning("Please enter a name.")

                    with col2:
                        if st.button("Cancel", key="cancel_button"):
                            # Hide the pop-up without saving
                            st.session_state.show_popup = False
                            st.rerun() # Rerun to hide the pop-up

            for menu, menu_items in st.session_state.menu_items.items():               
                with st.expander(menu):
                    # Assuming menu_items is a dict of {request_name: request_data}
                    for item_name, item_data in menu_items.items():
                        if st.button(item_name, key=f"btn_{menu}_{item_name}"):
                            self._load_request(item_data)
                            st.rerun()

    def _load_request(self, request_data):
        """Loads request data into the UI components."""
        self.rest_params['method'] = request_data.get('method', 'GET')
        self.rest_params['url'] = request_data.get('url', '')
        self.rest_params['body'] = request_data.get('body', '')

        # Update session state for dynamic tabs
        params = request_data.get('params', {})
        st.session_state['params'] = self._convert_dict_to_list_of_dicts(params)
        self.rest_params['params'] = params

        headers = request_data.get('headers', {})
        st.session_state['headers'] = self._convert_dict_to_list_of_dicts(headers)
        self.rest_params['headers'] = headers

    def _convert_dict_to_list_of_dicts(self, data_dict):
        """Converts {'k1':'v1', 'k2':'v2'} to [{'k1':'v1'}, {'k2':'v2'}]."""
        return [{key: value} for key, value in data_dict.items()]

    def footer(self):
        st.markdown("---")
        st.markdown("Developed by [HUW](https://devappzone.com)")