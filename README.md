
# Product Description Writer

An AI-powered Product Description Writer built using Python, Streamlit, and Google Gemini API.

## Features

- Accepts product name, features, and target audience.
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

## Installation

1. Clone this repository.
2. Install the required packages:

   pip install -r requirements.txt

3. Create a `.env` file in the project folder.
4. Add your Gemini API key:

   GEMINI_API_KEY=your_api_key_here

5. Run the application:

   streamlit run app.py

## Project Structure

product-description-writer/
- app.py
- requirements.txt
- README.md
- .gitignore

## Security

Keep your API key private. Never upload your `.env` file to GitHub.

## Author 
Rudra Bade