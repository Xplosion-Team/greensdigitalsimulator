# 🧠 Greens Digital Twin Brain API Summary

This document provides a high-level overview of the available endpoints in the Greens Digital Twin Brain API.

## Base URL

`http://localhost:8000` (Local Development)

## Endpoints

### 1. Root & Health

- **GET `/`**: Connectivity check.
- **GET `/health`**: System health status.

### 2. Brain Interactions

- **POST `/v1/brain/query`**: The primary interaction loop.
  - **Body**:

    ```json
    {
      "text": "What is my glucose prediction?",
      "current_glucose": 115.0,
      "digital_twin_id": 1,
      "provider": "openai" (optional)
    }
    ```

  - **Response**: Includes an AI-generated explanation and simulation data for graphing.

### 3. Integrations

- **POST `/v1/brain/sms`**: Twilio SMS webhook for mobile-to-brain messaging.

## Authentication

Currently, the API relies on environment-level keys (e.g., `OPENAI_API_KEY`) and does not require per-request auth headers in its current state.

## CORS

Enabled for:

- `http://localhost:8080`
- `http://localhost:5173`
- `lovable.dev` subdomains
