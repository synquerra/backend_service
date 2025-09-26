# Project Setup Guide

## Prerequisites
Ensure you have the following installed on your system:
- Python
- Virtual Environment (`venv`)
- Uvicorn (for running the FastAPI application)

## Setting Up the Virtual Environment

### 1. Navigate to your project directory
Run the following command:
```sh
cd path/to/your/project
```

### 2. Create a virtual environment
Run the following command:
```sh
python -m venv .venv
```

### 3. Activate the Virtual Environment
Run the following command:
```sh
source .venv/Scripts/activate
```

### 4. Set the Path If Required (Optional, for Persistent Environment)
Run the following command to set the path permanently:
```sh
setx PATH "<C:\Python\apaar_backend_api\>.venv\Scripts;%PATH%"
```

## Installing dependencies

### Option 1 : Without Virtual Environment via python CLI
Run the following command:
```sh 
pip install -r requirements.txt
```

### Option 2 : With Virtual Environment via python CLI
Run the following command:
```sh 
.venv/Scripts/python -m pip install -r requirements.txt
```

## Running the Application

### Option 1: Using Uvicorn Directly
```sh
uvicorn app.main:app --reload
```

### Option 2: Using  Virtual Environment to Run Uvicorn
```sh
.venv/Scripts/python -m uvicorn app.main:app --reload
```

## 5: Run UnitTestCases
### Using  Virtual Environment
Run the following command:
```sh 
.venv/Scripts/python -m pytest

Example Result
collected 2 items
Ran 2 tests in 0.000s
=============== 2 passed, 3 warnings in 0.66s ==================
All tests passed. Proceeding with push.

```

## 6 Setup PyTest via git CLI (Optional)
### Using git bash command
#### 1. Create a Git Hook for Pre-Push
```sh
cd .git/hooks/
```
#### 2. Touch and Set Permission in Hook
```sh
touch pre-push
chmod +x pre-push
```
#### 3. Copy and Paste following code in Pre-Push git file
```sh
#!/bin/bash
echo "Running tests before push..."
.venv/Scripts/python -m pytest
if [ $? -ne 0 ]; then
    echo "Tests failed! Fix errors before pushing."
    exit 1
fi
echo "All tests passed. Proceeding with push."
```
#### 4. Close and reopen git bash
## Test Case Setup Done with git



## Notes
- This will start the FastAPI application and enable live reloading.
- Make sure the virtual environment (`.venv`) is activated before running the application.
- If you encounter issues, check your Python and Uvicorn installations.
- UnitTestCases is mandatory for all methods

---
