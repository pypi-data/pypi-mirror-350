import requests
from requests import Response 
from enum import Enum

# HTTP STATUS MESSAGE

GET: str                 = "200: Get"                              # HTTP 200
POST  : str              = "201: Created"                          # HTTP 201
UPDATE: str              = "203: Non-Authoritative Information"    # HTTP 203
DELETE: str              = "204: No Content"                       # HTTP 204
ERROR_BAD_REQUEST: str   = "400: Bad Request"                      # HTTP 400
ERROR_NOT_FOUND: str     = "404: Not Found"                        # HTTP 404


class HTTP_Method(Enum):
    GET     = 0
    POST    = 1
    PUT     = 2
    DELETE  = 3
    
    
def fetch(
    url: str, 
    method: HTTP_Method = HTTP_Method.GET,
    request_headers: dict = {"Content-Type": "application/json"}, 
    request_dict: dict={}) -> Response:
    
    """sumary_line
    
    外部通信を行う:
    引数:
        url -- HTTPリクエストを送信する先の（エンドポイント）URL
        method --  HTTPリクエストメソッド Default: HTTP_Method.GET
        request_headers -- リクエストヘッダー Default:  {"Content-Type": "application/json"}
        request_dict -- dict
    戻り値: 
        Responce
    """
    
    match method:
        case HTTP_Method.GET:
            response = requests.get(url, 
                                    json=request_dict, 
                                    headers=request_headers)
            return response
        
        case HTTP_Method.POST:
            response = requests.post(url, 
                                     json=request_dict, 
                                     headers=request_headers)
            return response
        
        case HTTP_Method.PUT:
            response = requests.put(url, 
                                    json=request_dict, 
                                    headers=request_headers)
            return response
        
        case HTTP_Method.DELETE:
            response = requests.delete(url, 
                                       json=request_dict, 
                                       headers=request_headers)
            return response
        
        case _:
            pass