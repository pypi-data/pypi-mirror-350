from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(
    api_key="YOUR_API_KEY",
    base_id="YOUR_BASE_ID",
)
extraction_agent = sdk.init_agent(agent_id="YOUR_AGENT_ID")
extracted_response = extraction_agent.extract(file_path="file_path")
print("=========================================")
print("Extracted response:", extracted_response)
