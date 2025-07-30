from splore_sdk import SploreSDK
from splore_sdk.utils.markdown_converter import md_to_html

# Initialize SDK with API key, base_id from splore console
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Initialize Agent for extraction
extraction_agent = sdk.init_agent(agent_id="YOUR_AGENT_ID")

# basic extraction flow
extracted_data = extraction_agent.extract(file_path="absolute_file_path")
print("Extracted Data:", extracted_data)

# get all extracted response
response = extraction_agent.extractions.all_extracted_response()
print("All Extracted Response:", response)

# Upload file
file_response = extraction_agent.file_uploader.upload_file(
    file_path="absolute_file_path"
)

file_id = file_response.get("fileId")
print("File uploaded with ID:", file_id)

# Start extraction
start_response = extraction_agent.extractions.start(file_id=file_id)
print("Extraction started:", start_response)

# Check processing status
status_response = extraction_agent.extractions.processing_status(file_id=file_id)
print("Processing status:", status_response)

# Get extracted response
extracted_data = extraction_agent.extractions.extracted_response(file_id=file_id)
markdown_texts = map(lambda x: md_to_html(x[response]), extracted_data)
print("Extracted Data:", markdown_texts)
