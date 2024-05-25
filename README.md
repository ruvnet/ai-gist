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
- **Update Gist**: `PATCH /gists/{gist_id}`
- **Chat Completion**: `POST /chat`
- **Chat Gist**: `POST /chat/gist`

## Testing

Run the tests using pytest:
```bash
pytest
