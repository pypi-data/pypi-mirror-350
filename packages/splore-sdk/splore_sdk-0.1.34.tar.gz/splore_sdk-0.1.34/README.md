# Splore Python SDK  

The Splore Python SDK simplifies the process of interacting with the Splore document processing platform. Use it to upload files, process documents, and retrieve extracted data with minimal setup.

---

## 📌 Table of Contents  

- [Features](#features)  
- [Installation](#installation)  
- [Getting Started](#getting-started)  
- [Modules Overview](#modules-overview)  
  - [Agent Management](#agent-management)  
  - [Extractions](#extractions)  
  - [File Upload](#file-upload)  
  - [Search](#search)  
  - [Utility Functions](#utility-functions)
- [Advanced Usage](#advanced-usage)  
- [FAQ](#faq)  
- [Support](#support)  
- [License](#license)  
- [Testing Across Python Versions](#testing-across-python-versions)

---

## 🚀 Features  

- **Agent Management**: Create, update, retrieve, and delete agents.  
- **File Upload**: Upload documents for processing.  
- **Extractions**: Extract structured data from documents.  
- **Search**: Perform web searches and retrieve search history.  
- **AWS S3 Integration**: Process files directly from S3.  
- **Task Monitoring**: Track the progress of extraction jobs.  
- **Error Handling**: Provides meaningful errors and retry mechanisms.  
- **Python 3.7+ Compatibility**: tested supported version after 3.7.17 can be used for python 3.7 and above.

---

## 📥 Installation  

Install the SDK via pip:  

```bash
pip install splore-sdk
```

For optional example dependencies:  

```bash
pip install splore-sdk[examples]
```

---

## 🏁 Getting Started  

### Prerequisites  

1. **API Key and Base ID**: Obtain these from the Splore console.  
2. **Python 3.7+**: Ensure Python is installed.  

### Quick Start Example

```python
from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Initialize Agent for extraction
extraction_agent = sdk.init_agent(agent_id="YOUR_AGENT_ID")

try:
    # Basic extraction flow with custom polling timeout
    # Set max_poll_timeout to 300 seconds (5 minutes)
    extracted_response = extraction_agent.extract(
        file_path="absolute_file_path",
        max_poll_timeout=300  # 5 minutes
    )
    print("Extraction completed successfully:", extracted_response)
except TimeoutError as e:
    print(f"Extraction timed out after 5 minutes: {str(e)}")
    # Handle timeout - e.g., retry or notify user
except Exception as e:
    print(f"An error occurred during extraction: {str(e)}")
    # Handle other potential errors
```

---

## 📦 Modules Overview  

### 🔹 [Agent Management](#agent-management)  

Manage agents for document processing.  

#### Example Usage  

```python
from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Create an agent
agent_payload = {"name": "Test Agent", "config": {"key": "value"}}
create_response = sdk.create_agent(agent_payload)
print("Create Agent Response:", create_response)

# Get agent details
agent_id = create_response.get("id")
get_response = sdk.agents.get_agents(agentId=agent_id)
print("Get Agent Response:", get_response)

# Get all agents
all_agents = sdk.agents.get_agents()
print("All Agents:", all_agents)

# Update the agent
update_payload = {"name": "Updated Agent Name"}
update_response = sdk.agents.update_agent(agent_payload=update_payload)
print("Update Agent Response:", update_response)

# Delete the agent
delete_response = sdk.agents.delete_agents(agentId=agent_id)
print("Delete Agent Response:", delete_response)
```

### 🔹 [Extractions](#extractions)  

Handle document processing and extraction.  

#### Example Usage

```python
from splore_sdk import SploreSDK
from splore_sdk.utils.decorators import poll_with_timeout

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Get all agents
agents = sdk.agents.get_agents()
agent_id = agents[0]["id"]  # Adjust as needed

# Initialize agent
extraction_agent = sdk.init_agent(agent_id=agent_id)

# Upload file
upload_response = extraction_agent.file_uploader.upload_file(file_path="path/to/file.pdf")
file_id = upload_response
print("File uploaded with ID:", file_id)

# Using polling_with_timeout to monitor indexing status
@poll_with_timeout(
    condition=lambda resp: resp.get("fileProcessingStatus") == "INDEXED",
    max_timeout=300,  # 5 minutes
    min_poll_interval=10,
    max_poll_interval=60
)
def check_indexing_status(file_id):
    return extraction_agent.extractions.processing_status(file_id)

try:
    indexing_status = check_indexing_status(file_id)
    print("File indexing completed successfully")
except TimeoutError as e:
    print(f"Indexing timed out: {str(e)}")
    # Handle timeout - e.g., retry upload or notify user

# Start extraction
extraction_agent.extractions.start(file_id=file_id)

# Using polling_with_timeout to monitor extraction status
@poll_with_timeout(
    condition=lambda resp: resp.get("file", {}).get("status") == "COMPLETED",
    max_timeout=600,  # 10 minutes
    min_poll_interval=15,
    max_poll_interval=90
)
def check_extraction_status(file_id):
    return extraction_agent.extractions.processing_status(file_id)

try:
    extraction_status = check_extraction_status(file_id)
    print("Extraction completed successfully")
    # Retrieve extracted data
    extracted_data = extraction_agent.extractions.extracted_response(file_id=file_id)
    print("Extracted Data:", extracted_data)
except TimeoutError as e:
    print(f"Extraction timed out: {str(e)}")
    # Handle timeout - e.g., retry extraction or notify user
```
#### Example of re-running extraction with existing extraction_id
```python
from splore_sdk import SploreSDK
from splore_sdk.utils.decorators import poll_with_timeout

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Get all agents
agents = sdk.agents.get_agents()
agent_id = agents[0]["id"]  # Adjust as needed

# Initialize agent
extraction_agent = sdk.init_agent(agent_id=agent_id)

extraction_id = "existing_extraction_id"
retried_extraction = extraction_agent.extractions.start_extraction_by_extraction_id(extraction_id)
print("Retried Extraction Response:", retried_extraction)

# Get extraction details by extraction_id
extraction_details = extraction_agent.extractions.get_extraction_by_extraction_id(extraction_id)
print("Extraction Details:", extraction_details)
```

#### Example of retry_extraction
```python
from splore_sdk import SploreSDK
from splore_sdk.utils.decorators import poll_with_timeout

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Get all agents
agents = sdk.agents.get_agents()
agent_id = agents[0]["id"]  # Adjust as needed

# Initialize agent
extraction_agent = sdk.init_agent(agent_id=agent_id)

# Example of retrying extraction using retry_extraction method
extraction_id = "existing_extraction_id"

# Start retrying extraction
retried_extraction = extraction_agent.retry_extraction(extraction_id, max_poll_timeout=600)  # 10 minutes timeout
print("Retry Extraction Response:", retried_extraction)
```

### 🔹 [Search](#search)  

**Beta Feature** - The search API is currently in beta and its signature may change in future releases.

Perform web searches and manage search history.  

#### Example Usage

```python
from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Initialize agent
agent_id = "YOUR_AGENT_ID"
search_agent = sdk.init_agent(agent_id=agent_id)

# Perform a search
search_results = search_agent.search.search(query="artificial intelligence", count=5, engine="google")
print("Search Results:", search_results)

# Get search history
history = search_agent.search.get_history(page=0, size=10)
print("Search History:", history)
```

### 🔹 [File Upload](#file-upload)  

Upload files to Splore for processing.  

#### Example Usage

```python
from splore_sdk import SploreSDK

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Upload file with metadata
metadata = {
    "file_name": "document.pdf",
    "custom_extraction": "false",
    "is_data_file": "true"
}

with open("path/to/file.pdf", "rb") as file:
    response = sdk.file_uploader.upload_file(file_stream=file, metadata=metadata)
    print("Upload Response:", response)
```

### 🔹 [AWS Integration](#aws-integration)  

Download files from AWS S3 for extraction.  

#### Example Usage

```python
from splore_sdk import SploreSDK
from examples.aws import download_from_s3

# Initialize SDK
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Initialize extraction agent
extraction_agent = sdk.init_agent(agent_id="YOUR_AGENT_ID")

# Create a temporary file destination
file_ref = sdk.file_uploader.create_temp_file_destination(file_extension=".pdf")
s3_uri = "s3://abc/def/abc.pdf"

# Download file from S3
download_from_s3(s3_uri, file_ref)

# Start extraction
response = extraction_agent.extract(file_path=file_ref)
print("Extraction Response:", response)
```

### 🔹 [Utility Functions](#utility-functions)

Helper functions to simplify common tasks.

#### Markdown to HTML Conversion

Convert markdown content to HTML using the `md_to_html` utility function.

```python
from splore_sdk.utils import md_to_html

# Basic usage
html = md_to_html("# Hello World")
print(html)  # Output: <h1>Hello World</h1>

# Convert markdown with multiple features
markdown_text = """
# Title

This is a **bold** text with *italic* formatting.

1. Ordered list item
2. Another item

> Blockquote example
"""

html = md_to_html(markdown_text)
print(html)
```

#### Advanced Usage with MarkdownConverter

For more control over the conversion process, use the `MarkdownConverter` class.

```python
from splore_sdk.utils import MarkdownConverter

# Create a converter instance
converter = MarkdownConverter()

# Convert with specific extensions
html = converter.convert(
    markdown_text,
    extensions=['extra', 'codehilite', 'toc'],
    extension_configs={
        'codehilite': {
            'linenums': True,
            'css_class': 'highlight'
        }
    },
    safe_mode=True
)

# Save to file
with open("output.html", "w") as f:
    f.write(html)
```

#### Formatting Extracted Responses

Use markdown to format extracted data into well-structured documents:

```python
# Initialize SDK with API key, base_id from splore console
sdk = SploreSDK(api_key="YOUR_API_KEY", base_id="YOUR_BASE_ID")

# Initialize Agent for extraction
extraction_agent = sdk.init_agent(agent_id="YOUR_AGENT_ID")

# Get extracted response
extracted_data = extraction_agent.extract(file_path="absolute_file_path")

# Convert extracted responses to HTML
markdown_texts = map(lambda x: md_to_html(x["response"]), extracted_data)
print("Extracted Data:", markdown_texts)
```

### Decorator Examples

#### retry_with_timeout Example
```python
from splore_sdk.utils.decorators import retry_with_timeout

# Function that might fail
@retry_with_timeout(max_retries=3, backoff_factor=1, max_timeout=10)
def fetch_data(url):
    """Fetch data with retry logic"""
    try:
        # Simulate network request
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Request failed: {str(e)}")
        raise

# Usage
try:
    data = fetch_data("https://api.example.com/data")
    print("Data fetched successfully:", data)
except Exception as e:
    print(f"Failed to fetch data after retries: {str(e)}")
```

#### poll_with_timeout Example
```python
from splore_sdk.utils.decorators import poll_with_timeout

# Function that needs polling
@poll_with_timeout(
    condition=lambda resp: resp.get("status") == "COMPLETED",
    max_timeout=30,  # 30 seconds
    min_poll_interval=2,  # 2 seconds
    max_poll_interval=5  # 5 seconds
)
def check_status(task_id):
    """Check task status with polling"""
    # Simulate status check
    status = get_task_status(task_id)
    print(f"Current status: {status}")
    return status

# Usage
try:
    final_status = check_status("task123")
    print("Task completed successfully")
except TimeoutError as e:
    print(f"Task monitoring timed out: {str(e)}")
```

---

## ⚙️ Advanced Usage  

### 🔸 Polling Interval Configuration  

Customize the polling interval for extraction status checks.  

```python
while True:
    status = sdk.extractions.processing_status(file_id=file_id)
    if status.get("fileProcessingStatus") == "COMPLETED":
        break
    sleep(5)  # Set custom polling interval
```

### 🔸 Error Handling  

Handle errors gracefully for better debugging.  

```python
try:
    sdk.extractions.upload_file("path/to/file.pdf")
except Exception as e:
    print("Error uploading file:", str(e))
```

### 🔸 Python 3.7 Compatibility  

The SDK now supports Python 3.7 and above.

---

## ❓ FAQ  

### 1️⃣ How do I get an API Key?  
Sign up on the Splore console and navigate to the API section to generate a key.  

### 2️⃣ Can I use this SDK asynchronously?  
Asynchronous support will be added in a future release.  

### 3️⃣ Which file formats are supported?  
Currently, only **PDF files** are supported.  

### 4️⃣ How do I handle search functionality?  
The SDK provides a dedicated `search` capability that allows you to perform web searches and manage search history. Use the `search.search()` method to perform searches and `search.get_history()` to retrieve search history.  

### 5️⃣ How do I check the SDK version?  
```python
from splore_sdk import __version__
print("Splore SDK Version:", __version__)
```

---

## 🔗 Support  

For any questions or issues, please:  

- Open a ticket on [GitHub Issues](https://github.com/splorehq/splore-sdk-py/issues)  
- Email us at **support@splore.com**  

---

## 📜 License  

This SDK is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Testing Across Python Versions

This package supports Python 3.7 through 3.13. We use different build systems based on the Python version:

- **Python 3.7**: Uses setuptools (via setup.py)
- **Python 3.8+**: Uses PDM (via pyproject.toml)

### Available Python Versions

The testing scripts are configured to work with the following Python versions:
- 3.7.17
- 3.8.20
- 3.9.4
- 3.10.16
- 3.11.11
- 3.12.0/3.12.9
- 3.13.2

### Running Tests

1. Ensure you have [pyenv](https://github.com/pyenv/pyenv) installed to manage Python versions
2. The testing script will automatically detect which of the above versions are installed on your system

3. Run the test script which will automatically detect and test all available Python versions:
   ```bash
   # Run tests on all available Python versions
   ./test_all_versions.sh
   ```

For testing only on Python 3.7:

```bash
# Test Python 3.7 using a direct approach with virtualenv (recommended)
./test_py37_direct.sh

# Or test Python 3.7 using a custom tox approach
./test_py37_tox.sh
```

For testing on specific Python versions:

```bash
# Test specific Python versions with tox
tox -e py38,py39,py310 --skip-missing-interpreters
```

### Known Issues

- Python 3.7 requires special handling due to syntax incompatibilities with newer pip versions
- Virtual environments must be created with the correct Python binary to avoid issues
- The scripts now detect installed Python versions to avoid errors with missing interpreters
- Direct testing approach is recommended for Python 3.7 as it's more reliable than using tox
