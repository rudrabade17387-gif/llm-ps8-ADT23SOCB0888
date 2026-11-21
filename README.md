# Product Description Writer

**Problem Statement:** PS 8 – Product Description Writer  
**University Number:** ADT23SOCB0888  
**Roll Number:** 08

## Project Overview

Product Description Writer is an AI-powered application that generates professional product listings using the Google Gemini API. It helps users create attractive product descriptions by entering basic product details.

## Features

- Accepts product name, product features, and target audience.
- Generates an attractive product title.
- Generates exactly three key benefits.
- Creates a product description containing exactly 60 words.
- Allows users to download the generated product listing.

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- Google GenAI SDK
- Python-dotenv

## How to Run the Project

1. Clone this repository:

   `git clone https://github.com/rudrabade17387-gif/llm-ps8-ADT23SOCB0888.git`

2. Open the project folder.

3. Install the required packages:

   `pip install -r requirements.txt`

4. Create a `.env` file in the project folder and add your Gemini API key:

   `GEMINI_API_KEY=your_api_key_here`

5. Run the application:

   `streamlit run app.py`

## Security

The API key is stored in a local `.env` file. The `.env` file and virtual environment are excluded from GitHub using `.gitignore`.

## Repository

https://github.com/rudrabade17387-gif/llm-ps8-ADT23SOCB0888
