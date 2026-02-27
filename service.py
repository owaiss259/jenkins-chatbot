
import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

load_dotenv()

JENKINS_URL = os.getenv("JENKINS_URL")
USERNAME = os.getenv("JENKINS_USERNAME")
API_TOKEN = os.getenv("JENKINS_API_TOKEN")
JOB_NAME = os.getenv("JOB_NAME")

def trigger_pipeline():
    try:
        print("Getting crumb...")

        crumb_url = f"{JENKINS_URL}/crumbIssuer/api/json"
        crumb_response = requests.get(
            crumb_url,
            auth=HTTPBasicAuth(USERNAME, API_TOKEN)
        )

        print("Crumb status:", crumb_response.status_code)

        if crumb_response.status_code != 200:
            print("Crumb failed:", crumb_response.text)
            return False

        crumb_data = crumb_response.json()
        crumb = crumb_data["crumb"]
        crumb_field = crumb_data["crumbRequestField"]

        print("Triggering job...")

        build_url = f"{JENKINS_URL}/job/{JOB_NAME}/build"

        response = requests.post(
            build_url,
            auth=HTTPBasicAuth(USERNAME, API_TOKEN),
            headers={crumb_field: crumb}
        )

        print("Build status:", response.status_code)
        print("Build response:", response.text)

        return response.status_code in [200, 201]

    except Exception as e:
        print("FULL ERROR:", str(e))
        return False