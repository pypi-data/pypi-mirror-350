from splore_sdk import SploreSDK
import multiprocessing


def extract_data(api_key, base_id, agent_id, file_path):
    sdk = SploreSDK(api_key=api_key, base_id=base_id)
    extraction_agent = sdk.init_agent(agent_id=agent_id)
    extracted_data = extraction_agent.extract(file_path=file_path)
    print("=========================================")
    print("File Path:", file_path)
    print("Extracted Data:", extracted_data)


if __name__ == "__main__":
    api_key = "YOUR_API_KEY"
    base_id = "YOUR_BASE_ID"
    agent_id = "YOUR_AGENT_ID"
    file_paths = ["absolute_file_path1", "absolute_file_path2"]
    processes = []
    for file_path in file_paths:
        p = multiprocessing.Process(
            target=extract_data, args=(api_key, base_id, agent_id, file_path)
        )
        processes.append(p)
        p.start()
    for p in processes:
        p.join()
