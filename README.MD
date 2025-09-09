# Simple Auth

This is a simple api with an auth implementation built with **FastAPI**.  
This project is built with **FastAPI** and is organized for scalability and maintainability.

## Features

- Modular structure for routes, middlewares, and utilities
- Environment-based configuration
- Virtual environment for dependency isolation

## Project Structure

```
.env                # Environment variables
requirements.txt    # Python dependencies
src/
    main.py         # Application entry point
    routes.py       # API route definitions
    config/         # Configuration files
    constants/      # Constant values
    middlewares/    # Custom middlewares
    modules/        # Application modules
    utils/          # Utility functions
```

## Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/benkwash/simple_python_auth_fastapi.git
    cd simple_python_auth_fastapi
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
    - Copy `.env.example` to `.env` and update values as needed.

5. **Run the application locally:**
    ```sh
    uvicorn src.main:app --reload
    ```

## Usage

- Access the API at `http://localhost:8000`
- Interactive API docs available at `http://localhost:8000/docs`


