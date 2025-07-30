import time
import concurrent.futures
from splore_sdk.sdk import SploreSDK, AgentSDK


agent_id = "agent_id"
base_id = "base_id"
api_key = "api_key"
save_result = False
file_name = "file_name"


def sdk_test(data):
    try:
        sdk = SploreSDK(api_key=api_key, base_id=base_id)
        agent = sdk.init_agent(agent_id=agent_id)
        # get extracted response
        extracted_response = agent.extract(file_path=data)
        # extracted_response = agent.extractions.start(file_id=data)
        # extracted_response = agent.extractions.processing_status(file_id=data)
        # extracted_response = agent.extractions.extracted_response(file_id=data)
        if save_result:
            with open(f"{file_name}.txt", "w") as f:
                f.write(str(extracted_response))
        return extracted_response
    except Exception as e:
        return f"Error: {e}"


def main():
    print("Starting...")
    data_list = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(sdk_test, data) for data in data_list]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())


if __name__ == "___main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Completed in {time.time() - start:.2f} seconds")
