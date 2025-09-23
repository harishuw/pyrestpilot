import os
import json

class Local:

    def __init__(self):
        try:
            os.mkdir("saved_requests")   
        except FileExistsError:
            print(f"Folder '' already exists.")
        except Exception as e:
            print(f"An error occurred: {e}")   
        cwd = os.getcwd()
        print(cwd)
        self.folders = [f for f in os.listdir(cwd + "/saved_requests")]
        
    def create_group(self, group_name):
        try:
            os.mkdir(f"saved_requests/{group_name}")   
            self.folders.append(group_name)
            return True
        except FileExistsError:
            print(f"Folder '{group_name}' already exists.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")   
            return False

    def save_request(self, group_name,request_name, rest_params):
        try:
            if group_name not in self.folders:
                created = self.create_group(group_name)
                if not created:
                    return False            
            with open(f"saved_requests/{group_name}/{request_name}.json", "w") as f:
                json.dump(rest_params, f, indent=2)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")   
            return False

    def load_request(self, filename):


        pass

    def delete_request(self, filename):

        pass

    def list_groups(self):
        return self.folders
    
    def list_saved_requests(self):
        group_list = {}
        for folder in self.folders:
            group_list[folder] = {}
            files = os.listdir(f"saved_requests/{folder}")
            for file in files:
                if file.endswith(".json"):
                    file_key = file.rsplit('.', 1)[0]
                    json_data = json.load(open(f"saved_requests/{folder}/{file}"))
                    group_list[folder][file_key] = json_data
        return group_list
        
