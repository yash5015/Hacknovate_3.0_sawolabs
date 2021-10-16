import bs4
import requests
import os
htmlDjango = """
    {% load static %}
    {% csrf_token %}
    <div id="sawo-container" style="height: 300px; width: 300px;"></div>
    <script src="https://websdk.sawolabs.com/sawo.min.js"></script>  
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        const csrfToken = '{{ csrf_token}}';
        var config = {
            containerID: "sawo-container",
            identifierType: "{{sawo.identifier}}",
            apiKey: "{{sawo.auth_key}}",
            onSuccess: (payload) => {
                axios({
                    method:"post",
                    url: "/{{sawo.to}}",
                    data: {payload},
                    headers:{"X-CSRFToken":csrfToken}
                    })
                .then((res)=>{
                    location.reload()
                })
            },
        };
        var sawo = new Sawo(config);
        sawo.showForm();
    </script>
"""

html = """
    <div id="sawo-container" style="height: 300px; width: 300px;"></div>
    <script src="https://websdk.sawolabs.com/sawo.min.js"></script>  
    <script src="https://unpkg.com/axios/dist/axios.min.js"></script>
    <script>
        const csrfToken = '{{ csrf_token}}';
        var config = {
            containerID: "sawo-container",
            identifierType: "{{sawo.identifier}}",
            // Add the API key copied from 2nd step
            apiKey: "{{sawo.auth_key}}",
            onSuccess: (payload) => {
                axios({
                    method:"post",
                    url: "/{{sawo.to}}",
                    data: {payload},
                    headers:{"X-CSRFToken":csrfToken}
                    })
                .then((res)=>{
                    location.reload()
                })
            },
        };
        var sawo = new Sawo(config);
        sawo.showForm();
    </script>
"""

def createTemplate(file_path,flask=False):
    txt = html if flask else htmlDjango
    # with open(file_path+"/_sawo.html", "w") as outf:
    #     outf.write(str(txt))
    PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
    main=os.path.join(PROJECT_PATH,file_path)
    try:
        os.makedirs(main)
        p=file_path+"/_sawo.html"
        f = open(p, "a")
        f.write(txt)
        f.close()
    except:
        pass

def getContext(data,location):
    arr = data[:1]
    auth_key = arr[0].api_key
    identifier = arr[0].identifier
    context = {
        "auth_key":auth_key,
        "identifier":identifier,
        "to":location
    }
    return context

def verifyToken(payload):
    if payload != {}:
        data = {'user_id': payload["user_id"]}
        res = requests.post('https://api.sawolabs.com/api/v1/userverify/', data=data)
        if res.status_code == 200:
            response_data = res.json()
            if response_data['verification_token'] == payload['verification_token']:
                return True
            else:
                return False
        else:
            return False
    else:
        return False
