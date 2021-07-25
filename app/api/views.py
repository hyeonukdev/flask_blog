from flask import Flask
from flask import request

from app.api import api


@api.route("/api")
def api_test():
    ''' example method '''
    # http://127.0.0.1:5000/api?temp=test
    url = request.url
    params = {
        "a1": "1",
        "a2": "2"
    }
    temp = request.args.get('temp')
    result = url + ' + ' + str(params) + ' + ' + temp
    return result


'''
headers = {"Accept": "application/json", "Content-Type": "application/json"}
req = requests.get(endpoint, params=params, headers=headers)
result = req.json()
'''