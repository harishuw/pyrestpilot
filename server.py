import httpx

class Server:

    def __init__(self):
        pass

    def send_request(self, rest_params):
        #headers=httpx.Headers(eval(headers))
        client = httpx.Client()
        method = rest_params.get("method", "GET")
        url = rest_params.get("url", "")
        json_data = rest_params.get("body", "")
        data = rest_params.get("data", {})
        headers = rest_params.get("headers", {})
        kwargs = rest_params.get("kwargs", {})
        for key,value in headers.items():
            if not key:
                headers.pop(key)
                break
        response = client.request(method, url,json=json_data,data=data, headers=headers, **kwargs)
        return response
 