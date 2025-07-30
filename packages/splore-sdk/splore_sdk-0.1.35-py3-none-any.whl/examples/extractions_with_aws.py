from splore_sdk import SploreSDK
from examples.aws import download_from_s3

##  example -1 (basic flow to complete extraction using S3)

# Initialize SDK with API key, base_id from splore console
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# you can get agent id from agents module. (check agents example)
extraction_agent = sdk.init_agent(agent_id="YOUR_AGENT_ID")

# create a temporary file destination to download file from s3.
file_ref = sdk.file_uploader.create_temp_file_destination(file_extension=".pdf")
s3_uri = "s3://abc/def/abc.pdf"
download_from_s3(s3_uri, file_ref)
response = extraction_agent.extract(file_path=file_ref)
print(response)
