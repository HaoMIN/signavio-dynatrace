import requests
import json
import dynatrace
from dynatrace.environment_v2.settings import SettingsObject, SettingsObjectCreate

with open('_au_prod.json') as file:
    # Load the JSON data
    env_parameter_json = json.load(file)

# enviornment url
host = env_parameter_json['host']
validatorEndpoint = "/api/config/v1/calculatedMetrics/service/validator"
creatMetricEndpoint = "/api/config/v1/calculatedMetrics/service"

validatorUrl = host + validatorEndpoint
creatMetricUrl = host + creatMetricEndpoint

# staging, token name: dashboard
dashboardAPIToken = env_parameter_json['dashboardAPIToken']

def __update_metric_meta():
  # Define the JSON payload for metric metadata
  baseUrl = host
  dtClient = dynatrace.Dynatrace(baseUrl, dashboardAPIToken)

  payload_updateTag = {
    "description": "metric for apigw outing calls to global server",
    "tags": ["suiteapigw"],
    "unit": "COUNT"
  }

  settings_object_metric_meta = SettingsObjectCreate(schema_id="builtin:metric.metadata", value=payload_updateTag, scope=f"metric-calc:service.apigw_out_all_script")
  dtClient.settings.create_object(
    validate_only=False, body=settings_object_metric_meta)

# Define the JSON payload
with open('_metric_temp.json') as file:
    # Load the JSON data
    calMetric_payload = json.load(file)

# Convert the payload to JSON format
payload_json_cal_metric = json.dumps(calMetric_payload)

# header post object
headersPostObject = {
    "Authorization": "Api-Token " + dashboardAPIToken,
    "Content-Type": "application/json"
}

response = requests.post(validatorUrl, headers=headersPostObject, data=payload_json_cal_metric)

if (response.status_code == 204):
   response = requests.post(creatMetricUrl, headers=headersPostObject, data=payload_json_cal_metric)
   response_json = response.json()
   if (response.status_code == 400 and any(violation['message'] == 'TsmMetricKey already defined' for violation in response_json['error']['constraintViolations'])):
      print('Ignoring metric exists error')
   else:
    __update_metric_meta()
    print(response.text)
else:
    print(response.text)





