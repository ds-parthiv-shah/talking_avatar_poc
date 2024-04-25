import requests
import json
from time import sleep

def get_response(input_text):

    url = "https://api.d-id.com/talks"

    payload = {
    "script": {
        "type": "text",
        "input":input_text
    },
    "source_url": "https://portalqa.integrari.com/documents/375190901/508284645/Banker+Avatar.jpg"
    
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": 'Basic YWpheS5wYW5kZXlAcGFuYW1heGlsLmNvbQ:GsoBd5nvjTOCNtntgRi8J'
    }

    response = requests.post(url, json=payload, headers=headers)
    res = json.loads(response.text)
    id = str(res['id'])
    return id


def check_video_generation_status(id):
    url = f"https://api.d-id.com/talks/{id}"
    headers = {"accept": "application/json",
            "authorization": 'Basic YWpheS5wYW5kZXlAcGFuYW1heGlsLmNvbQ:GsoBd5nvjTOCNtntgRi8J'}
    max_retries = 10
    retries = 0
    while retries < max_retries:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            status = response.json().get("status")
            if status == "started":
                print("Video generation is still pending. Retrying in 5 seconds...")
                sleep(5)
                retries += 1
            elif status == "done":
                print("Video generation completed successfully!")
                #print(response.text)
                return response.text
            else:
                print("Unexpected status:", status)
                print(response.text)
                return False
        else:
            print("Error checking status:", response.status_code)
            return False

    print("Timeout: Video generation took too long.")
    return False


  
        

# # Example usage
# url = response['result_url']
# destination = "examplefile.mp4"
# download_file(url, destination)


#Example get response
# url = "https://api.d-id.com/talks/"+id

# headers = {"accept": "application/json",
#            "authorization": 'Basic cGFydGhpdi5zaGFoQHBhbmFtYXhpbC5jb20:j_eiX_LyeB4hp3oe75cc6'}

# response = requests.get(url, headers=headers)
# print(response)


