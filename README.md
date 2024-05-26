```
 _____ _ _____ _     _   
|  _  |_|   __|_|___| |_ 
|     | |  |  | |_ -|  _|
|__|__|_|_____|_|___|_|  
                                      
    Created by rUv
```
# Ai Gist

Ai Gist is python application designed to help you create and manage GitHub gists effortlessly using the GitHub API. With built-in SQLite for persistence and seamless integration with AI language models (LLMs), Ai Gist offers powerful capabilities for automating your workflow.

## Key Features

- **Easy Gist Management**: Create, update, and list GitHub gists with simple API calls.
- **AI-Powered Interactions**: Utilize advanced AI language models to interpret user messages and perform actions based on responses.
- **SQLite Integration**: Store and manage data locally with SQLite, ensuring persistence and reliability.
- **FastAPI Framework**: Benefit from the high performance and ease of use provided by the FastAPI framework.

Get started quickly by installing the application and running the server to leverage these features for an enhanced coding experience.


## Setup

1. **Create a GitHub Codespace**:
   - Create a new GitHub Codespace for your repository.
   - Ensure your GitHub token is stored as a secret in the Codespace.

2. **Install Dependencies**:
   - The setup script will automatically install necessary dependencies and set up the environment.

3. **Install the Package**:
   - Install the package in editable mode:
     ```bash
     pip install aigist
     ```

4. **Initialize the Database**:
   - Run the database initialization script to create the necessary database and tables:
     ```bash
     python init_db.py
     ```

5. **Run the Application**:
   - Start the FastAPI server using Uvicorn:
     ```bash
     aigist
     ```

## Configuration

- **Environment Variables**:
  - Ensure the following environment variables are set:
    - `GITHUB_TOKEN`: Your GitHub token.
    - `LITELLM_API_BASE`: The base URL for the LiteLLM API.
    - `LITELLM_API_KEY`: Your LiteLLM API key.
    - `LITELLM_MODEL`: The model to use for LiteLLM (e.g., gpt-4o-2024-05-1).

## Endpoints

- **Create Gist**: `POST /gists`
  - **Request Body**:
    ```json
    {
      "description": "Sample Gist",
      "public": true,
      "files": [
        {
          "filename": "sample.txt",
          "content": "This is a sample gist content."
        }
      ]
    }
    ```

- **Update Gist**: `PATCH /gists/{gist_id}`
  - **Request Body**:
    ```json
    {
      "description": "Updated Sample Gist",
      "files": [
        {
          "filename": "sample.txt",
          "content": "This is the updated sample gist content."
        }
      ]
    }
    ```

- **List Gists**: `GET /gists`
  - **Query Parameters**:
    - `page`: The page number (default: 1).
    - `per_page`: The number of gists per page (default: 30, max: 100).
    - `since`: Filter gists created after this date (ISO 8601 format).
    - `until`: Filter gists created before this date (ISO 8601 format).

- **Chat Completion**: `POST /chat`
  - **Request Body**:
    ```json
    {
      "messages": [
        {
          "role": "user",
          "content": "Your message here"
        }
      ],
      "stream": false
    }
    ```

- **Chat Gist**: `POST /chat/gist`
  - **Request Body**:
    ```json
    {
      "messages": [
        {
          "role": "user",
          "content": "Your message here"
        }
      ],
      "stream": false
    }
    ```

## Testing

Run the tests using pytest:
```bash
pytest
```

## Database Setup

To ensure the database and table setup is correct, run the `init_db.py` script:
```bash
python init_db.py
```

### Example JSON Payloads

- **Create Gist**:
  ```json
  {
    "description": "Sample Gist",
    "public": true,
    "files": [
      {
        "filename": "sample.txt",
        "content": "This is a sample gist content."
      }
    ]
  }
  ```

- **Update Gist**:
  ```json
  {
    "description": "Updated Sample Gist",
    "files": [
      {
        "filename": "sample.txt",
        "content": "This is the updated sample gist content."
      }
    ]
  }
  ```

## Chat System

The chat system leverages LiteLLM to interpret user messages and perform actions based on the responses. The endpoint `/chat/gist` handles incoming chat requests, processes them through LiteLLM, and performs actions such as creating or updating gists based on the responses.

### How It Works

1. **Receiving Chat Messages**: The endpoint `/chat/gist` receives a POST request with a list of chat messages.
2. **Calling LiteLLM API**: The `chat_completion` function sends these messages to the LiteLLM API using the GPT-4o model.
3. **Processing the Response**: Based on the `action` field in the response, the endpoint either creates or updates a gist.
4. **Handling Errors**: Any exceptions are caught and a 500 Internal Server Error is returned with the error details.

### LiteLLM Features

LiteLLM offers numerous features that streamline interaction with various LLM providers:

- **Unified Interface**: Supports 100+ LLMs using the same Input/Output format, including OpenAI, Hugging Face, Anthropic, Cohere, and more.
- **Error Handling and Retries**: Automatic error handling and retry mechanism, switching to alternative providers if one fails.
- **Streaming Support**: Efficiently handle memory-intensive tasks by retrieving large model outputs in chunks.
- **Open-Source and Community-Driven**: Benefit from transparency and ongoing development by the open-source community.
- **Reduced Complexity**: Simplifies interactions with different provider APIs.
- **Increased Flexibility**: Allows experimentation with various LLMs.
- **Improved Efficiency**: Saves time with uniform code structure and automated error handling.
- **Cost-Effectiveness**: Optimizes costs by exploring different pricing models across providers.

For more details, refer to the [LiteLLM documentation](https://docs.litellm.ai).
 