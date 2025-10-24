# FastAPI and Vue.js Login Demo

This project demonstrates a simple login application using FastAPI for the backend and Vue.js for the frontend. Below are the instructions for setting up and running both parts of the application.

## Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   Make sure you have Node.js and npm installed. Run the following command to install the required packages:
   ```bash
   npm install
   ```

3. **Run the Vue.js application**:
   Start the development server:
   ```bash
   npm run serve
   ```
   The application will be available at `http://localhost:8081` (vite dev server is configured to run on port 8081 in `vite.config.js`).

## Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   Make sure you have Python and pip installed. Run the following command to install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the FastAPI application**:
   Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn app.main:app --reload --port 9000
   ```
   The API will be available at `http://localhost:9000`.

## Linking Vue.js with FastAPI

To connect the Vue.js frontend with the FastAPI backend, follow these steps:

1. **CORS Configuration**:
   Ensure that CORS is set up in the FastAPI application to allow requests from the Vue.js frontend. This is typically done in `main.py`.

2. **HTTP Requests**:
   Use Axios or the Fetch API in your Vue.js components (e.g., `Login.vue`) to make HTTP requests to the FastAPI endpoints for user authentication.

3. **Testing**:
   After both servers are running, you can test the login functionality by navigating to the Vue.js application in your browser and submitting the login form.

## Project Structure

- **backend/**: Contains the FastAPI backend code.
- **frontend/**: Contains the Vue.js frontend code.

This project serves as a basic template for building applications that require user authentication using FastAPI and Vue.js.