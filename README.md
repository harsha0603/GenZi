# Genzicare Chatbot

A real estate chatbot for WhatsApp that provides dynamic, context-aware responses using FastAPI, GPT-4, and a hybrid approach to intent classification. The chatbot leverages a TF-IDF + Logistic Regression model (with rule-based overrides) to distinguish between general, database-specific, and irrelevant queries. For database queries, it fetches property data from MySQL (using SQLAlchemy) and generates a combined response via GPT-4. For general queries, it directly uses GPT-4 to generate natural language responses.

---

## Table of Contents

- [Overview](#Overview)
- [Features](#Features)
- [Project Structure](#project-structure)
- [Setup](#setup)
  - [Environment Variables](#environment-variables)
  - [Dependencies](#dependencies)
- [Running the Project](#running-the-project)
  - [Local Server & Ngrok](#local-server--ngrok)
  - [Twilio WhatsApp Sandbox](#twilio-whatsapp-sandbox)
- [Functionality](#functionality)
  - [Intent Classification](#intent-classification)
  - [LLM Integration](#llm-integration)
  - [Database Querying](#database-querying)
- [Testing](#testing)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## Overview

Genzicare Chatbot is designed to assist users with real estate queries in Singapore via WhatsApp. The system uses a hybrid approach for intent classification to decide whether to generate a response using GPT-4 directly or to fetch structured property data from a database and then generate a context-aware response.

---

## Features

- **Hybrid Intent Classification:**  
  - Uses a pre-trained TF-IDF + Logistic Regression model along with rule-based overrides.  
  - Three intent labels: `general_query`, `database_query`, and `irrelevant`.

- **Dynamic Response Generation:**  
  - GPT-4 generates natural language responses in the persona of a knowledgeable real estate agent.

- **Robust Database Querying:**  
  - Extracts structured parameters from natural language queries via GPT-4.  
  - Uses SQLAlchemy to query MySQL (or SQLite for testing) based on parameters such as property type, rent range, building name, and address.

- **Stateful Conversations:**  
  - Maintains conversation context to handle follow-up queries.

- **Twilio WhatsApp Integration:**  
  - Sends and receives messages through Twilio’s WhatsApp Sandbox.

- **Logging & Monitoring:**  
  - Detailed logging throughout the system for debugging and performance monitoring.

---

## Project Structure
``` bash
genzicare-chatbot/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Configuration and environment setup
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py              # API endpoints (webhook)
│   │   └── dependencies.py        # API dependencies
│   ├── core/
│   │   ├── __init__.py
│   │   ├── intent_classifier.py   # Hybrid intent classifier (TF-IDF + rules)
│   │   ├── llm_processor.py       # GPT-4 integration and structured extraction
│   │   ├── query_builder.py       # Builds SQL queries based on extracted parameters
│   │   └── history_manager.py     # Manages conversation state
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py              # SQLAlchemy models for real estate data
│   │   └── database.py            # Database connection (MySQL/SQLite)
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py             # Utility functions (e.g., Twilio helper)
├── scripts/
│   ├── setup_db.py                # Script to initialize/seed the database
│   └── start_server.py            # Script to run the application
├── tests/
│   ├── __init__.py
│   └── test_api.py                # API endpoint tests
├── .env                         # Environment variables (not to be committed)
├── Dockerfile                   # (Optional) Containerization
└── README.md                    # Project documentation
```
## Setup
### Environment Variables
Create a .env file in the root directory with the following variables (update with your credentials):
``` bash
# FastAPI configuration
DATABASE_URL="mysql+mysqlconnector://username:password@localhost/real_estate"

# Twilio configuration
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# GPT-4 API configuration
API_URL=https://api.openai.com/v1/chat/completions
API_KEY=your_gpt4_api_key_here
```
## Dependencies
### Install the required packages using pip:
``` bash
pip install -r requirements.txt
```
## Running the Project
### Local Server & Ngrok
- Start FastAPI Server:
``` bash
uvicorn app.main:app --reload
```
- Expose Your Local Server:
  Use ngrok to expose port 8000:
  ```bash
  ngrok http 8000
  ```
  Copy the public URL provided by ngrok.
## Twilio WhatsApp Sandbox
### Configure Sandbox:
- In your Twilio Console, set the Inbound URL to:
``` bash
https://<your-ngrok-id>.ngrok-free.app/webhook
```
- Link Your WhatsApp:
Follow Twilio's instructions to link your WhatsApp number.

## Functionality

### Intent Classification
#### Hybrid Approach:
- Combines a TF-IDF + Logistic Regression model with rule-based overrides for domain-specific keywords.

#### Categories:
- **general_query**
- **database_query**
- **irrelevant**

### LLM Integration
#### GPT-4 Integration:
- Generates natural language responses.

#### Structured Extraction:
- Extracts parameters from natural language queries to build SQL queries.

### Database Querying
#### SQLAlchemy:
- Interacts with MySQL (or SQLite for testing) using defined models in `app/db/models.py`.

#### Query Builder:
- Builds dynamic SQL queries based on structured parameters.

### Communication
#### Twilio Integration:
- Sends and receives WhatsApp messages through Twilio’s Sandbox.

## Future Enhancements

### Refine Intent Classification:
- Integrate advanced NLP models for better accuracy.

### Enhanced Query Extraction:
- Improve prompt engineering for structured parameter extraction.

### Persistent State Management:
- Use a distributed cache (e.g., Redis) for session tracking.

### Production Deployment:
- Migrate from Twilio Sandbox to WhatsApp Business API after Meta approval.
