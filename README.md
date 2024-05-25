```                       
 _____ _ _____ _     _   
|  _  |_|   __|_|___| |_ 
|     | |  |  | |_ -|  _|
|__|__|_|_____|_|___|_|  
                                      
    Created by rUv
```
# Ai Gist

This project provides a FastAPI application to create and update GitHub gists using the GitHub API. It includes SQLite for persistence and is designed to run in a GitHub Codespace.

## Setup

1. **Create a GitHub Codespace**:
   - Create a new GitHub Codespace for your repository.
   - Ensure your GitHub token is stored as a secret in the Codespace.

2. **Install Dependencies**:
   - The setup script will automatically install necessary dependencies and set up the environment.

3. **Run the Application**:
   - Start the FastAPI server using Uvicorn:
     ```bash
     uvicorn app.main:app --reload
     ```

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

To ensure the database and table setup is correct, run the `setup_database.sh` script:
```bash
./setup_database.sh
```

To check the database contents, use the `check_db.sh` script:
```bash
./check_db.sh
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

This `README.md` provides comprehensive instructions and examples for using the FastAPI application to manage GitHub gists.
 