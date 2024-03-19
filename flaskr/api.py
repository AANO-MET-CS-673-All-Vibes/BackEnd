from flask import Flask, request

# response(): returns an API JSON response with the correct status and headers 

def response(json):
    return json, 200, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}

# get_remote_ip(): returns the IP address of the API's caller
# The point of this is to account for proxies like Cloudflare (which I imagine we will end up using)

def get_remote_ip():
    if request.environ.get("HTTP_CF_CONNECTING_IP") is None:
        return request.remote_addr
    else:
        return request.environ.get("HTTP_CF_CONNECTING_IP")
