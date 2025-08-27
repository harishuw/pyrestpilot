import httpx

class Server:

    def __init__(self):
        pass

    def send_request(self, rest_params):
        #headers=httpx.Headers(eval(headers))
        client = httpx.Client()
        method = rest_params.get("method", "GET")
        url = rest_params.get("url", "")
        data = rest_params.get("body", "")
        headers = rest_params.get("headers", {})
        kwargs = rest_params.get("kwargs", {})
        for key,value in headers.items():
            if key=="":
                headers.pop(key)
                break
        response = client.request(method, url,data=data, headers=headers, **kwargs)
        return response
        print(r.status_code)
        print(r.text)
        print(r.headers)
        print(r.cookies)
        print(r.history)
        print(r.request.headers)
        print(r.request.url)
        print(r.request.method)