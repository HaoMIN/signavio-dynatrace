import requests
import json

# Open the file
with open('_dashboard_temp.json') as file:
    # Load the JSON data
    dashboard_payload = json.load(file)

with open('_au_prod.json') as file:
    # Load the JSON data
    env_parameter_json = json.load(file)

# enviornment url
host = env_parameter_json['host']
validatorEndpoint = "/api/config/v1/dashboards/validator"
createDashboardEndpoint = "/api/config/v1/dashboards"

validatorUrl = host + validatorEndpoint
creatorDashboardUrl = host + createDashboardEndpoint

# staging, token name: dashboard
dashboardAPIToken = env_parameter_json['dashboardAPIToken']

# convert the payload to JSON format
dashboard_payload_json = json.dumps(dashboard_payload)

# header post object
headersPostObject= {
    "Authorization": "Api-Token " + dashboardAPIToken,
    "Content-Type": "application/json"
}

response = requests.post(validatorUrl, headers=headersPostObject, data=dashboard_payload_json)

if (response.status_code == 204):
    response = requests.post(creatorDashboardUrl, headers=headersPostObject, data=dashboard_payload_json)

print(response.status_code)
print(response.text)
