from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Create an agent
agent_payload = {"name": "Test Agent", "config": {"key": "value"}}
create_response = sdk.agents.create_agent(agent_payload)
print("Create Agent Response:", create_response)

# Get agent details
agent_id = create_response.get("id")
get_response = sdk.agents.get_agents(agentId=agent_id)
print("Get Agent Response:", get_response)

# get all agents
all_agents = sdk.agents.get_agents()
print("all agents", all_agents)
# Update the agent
update_payload = {"name": "Updated Agent Name"}
update_response = sdk.agents.update_agent(agent_payload=update_payload)
print("Update Agent Response:", update_response)

# Delete the agent
delete_response = sdk.agents.delete_agents(agentId=agent_id)
print("Delete Agent Response:", delete_response)
