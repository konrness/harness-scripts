import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
api_key = os.getenv("API_KEY")
account_id = os.getenv("ACCOUNT_ID")
org_id = os.getenv("ORG_ID")
project_id = os.getenv("PROJECT_ID")

def fetch_pipeline_yaml(account_id, org_id, project_id, pipeline_id):
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key,
        'Load-From-Cache': 'true'
    }
    params = {
        'accountIdentifier': account_id,
        'orgIdentifier': org_id,
        'projectIdentifier': project_id
    }

    print(f" - Requesting pipeline: {pipeline_id}")
    response = requests.get(f"https://app.harness.io/pipeline/api/pipelines/{pipeline_id}", params=params, headers=headers)

    if response.status_code == 200:
      json_response = response.json()
      return json_response['data']['yamlPipeline']
    else:
       print("Error fetching pipeline:", response.json())
       return ""

# Function to fetch pipelines from a single page and append to the pipelines list
def fetch_pipelines(account_id, org_id, project_id, page_size=25, page_number=0):
    
    pipelines = {}

    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }
    params = {
        'accountIdentifier': account_id,
        'orgIdentifier': org_id,
        'projectIdentifier': project_id,
        'page': str(page_number),
        'size': page_size
    }

    more_pages = True
    while more_pages:
      print("Requesting page: " + str(page_number))
      params['page'] = str(page_number)
      response = requests.post('https://app.harness.io/pipeline/api/pipelines/list', params=params, headers=headers)

      if response.status_code == 200:
          json_response = response.json()
          pipeline_list = json_response['data']['content']

          for pipeline in pipeline_list:
            pipelines[pipeline['identifier']] = fetch_pipeline_yaml(account_id, org_id, project_id, pipeline['identifier'])

          # Check if there are more pages
          more_pages = not json_response['data']['last']
          page_number += 1
          
    return pipelines

pipelines = fetch_pipelines(account_id, org_id, project_id)

print(len(pipelines))

print(pipelines[0])