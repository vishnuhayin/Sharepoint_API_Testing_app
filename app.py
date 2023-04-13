from flask import Flask, render_template, request, jsonify
import requests
from requests_ntlm import HttpNtlmAuth

app = Flask(__name__)   

'''
if access token is provided
'''
# @app.route('/', methods=['POST','GET'])
# def index():
#     if request.method == 'POST':
#         site_url = request.form['data']
#         accessToken = request.form['token']

#         url = "https://"+site_url+"/_api/web/GetFolderByServerRelativeUrl('/Shared Documents')" #getting folder from shared documents
#         headers = {
#             'Authorization': "Bearer " + accessToken,
#             'Accept':'application/json;odata=verbose'
#         }

#         print(url,",",headers)
#         response = requests.request("GET", url, headers=headers)

#         return jsonify(response)

#     else:
#         return render_template('index.html')
    

    
'''
if username and password are provided
'''    
@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        site_url = request.form['data']
        username = request.form['username']
        password = request.form['password']

        url = "https://"+site_url+"/_api/web/lists/getbytitle('<your_list_name>')/items"#getting item from a list
        cred = HttpNtlmAuth(username, password)
        response = requests.get(url, auth=cred)

        return jsonify(response)

    else:
        return render_template('index.html')
    

if __name__ == "__main__":
    app.run(debug=True)
