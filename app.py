from flask import Flask, render_template, request, jsonify
import requests
from requests_ntlm import HttpNtlmAuth

from website import create_app

app = create_app()   

'''
if access token is provided
'''
@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':

        client_id = request.form['client_id']
        client_secret = request.form['client_secret']
        site_url = request.form['site_url']
        list_name = request.form['list_name']

        tenant =  'allianzms' # e.g. https://tenant.sharepoint.com
        tenant_id = '6e06e42d-6925-47c6-b9e7-9581c7ca302a' # tenant_id of allianzms 
        client_id = client_id + '@' + tenant_id
        
        data = {
            'grant_type':'client_credentials',
            'resource': "00000003-0000-0ff1-ce00-000000000000/" + tenant + ".sharepoint.com@" + tenant_id, # "00000003-0000-0ff1-ce00-000000000000" is a constant used in an add-in that is accessing SharePoint
            'client_id': client_id,
            'client_secret': client_secret,
        }

        headers = {
            'Content-Type':'application/x-www-form-urlencoded'
        }

        url = "https://accounts.accesscontrol.windows.net/tenant_id/tokens/OAuth/2"

        try:
            r = requests.post(url, data=data, headers=headers)
            json_data = json.loads(r.text)
        except:
            print("POST request to get access token failed")
            return render_template('index.html')

        print(json_data) # access token is available inside this

        headers = {
            'Authorization': "Bearer " + json_data['access_token'],
            'Accept':'application/json;odata=verbose',
            'Content-Type': 'application/json;odata=verbose'
        }

        url = "https://tenant.sharepoint.com/sites/TestCommunication/_api/web/lists/getbytitle('"+list_name+"')/items"
        
        try:
            l = requests.get(url, headers=headers)
        except:
            print("GET request to get list data")
            return render_template('index.html')

        return jsonify(l)

    else:
        return render_template('index.html')
    

    
'''
if username and password are provided
'''    
# @app.route('/', methods=['POST','GET'])
# def index():
    # if request.method == 'POST':
    #     site_url = request.form['data']
    #     username = request.form['username']
    #     password = request.form['password']

    #     url = "https://"+site_url+"/_api/web/lists/getbytitle('<your_list_name>')/items"#getting item from a list
    #     cred = HttpNtlmAuth(username, password)
    #     response = requests.get(url, auth=cred)

    #     return jsonify(response)

    # else:
    #     return render_template('index.html')
    

if __name__ == "__main__":
    app.run(debug=True)


# Sample of json_data
# {
# 'token_type': 'Bearer', 
# 'expires_in': '86399', 
# 'not_before': '1605580031', 
# 'expires_on': '1605666731', 
# 'resource': '00000003-0000-0ff1-ce00-000000000000/tenant.sharepoint.com@tenant_id',
# 'access_token': 'eyJ0eyJhdWQiOiIwMDAwMDAw......'
# }